# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Paciente',
    'category': 'Uncategorized',
    'author': 'Carlos Lescano Leon',
    'summary': 'Módulo primario para el manejo de pacientes',
    'license': 'LGPL-3',
    'description': """
This module gives you a quick view of your patients directory, accessible from your home page.
You can track your patients and their related interaction with the company and sales.
""",
    'depends': ['base','mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/cita_paciente_views.xml',
        'views/diagnostico_views.xml',
        'views/doctor_views.xml',
        'views/paciente_views.xml'
        
    ]
}
