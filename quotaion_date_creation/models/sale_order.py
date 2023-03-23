from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    date_create_quotation = fields.Date('Date Create Quotation')
    
    @api.onchange('requested_date')
    def _requested_date_in_notes(self):
        if self.requested_date and self.template_id and self.template_id.note:
            self.note = ('FECHA SOLICITADA: %s \n') % self.requested_date + self.template_id.note 