from odoo import fields, models, api


class ReportMonth(models.Model):
    _name = 'report.month'
    _description = 'Description'

    department_id = fields.Many2one('hr.department')
    spending_limit = fields.Float(compute='compute_spending_limit')
    actual_spending = fields.Float(compute='_compute_actual_spending')
    months = fields.Char()

    def _compute_actual_spending(self):
        for team in self:
            def filter_month(f_rec):
                return f_rec.create_date.strftime('%b') == team.months

            opportunity_data = self.env['purchase.order'].search(
                [('state', '=', 'purchase'), ('department_id.id', 'in', team.department_id.mapped('id'))]).filtered(
                filter_month)
            if len(opportunity_data) == 0:
                team.actual_spending = 0
            else:
                for rec in opportunity_data:
                    team.actual_spending += sum(rec.mapped('amount_total'))

    def compute_spending_limit(self):
        for rec in self:
            rec.spending_limit = rec.department_id.monthly_spending_limit
