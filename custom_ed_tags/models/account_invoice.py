from odoo import models, api, fields, _

class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.multi
    def action_invoice_open(self):

        for acc in self:
            record = acc.env['res.partner.category']
            tag_id = record.search([('name', '=', 'With Delay')]).id
            for rec in acc.journal_id: 
                if rec.code == "MRO":
                    acc.partner_id.category_id = [(4,tag_id)]
        res = super(AccountInvoice, self).action_invoice_open()
        return res 
