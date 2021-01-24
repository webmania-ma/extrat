# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _

class pos_config(models.Model):
    _inherit = 'pos.config' 

    multi_receipt_count = fields.Integer('Multi Receipt Count', default=1)
    receipt_width = fields.Integer("Receipt width",default=300)
    allow_uom = fields.Boolean("Allow UOM name",default=True)
    allow_currency = fields.Boolean("Allow currency symbol", default=True)
    receipt_padding = fields.Integer("Padding",default=15)
    receipt_font_size = fields.Integer("Font size",default=14)
    receipt_watermark = fields.Char("Watermark")
    image = fields.Binary("Receipt Logo")

