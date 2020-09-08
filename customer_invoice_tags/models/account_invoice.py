from odoo import models, api, fields
class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.multi
    def action_invoice_open(self):
        tag_id = self.env.ref('customer_invoice_tags.delay').id 
        for acc in self:
            for rec in acc.journal_id: 
                if rec.code == "MRO":
                    acc.partner_id.category_id = [(4,tag_id,0)]
        res = super(AccountInvoice, self).action_invoice_open()
        return res 
