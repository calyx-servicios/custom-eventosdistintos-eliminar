from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class AccountPaymentGroup(models.Model):
    _inherit = "account.payment.group"
    
    def create_template_report(self):
        return self.env.ref('receipt_invoice.action_report_preprinted_report').report_action(self)