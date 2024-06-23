# -*- coding: utf-8 -*-
# from odoo import http


# class Hospital2(http.Controller):
#     @http.route('/hospital2/hospital2/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hospital2/hospital2/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hospital2.listing', {
#             'root': '/hospital2/hospital2',
#             'objects': http.request.env['hospital2.hospital2'].search([]),
#         })

#     @http.route('/hospital2/hospital2/objects/<model("hospital2.hospital2"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hospital2.object', {
#             'object': obj
#         })
