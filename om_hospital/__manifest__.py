{
    "name": "Hospital Mangment System",
    "author": "Ahmed Salah",
    "license": "LGPL-3",
    "version": "17.0.1.1",
    "depends": [
        'base',
        'sale_management',
        'mail',
        'product',
        'account',
    ],
    "data": [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/patient_view.xml',
        'views/patient_readonly_view.xml',
        'views/appointment_views.xml',
        'views/appointment_lines_views.xml',
        'views/patient_tag_view.xml',
        'views/account_move_views.xml',
        'views/menu.xml',
        'report/patient_details_template.xml',
        'report/report.xml',
    ]
}
