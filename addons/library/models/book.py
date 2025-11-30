from odoo import models, fields

class Book(models.Model):
    _name = 'book'
    _description = 'Book'

    name = fields.Char(string='Name', required=True)
    isbn = fields.Char(string='ISBN', required=True)
    is_best_seller = fields.Boolean(string='Is Best Seller', default=False)
    edition_number = fields.Float(string='Edition Number')
    description = fields.Text(string='Description')
    date_published = fields.Date(string='Date Published')
    book_genre = fields.Selection([
        ('novel', 'Novel'),
        ('poetry', 'Poetry'),
        ('science_fiction', 'Science Fiction'),
        ('biography', 'Biography'),
        ('history', 'History'),
        ('children', 'Children'),
    ], string='Book Genre')