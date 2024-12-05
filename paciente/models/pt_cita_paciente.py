# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api,fields,models, _
from odoo.addons.base.models.res_country import Country,CountryState
from datetime import datetime

class CitaPaciente(models.Model):
    _name = 'pt.cita_paciente'
    _description = 'Cita paciente'
    idPaciente = fields.Many2one('pt.paciente',string="Paciente")
    doctor = fields.Many2one('pt.doctor',string="Doctor")
    servicio = fields.Selection(
        [('control',"Control programado"),('medida',"Medida de vista"),('Consulta',"Consulta oftalmológica"),('lentes',"Lentes y óptica")],string="Tipo de servicio")
    fechaCita = fields.Date(string="Fecha de cita",default=datetime.today())
    horaCita = fields.Float(string="Hora")
    signos = fields.Text(string="Signos y síntomas")
    examen = fields.Text(string="Examen físico")
    antecedentes = fields.Text(string="Antecedentes")
    idsDiagnostico = fields.Many2many('pt.diagnostico',string="Diagnósticos")




    def name_get(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        if isinstance(ids, (int, long)):
            ids = [ids]

        res = []
        for record in self.browse(cr, uid, ids, context=context):
            name = record.nombreDoctor
            res.append((record.id, name))

        return res      
     





