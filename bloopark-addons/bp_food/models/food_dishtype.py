import time

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.osv import expression
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT

from odoo import models, fields, api


class DishType(models.Model):
    _name = "food.dishtype"
    _description = "describes the different types of dishes that can be added"

    name = fields.Char(string="New Dish Name", required=True)
    dish_ingredients = fields.Char(string="Specify the Dish Ingredients")
    dish_type = fields.Selection([
        ('veg', 'Vegetarian'),
        ('nonveg', 'Non-Vegertarian'),
        ('mix', 'Mixed')], string='Type of Dish')
    dish_price = fields.Integer(string='Price of the Dish')
    dish_cuisine = fields.Char(string='Cuisine it belongs to')
    dish_comments = fields.Char(string='Add Comments about Dish')
    status = fields.Selection(string='Status', selection=[
        ('open', 'Open'),
        ('inprogress', 'In Progress'),
        ('finished', 'Finished'),
    ], default='open', required=True)


    def dish_final(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Menu Details and Dishes',
            'view_mode': 'tree',
            'res_model': 'food.menu',
        }
