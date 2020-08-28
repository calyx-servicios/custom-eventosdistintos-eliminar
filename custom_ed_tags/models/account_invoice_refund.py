from odoo import models, api, fields, _

class AccountInvoiceRefund(models.TransientModel):
    _inherit = "account.invoice.refund"

    @api.multi
    def invoice_refund(self):
        for acc in self:
            tag_ids = []
            record = acc.env['res.partner.category']
            tag_cancel = record.search([('name', '=', 'Canceled event')]).id
            tag_ids.append(tag_cancel)
            tag_credit = record.search([('name', '=', 'With Credit Note')]).id
            tag_ids.append(tag_credit) 
            if acc.filter_refund == "cancel":
                acc.invoice_id.partner_id.category_id = [(6, 0, tag_ids)]
        res = super(AccountInvoiceRefund, self).invoice_refund()
        return res 