# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'Calendar Event Locations',
    'summary': """
        Calendar Event Locations""",

    'author': 'Calyx Servicios S.A., Odoo Community Association (OCA)',
    'maintainers': ['Garaceliguzman'],

    'website': 'http://odoo.calyx-cloud.com.ar/',
    'license': 'AGPL-3',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'version': '11.0.1.0.0',
    # see https://odoo-community.org/page/development-status
    'development_status': 'Production/Stable',

    # any module necessary for this one to work correctly
    'depends': ['calendar_colors'],

    # always loaded
    'data': [
        'views/calendar_event_locations_view.xml'
    ],
}
