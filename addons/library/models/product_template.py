from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    book_id = fields.Many2one(
        comodel_name='library.book',
        string='Book'
    )