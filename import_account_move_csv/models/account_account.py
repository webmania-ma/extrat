# -*- coding: utf-8 -*-

from odoo import models, fields


class AccountAccount(models.Model):
    _inherit = 'account.account'

    no_retrieve_partner = fields.Boolean("Don't retrieve partner in import account move")
