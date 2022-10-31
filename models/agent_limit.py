from odoo import fields, models, api


class AgentLimit(models.Model):
    _name = 'agent.limit'
    _description = 'Description'

    agent_id = fields.Many2one('res.users')
    limit = fields.Float()

    _sql_constraints = [(
        'check_limit',
        'CHECK(limit > 0)',
        "boom.",
    ), ]

