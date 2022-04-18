# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SaleOrderExt(models.Model):
    _inherit = "sale.order"

    approvals_is_active = fields.Boolean(
        compute="_compute_approvals_is_active")
    sale_order_approver_lines = fields.One2many(
        "sale.order.approvers", "order_id", readonly=True)
    requires_approval = fields.Boolean(compute="_compute_requires_approval")
    current_user_approver = fields.Boolean(
        compute="_compute_current_user_approver")

    def _compute_approvals_is_active(self):
        for rcd in self:
            rcd.approvals_is_active = self.env['ir.config_parameter'].sudo(
            ).get_param('sales_approvals_workflow.use_approvals_so')

    def _compute_requires_approval(self):
        for rcd in self:
            if rcd.sale_order_approver_lines and rcd.approvals_is_active:
                if rcd.sale_order_approver_lines.filtered(lambda x: x.app_status == False):
                    rcd.requires_approval = True
                else:
                    rcd.requires_approval = False
            else:
                rcd.requires_approval = False

    def _compute_current_user_approver(self):
        for rcd in self:
            partner_object = rcd.sale_order_approver_lines.filtered(
                lambda x: x.name == self.env.user.partner_id and x.app_status == False)
            if partner_object:
                rcd.current_user_approver = True
            else:
                rcd.current_user_approver = False

    def approve_order(self):
        partner_approver_line_object = self.sale_order_approver_lines.filtered(
            lambda x: x.name == self.env.user.partner_id)
        partner_approver_line_object.app_status = True
        self.message_post(
            message_type='notification',
            subtype_id = self.env.ref('mail.mt_comment').id,
            body=f'{self.env.user.partner_id.name} has approved this Quotation',
            partner_ids = [self.create_uid.partner_id.id],
            )

    def manager_approve_order(self):
        for record in self:
            for approver_line in record.sale_order_approver_lines:
                approvers_string = ', '
                approver_line.app_status = True
                self.message_post(
                    message_type='notification',
                    subtype_id = self.env.ref('mail.mt_comment').id,
                    body=f'Mansger {self.env.user.partner_id.name} has approved this Quotation on behalf of: {approvers_string.join(record.sale_order_approver_lines.mapped("name.name"))}',
                    )

    @api.constrains("team_id", "order_line")
    def fill_sale_order_approver_lines(self):
        if self.approvals_is_active:
            self.write({"sale_order_approver_lines": [(5, 0, 0)]})
            approvers = self.team_id.approver_lines.filtered(
                lambda x: x.min <= self.amount_total <= x.max)
            if approvers:
                for approver in approvers:
                    self.write({
                        "sale_order_approver_lines": 
                            [(0, 0, {"name": approver.name.id})]
                        })
                    send_notification = self.env['ir.config_parameter'].sudo(
                    ).get_param('sales_approvals_workflow.send_notification_to_approver')
                    
                    if send_notification:
                        notification_ids = [(0, 0, {
                            'res_partner_id': approver.name.id,
                            'notification_type': 'inbox'
                        })]

                        link = f"""
                            <p style="margin-top:24px; margin-bottom:16px">
                                <a style="background-color:#875A7B; padding:10px; text-decoration:none; 
                                    color:#fff; border-radius:5px" href="#" data-oe-model="{self._name}"
                                    data-oe-id="{self.id}">
                                    View S.O.
                                </a>
                            </p>
                        """

                        body = f"""
                            <div>
                                Dear {approver.name.name},
                            </div>
                            <div>
                                You have been assigned to approve the S.O.: {self.name}.
                            </div>
                            {link}
                        """
                        self.message_post(
                            body=body,
                            subject="Sale Order Approval",
                            subtype_id = self.env.ref('mail.mt_comment').id,
                            message_type='notification',
                            notification_ids=notification_ids
                            )
                    else:
                        pass
            else:
                pass
        else:
            pass
