# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class IrActionsReport(models.Model):
    _inherit = "ir.actions.report"

    preview = fields.Boolean(string="Preview?", default=False)

    @api.model
    def get_report_from_name(self, report_name):
        """Get the first record of ir.actions.report having the ``report_name`` as value for
        the field report_name.
        """
        report_obj = self.env["ir.actions.report"]
        conditions = [("report_name", "=", report_name)]
        fields = ["preview"]
        context = self.env["res.users"].context_get()
        report_obj = report_obj.with_context(context).search_read(
            conditions, fields, limit=1
        )
        return report_obj
