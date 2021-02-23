from odoo import fields, models, _
from odoo.exceptions import Warning


class CrmEventType(models.Model):
    _name = "crm.event.type"
    _rec_name = "event_type"
    _order = "sequence"

    event_type = fields.Char("Event Type")
    active = fields.Boolean(default=True)
    sequence = fields.Integer(default=10)

    def unlink(self):
        crm_obj = self.env["crm.lead"]
        rule_ranges = crm_obj.search([("event_type", "=", self.id)])
        if rule_ranges:
            raise Warning(
                _(
                    "You are trying to delete a record "
                    "that is still referenced in one o more crm, "
                    "try to archive it."
                )
            )
        return super(CrmEventType, self).unlink()
