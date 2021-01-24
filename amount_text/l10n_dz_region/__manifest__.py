# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
#
# Copyright (c) 2016  - Osis - www.osis.dz

{
    'name': 'Algeria - Region',
    'version': '0.4',
    'category': 'Sales',
    "license": "AGPL-3",
    'description': """
This is the module to manage the wilaya & commune for Algeria in Odoo.
========================================================================

This module applies to companies based in Algeria.
.

**Email:** contact@osis.dz
""",
    'author': 'Osis',
    'website': 'http://www.osis.dz/',
    'depends': ['sale'],
    'data': [
	'security/ir.model.access.csv',
        'data/wilayas_data.xml',
        'data/commune_data.xml',
	'views/res_commune.xml'
    ],

    'installable': True,
    'application': False,
    'auto_install': False,
}

