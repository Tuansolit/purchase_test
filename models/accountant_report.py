from odoo import fields, models, api
from datetime import datetime


class AccountantReport(models.TransientModel):
    _name = 'accountant.report'
    _description = 'Description'

    name = fields.Char()
    months = fields.Selection(
        [
            ('Jan', 'January'),
            ('Feb', 'February'),
            ('Mar', 'March'),
            ('Apr', 'April'),
            ('May', 'May'),
            ('Jun', 'June'),
            ('Jul', 'July'),
            ('Aug', 'August'),
            ('Sep', 'September'),
            ('Oct', 'October'),
            ('Nov', 'November'),
            ('Dec', 'December'),
        ],
        default=datetime.today().strftime('%b'))
    department_ids = fields.Many2many('hr.department', string='Department')

    def action_view_report(self):
        for rec in self.env['report.month'].search([]):
            rec.months = self.months

        def filter_month(f_rec):
            return f_rec.create_date.strftime('%b') == self.months

        if not self.department_ids:
            reports = self.env['report.month'].search([])
        else:
            reports = self.env['report.month'].search(
                [('department_id', 'in', self.department_ids.mapped('id'))])
        # plans = self.mapped('plan_id')

        action = self.env["ir.actions.actions"]._for_xml_id("test_purchase.report_month_act_window")
        action['domain'] = [('id', 'in', reports.ids)]

        context = {
            'default_move_type': 'out_plan',
        }
        action['context'] = context
        return action
