from odoo import models, fields, api

class BookRental(models.Model):
    _name = 'library.book.rental'
    _description = 'Book Rental'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    book_id = fields.Many2one(
        comodel_name='library.book',
        string='Book',
        required=True
    )
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Partner',
        required=True
    )
    start_date = fields.Date(
        string='Start Date',
        required=True,
        default=fields.Date.context_today
    )
    end_date = fields.Date(
        string='End Date',
        required=True
    )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('rented', 'Rented'),
        ('returned', 'Returned'),
    ], string='State', default='draft')
    user_id = fields.Many2one(
        'res.users',
        string='User',
        default=lambda self: self.env.user,
        required=True
    )

    def action_rent(self):
        self.write({'state': 'rented'})

    def action_return(self):
        self.write({'state': 'returned'})

    def action_draft(self):
        self.write({'state': 'draft'})

    def _cron_check_due_rentals(self):
        yesterday = fields.Date.subtract(fields.Date.today(), days=1)
        due_rentals = self.search([
            ('state', '=', 'rented'),
            ('end_date', '=', yesterday)
        ])
        for rental in due_rentals:
            self.env['mail.activity'].create({
                'res_id': rental.id,
                'res_model_id': self.env['ir.model']._get_id(self._name),
                'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                'summary': 'Review due rental',
                'user_id': rental.user_id.id,
            })

