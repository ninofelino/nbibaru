# -*- coding: utf-8 -*-

from odoo import models, fields, api
class felino(models.Model):
     _name = 'felino.felino'
     name = fields.Char()
     barcode = fields.Char()
     catagory = fields.Char()
     article = fields.Char()
     ukuran  = fields.Char()
     index  = fields.Integer()
     ondhand  = fields.Integer()
     sale_price = fields.Char()
     list_price = fields.Char()
     description = fields.Text()
     
