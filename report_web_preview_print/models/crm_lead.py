from odoo import models, fields, api, _

class CrmLead(models.Model):
    _inherit = "crm.lead"

    name_honoree = fields.Char(string='Name of the Honoree')

    event_type_id = fields.Many2one(
        comodel_name="crm.event.type",
        string="Event Type",
    )

