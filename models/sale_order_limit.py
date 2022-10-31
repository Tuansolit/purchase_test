from odoo import fields, models, api


class SaleOrderLimit(models.Model):
    _name = 'sale.order.limit'
    _description = 'Description'

    agent_ids = fields.Many2many('agent.limit')
    name = fields.Char()

    def action_view_sale_limit(self):
        a = self.env.ref('test_purchase.sale_order_limit_1')

        view_id = self.env.ref('test_purchase.sale_limit_tree_view').id
        return {
            'type': 'ir.actions.act_window',
            'name': 'Bao cao chi tiet',
            'view_mode': 'form',
            'view_id': view_id,
            'res_model': 'sale.order.limit',
            'res_id': a.id,
            'target': 'current',
        }
