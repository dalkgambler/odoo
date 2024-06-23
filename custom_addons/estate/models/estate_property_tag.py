from odoo import models, fields


class estate_property_tag(models.Model):
    _name="estate.property.tag"
    _description="Tag for Properties"
    _order="name"

    name=fields.Char('TagName')
    color=fields.Integer('Color')
    
    _sql_constraints = [

        ('unique_name', 'UNIQUE(name)', 'name must be unique')

    ]