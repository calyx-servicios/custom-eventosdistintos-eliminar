# Copyright (C) 2019 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from num2words import num2words


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    agreement_template_id = fields.Many2one(
        'agreement',
        string="Agreement Template",
        domain="[('is_template', '=', True)]")
    party_partner_id = fields.Many2one(
        'res.partner',
        string="Party Partner")
    agreement_id = fields.Many2one('agreement', string="Agreement", copy=False)

    @api.multi
    @api.depends('payment_term_id', 'amount_total')
    def _onchange_payment_term(self):
        for sale in self:
            if sale.payment_term_id and sale.payment_term_id.plan:
                split = sale.payment_term_id.plan_split
                if split > 0:
                    sale.sign_amount = sale.amount_total/split
                    sale.remain_amount = sale.amount_total-sale.sign_amount
                    if sale.amount_total > 0:
                        sale.sign_percentage = round(
                            100*(sale.sign_amount/sale.amount_total), 2)
                        sale.remain_percentage = 100-sale.sign_percentage
                        words = num2words(sale.amount_total, lang='es')
                        sale.amount_words = words.upper()
                        words = num2words(sale.sign_amount, lang='es')
                        sale.sign_words = words.upper()

    sign_amount = fields.Monetary(
        string='Sign Amount', compute=_onchange_payment_term)
    remain_amount = fields.Monetary(
        string='Remain Amount', compute=_onchange_payment_term)
    sign_percentage = fields.Monetary(
        string='Sign Percentage', compute=_onchange_payment_term)
    remain_percentage = fields.Monetary(
        string='Remain Percentage', compute=_onchange_payment_term)
    sign_words = fields.Char(
        string='Sign Amount Words', compute=_onchange_payment_term)
    amount_words = fields.Char(
        string='Amount Words', compute=_onchange_payment_term)

    @api.multi
    def action_generate_template(self):
        for order in self:
            if not order.agreement_id:
                if order.agreement_template_id:
                    order.agreement_id = order.agreement_template_id.copy(default={
                        'name': order.name,
                        'is_template': False,
                        'sale_id': order.id,
                        'partner_id': order.partner_id.id,
                        'analytic_account_id':
                            order.analytic_account_id and
                            order.analytic_account_id.id or False,
                    })
                    for line in self.order_line:
                        # Create agreement line
                        self.env['agreement.line'].create({
                            'product_id': line.product_id.id,
                            'name': line.name,
                            'agreement_id': order.agreement_id.id,
                            'qty': line.product_uom_qty,
                            'sale_line_id': line.id,
                            'uom_id': line.product_uom.id
                        })

    @api.multi
    def _action_confirm(self):
        res = super(SaleOrder, self)._action_confirm()
        for order in self:
            if not order.agreement_id:
                if order.agreement_template_id:
                    self.action_generate_template()
        return res
