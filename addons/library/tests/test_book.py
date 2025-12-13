from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

class TestBook(TransactionCase):

    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        self.author = self.env['library.author'].create({'name': 'Test Author'})
        self.book = self.env['library.book'].create({
            'name': 'Test Book',
            'isbn': '978-3-16-148410-0',
            'author_id': self.author.id,
        })

    def test_book_creation(self):
        self.assertEqual(self.book.name, 'Test Book')
        self.assertEqual(self.book.author_id, self.author)

    def test_isbn_unique_constraint(self):
        with self.assertRaises(Exception):
            self.env['library.book'].create({
                'name': 'Another Book',
                'isbn': '978-3-16-148410-0',
                'author_id': self.author.id,
            })

    def test_date_published_constraint(self):
        with self.assertRaises(ValidationError):
            self.book.date_published = '2999-12-31'
