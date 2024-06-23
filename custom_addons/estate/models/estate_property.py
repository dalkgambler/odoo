from odoo import models, fields, api , exceptions, tools

class estate_property(models.Model):
    _name = "estate.property"
    _description = "Owned Properties"
    _order = "id desc"

    name = fields.Char('Property Name',required=True)
    company_id=fields.Many2one('res.company','Responsible Company',default=lambda self: self.env.user.company_id)
    property_type_id= fields.Many2one('estate.property.type','Property Type')
    property_tag_ids= fields.Many2many('estate.property.tag',string='Product tag')
    property_offer_ids= fields.One2many('estate.property.offer','property_id','Offers')
    partner_id=fields.Many2one('res.partner','buyer')
    user_id=fields.Many2one('res.users','Salesman', readonly=True, default=lambda self :self.env.user)
    description = fields.Text('Property Description')
    postcode = fields.Char('ZIP Code', help='DÖNER')
    date_availability=fields.Date('Dates Available', copy=False, default=fields.Date.add(fields.Date.today(),days=90))
    expected_price=fields.Float('expected Price', required=True)
    selling_price=fields.Float('selling Price', readonly=True, copy=False)
    bedrooms=fields.Integer('# bedrooms', default=2)
    living_area=fields.Integer('# of sqm')
    facades=fields.Integer('facades')
    garage=fields.Boolean('has Garage',help='BOOL')
    garden=fields.Boolean('has Garden',help='boooleb')
    garden_area=fields.Integer('# of Garden sqm')
    total_area=fields.Integer('# of total sqm',compute='_compute_total_area')
    best_price=fields.Float('Best offer',compute="_compute_best_price")
    garden_orientation=fields.Selection(
        selection=[('n','North'),('e','East'),('s','South'),('w','West')],
        help="Main Orientation of the garden. Preferably South"
    )
    state=fields.Selection(
        selection=[('new','New'),('offer received','Offer Received'),('offer accepted','Offer Accepted'),('sold','Sold'),('canceled','Canceled')],
        default='new',
        copy=False,
        required=True
    )
    
    level = fields.Integer('# of levels from ground floor',required=True)
    active = fields.Boolean('Active', default=True)





    sequence = fields.Integer('Sequence',default=10)
    @api.depends('living_area','garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area=record.living_area+record.garden_area
    @api.depends('property_offer_ids')
    def _compute_best_price(self):
        
        for record in self:
            if(len(record.property_offer_ids)>0):
                record.best_price= max(record.mapped('property_offer_ids.price'))
            else:
                record.best_price=0
    @api.onchange('garden')
    def _onchange_garden(self):
        if(self.garden==True):
            self.garden_area=10
            self.garden_orientation="n"
        else:
            self.garden_area=0
            self.garden_orientation=""
    @api.onchange('bedrooms')
    def _onchange_bedrooms(self):
        return {'warning': {
                'title': ("Warning"),
                'message': (self.partner_id.name)}}
    
    def action_sell(self):
        for record in self:
            if record.state!='canceled':
                record.state='sold'
            else:
                raise exceptions.UserError("It has already been canceled or sold")

    def action_cancel(self):
        for record in self:
            if record.state!='sold':
                record.state='canceled'
            else:
                raise exceptions.UserError("It is already sold or sold")
    @api.constrains('selling_price','expected_price')
    def _constrain_sellig_price(self):
        for record in self:
            if not tools.float_utils.float_is_zero(record.selling_price,2):
                print(1)
                if tools.float_utils.float_compare(record.selling_price,record.expected_price*0.9,2)<0:
                    print(2)
                    raise exceptions.UserError("cannot be lower than 90 percent of the expected price")

    _sql_constraints = [
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'WTF how is this possible'),
        ('check_expected_price', 'CHECK(expected_price >= 0)','We cant lose money! you are fired')
    ]

    def unlink(self):
        for record in self:
            print("nigga")
            # if (record.state!='new' or record.state!='canceled'):
            #     raise exceptions.UserError("Can only delete New or canceled properties")
            # else:
            #     print("supernigga")
            return super().unlink()
    
            