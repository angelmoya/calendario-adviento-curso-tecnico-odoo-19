from odoo import models, fields

class LibraryAuthor(models.Model):
    _name = 'library.author'
    _description = 'Author'

    name = fields.Char(string='Name', required=True)