from odoo import models, api, fields
class AccountInvoiceRefund(models.TransientModel):
    _inherit = "account.invoice.refund"

    @api.multi
    def invoice_refund(self):
        tag_ids = [self.env.ref('customer_invoice_tags.canceled_event').id ,self.env.ref('customer_invoice_tags.credit_note').id]
        for acc in self:
            if acc.filter_refund == "cancel":
                acc.invoice_id.partner_id.category_id = [(6,0,tag_ids)]
        res = super(AccountInvoiceRefund, self).invoice_refund()
        return res 