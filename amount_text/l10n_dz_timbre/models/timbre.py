# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
#
# Copyright (c) 2016  - Osis - www.osis-dz.net


from math import ceil
from odoo import api, fields, models, _
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError

class ConfigTimbre(models.Model):
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _name='config.timbre'
    _description='Fiscal Timbre configuration'

    name =  fields.Char('Nom', required=True)
    valeur = fields.Float('Valeur du timbre', digits=dp.get_precision('Product Price'), required=True)
    tranche = fields.Float('Tranche', digits=dp.get_precision('Product Price'), required=True)
    min_value = fields.Float('Valeur Minimum', digits=dp.get_precision('Product Price'),required=True)
    max_value = fields.Float('Plafond', digits=dp.get_precision('Product Price'),required=True)

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'name must be unique per Company!'),
    ]

    @api.model
    def _timbre(self, montant):
        res = {}
        timbre_obj = self.env['config.timbre']
        liste_obj  = timbre_obj.search([])
        if not liste_obj :
           raise UserError(_('Pas de confiuration du calcul Timbre.'))
        dict = liste_obj[-1]
        montant_avec_timbre = ceil((montant * dict['valeur']) / dict['tranche'])
        if montant_avec_timbre > dict['max_value']:
           montant_avec_timbre = dict['max_value']
        if montant_avec_timbre < dict['min_value']:
           montant_avec_timbre = dict['min_value']

        res['timbre'] = montant_avec_timbre
        res['amount_timbre'] = montant + montant_avec_timbre
        return res




