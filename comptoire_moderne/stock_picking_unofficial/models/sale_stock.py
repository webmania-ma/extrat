# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import fields, models, _, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    unoffcial_bc = fields.Boolean('BC OF', default=False)


class stockPicking(models.Model):
    _inherit = 'stock.picking'

    unoffcial_bl = fields.Boolean('BC OF', default=False, readonly=True)


    @api.model
    def create(self, vals):
        # pr = ""
        # defaults = self.default_get(['name', 'picking_type_id'])
        # if vals.get('name', '/') == '/' and defaults.get('name', '/') == '/' and vals.get('picking_type_id', defaults.get('picking_type_id')):
        #      pr = self.env['stock.picking.type'].browse(
        #         vals.get('picking_type_id', defaults.get('picking_type_id'))).sequence_id.prefix

        if vals.get("origin", False):
            so = self.env['sale.order'].search([('name','=',vals.get("origin"))]) or False

            if so:	
                if so[0].unoffcial_bc:
                   vals['name'] = self.env['ir.sequence'].next_by_code('stock.picking.unofficial.abdelmajid')
                   vals['unoffcial_bl'] = True

        return super(stockPicking, self).create(vals)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
