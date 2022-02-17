# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class CrmTeam(models.Model):
    _inherit = "crm.team"

    approvals_is_active = fields.Boolean(
        compute="_compute_approvals_is_active")
    approver_lines = fields.One2many(
        "sale.approvers", "team_id", string="Approvers Lines")

    def _compute_approvals_is_active(self):
        for rcd in self:
            rcd.approvals_is_active = self.env['ir.config_parameter'].sudo(
            ).get_param('sales_approvals_workflow.use_approvals_so')
