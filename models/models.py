# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrderExt(models.Model):
    _inherit="sale.order"

    approvals_is_active = fields.Boolean(compute="_compute_approvals_is_active")
    sale_order_approver_lines = fields.One2many("sale.order.approvers","order_id",readonly=True)
    requires_approval = fields.Boolean(compute="_compute_requires_approval")
    

    
    
    def _compute_requires_approval(self):
        for rcd in self:
            if rcd.sale_order_approver_lines and rcd.approvals_is_active:
                if rcd.sale_order_approver_lines.filtered(lambda x: x.app_status == False):
                    rcd.requires_approval = True
            else:
                rcd.requires_approval = False

    def approve_order(self):
        pass





    @api.constrains("team_id","order_line")
    def fill_sale_order_approver_lines(self):
        if approvals_is_active:
            self.write({"sale_order_approver_lines":[(5, 0, 0)]})
            approvers = self.team_id.approver_lines.filtered(lambda x: x.min <= self.amount_total <= x.max )
            if approvers:
                for approver in approvers:
                    self.write({"sale_order_approver_lines":[(0, 0, {"name":approver.name.id})]})
        else:
            pass

        


    def _compute_approvals_is_active(self):
        for rcd in self:
            rcd.approvals_is_active =self.env['ir.config_parameter'].sudo().get_param('sales_approvals_workflow.use_approvals_so') 


class SaleOrderApproversLines(models.Model):
    _name="sale.order.approvers"

    order_id = fields.Many2one("sale.order")
    name = fields.Many2one("res.partner",string="Approver",required="True")
    app_status = fields.Boolean(string="Approval Status",default=False)



class CrmTeam(models.Model):
    _inherit="crm.team"

    approvals_is_active = fields.Boolean(compute="_compute_approvals_is_active")
    approver_lines = fields.One2many("sale.approvers","team_id",string="Approvers Lines")

    def _compute_approvals_is_active(self):
        for rcd in self:
            rcd.approvals_is_active =self.env['ir.config_parameter'].sudo().get_param('sales_approvals_workflow.use_approvals_so') 

class SaleApprovals(models.Model):
    _name = "sale.approvers"

    team_id = fields.Many2one("crm.team")
    name = fields.Many2one("res.partner",string="Approver",required="True")
    min = fields.Float(string="Minimum amount to approve")
    max = fields.Float(string="Maximum amount to approve")

