# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api,fields,models, _
from odoo.addons.base.models.res_country import Country,CountryState
from datetime import datetime

class ContactoCliente(models.Model):
    _name = 'pt.contacto_cliente'
    _description = 'Contacto cliente'

    idCliente = fields.Many2one('pt.cliente',string="Cliente")
    tipoContacto = fields.Selection(
        [('llamada',"Contacto por teléfono"),('correo',"Contacto por correo"),('compra',"Compra de artículos"),('atencion',"Atención oftalmológica"),('informacion',"Contacto para pedir información")],string="Tipo de contacto")
    fechaContacto = fields.Date(string="Fecha de contacto",default=datetime.today())
    respuesta = fields.Selection([('si',"Sí"),('no',"No")],default='no',string="¿Hubo respuesta?")



        
     





