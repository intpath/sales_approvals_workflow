# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SaleOrderApproversLines(models.Model):
    _name = "sale.order.approvers"

    order_id = fields.Many2one("sale.order")
    name = fields.Many2one("res.partner", string="Approver", required="True")
    app_status = fields.Boolean(string="Approval Status", default=False)
    is_notified = fields.Boolean("Is Notified?", readonly=True)


class SaleApprovals(models.Model):
    _name = "sale.approvers"

    team_id = fields.Many2one("crm.team")
    name = fields.Many2one("res.partner", string="Approver", required="True")
    min = fields.Float(string="Minimum amount to approve")
    max = fields.Float(string="Maximum amount to approve")
