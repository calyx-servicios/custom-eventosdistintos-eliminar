from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    date_create_quotation = fields.Date('Date Create Quotation')
    
    @api.onchange('requested_date')
    def _requested_date_in_notes(self):
        self.note = ('Fecha Solicitada: %s \n') % self.requested_date + self.template_id.note 