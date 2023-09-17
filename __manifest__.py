#yang boleh diganti name dan data 
{
    'name' : 'Haus Management Fleet',
    'version' : '1.0',
    'summary':'Modul ini merupakan modul untuk mempermudah proses management fleet',
    'sequence':1,
    'description':""" Haus Management Fleet """,
    'category':'Productivity',
    'website':'',
    'license': 'LGPL-3',
    'depends':['mail','board'],#untuk modul yang di butuhkan
    'data':[ 
        'views/management_fleet_task.xml',
        'views/management_fleet_schedule.xml',
        'views/management_fleet_dashboard.xml',
        'data/cron_task_schedule.xml',
        'views/menu.xml',
        'security/ir.model.access.csv',
    ],#untuk xml
    'assets':{
        'web.assets_backend':[
            'odoo_fleet_management/static/src/js/pin_point.js',
        ]
    },
    'demo':[], #untuk data demo
    'qweb':[],
    'installable':True, #untuk bisa di install
    'application':True ,#untuk bisa di buka
    'auto_install':False, #untuk bisa di install otomatis
}