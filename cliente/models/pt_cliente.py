# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import odoo
from odoo import api,fields,models, _
from odoo.addons.base.models.res_country import Country,CountryState
from datetime import datetime

class Cliente(models.Model):
    _name = 'pt.cliente'

 

    nombres = fields.Char(string ="Nombres",required=True)
    apellidoPaterno = fields.Char(string="Apellido paterno")
    apellidoMaterno = fields.Char(string="Apellido materno")
    DNI = fields.Char(string="DNI",required=True)
    fechaNacimiento = fields.Date(string="Fecha de nacimiento",default=datetime.today())
    telefono = fields.Char(string="Telefono")
    celular = fields.Char(string="Celular")
    correo = fields.Char(string="Correo Electrónico")
    pais_id = fields.Many2one('res.country',string="País",default="Peru")
    departamento_id = fields.Many2one("res.country.state",string="Departamento",domain="[('country_id', '=?', pais_id)]")
    notas = fields.Text(string="Notas")
    name = fields.Char(string="Nombre Completo",compute='_onchange_proc',readonly=True)
    idsContacto = fields.One2many('pt.contacto_cliente','idCliente')


    @api.depends('name')
    def _onchange_proc(self):

        for record in self:
            Nom     = record.nombres
            ApeP    = record.apellidoPaterno
            ApeM    = record.apellidoMaterno

            output  =   str(ApeP)+" "+str(ApeM)+", "+str(Nom)
            record.name = output


    def create(self,vals):
        self.create_Contact_data(vals)
        res= super().create(vals)
        return res
    
    def create_Contact_data(self,vals):

        line_dic = {
            'name': str(vals['apellidoPaterno'])+" "+str(vals['apellidoMaterno'])+", "+str(vals['nombres']),
            'email':str(vals['correo']),
            'phone':str(vals['telefono']),
            'mobile':str(vals['celular']),
            'active':True,
            'type':'contact'
        }
        self.env['res.partner'].create(line_dic)



    
    