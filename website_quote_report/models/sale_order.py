from odoo import models, fields, api, _

class SaleOrder(models.Model):
    _inherit = "sale.order"

    name_honoree = fields.Char(string='Name of the Honoree')

    event_type_id = fields.Many2one(
        comodel_name="crm.event.type",
        string="Event Type",
    )
    requested_date = fields.Datetime(string="Requested Date")