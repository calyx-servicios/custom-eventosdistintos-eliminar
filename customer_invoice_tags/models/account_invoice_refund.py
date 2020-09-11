from odoo import models, api, fields
class AccountInvoiceRefund(models.TransientModel):
    _inherit = "account.invoice.refund"

    @api.multi
    def invoice_refund(self):
        tag_canceled_event_id = self.env.ref('customer_invoice_tags.canceled_event').id 
        tag_credit_note_id = self.env.ref('customer_invoice_tags.credit_note').id
        for acc in self:
            if (acc.journal_document_type_id.document_type_id.code == "8" or acc.journal_document_type_id.document_type_id.code == "3") and acc.filter_refund != "refund"  :
                acc.invoice_id.partner_id.category_id = [(4,tag_credit_note_id,0)]
                acc.invoice_id.partner_id.category_id = [(4,tag_canceled_event_id,0)]
        res = super(AccountInvoiceRefund, self).invoice_refund()
        return res 