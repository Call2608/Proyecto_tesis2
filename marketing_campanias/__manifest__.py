# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Marketing y Campañas',
    'category': 'Uncategorized',
    'author': 'Carlos Lescano Leon',
    'summary': 'Módulo para manejo de marketing y campañas',
    'license': 'LGPL-3',
    'description': """
    Este módulo sirve para manejar el marketing y campañas de la empresa.
""",
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/campania_views.xml'

        
    ]
}
