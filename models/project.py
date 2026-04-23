from odoo import models, fields, api
from odoo.exceptions import ValidationError
class ClientProject(models.Model):
    _name = 'client.project'
    _description = 'Client Project'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_start desc'
    name = fields.Char(string='Project Name', required=True,
        tracking=True)
    reference = fields.Char(string='Reference', readonly=True,
        default='New')
    client_id = fields.Many2one('res.partner', string='Client',
        required=True, tracking=True)
    user_id = fields.Many2one('res.users', string='Project Manager',
        default=lambda self: self.env.user)
    date_start = fields.Date(string='Start Date',
        default=fields.Date.today)
    date_end = fields.Date(string='End Date')
    budget = fields.Monetary(string='Budget',
        currency_field='currency_id')
    currency_id = fields.Many2one('res.currency',
        default=lambda self: self.env.company.currency_id)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('on_hold', 'On Hold'),
        ('closed', 'Closed'),
    ], string='Status', default='draft', tracking=True)
    description = fields.Html(string='Description')
    is_over_budget = fields.Boolean(compute='_compute_over_budget',
        store=True)
    actual_cost = fields.Monetary(string='Actual Cost',
        currency_field='currency_id')
    completion_pct = fields.Float(string='Completion %',
        digits=(5, 2))
    @api.depends('budget', 'actual_cost')
    def _compute_over_budget(self):
        for rec in self:
            rec.is_over_budget = rec.actual_cost > rec.budget
    @api.model
    def create(self, vals):
        if vals.get('reference', 'New') == 'New':
            vals['reference'] = self.env['ir.sequence'].next_by_code(
                'client.project') or 'New'
        return super().create(vals)
    def action_start(self):
        self.write({'state': 'active'})
    def action_hold(self):
        self.write({'state': 'on_hold'})
    def action_open_close_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Close Project',
            'res_model': 'close.project.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'active_id': self.id},
        }