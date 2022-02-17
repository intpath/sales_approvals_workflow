from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    use_approvals_so = fields.Boolean(string="Activate appovals on Sales")
    send_notification_to_approver = fields.Boolean(string="Send notification to approvers")

    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            use_approvals_so=self.env['ir.config_parameter'].sudo(
            ).get_param('sales_approvals_workflow.use_approvals_so'),
            send_notification_to_approver=self.env['ir.config_parameter'].sudo(
            ).get_param('sales_approvals_workflow.send_notification_to_approver')
        )
        return res


    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param(
            'sales_approvals_workflow.use_approvals_so', self.use_approvals_so)
        self.env['ir.config_parameter'].sudo().set_param(
            'sales_approvals_workflow.send_notification_to_approver', self.send_notification_to_approver)
