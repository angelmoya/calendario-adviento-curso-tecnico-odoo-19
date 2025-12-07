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
    default_tag_ids = fields.Many2many(
        comodel_name='library.tag',
        string='Default Tags'
    )