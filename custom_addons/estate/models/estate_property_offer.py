from odoo import models, fields, api, exceptions, tools

class estate_property_offer(models.Model):
    _name='estate.property.offer'
    _description='Offers for different Properties'
    _order='price desc'


    price=fields.Float('Price')
    state=fields.Selection([('accepted','Accepted'),('refused','Refused')],'Status',copy=False)
    partner_id=fields.Many2one('res.partner','Client',required=True)
    property_id=fields.Many2one('estate.property','Property',required=True)
    property_type_id=fields.Many2one(related="property_id.property_type_id")
    validity=fields.Integer('days valid',default=7)
    date_deadline=fields.Date('deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline')

    

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            if 'create_day' in record:
                record.date_deadline= fields.Date.add(record.create_day,days=record.validity)
            else:
                record.date_deadline= fields.Date.add(fields.Date.today(),days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if 'create_day' in record:
                record.validity=(record.date_deadline - record.create_day).days
            else:
                record.validity=(record.date_deadline - fields.Date.today()).days
    def action_confirm(self):
        print(self)
        for record in self:
            print(record)
            already_accepted=0
            for line in record.property_id.property_offer_ids:
                if line.state=="accepted":
                    already_accepted=1
            if already_accepted==0:
                record.state="accepted"
                record.property_id.partner_id=record.partner_id
                record.property_id.selling_price=record.price
                record.property_id.state='offer accepted'
            else:
                raise exceptions.UserError("User ERROR!! Bist du blöd? \nthere can only be one accepted offer!!")

    def action_decline(self):
        for record in self:
            record.state='refused'
            
    _sql_constraints = [
        
        ('check_price', 'CHECK(price > 0)',
         'The Offer needs to be bigger than 0')
    ]

    @api.model
    def create(self, vals):
        print(vals)
    
        property_id=self.env['estate.property'].browse(vals['property_id'])
        print(property_id)
        current_price=vals['price']
        highest_price=0
        
        
        for offer in property_id.property_offer_ids:
            print(offer.price)
            if tools.float_utils.float_compare(highest_price,offer.price,2)<=0:
                highest_price=offer.price
        print(highest_price)
        if tools.float_utils.float_compare(highest_price,current_price,2)>=0:
            raise exceptions.UserError("price must be higher than"+str(highest_price)+" aids")
        if(property_id.state=='new'):
            property_id.state='offer received'
        return super().create(vals)