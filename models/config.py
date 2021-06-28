from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    
    use_approvals_so = fields.Boolean(string="Activate appovals on Sales")

    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            use_approvals_so=self.env['ir.config_parameter'].sudo().get_param('sales_approvals_workflow.use_approvals_so')
        )
        return res


    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('sales_approvals_workflow.use_approvals_so', self.use_approvals_so)