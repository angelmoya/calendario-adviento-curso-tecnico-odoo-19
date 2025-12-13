from odoo import api, models, fields
from odoo.exceptions import ValidationError

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Book'

    name = fields.Char(string='Name', required=True)
    isbn = fields.Char(string='ISBN', required=True, copy=False)
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
        relation='library_book_tag_rel',
        column1='book_id',
        column2='tag_id',
        string='Tags',
        compute='_compute_tag_ids',
        store=True,
        readonly=False
    )
    product_ids = fields.One2many(
        comodel_name='product.template',
        inverse_name='book_id',
        string='Products'
    )
    product_qty = fields.Integer(
        string='Product Quantity',
        compute='_compute_product_qty',
        store=True
    )
    active = fields.Boolean(
        string='Active',
        default=True)
    catalog_date = fields.Datetime(
        string='Catalog Date',
        default=fields.Datetime.now
    )
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='User',
        default=lambda self: self.env.user
    )

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        author = self.env['library.author'].search([], limit=1)
        if author:
            res.update({
                'author_id': author.id
            })
        return res

    # _sql_constraints = [
    #     ('isbn_unique', 'unique(isbn)', 'The ISBN must be unique across all books.')
    # ]
    _check_isbn_unique = models.Constraint(
        'unique(isbn)',
        'The ISBN must be unique across all books.',
    )

    @api.constrains('date_published')
    def _check_date_published(self):
        # for book in self:
        #     if book.date_published and book.date_published > fields.Date.today():
        if self.filtered(lambda b: b.date_published and b.date_published > fields.Date.today()):
            raise ValidationError('The date published cannot be in the future.')
    

    @api.depends('product_ids')
    def _compute_product_qty(self):
        for book in self:
            book.product_qty = len(book.product_ids)
    
    @api.depends('author_id')
    def _compute_tag_ids(self):
        for book in self:
            if book.author_id:
                book.tag_ids = book.author_id.default_tag_ids.ids
    
    def action_clean_tags(self):
        for book in self:
            book.tag_ids = False
    
    # def action_update_autrho_tags_with_other_books_tags(self):
    #     self.with_context(add_other_book_tags=True).action_update_author_tags()
    
    def action_update_author_tags(self):
        # for book in self:
        #     if book.author_id:
        for book in self.filtered(lambda b: b.author_id):
            book.author_id.default_tag_ids = book.tag_ids
            if self.env.context.get('add_other_book_tags'):
                book.author_id.default_tag_ids |= book.author_id.book_ids.tag_ids
    
    def action_open_books_with_same_tags(self):
        self.ensure_one()
        domain = [('tag_ids', 'in', tag.id) for tag in self.tag_ids]
        domain.append(('id', '!=', self.id))
        books = self.env['library.book'].search(domain)
        return {
            'name': 'Books with Same Tags',
            'type': 'ir.actions.act_window',
            'res_model': 'library.book',
            'view_mode': 'list,form',
            # 'domain': [('tag_ids', '==', self.tag_ids.ids)],
            'domain': [('id', 'in', books.ids)],
        }
