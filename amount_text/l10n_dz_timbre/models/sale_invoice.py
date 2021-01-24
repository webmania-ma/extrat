# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
#
# Copyright (c) 2016  - Osis - www.osis-dz.net


from math import ceil
from odoo import fields, models, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.one
    @api.depends('payment_term_id','amount_total')
    def _amount_timbre(self):
        for order in self:
            amount_timbre = order.amount_total
            if order.payment_term_id and order.payment_term_id.payment_type == 'cash':
                timbre = self.env['config.timbre']._timbre(order.amount_total)
                self.timbre = timbre['timbre']
                amount_timbre = timbre['amount_timbre']
            self.amount_timbre = amount_timbre

    @api.onchange('payment_term_id')
    def onchange_payment_term(self):
        if not self.payment_term_id:
            self.update({
                'payment_type': False,
            })
            return
        values = {
            'payment_type': self.payment_term_id and self.payment_term_id.payment_type or False,
        }
        self.update(values)

    payment_type = fields.Char('Type de paiement')
    timbre = fields.Monetary(string='Timbre', store=True, readonly=True,
                             compute='_amount_timbre', track_visibility='always')
    amount_timbre = fields.Monetary(string='Total avec Timbre', store=True,
                                    readonly=True, compute='_amount_timbre', track_visibility='always')

    @api.multi
    def _prepare_invoice(self):
        res = super(SaleOrder, self)._prepare_invoice()
        res['payment_type'] =  self.payment_type
        return res

class AccountInnvoice(models.Model):
    _inherit = "account.invoice"

    @api.one
    @api.depends('payment_term_id','amount_total')
    def _amount_timbre(self):
        for order in self:
            amount_timbre = order.amount_total
            if order.payment_term_id and order.payment_term_id.payment_type == 'cash':
               timbre = self.env['config.timbre']._timbre(order.amount_total)
               self.timbre = timbre['timbre']
               amount_timbre = timbre['amount_timbre']
            self.amount_timbre = amount_timbre

    @api.onchange('payment_term_id')
    def onchange_payment_term(self):
        if not self.payment_term_id:
            self.update({
                'payment_type': False,
            })
            return
        values = {
            'payment_type': self.payment_term_id and self.payment_term_id.payment_type or False,
        }
        self.update(values)

    payment_type = fields.Char('Type de paiement')
    timbre = fields.Monetary(string='Timbre', store=True, readonly=True,
                             compute='_amount_timbre', track_visibility='always')
    amount_timbre = fields.Monetary(string='Total avec Timbre', store=True,
                                    readonly=True, compute='_amount_timbre', track_visibility='always')



