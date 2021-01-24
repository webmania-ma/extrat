# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
#
# Copyright (c) 2016  - Osis - www.osis-dz.net

{
    'name': 'Algeria - Amount to Text',
    'version': '0.2',
    'category': 'Accounting',
    'description': """
This is the module print amount to Text with fiscal timbre.
========================================================================

This module applies to companies based in Algeria.

**Email:** contact@osis.dz
""",
    'author': 'Osis',
    'website': 'http://www.osis-dz.net/',
    'depends': ['l10n_dz_timbre'],
    'data': [
        'views/order_invoice.xml',

    ],

    'installable': True,
    'application': False,
    'auto_install': False,
}
