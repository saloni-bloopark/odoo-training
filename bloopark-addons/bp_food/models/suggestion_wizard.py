from odoo import fields, models, api
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError


class CheckBookingWizard(models.Model):
    _name = 'check.booking.table'
    _description = "Booking"

    current_tables = fields.Many2many('food.table')
    # current_table_end = fields.Datetime(related='current_tables.end_time',
    #                                        string='Booked End Table', readonly=True)
    name = fields.Char("name")
    customer = fields.Many2one('res.partner')
    request_start_date = fields.Datetime("Request Start DateTime")
    request_end_date = fields.Datetime("Request End DateTime")
    existing_table = fields.Many2one('food.table', required=True)
    available_end = fields.Datetime(related='existing_table.end_time')
    available_start = fields.Datetime(related='existing_table.start_time')


    @api.constrains('request_start_date', 'request_end_date')
    def _check_table_time(self):
        if self.request_end_date <= self.request_start_date:
            # print(self.end_time)
            raise ValidationError('End time must be after Start time')

    @api.constrains('request_start_date', 'available_end')
    def _check_availability(self):
        for rec in self:
            if rec.request_end_date <= rec.request_start_date:
                raise ValidationError('Invalid end date!')
            elif (rec.request_start_date > rec.available_start) and (rec.request_end_date < rec.available_end):
                raise ValidationError('This table is already booked for this time window!')
            elif (rec.request_start_date < rec.available_end) and (rec.request_end_date > rec.available_end):
                raise ValidationError('Table cannot be booked starting at this time!')
            elif (rec.request_start_date < rec.available_start) and (rec.request_end_date > rec.available_start):
                raise ValidationError('Table cannot be booked until this time!')
            elif rec.request_start_date < datetime.now():
                raise ValidationError('Your table cannot be booked in the past!')
            else:
                raise ValidationError('Yay! Table can be booked.')