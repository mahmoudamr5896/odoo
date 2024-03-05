# -*- coding: utf-8 -*-
{
    'name': 'Hospitals',
    'version': '17.0.1.0.0',
    'summary': 'Hospitals Management System',
    'description': """ This Hospitals Management System""",
    'author': 'Mahmoud Amr',
    'depends': ['base'],
    'data': [
        'security/view.xml',
        'security/ir.model.access.csv',
        'views/hospital.xml',
        'views/base_view.xml',
        'reports/patient_report.xml',

    ],
    'application': True,
}
