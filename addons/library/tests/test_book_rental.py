from odoo.tests.common import TransactionCase
from odoo import fields

class TestBookRental(TransactionCase):

    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        self.partner = self.env['res.partner'].create({'name': 'Test Partner'})
        self.author = self.env['library.author'].create({'name': 'Test Author'})
        self.book = self.env['library.book'].create({
            'name': 'Test Book',
            'isbn': '978-3-16-148410-0',
            'author_id': self.author.id,
        })
        self.rental = self.env['library.book.rental'].create({
            'book_id': self.book.id,
            'partner_id': self.partner.id,
            'start_date': fields.Date.today(),
            'end_date': fields.Date.add(fields.Date.today(), days=7),
        })

    def test_rental_creation(self):
        self.assertEqual(self.rental.state, 'draft')

    def test_state_transitions(self):
        self.rental.action_rent()
        self.assertEqual(self.rental.state, 'rented')
        self.rental.action_return()
        self.assertEqual(self.rental.state, 'returned')
        self.rental.action_draft()
        self.assertEqual(self.rental.state, 'draft')

    def test_cron_check_due_rentals(self):
        self.rental.action_rent()
        self.rental.end_date = fields.Date.subtract(fields.Date.today(), days=1)
        self.env['library.book.rental']._cron_check_due_rentals()
        activity = self.env['mail.activity'].search([
            ('res_id', '=', self.rental.id),
            ('res_model_id', '=', self.env['ir.model']._get_id('library.book.rental')),
        ])
        self.assertTrue(activity)
