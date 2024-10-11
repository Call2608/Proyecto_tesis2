# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import odoo
from odoo import api,fields,models, _
from odoo.addons.base.models.res_country import Country,CountryState
from datetime import timedelta, date, datetime
from odoo.exceptions import ValidationError, AccessError

class Campania(models.Model):
    _name = 'pt.campania'

    identificador = fields.Char(string ="Identificador",required=True)
    plantilla_correo =fields.Many2one(
        'mailing.mailing', string='Marketing Template',
        readonly=False, store=True)
    fecha_ini= fields.Date(string="Fecha de inicio",default=datetime.today())
    fecha_fin= fields.Date(string="Fecha de fin",default=datetime.today())
    estado = fields.Selection([
        ('draft', 'Nuevo'),
        ('running', 'En proceso'),
        ('stopped', 'Pausado')
        ], copy=False, default='draft',
        group_expand='_group_expand_states')
    notas = fields.Text(string="Notas")
    sent = fields.Integer(compute='_compute_statistics',readonly='1')
    delivered =fields.Integer(compute='_compute_statistics',readonly='1')
    opened = fields.Integer(compute='_compute_statistics',readonly='1')

    model_id = fields.Many2one(
        'ir.model', string='Model', index=True, required=True, ondelete='cascade',
        default=lambda self: self.env.ref('base.model_res_partner', raise_if_not_found=False),
        domain="['&', ('is_mail_thread', '=', True), ('model', '!=', 'mail.blacklist')]")
    model_name = fields.Char(string='Model Name', related='model_id.model', readonly=True, store=True)
    mailing_filter_id = fields.Many2one(
        'mailing.filter', string='Favorite Filter',
        domain="[('mailing_model_name', '=', model_name)]",
        compute='_compute_mailing_filter_id', readonly=False, store=True)
    mailing_filter_domain = fields.Char('Favorite filter domain', related='mailing_filter_id.mailing_domain')
    mailing_filter_count = fields.Integer('# Favorite Filters', compute='_compute_mailing_filter_count')





    @api.depends('model_id', 'domain')
    def _compute_mailing_filter_count(self):
        filter_data = self.env['mailing.filter']._read_group([
            ('mailing_model_id', 'in', self.model_id.ids)
        ], ['mailing_model_id'], ['__count'])
        mapped_data = {mailing_model.id: count for mailing_model, count in filter_data}
        for campaign in self:
            campaign.mailing_filter_count = mapped_data.get(campaign.model_id.id, 0)

    @api.depends('model_name')
    def _compute_mailing_filter_id(self):
        for mailing in self:
            mailing.mailing_filter_id = False



    def _group_expand_states(self, states, domain, order):
        return [key for key, val in self._fields['state'].selection]

    def action_start_campaign(self):
        if any(not campania.fecha_fin for campania in self):
            raise ValidationError(_('Debes acotar las fechas de la campaña para poder iniciarla.'))

        # trigger CRON job ASAP so that participants are synced
        self.write({'estado': 'running'})

    def action_stop_campaign(self):
        self.write({'estado': 'stopped'})

    def _compute_statistics(self):
        """ Compute statistics of the mass mailing """
        for key in (
            'scheduled', 'expected', 'canceled', 'sent', 'pending', 'delivered', 'opened',
            'process', 'clicked', 'replied', 'bounced', 'failed', 'received_ratio',
            'opened_ratio', 'replied_ratio', 'bounced_ratio',
        ):
            self[key] = False
        if not self.ids:
            return
        # ensure traces are sent to db
        self.env['mailing.trace'].flush_model()
        self.env['mailing.mailing'].flush_model()
        self.env.cr.execute("""
            SELECT
                m.id as mailing_id,
                COUNT(s.id) AS expected,
                COUNT(s.sent_datetime) AS sent,
                COUNT(s.trace_status) FILTER (WHERE s.trace_status = 'outgoing') AS scheduled,
                COUNT(s.trace_status) FILTER (WHERE s.trace_status = 'cancel') AS canceled,
                COUNT(s.trace_status) FILTER (WHERE s.trace_status = 'process') AS process,
                COUNT(s.trace_status) FILTER (WHERE s.trace_status = 'pending') AS pending,
                COUNT(s.trace_status) FILTER (WHERE s.trace_status in ('sent', 'open', 'reply')) AS delivered,
                COUNT(s.trace_status) FILTER (WHERE s.trace_status in ('open', 'reply')) AS opened,
                COUNT(s.links_click_datetime) AS clicked,
                COUNT(s.trace_status) FILTER (WHERE s.trace_status = 'reply') AS replied,
                COUNT(s.trace_status) FILTER (WHERE s.trace_status = 'bounce') AS bounced,
                COUNT(s.trace_status) FILTER (WHERE s.trace_status = 'error') AS failed
            FROM
                mailing_trace s
            RIGHT JOIN
                mailing_mailing m
                ON (m.id = s.mass_mailing_id)
            WHERE
                m.id IN %s
            GROUP BY
                m.id
        """, (tuple(self.ids), ))
        for row in self.env.cr.dictfetchall():
            total = (row['expected'] - row['canceled']) or 1
            row['received_ratio'] = float_round(100.0 * row['delivered'] / total, precision_digits=2)
            row['opened_ratio'] = float_round(100.0 * row['opened'] / total, precision_digits=2)
            row['replied_ratio'] = float_round(100.0 * row['replied'] / total, precision_digits=2)
            row['bounced_ratio'] = float_round(100.0 * row['bounced'] / total, precision_digits=2)
            self.browse(row.pop('mailing_id')).update(row)

    
    