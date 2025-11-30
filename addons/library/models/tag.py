from odoo import models, fields

class LibraryTag(models.Model):
    _name = 'library.tag'
    _description = 'Tag'

    name = fields.Char(string='Name', required=True)
    book_ids = fields.Many2many(
        comodel_name='library.book',
        relation='library_book_tag_rel',
        column1='tag_id',
        column2='book_id',
        string='Books'
    )