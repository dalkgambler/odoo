from odoo import models, fields, api

class estate_property_type(models.Model):
    _name='estate.property.type'
    _description='Different Types of Property'
    _order='sequence'

    name=fields.Char('Property Type', required= True)
    sequence=fields.Integer('Sequence',default=10)
    property_ids=fields.One2many('estate.property','property_type_id','Properties')
    offer_ids=fields.One2many('estate.property.offer','property_type_id','Offers')
    offer_count=fields.Integer("total offers", compute="_compute_offer_count")

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count=len(record.offer_ids)

    


    _sql_constraints = [

        ('unique_name', 'UNIQUE(name)', 'name must be unique')

    ]
