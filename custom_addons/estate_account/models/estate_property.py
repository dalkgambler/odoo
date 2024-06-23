from odoo import models,exceptions,api


class estate_property(models.Model):
    _inherit = "estate.property"
    

    def action_sell(self):
        print("nogger schmeckt gut")
        journal = self.env['account.move'].sudo().with_context(default_move_type='out_invoice')._get_default_journal()
        invoice_vals_list={
        'partner_id': self.partner_id,
        'move_type': 'out_invoice',
        'journal_id': journal.id,
        'invoice_line_ids': [
            (0,0,
                {
                    'name':self.name,
                    'quantity':1,
                    'price_unit':self.selling_price*0.06
                    }),
            (0,0,{
                    'name':'administrative_fees',
                    'quantity':1,
                    'price_unit':100
            })]

        }
        print(" reached ".center(100, '='))
        self.env['account.move'].sudo().with_context(default_move_type='out_invoice').create(invoice_vals_list)
        return super().action_sell()


