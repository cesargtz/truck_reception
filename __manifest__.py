# -*- coding: utf-8 -*-

{
    'name': 'Truck Reception',
    'version': '10.0',
    'author': 'QX UNIT DE MÉXICO SA DE CV',
    'website': 'http://www.qxunit.com.mx',
    'depends': ['truck', 'vehicle_reception'],
    'data': [
        'security/ir.model.access.csv',
        'security/truck_reception_access_rules.xml',
        'views/purchase_order.xml',
        'views/truck_reception.xml',
        'views/sequenci.xml',
        'views/papperformat.xml',
        'views/report_reception.xml',
    ]
}
