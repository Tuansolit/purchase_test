from odoo import fields, models, api
from odoo.exceptions import ValidationError


class HrDepartment(models.Model):
    _inherit = 'hr.department'
    _description = 'Description'

    monthly_spending_limit = fields.Float(string='Spending Limit/Month')
    # actual_spending = fields.Float(compute='_compute_actual_spending')
    months = fields.Char()

    # def _compute_actual_spending(self):
    #     for team in self:
    #         def filter_month(f_rec):
    #             return f_rec.create_date.strftime('%b') == team.months
    #
    #         opportunity_data = self.env['purchase.order'].search(
    #             [('state', '=', 'purchase'), ('department_id.id', '=', team.id)]).filtered(filter_month)
    #         if len(opportunity_data) == 0:
    #             team.actual_sale = 0
    #         else:
    #             for rec in opportunity_data:
    #                 team.actual_sale += sum(rec.order_ids.mapped('amount_untaxed'))
