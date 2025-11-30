from odoo import models, fields

class LibraryAuthor(models.Model):
    _name = 'library.author'
    _description = 'Author'

    name = fields.Char(string='Name', required=True)
    book_ids = fields.One2many(
        comodel_name='library.book',
        inverse_name='author_id',
        string='Books'
    )