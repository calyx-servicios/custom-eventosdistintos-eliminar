# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.addons.base.res.res_partner import WARNING_MESSAGE, WARNING_HELP
from dateutil.relativedelta import relativedelta
import logging
_logger = logging.getLogger(__name__)


    

class AccountPaymentTerm(models.Model):
    _inherit = "account.payment.term"
    
    plan = fields.Boolean(default=False, help="This is a plan payment term")
    plan_day=fields.Integer('Day of Month')
    plan_split=fields.Integer('Plan Split')

    @api.one
    def compute(self, value, date_ref=False):
        date_ref = date_ref or fields.Date.today()
        
        amount = value
        result = []
        if self.env.context.get('currency_id'):
            currency = self.env['res.currency'].browse(self.env.context['currency_id'])
        else:
            currency = self.env.user.company_id.currency_id
        if not self.plan:
            for line in self.line_ids:
                if line.value == 'fixed':
                    amt = currency.round(line.value_amount)
                elif line.value == 'percent':
                    amt = currency.round(value * (line.value_amount / 100.0))
                elif line.value == 'balance':
                    amt = currency.round(amount)
                if amt:
                    next_date = fields.Date.from_string(date_ref)
                    if line.option == 'day_after_invoice_date':
                        next_date += relativedelta(days=line.days)
                    elif line.option == 'fix_day_following_month':
                        next_first_date = next_date + relativedelta(day=1, months=1)  # Getting 1st of next month
                        next_date = next_first_date + relativedelta(days=line.days - 1)
                    elif line.option == 'last_day_following_month':
                        next_date += relativedelta(day=31, months=1)  # Getting last day of next month
                    elif line.option == 'last_day_current_month':
                        next_date += relativedelta(day=31, months=0)  # Getting last day of next month
                    result.append((fields.Date.to_string(next_date), amt))
                    amount -= amt
            
        else:
            date_ref = fields.Date.today()
            for i in range(self.plan_split):
                next_date = fields.Date.from_string(date_ref)
                amt = currency.round(value / self.plan_split)
                next_date += relativedelta(day=self.plan_day, months=i+1)
                if i==self.plan_split-1:
                    amount = sum(amt for _, amt in result)
                    dist = currency.round(value - amount)
                    amt =dist
                result.append((fields.Date.to_string(next_date), amt))


        return result