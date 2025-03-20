# Copyright 2025 - TODAY, Wesley Oliveira <wesley.oliveira@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductTemplate(models.Model):

    _inherit = "product.template"

    lrm_is_subcontracted = fields.Boolean(
        compute="_compute_lrm_is_subcontracted", default=False
    )

    @api.depends("seller_ids")
    def _compute_lrm_is_subcontracted(self):
        for template in self:
            template.lrm_is_subcontracted = False
            subcontractor_ids = template.seller_ids.filtered(
                lambda x: x.is_subcontractor
            )
            if subcontractor_ids:
                template.lrm_is_subcontracted = True

    def action_subcontract_bom_cost(self):
        templates = self.filtered(
            lambda t: t.product_variant_count == 1 and t.bom_count > 0
        )
        if templates:
            return templates.mapped("product_variant_id").action_subcontract_bom_cost()


class ProductProduct(models.Model):

    _inherit = "product.product"

    lrm_is_subcontracted = fields.Boolean(
        compute="_compute_lrm_is_subcontracted", default=False
    )

    @api.depends("seller_ids")
    def _compute_lrm_is_subcontracted(self):
        for product in self:
            product.lrm_is_subcontracted = False
            subcontractor_ids = product.seller_ids.filtered(
                lambda x: x.is_subcontractor
            )
            if subcontractor_ids:
                product.lrm_is_subcontracted = True

    def action_subcontract_bom_cost(self):
        for product in self:
            product.action_bom_cost()
            subcontractor_ids = product.seller_ids.filtered(
                lambda x: x.is_subcontractor
            )
            if product.lrm_is_subcontracted and subcontractor_ids:
                product.standard_price = (
                    product.standard_price + subcontractor_ids[0].price
                )
