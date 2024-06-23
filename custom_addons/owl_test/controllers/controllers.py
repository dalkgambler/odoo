from odoo import http
from odoo.http import request, route

class OwlPlayground(http.Controller):
    @http.route(['/owl_test'], type='http', auth='public')
    def show_playground(self):
        """
        Renders the owl playground page
        """
        print("test")
        return request.render('owl_test.testsite')
