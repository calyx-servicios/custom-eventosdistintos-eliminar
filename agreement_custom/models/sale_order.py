# Copyright (C) 2019 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from num2words import num2words
import logging

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    agreement_template_id = fields.Many2one(
        "agreement",
        string="Agreement Template",
        domain="[('is_template', '=', True)]",
    )

    agreement_id = fields.Many2one("agreement", string="Agreement", copy=False)
    start_date = fields.Datetime(
        string="Start Date", help="When the agreement starts."
    )
    end_date = fields.Datetime(
        string="End Date", help="When the agreement ends."
    )

    sign_date = fields.Date(
        string="Sign Date", help="When the agreement must be signed."
    )

    dynamic_description = fields.Html(
        string="Dynamic Description", help="Compute dynamic description"
    )

    @api.multi
    @api.depends("agreement_id", "agreement_id.stage_id")
    def _onchange_stage(self):

        for sale in self:

            close = False
            if sale.agreement_id:
                _logger.debug(
                    "_onchange_stage====>%s", self.agreement_id.stage_id
                )
                stage = self.env["agreement.stage"].search(
                    [("close_stage", "=", True)]
                )
                if stage:

                    stage = stage and stage[0]
                    if self.agreement_id.stage_id.id == stage.id:
                        close = True
            sale.close = close

    close = fields.Boolean(string="Agreement Close", compute="_onchange_stage")

    @api.multi
    @api.onchange(
        "start_date",
        "end_date",
        "sign_date",
        "agreement_id",
        "partner_id",
        "name",
        "amount_total",
        "invoice_ids",
        "invoice_ids.state",
        "opportunity_id",
    )
    def _onchange_dynamic(self):
        for sale in self:
            if sale.agreement_id:
                sale.agreement_id.start_date = sale.start_date
                sale.agreement_id.end_date = sale.end_date
                sale.agreement_id.sign_date = sale.sign_date
                sale.dynamic_description = (
                    sale.agreement_id.dynamic_description
                )

    @api.multi
    @api.onchange("opportunity_id")
    def _onchange_opportunity(self):
        for sale in self:
            if sale.opportunity_id:
                sale.partner_id = sale.opportunity_id.partner_id.id
                requested_date = sale.opportunity_id.requested_date
                sale.start_date = requested_date
                sale.end_date = requested_date

    @api.multi
    @api.depends(
        "payment_term_id", "amount_total", "invoice_ids", "invoice_ids.state"
    )
    def _onchange_payment_term(self):
        for sale in self:
            if sale.payment_term_id and sale.payment_term_id.plan:
                # split = sale.payment_term_id.plan_split
                invoiced = 0.0
                for invoice in sale.invoice_ids:
                    if invoice.state not in ("draft", "canceled"):
                        invoiced += invoice.amount_total
                if sale.payment_term_id:
                    sale.sign_amount = invoiced
                    sale.remain_amount = sale.amount_total - sale.sign_amount
                    if sale.amount_total > 0:
                        sale.sign_percentage = round(
                            100 * (sale.sign_amount / sale.amount_total), 2
                        )
                        sale.remain_percentage = 100 - sale.sign_percentage
                        words = num2words(sale.amount_total, lang="es")
                        sale.amount_words = words.upper()
                        words = num2words(sale.sign_amount, lang="es")
                        sale.sign_words = words.upper()

    sign_amount = fields.Monetary(
        string="Sign Amount", compute=_onchange_payment_term
    )
    remain_amount = fields.Monetary(
        string="Remain Amount", compute=_onchange_payment_term
    )
    sign_percentage = fields.Float(
        string="Sign Percentage", compute=_onchange_payment_term
    )
    remain_percentage = fields.Float(
        string="Remain Percentage", compute=_onchange_payment_term
    )
    sign_words = fields.Char(
        string="Sign Amount Words", compute=_onchange_payment_term
    )
    amount_words = fields.Char(
        string="Amount Words", compute=_onchange_payment_term
    )
    stage_id = fields.Many2one(
        related="agreement_id.stage_id", string="Agreement Stage"
    )

    @api.multi
    def action_generate_template(self):
        for order in self:
            if not order.agreement_id:
                if order.agreement_template_id:
                    name = order.agreement_template_id.name
                    name += "| " + order.name
                    order.agreement_id = order.agreement_template_id.copy(
                        default={
                            "name": name,
                            "is_template": False,
                            "sale_id": order.id,
                            "partner_id": order.partner_id.id,
                            "analytic_account_id": (
                                order.analytic_account_id
                                and order.analytic_account_id.id
                                or False
                            ),
                            "start_date": order.start_date,
                            "end_date": order.end_date,
                            "sign_date": order.sign_date,
                        }
                    )
                    for line in self.order_line:
                        # Create agreement line
                        self.env["agreement.line"].create(
                            {
                                "product_id": line.product_id.id,
                                "name": line.name,
                                "agreement_id": order.agreement_id.id,
                                "qty": line.product_uom_qty,
                                "sale_line_id": line.id,
                                "uom_id": line.product_uom.id,
                            }
                        )
            if order.agreement_id:
                order.dynamic_description = (
                    order.agreement_id.dynamic_description
                )

    @api.multi
    def _action_confirm(self):
        res = super(SaleOrder, self)._action_confirm()
        for order in self:
            if not order.agreement_id:
                if order.agreement_template_id:
                    self.action_generate_template()
        return res

    @api.multi
    def _print_contract(self):
        for order in self:
            if not order.agreement_id:
                if order.agreement_template_id:
                    order.agreement_id

    @api.multi
    def print_agreement_contract(self):

        self.ensure_one()
        action = self.env.ref(
            "agreement_custom.partner_agreement_contract_document_preview"
        )
        vals = action.read()[0]
        context = vals.get("context", {})

        context["active_id"] = self.agreement_id.id
        context["active_ids"] = [self.agreement_id.id]
        vals["context"] = context
        return vals

    @api.multi
    def print_contract(self):

        self.ensure_one()
        action = self.env.ref(
            "agreement_custom.sale_agreement_contract_document_preview"
        )
        vals = action.read()[0]
        context = vals.get("context", {})

        context["active_id"] = self.id
        context["active_ids"] = [self.id]
        vals["context"] = context
        return vals

    @api.multi
    def close_agreement_contract(self):

        self.ensure_one()
        stage = self.env["agreement.stage"].search(
            [("close_stage", "=", True)]
        )
        if stage:
            stage = stage and stage[0]
            self.agreement_id.stage_id = stage.id
