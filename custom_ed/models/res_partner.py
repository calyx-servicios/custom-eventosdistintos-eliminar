# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.addons.base.res.res_partner import WARNING_MESSAGE, WARNING_HELP
import logging
_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = 'res.partner'

    
    @api.model
    def create(self, vals):
        if vals.get('sequence', 0) == 0:
            if 'company_id' in vals:
                vals['sequence'] = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code('res.partner') or 0
            else:
                vals['sequence'] = self.env['ir.sequence'].next_by_code('res.partner') or 0
        result = super(ResPartner, self).create(vals)
        return result

    sequence = fields.Integer(string='Sequence')

    def make_domain(self, domain_name, code):
        domain_code= [(domain_name,'ilike','%')]
        if code:
            i=code.find(' ')
            domain_code=[]
            while i!= -1:
                domain_code.append((domain_name,'ilike',code[0:i]))
                code=code[i+1:]
                i=code.find(' ')
            domain_code.append((domain_name,'ilike',code))
        return domain_code
    

    @api.multi
    def name_get(self):
 
        def _name_get(d):
            name = d.get('name','')
            sequence = self._context.get('sequence', True) and d.get('sequence',False) or False
            if sequence:
                name = '%s [%s]' % (name, sequence)
            return (d['id'], name)

        result = []
        for partner in self:
            name = partner.name
            sequence = None
            if partner.sequence:
                sequence = partner.sequence
 
            mydict = {
                      'id': partner.id,
                      'name': name,
                      'sequence': sequence,
                       }
            result.append(_name_get(mydict))
        return result


    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        if not args:
            args = []
        
        if name:
            number=0
            try:
                number=int(name)
            except:
                pass
            if number>0:
                domain = []
                doc_domain = self.make_domain('sequence',name)
                return self.search(doc_domain + args, limit=limit).name_get()
            else:               
                code_domain = self.make_domain('name',name)
                return self.search(code_domain + args, limit=limit).name_get()
        else:
            code_domain = self.make_domain('name','')
            return self.search(code_domain + args, limit=limit).name_get()

    