# -*- coding: utf-8 -*-
# from odoo import http


# class ProductEvalView(http.Controller):
#     @http.route('/product__eval_view/product__eval_view/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/product__eval_view/product__eval_view/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('product__eval_view.listing', {
#             'root': '/product__eval_view/product__eval_view',
#             'objects': http.request.env['product__eval_view.product__eval_view'].search([]),
#         })

#     @http.route('/product__eval_view/product__eval_view/objects/<model("product__eval_view.product__eval_view"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('product__eval_view.object', {
#             'object': obj
#         })
