from odoo import fields, models, api
import random


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'
    _description = 'Description'

    suggested_vendor = fields.Many2one('res.partner', compute='_compute_vendor_suggestion')

    @api.depends('product_id.seller_ids')
    def _compute_vendor_suggestion(self):
        for rec in self:
            if rec.product_id.seller_ids:
                a = min(rec.product_id.seller_ids.mapped('price'))
                vendor1 = [x for x in rec.product_id.seller_ids if x.price == a]
                b = min(rec.product_id.seller_ids.mapped('delay'))
                vendor2 = [x.name for x in vendor1 if x.delay == b]
                if len(vendor2) > 1:
                    rec.suggested_vendor = random.choice(vendor2)
                else:
                    rec.suggested_vendor = vendor2[0]
            else:
                rec.suggested_vendor = False
