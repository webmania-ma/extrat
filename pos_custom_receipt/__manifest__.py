# -*- coding: utf-8 -*-

{
    'name': 'Pos Custom receipt',
    'version': '1.0',
    'category': 'Point of Sale',
    'sequence': 6,
    'author': 'Webveer',
    'summary': 'Pos Custom receipt allows you to customize your receipt according to your requirement.',
    'description': """

=======================

Pos Custom receipt allows you to customize your receipt according to your requirement.

""",
    'depends': ['point_of_sale'],
    'data': [
        'views/views.xml',
    ],
    'qweb': [
        'static/src/xml/pos.xml',
    ],
    'images': [
        'static/description/receipt1.jpg',
    ],
    'installable': True,
    'website': '',
    'auto_install': False,
    'price': 39,
    'currency': 'EUR',
}
