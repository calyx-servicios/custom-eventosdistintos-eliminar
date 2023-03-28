from odoo import models, fields, api, _
from datetime import datetime, timedelta

class SaleOrder(models.Model):
    _inherit = "sale.order"

    date_create_quotation = fields.Date('Date Create Quotation')
    
    @api.onchange('requested_date')
    def _requested_date_in_notes(self):
        if self.requested_date and self.template_id and self.template_id.note:
            date = datetime.strptime(self.requested_date, '%Y-%m-%d %H:%M:%S') - timedelta(hours=3)
            self.note = ('FECHA SOLICITADA: %s \n') % date + self.template_id.note 
