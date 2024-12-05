from odoo import api,fields,models, _
from odoo.addons.base.models.res_country import Country,CountryState
from datetime import datetime


class Diagnostico(models.Model):
    _name = 'pt.diagnostico'
    _description = 'Diagnóstico de cita'

    nombreDiagnostico = fields.Char(string="Nombre del diagnóstico")
    codigoDiagnostico = fields.Char(string= "Código del diagnóstico")
