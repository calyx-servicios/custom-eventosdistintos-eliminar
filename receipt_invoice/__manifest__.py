# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'Receipt Invoice Duplicate',
    'summary': """
        Payment receipt and duplicate customers""",

    'author': 'Calyx Servicios S.A., Odoo Community Association (OCA)',
    'maintainers': ['Garaceliguzman'],

    'website': 'http://odoo.calyx-cloud.com.ar/',
    'license': 'AGPL-3',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Accounting',
    'version': '11.0.1.0.0',
    # see https://odoo-community.org/page/development-status
    'development_status': 'Production/Stable',

    # any module necessary for this one to work correctly
    'depends': ['base','account_payment_group'],

    # always loaded
    'data': [
        'views/account_payment_group_view.xml',
        'views/template.xml'
    ],
}
