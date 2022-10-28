from odoo import fields, models

class PosConfig(models.Model):
    _inherit = "pos.config"

    pos_auto_invoice = fields.Boolean('POS auto invoice',
        help='POS auto to checked to invoice button', default=True)
    receipt_invoice_number = fields.Boolean('Receipt show invoice information', default=True)