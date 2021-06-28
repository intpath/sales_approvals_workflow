# -*- coding: utf-8 -*-
# from odoo import http


# class SalesApprovalsWorkflow(http.Controller):
#     @http.route('/sales_approvals_workflow/sales_approvals_workflow/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sales_approvals_workflow/sales_approvals_workflow/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sales_approvals_workflow.listing', {
#             'root': '/sales_approvals_workflow/sales_approvals_workflow',
#             'objects': http.request.env['sales_approvals_workflow.sales_approvals_workflow'].search([]),
#         })

#     @http.route('/sales_approvals_workflow/sales_approvals_workflow/objects/<model("sales_approvals_workflow.sales_approvals_workflow"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sales_approvals_workflow.object', {
#             'object': obj
#         })
