{
    'name': 'Project Tracker',
    'version': '0.1',
    'summary': 'Track client projects and deliverables',
    'author': 'Tapiwa Sande',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/wizard_views.xml',
        'views/project_views.xml',
    ],
    'installable': True,
    'application': True,
}