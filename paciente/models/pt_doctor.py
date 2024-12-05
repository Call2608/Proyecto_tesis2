from odoo import api,fields,models, _
from odoo.addons.base.models.res_country import Country,CountryState
from datetime import datetime


class Doctor(models.Model):
    _name = 'pt.doctor'
    _description = 'Doctor'

    
    nombreDoctor = fields.Char(string="Nombre del Doctor")
    codigoCMP = fields.Char(string= "Código CMP")

    _rec_name= 'nombreDoctor'


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

