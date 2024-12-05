# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import odoo
from odoo import api,fields,models, _
from odoo.addons.base.models.res_country import Country,CountryState
from datetime import datetime


class Paciente(models.Model):
    _name = 'pt.paciente'
    _inherit = ['mail.thread']
 

    nombres = fields.Char(string ="Nombres",required=True)
    apellidoPaterno = fields.Char(string="Apellido paterno")
    apellidoMaterno = fields.Char(string="Apellido materno")
    DNI = fields.Char(string="DNI",required=True)
    fechaNacimiento = fields.Date(string="Fecha de nacimiento",default=datetime.today())
    edad = fields.Char(string="Edad",compute='_onchange_birth',readonly=True)
    sexo = fields.Selection([('f',"Femenino"),('m',"Masculino")])
    telefono = fields.Char(string="Telefono")
    correo = fields.Char(string="Correo Electrónico")
    notas = fields.Text(string="Notas")
    name = fields.Char(string="Nombre Completo",compute='_onchange_proc',readonly=True)
    idsCitas = fields.One2many('pt.cita_paciente','idPaciente')


    @api.depends('name')
    def _onchange_proc(self):

        for record in self:
            Nom     = record.nombres
            ApeP    = record.apellidoPaterno
            ApeM    = record.apellidoMaterno
            output  =   str(ApeP)+" "+str(ApeM)+", "+str(Nom)
            record.name = output

    @api.depends('edad')
    def _onchange_birth(self):
        today = datetime.today()
        for record in self:
            age     = record.fechaNacimiento
            output  =   today.year - age.year - ((today.month, today.day) < (age.month, age.day))
            record.edad = output


    def create(self,vals,repetition='0'):
        if(repetition=='0'):
            repetition='1'
            self.create_Contact_data(vals,repetition)
            self.create_Client_data(vals,repetition)
        res= super().create(vals)
        return res
    
    def create_Contact_data(self,vals,repetition):

        line_dic = {
            'name': str(vals['apellidoPaterno'])+" "+str(vals['apellidoMaterno'])+", "+str(vals['nombres']),
            'email':str(vals['correo']),
            'phone':str(vals['telefono']),
            'active':True,
            'type':'contact'
        }
        if(repetition=='1'):
            self.env['res.partner'].create(line_dic)


    def create_Client_data(self,vals,repetition):

        line_dic = {
            'nombres': str(vals['nombres']),
            'apellidoPaterno': str(vals['apellidoPaterno']),
            'DNI':str(vals['DNI']),
            'apellidoMaterno': str(vals['apellidoMaterno']),
            'correo':str(vals['correo']),
            'telefono':str(vals['telefono']),
            'fechaNacimiento':datetime.strptime(vals['fechaNacimiento'],'%Y-%m-%d')
        }
        if(repetition=='1'):
            self.env['pt.cliente'].create(line_dic,repetition)



    
    def go_to_client_view(self):


        url_base = "{}/web?&#id={}&cids=1&view_type=form&model={}&action={}"
        action = "135" # Name of the action defined in some XML
        model_name = "pt.cliente"
        target_record_id = self.id
        url = url_base.format('http://localhost:8069', target_record_id, model_name, action)
        return{
            'name': "To model cliente",
            'type': 'ir.actions.act_url',
            'url': url,  # The url is the same as above
            'target': 'self'
        }