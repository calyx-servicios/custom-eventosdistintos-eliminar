# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "POS Electronic Receipt Invoice Information",
    "summary": '''
        This module adds invoice information in electronic 
        receipt of the point of sale.
    ''',
    "author": "Calyx Servicios S.A.",
    "maintainers": ["PerezGabriela"],
    "website": "http://odoo.calyx-cloud.com.ar/",
    "license": "AGPL-3",
    "category": "Point of Sale",
    "version": "11.0.2.0.0",
    "installable": True,
    "application": True,
    "depends": [
        "point_of_sale"
    ],
    "data": [
        "views/import_library.xml",
        "views/pos_config.xml",
    ],
    "qweb": [
        "static/src/xml/pos_electronic_receipt_invoice.xml"
    ],
}