from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    use_approvals_so = fields.Boolean(string="Activate appovals on Sales")
    send_notification_to_approver = fields.Boolean(string="Send notification to approvers")

    use_category_approvals_so = fields.Boolean(string="Activate Category appovals on Sales")
    send_notification_to_category_approvers = fields.Boolean(string="Send notification to category approvers")

    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            use_approvals_so=self.env['ir.config_parameter'].sudo(
            ).get_param('sales_approvals_workflow.use_approvals_so'),
            send_notification_to_approver=self.env['ir.config_parameter'].sudo(
            ).get_param('sales_approvals_workflow.send_notification_to_approver'),
            use_category_approvals_so=self.env['ir.config_parameter'].sudo(
            ).get_param('sales_approvals_workflow.use_category_approvals_so'),
            send_notification_to_category_approvers=self.env['ir.config_parameter'].sudo(
            ).get_param('sales_approvals_workflow.send_notification_to_category_approvers'),
        )
        return res


    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param(
            'sales_approvals_workflow.use_approvals_so', self.use_approvals_so)
        self.env['ir.config_parameter'].sudo().set_param(
            'sales_approvals_workflow.send_notification_to_approver', self.send_notification_to_approver)
        self.env['ir.config_parameter'].sudo().set_param(
            'sales_approvals_workflow.use_category_approvals_so', self.use_category_approvals_so)
        self.env['ir.config_parameter'].sudo().set_param(
            'sales_approvals_workflow.send_notification_to_category_approvers', self.send_notification_to_category_approvers)
