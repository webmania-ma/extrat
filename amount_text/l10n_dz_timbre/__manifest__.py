# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
#
# Copyright (c) 2016  - Osis - www.osis.dz

{
    'name': 'Algeria - Fiscal Timbre ',
    'version': '0.3',
    'category': 'Localization',
    'description': """
This is the module to manage the Fiscal Timbre in Odoo.
========================================================================

This module applies to companies based in Algeria.
.

**Email:** contact@osis.dz
""",
    'author': 'Osis',
    'website': 'http://www.osis.dz/',
    "license": "AGPL-3",
    'depends': ['l10n_dz'],
    'data': [

	'data/timbre_data.xml',
        'security/ir.model.access.csv',
	'views/timbre_view.xml',
	'views/sale_invoice_view.xml'	,
	'views/account_view.xml',

    ],

    'installable': True,
    'application': False,
    'auto_install': False,
}
