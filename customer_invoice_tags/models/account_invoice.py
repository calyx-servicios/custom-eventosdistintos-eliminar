from odoo import models, api, fields
class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.multi
    def action_invoice_open(self):
        tag_canceled_event_id = self.env.ref('customer_invoice_tags.canceled_event').id 
        tag_credit_note_id = self.env.ref('customer_invoice_tags.credit_note').id
        tag_delay_id = self.env.ref('customer_invoice_tags.delay').id 
        for acc in self:
            if  acc.journal_document_type_id.document_type_id.internal_type == "credit_note":
                acc.partner_id.category_id = [(4,tag_credit_note_id,0)]
                acc.partner_id.category_id = [(4,tag_canceled_event_id,0)]
            for rec in acc.journal_id: 
                if rec.code == "MORA" or rec.name == "Moras":
                    acc.partner_id.category_id = [(4,tag_delay_id,0)]
        res = super(AccountInvoice, self).action_invoice_open()
        return res 
