from odoo import models, fields

class BookRental(models.Model):
    _name = 'library.book.rental'
    _description = 'Book Rental'

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
