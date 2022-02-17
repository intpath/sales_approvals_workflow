# -*- coding: utf-8 -*-
{
    'name': "Sales Price Range Approval Process",

    'summary': """
        This custom app enables you to create sales team approvers by total amount ranges, It doesn`t interfere with Odoo default process
        and Instead uses multiple roles to show/hide sale order confirmation to relevant user/approvers""",

    'description': """
        This custom app enables you to create sales team approvers by total amount ranges, It doesn`t interfere with Odoo default process
        and Instead uses multiple roles to show/hide sale order confirmation to relevant user/approvers
    """,

    'author': "IntegratedPath",
    'website': "http://www.int-path.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'sales',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','crm','sale_management'],
    'price':70,
    'currency':'USD',
    'license':'LGPL-3',
    
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/crm_team_view.xml',
        'views/res_config_view.xml',
        'views/sale_order_view.xml',
        'views/res_partner_view.xml'
    ],
}
