from odoo import models, fields, api
class CloseProjectWizard(models.TransientModel):
    _name = 'close.project.wizard'
    _description = 'Close Project Wizard'
    project_id = fields.Many2one('client.project',
        string='Project', required=True)
    close_reason = fields.Selection([
        ('completed', 'Successfully Completed'),
        ('cancelled', 'Cancelled by Client'),
        ('budget', 'Budget Exhausted'),
    ], string='Close Reason', required=True)
    final_notes = fields.Text(string='Final Notes')
    final_cost = fields.Float(string='Final Cost')
    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        active_id = self.env.context.get('active_id')
        if active_id:
            res['project_id'] = active_id
        return res
    def action_close(self):
        self.project_id.write({
            'state': 'closed',
            'actual_cost': self.final_cost,
        })
        self.project_id.message_post(
            body=f'Project closed. Reason: {self.close_reason}. {self.final_notes or ""}',
            subtype_xmlid='mail.mt_note'
        )
        return {'type': 'ir.actions.act_window_close'}
