# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.addons.base.res.res_partner import WARNING_MESSAGE, WARNING_HELP
import datetime
import logging
_logger = logging.getLogger(__name__)


class Agreement(models.Model):
    _inherit = 'agreement'

    # compute the dynamic content for mako expression inside a try in case the user fuck it
    @api.multi
    def _compute_dynamic_description(self):
        try:
            super(Agreement, self)._compute_dynamic_description()
        except:
            pass
            

    description = fields.Html(
        string="Description",
        track_visibility='onchange',
        help="Description of the agreement",)

    dynamic_description = fields.Html(
        compute="_compute_dynamic_description",
        string="Dynamic Description",
        help='Compute dynamic description')

    start_date = fields.Datetime(
        string="Start Date",
        track_visibility='onchange',
        help="When the agreement starts.")
    end_date = fields.Datetime(
        string="End Date",
        track_visibility='onchange',
        help="When the agreement ends.")

    sign_date = fields.Date(
        string="Sign Date",
        track_visibility='onchange',
        help="When the agreement must be signed.")
    

    sale_id = fields.Many2one('sale.order', string='Sales Order')

    @api.multi
    def get_start_date(self):
        if self.start_date:
            start=datetime.datetime.strptime(self.start_date, '%Y-%m-%d %H:%M:%S')
            return start.strftime("%d/%m/%Y")
    
    @api.multi
    def get_start_time(self):
        if self.start_date:
            start=datetime.datetime.strptime(self.start_date, '%Y-%m-%d %H:%M:%S')
            return start.strftime("%H:%M")
    
    @api.multi
    def get_end_date(self):
        if self.end_date:
            end=datetime.datetime.strptime(self.end_date, '%Y-%m-%d %H:%M:%S')
            return end.strftime("%d/%m/%Y")
    
    @api.multi
    def get_end_time(self):
        if self.end_date:
            end=datetime.datetime.strptime(self.end_date, '%Y-%m-%d %H:%M:%S')
            return end.strftime("%H:%M")
    
    @api.multi
    def get_sign_date(self):
        if self.sign_date:
            sign=datetime.datetime.strptime(self.sign_date, '%Y-%m-%d')
            return sign.strftime("%d de %B de %Y")