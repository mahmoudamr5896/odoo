from odoo import models, fields

class Ticket(models.Model):
    _name = 'ticket'
    _description = 'Ticket'

    name = fields.Char(string='Name', required=True)
    number = fields.Char(string='Number', required=True)
    tag = fields.Char(string='Tag')
    state = fields.Selection([('new', 'New'), ('doing', 'Doing'), ('done', 'Done')], default='new', string='State')
    file = fields.Binary(string='File')
    assign_to = fields.Many2one('res.users', string='Assign To')
    description = fields.Text(string='Description')
