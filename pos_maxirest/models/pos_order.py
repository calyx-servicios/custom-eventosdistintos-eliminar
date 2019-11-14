# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import UserError, ValidationError
import logging
_logger = logging.getLogger(__name__)


class PosTransfer(models.Model):
    _name = 'pos.transfer'

    order_id = fields.Many2one('pos.order', string='Order')
    source_id = fields.Many2one('restaurant.table', string='Source Table')
    destiny_id = fields.Many2one('restaurant.table', string='Destiny Table')
    date = fields.Date(string='Transfer Date',required=True,default=fields.Date.today)

class PosOrder(models.Model):
    _inherit = 'pos.order'

    transfer_ids = fields.One2many('pos.transfer', 'order_id',  string='Transfers')


    @api.model
    def create_from_ui(self, orders):
        order_ids=super(PosOrder, self).create_from_ui(orders)
        return order_ids

    def _transfer_fields(self, ui_transferline):
        return {
            'order_id': ui_transferline['order_id'],
            'source_id': ui_transferline['source_id'],
            'destiny_id': ui_transferline['destiny_id']
        }


    def add_transfer(self, data):
        context = dict(self.env.context)
        transfer=self.env['pos.transfer'].with_context(context).create(data)
        return transfer.id

    @api.model
    def _process_order(self, pos_order):
        order=super(PosOrder, self)._process_order(pos_order)
        _logger.debug('=====_process order ui %r', pos_order)
        if 'transfer_ids' in pos_order:
            for transfer in pos_order['transfer_ids']:
                data=transfer[2]
                data['order_id']=order.id
                order.add_transfer(self._transfer_fields(data))
        return order
    
    