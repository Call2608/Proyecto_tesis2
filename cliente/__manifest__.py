# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Cliente',
    'category': 'Uncategorized',
    'author': 'Carlos Lescano Leon',
    'summary': 'Primary module for client management',
    'license': 'LGPL-3',
    'description': """
This module gives you a quick view of your clients directory, accessible from your home page.
You can track your clients and their related interaction with the company and sales.
""",
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/contacto_cliente_views.xml',
        'views/cliente_views.xml'

        
    ]
}
