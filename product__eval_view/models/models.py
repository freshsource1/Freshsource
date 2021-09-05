# -*- coding: utf-8 -*-

from odoo import models, fields
from odoo import tools, api


class product__eval_view(models.Model):
    _name = 'product__eval_view.product__eval_view'
    _auto = False
    _description = 'product__eval_view.product__eval_view'

    supplier_name = fields.Text( string="Supplier Name", required=False)
    product_name = fields.Text( string="Product Name", required=False)
    product_qty = fields.Float(digites=(7, 2), string="Stock Quantity", required=False)
    cost_price = fields.Float(digites=(7, 2), string="Cost Price", required=False)
    complete_name = fields.Text( string="Grade", required=False)
    price_unit = fields.Float(digites=(7, 2), string="Sales Price", required=False)
    qty_done2 = fields.Float(digites=(7, 2), string="Sales Quantity", required=False)
    qty_done = fields.Float(digites=(7, 2), string="Stock Quantity", required=False)
    total_qty = fields.Float(digites=(7, 2), string="Sales Quantity", required=False)
    profit = fields.Float(string="Profit", required=False, compute="get_score")
    profitMargin = fields.Text(string="Profit Margin", required=False, compute="get_score")
    grade_ratio = fields.Text(string="Grade %", required=False, compute="get_score")
    score = fields.Text(string="Score", required=False, compute="get_score")
    supplier_rate = fields.Text(string="Rating", required=False, compute="get_score")
    # product_manufacturers = fields.Selection( compute="get_manufactures",string='Manufacturer', required=True)

    @api.depends('cost_price','price_unit')
    def get_score(self):
        for rec in self:
            print(rec)
            if rec.cost_price or rec.price_unit:
                rec.profit = rec.price_unit - rec.cost_price
                profitMarginTemp = ( rec.profit / rec.cost_price ) * 100
                rec.profitMargin = str(round(profitMarginTemp,2)) + '%'
                gradeRatioTemp = ( rec.qty_done / rec.total_qty ) * 100
                rec.grade_ratio = str(round(gradeRatioTemp,2)) + '%'
                scoreTemp = ((profitMarginTemp / 100) * (gradeRatioTemp / 100)) * 100
                rec.score = str(round(scoreTemp, 2)) + '%'
                if 0 < scoreTemp <= 10:
                    rec.supplier_rate = 1
                elif 10 < scoreTemp <= 20:
                    rec.supplier_rate = 2
                elif 20 < scoreTemp <= 30:
                    rec.supplier_rate = 3
                elif 30 < scoreTemp <= 40:
                    rec.supplier_rate = 4
                elif 40 < scoreTemp <= 50:
                    rec.supplier_rate = 5
                elif 50 < scoreTemp <= 60:
                    rec.supplier_rate = 6
                elif 60 < scoreTemp <= 70:
                    rec.supplier_rate = 7
                elif 70 < scoreTemp <= 80:
                    rec.supplier_rate = 8
                elif 80 < scoreTemp <= 90:
                    rec.supplier_rate = 9
                elif 90 < scoreTemp <= 100:
                    rec.supplier_rate = 10
                else:
                    rec.supplier_rate = 0
                print(rec.supplier_rate)
                print(rec.profit)



    # def get_manufactures(self):
    #     manufactures = []
    #     raw_data = self.env['product__eval_view.product__eval_view'].search([])
    #     print(raw_data)
    #     for rec in raw_data:
    #         manufactures.append((rec.product_name, rec.supplier_name))
    #     print(manufactures)
    #     return manufactures
    def init(self):
        # manufactures = []
        # raw_data = self.env['product__eval_view.product__eval_view'].search([])
        # print(raw_data)
        # for rec in raw_data:
        #     manufactures.append((rec.product_name, rec.supplier_name))
        # print(manufactures)

        tools.drop_view_if_exists(self._cr, 'product__eval_view_product__eval_view')
        self._cr.execute("""
        CREATE OR REPLACE VIEW product__eval_view_product__eval_view AS  (
        SELECT row_number() OVER () AS id, line.supplier_name, line.product_name, line.cost_price,
                       line.qty_done,line.complete_name, line.price_unit, line.qty_done2, line.product_qty,line.total_qty FROM (
                   SELECT rs.name AS supplier_name, pt.name AS product_name, pr.price_average AS cost_price,
                          pr.qty_ordered AS qty_ordered, sm.id As stockmove_id,sml.qty_done AS qty_done
						  ,sl2.complete_name AS complete_name
						  , sml.lot_id AS lot_id,sml2.picking_id As picking_id,
						  sp.sale_id as sales_id, sol.price_unit AS price_unit , sml2.qty_done AS qty_done2, sm.product_qty AS product_qty 
						  , pol.product_qty As total_qty
                    From purchase_report pr
                     INNER JOIN res_partner rs ON (rs.id = pr.partner_id)
                     INNER JOIN product_product pp ON (pp.id = pr.product_id)
                     INNER JOIN product_template  pt ON (pt.id =  pp.product_tmpl_id)                     
                     INNER JOIN purchase_order po ON (po.id = pr.order_id)
					 LEFT JOIN  stock_location sl ON (sl.usage = 'supplier')
					 INNER JOIN stock_move sm ON (sm.origin = po.name And sm.location_id != sl.id and sm.product_id = pr.product_id and sm.origin = po.name)
					 INNER JOIN stock_move_line sml ON (sml.move_id = sm.id)
                     INNER JOIN stock_location sl2 ON (sl2.id = sml.location_dest_id)   
					 LEFT JOIN stock_location sl3 ON (sl3.usage = 'customer')
					 INNER JOIN stock_move_line sml2 ON (sml2.product_id = pr.product_id And sml2.lot_id =sml.lot_id And sml2.location_dest_id = sl3.id) 
					 INNER JOIN stock_picking sp ON (sp.id = sml2.picking_id)
					 INNER JOIN sale_order_line sol ON (sol.order_id = sp.sale_id And sol.product_id = pr.product_id)
					 INNER JOIN purchase_order_line pol ON (pol.order_id = pr.order_id And pol.product_id = pr.product_id)					 
       )line
       )
         """)


