# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = "res.partner"

    def redirect_to_approved_orders(self, context={}):
        form_view_id = self.env.ref("sale.view_order_form").id
        tree_view_id = self.env.ref(
            "sale.view_quotation_tree_with_onboarding").id

        return {
            'type': 'ir.actions.act_window',
            'name': 'Sales Orders',
            'view_type': 'form',
            'view_mode': 'tree',
            'res_model': 'sale.order',
            'views': [(tree_view_id, 'tree'), (form_view_id, 'form')],
            'domain': [('sale_order_approver_lines.name', '=', self.id)],
            'target': 'current',
            'context': context,
        }
