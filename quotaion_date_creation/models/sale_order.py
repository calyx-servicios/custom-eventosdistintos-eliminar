from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    date_create_quotation = fields.Date('Date Create Quotation')
    
