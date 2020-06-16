# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT

import datetime
import pytz
from dateutil import tz

import logging

_logger = logging.getLogger(__name__)

# Main Agreement Section Records Model


class AgreementStage(models.Model):
    _inherit = "agreement.stage"

    close_stage = fields.Boolean(
        string="Is Close Stage", help="This sets this stage as the Close stage"
    )


class Agreement(models.Model):
    _inherit = "agreement"

    # # compute the dynamic content for mako expression inside a try in
    # case the user fuck it
    # @api.multi
    # @api.onchange('start_date','end_date','sign_date','description','sale_id','sale_id.partner')
    # def _compute_dynamic_description(self):
    #     try:
    #         super(Agreement, self)._compute_dynamic_description()
    #     except:
    #         pass

    description = fields.Html(
        string="Description",
        track_visibility="onchange",
        help="Description of the agreement",
    )

    dynamic_description = fields.Html(
        compute="_compute_dynamic_description",
        string="Dynamic Description",
        help="Compute dynamic description",
    )

    start_date = fields.Datetime(
        string="Start Date",
        track_visibility="onchange",
        help="When the agreement starts.",
    )
    end_date = fields.Datetime(
        string="End Date",
        track_visibility="onchange",
        help="When the agreement ends.",
    )

    sign_date = fields.Date(
        string="Sign Date",
        track_visibility="onchange",
        help="When the agreement must be signed.",
    )

    sale_id = fields.Many2one("sale.order", string="Sales Order")

    def convert_date(self, date_to_convert):
        """
        Function to convert from stored UTC Odoo default
         timezone to user timezone
        """

        timezone = pytz.timezone(self._context.get("tz") or "UTC")
        # utc_zone = tz.gettz('UTC')
        utc_timezone = pytz.timezone("UTC")

        # to_zone based on tz variable defined on context
        to_zone = tz.gettz(str(timezone))

        utc_date = datetime.datetime.strptime(
            date_to_convert, DEFAULT_SERVER_DATETIME_FORMAT
        )
        utc_date = utc_timezone.localize(utc_date)
        converted_date = utc_date.astimezone(to_zone)
        return converted_date

    @api.multi
    def get_event_name(self):
        name = "Evento"
        if self.sale_id and self.sale_id.opportunity_id:
            name = self.sale_id.opportunity_id.name
        return name

    @api.multi
    def get_start_date(self):
        if self.start_date:
            converted_date = self.convert_date(self.start_date)
            return converted_date.strftime("%d/%m/%Y")

    @api.multi
    def get_start_time(self):
        if self.start_date:
            converted_date = self.convert_date(self.start_date)
            return converted_date.strftime("%H:%M")

    @api.multi
    def get_end_date(self):
        if self.end_date:
            converted_date = self.convert_date(self.end_date)
            return converted_date.strftime("%d/%m/%Y")

    @api.multi
    def get_end_time(self):
        if self.end_date:
            converted_date = self.convert_date(self.end_date)
            return converted_date.strftime("%H:%M")

    @api.multi
    def get_sign_date(self):
        if self.sign_date:
            sign = datetime.datetime.strptime(self.sign_date, "%Y-%m-%d")
            return sign.strftime("%d de %B de %Y")
