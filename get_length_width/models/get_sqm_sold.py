from odoo import api, models, fields


class InheritProductTemplate(models.Model):
    _inherit = "product.template"

    length = fields.Float(string="Length")
    width = fields.Float(string="Width")
    gsm = fields.Float(string="GSM")


class SaleOrderSQM(models.Model):
    _inherit = "sale.order.line"

    length = fields.Float(string="Length", related='product_id.product_tmpl_id.length' ,readonly=False)
    width = fields.Float(string="Width", related='product_id.product_tmpl_id.width',readonly=False, )
    no_of_rolls = fields.Float(string="No of Rolls")
    total_sqm_sold = fields.Float(string="Total Sqm Sold")

    @api.onchange('length', 'width', 'no_of_rolls', 'product_uom_qty')
    def calculate_sqm_sold(self):
        self.total_sqm_sold = self.length * self.width * self.no_of_rolls
        self.product_uom_qty = (self.total_sqm_sold * self.product_id.product_tmpl_id.gsm) / 1000


    def _prepare_invoice_line(self , **optional_values):
        res = super(SaleOrderSQM, self)._prepare_invoice_line(**optional_values)
        res.update({'length': self.length,
                    'width': self.width,
                    'no_of_rolls': self.no_of_rolls,
                    'total_sqm_sold': self.total_sqm_sold,
                    })
        return res


class AccountMoveSQM(models.Model):
    _inherit = "account.move.line"

    length = fields.Float(string="Length")
    width = fields.Float(string="Width")
    no_of_rolls = fields.Float(string="No of Rolls")
    total_sqm_sold = fields.Float(string="Total Sqm Sold")
