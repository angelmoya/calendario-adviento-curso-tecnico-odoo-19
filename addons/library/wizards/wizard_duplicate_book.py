from odoo import models, fields, api, _
from odoo.exceptions import UserError

class WizardDuplicateBook(models.TransientModel):
    _name = 'wizard.duplicate.book'
    _description = 'Asistente para Duplicar Libro y Cambiar ISBN'

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
    author_id = fields.Many2one(
        comodel_name='library.author',
        string='Author'
    )
    tag_ids = fields.Many2many(
        comodel_name='library.tag',
        string='Tags',
    )

    @api.model
    def default_get(self, fields_list):
        """
        Sobreescribe default_get para obtener el ID del libro activo 
        (que Odoo pone en el contexto) e inicializar los campos.
        """
        res = super(WizardDuplicateBook, self).default_get(fields_list)
        
        # Odoo inyecta el ID del registro abierto en el contexto como 'active_id'.
        active_id = self.env.context.get('active_id')

        if self.env.context.get('active_model') != 'library.book':
            raise UserError(_('This wizard must be opened from a Library Book record.'))
        
        if active_id:
            original_book = self.env['library.book'].browse(active_id)
            
            res.update({
                'name': original_book.name,
                'is_best_seller': original_book.is_best_seller,
                'edition_number': original_book.edition_number,
                'description': original_book.description,
                'date_published': original_book.date_published,
                'book_genre': original_book.book_genre,
                'author_id': original_book.author_id.id,
                'tag_ids': [(6, 0, original_book.tag_ids.ids)],
            })
        
        return res

    def action_duplicate_and_update(self):
        """
        Ejecuta la copia del libro y sobrescribe los valores clave con 
        los datos proporcionados por el usuario en el Wizard.
        """
        self.ensure_one()
        
        new_book = self.env['library.book'].create({
            'name': self.name,
            'isbn': self.isbn,
            'is_best_seller': self.is_best_seller,
            'edition_number': self.edition_number,
            'description': self.description,
            'date_published': self.date_published,
            'book_genre': self.book_genre,
            'author_id': self.author_id.id,
            'tag_ids': self.tag_ids.ids,
        })
        
        # Devolver una acción para abrir inmediatamente el formulario del nuevo libro
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'library.book',
            'views': [(False, 'form')],
            'res_id': new_book.id,
            'target': 'current', # Abre el nuevo formulario en la misma ventana
        }