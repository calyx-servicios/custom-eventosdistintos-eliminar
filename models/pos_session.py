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