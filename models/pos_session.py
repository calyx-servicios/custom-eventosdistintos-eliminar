# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import UserError, ValidationError



class PosSession(models.Model):
    _inherit = 'pos.session'

    make_visible = fields.Boolean(string="User", compute='get_user')

    @api.depends('make_visible','state')
    def get_user(self, ):
        user_crnt = self._uid
        res_user = self.env['res.users'].search([('id', '=', self._uid)])
        for session in self:
            if session.state == 'closed' and not res_user.has_group('point_of_sale.group_pos_manager'):
                session.make_visible = False
            else:
                session.make_visible = True

    @api.multi
    def get_products_sold(self):
        self.ensure_one()
        products_sold = {}
        for order in self.order_ids:
            for line in order.lines:
                key = (line.product_id)
                products_sold.setdefault(key, 0.0)
                products_sold[key] += line.qty
        products= sorted([{
                'product_id': product.id,
                'product_name': product.name,
                'qty': qty
            } for (product), qty in products_sold.items()],key=lambda l: l['product_name'])
        return products

    @api.multi
    def get_journal_invoices(self):
        self.ensure_one()
        journal_invoices = {}
        for order in self.order_ids:
            key = (order.sale_journal)
            journal_invoices.setdefault(key, 0.0)
            journal_invoices[key] += order.amount_total
        journals= sorted([{
                'journal_id': journal.id,
                'journal_name': journal.name,
                'amount': amount
            } for (journal), amount in journal_invoices.items()],key=lambda l: l['journal_name'])
        return journals

    @api.multi
    def get_cashbox_lines(self):
        self.ensure_one()
        cashbox_lines = {}
        for statement in self.statement_ids:
            for line in statement.cashbox_end_id.cashbox_lines_ids:
                key = (line)
                cashbox_lines.setdefault(key, 0.0)
                cashbox_lines[key] += line.number
        products= sorted([{
                'coin_name': line.coin_value,
                'subtotal': line.subtotal,
                'qty': line.number
            } for (line), qty in cashbox_lines.items()],key=lambda l: l['coin_name'])
        return products

    @api.multi
    def get_customers_created(self):
        self.ensure_one()
        partner_obj = self.env['res.partner']
        customers_created = {}
        
        
        for session in self:
            if session.start_at and session.stop_at:
                partners_id=partner_obj.search([('create_date','>=',session.start_at),('create_date','<=',session.stop_at),('create_uid','=',session.user_id.id)])
                for partner in partner_obj.browse(partners_id):
                    key = (partner.id)
                    customers_created.setdefault(key, 0.0)
                
        customers= sorted([{
                'partner_id': partner.id,
                'partner_name': partner.name,
                'qty': qty
            } for (partner), qty in customers_created.items()],key=lambda l: l['partner_name'])
        return customers
    
    make_visible = fields.Boolean(string="User", compute='get_user')