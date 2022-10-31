from odoo import fields, models, api
from odoo.exceptions import UserError
import datetime


class PurchaseOrder(models.Model):
    _description = 'Description'
    _inherit = 'purchase.order'

    department_id = fields.Many2one('hr.department', required=True)

    def button_confirm(self):
        def filter_agent(f_rec):
            return f_rec.agent_id == self.env.user.id

        dep_id = self.env.ref('test_purchase.sale_order_limit_1').mapped('agent_ids').filtered(filter_agent)
        for rec in self:
            if self.env.user.has_group('test_purchase.ke_toan_vien_group_user'):
                continue
            elif rec.amount_total > dep_id.limit:
                rec.create_activity()
                raise UserError('Wait for accountant to confirm')
        return super(PurchaseOrder, self).button_confirm()

    def create_activity(self):
        self.ensure_one()
        # db_name = registry_get(self.env['ir.model'].sudo().search([('model', '=', 'mail.activity')]).name)
        # with registry().cursor() as cr:
        #     env = api.Environment(cr, SUPERUSER_ID, {})
        todos = [{
            'res_id': self.id,
            'res_model_id': self.env['ir.model'].sudo().search([('model', '=', 'purchase.order')]).id,
            'user_id': kt.id,
            'summary': 'can confirm',
            'note': 'Can nhan vien ke toan confirm',
            'activity_type_id': 4,
            'date_deadline': datetime.date.today(),
        } for kt in self.env.ref('test_purchase.ke_toan_vien_group_user').users]

        for todo in todos:
            self.env['mail.activity'].sudo().create(todo)
            self.env.cr.commit()
