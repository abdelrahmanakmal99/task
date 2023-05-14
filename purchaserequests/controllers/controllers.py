# -*- coding: utf-8 -*-
# from odoo import http


# class Purchaserequests(http.Controller):
#     @http.route('/purchaserequests/purchaserequests', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/purchaserequests/purchaserequests/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('purchaserequests.listing', {
#             'root': '/purchaserequests/purchaserequests',
#             'objects': http.request.env['purchaserequests.purchaserequests'].search([]),
#         })

#     @http.route('/purchaserequests/purchaserequests/objects/<model("purchaserequests.purchaserequests"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('purchaserequests.object', {
#             'object': obj
#         })
