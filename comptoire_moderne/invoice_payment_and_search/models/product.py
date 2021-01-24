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


class ProductProduct(models.Model):
    _inherit = 'product.product'


    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        keys = [l[0] for l in args]
        if 'name' in keys:
            new_args = []
            for l in args:
                if len(l) != 3:
                    new_args.append(l)
                if l[0] == 'name':
                    new_args.append(('name', 'ilike', l[2].replace(' ','%')))
            args = new_args
        return super(ProductProduct, self).search(args, offset, limit, order, count=count)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
