from odoo import models, fields, api

class DailyRentalAvailability(models.Model):
    _name = 'daily.rental.availability'
    _description = 'Daily Rental Availability'
    _auto = False
    _rec_name = 'date'
    
    book_id = fields.Many2one(
        comodel_name='library.book',
        string='Book',
        readonly=True
    )
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Partner',
        readonly=True
    )
    date = fields.Date(
        string='Date',
        readonly=True)
    
    
    def init(self):
        self.env.cr.execute(f"""
            DROP VIEW IF EXISTS {self._table} CASCADE;
            
            CREATE OR REPLACE VIEW {self._table} AS (
                SELECT
                    ROW_NUMBER() OVER(ORDER BY library_book_rental.id, calendar.date) AS id,
                    library_book_rental.book_id,
                    library_book_rental.partner_id,
                    calendar.date
                FROM
                    library_book_rental,
                    /* La función generate_series que expande cada fila */
                    generate_series(library_book_rental.start_date, 
                                    library_book_rental.end_date, 
                                    '1 day'::interval) AS calendar(date)
                ORDER BY
                    library_book_rental.book_id,
                    calendar.date
            );
        """)