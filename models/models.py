# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class SaleOrderExt(models.Model):
    _inherit="sale.order"

    approvals_is_active = fields.Boolean(compute="_compute_approvals_is_active")
    sale_order_approver_lines = fields.One2many("sale.order.approvers","order_id",readonly=True)
    requires_approval = fields.Boolean(compute="_compute_requires_approval")
    current_user_approver = fields.Boolean(compute="_compute_current_user_approver")
    
    
    
   


    def _compute_current_user_approver(self):
        for rcd in self:
            partner_object = rcd.sale_order_approver_lines.filtered(lambda x: x.name == self.env.user.partner_id and x.app_status == False )
            if partner_object :
                rcd.current_user_approver = True
            else:
                rcd.current_user_approver = False

    
    def _compute_requires_approval(self):
        for rcd in self:
            if rcd.sale_order_approver_lines and rcd.approvals_is_active:
                if rcd.sale_order_approver_lines.filtered(lambda x: x.app_status == False):
                    rcd.requires_approval = True
                else:
                    rcd.requires_approval = False

            else:
                rcd.requires_approval = False

    def approve_order(self):
        partner_approver_line_object = self.sale_order_approver_lines.filtered(lambda x: x.name == self.env.user.partner_id )
        partner_approver_line_object.app_status = True
        self.message_post(message_type='notification',body=f'{self.env.user.partner_id.name} has approved this Quotation')





    @api.constrains("team_id","order_line")
    def fill_sale_order_approver_lines(self):
        if self.approvals_is_active:
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


class ResPartnerExt(models.Model):
    _inherit="res.partner"

    def redirect_to_approved_orders(self,context={}):
        form_view_id = self.env.ref("sale.view_order_form").id
        tree_view_id = self.env.ref("sale.view_quotation_tree_with_onboarding").id
        
   
        return {
            'type': 'ir.actions.act_window',
            'name': 'Sales Orders',
            'view_type': 'form',
            'view_mode': 'tree',
            'res_model': 'sale.order',
            'views': [(tree_view_id,'tree'),(form_view_id, 'form')],
            'domain': [('sale_order_approver_lines.name', '=', self.id)],
            'target': 'current',
            'context':context,            
        }
       