import base64
import json

from odoo import Command, _
from odoo.exceptions import UserError
from odoo.tools import file_open


def post_init_hook(env):
    """Load only new module-owned showcase records; never rewrite real catalogue data."""
    sites = env["website"].search([("bewell_enabled", "=", True)])
    if len(sites) != 1:
        raise UserError(_("Activate Be Well on exactly one website before installing its demonstration catalogue."))
    site = sites
    env = env(context=dict(env.context, allowed_company_ids=[site.company_id.id]))
    site = site.with_env(env)

    def create_once(key, model, values):
        record = env.ref("bewell_demo_catalog." + key, raise_if_not_found=False)
        if record:
            return record
        record = env[model].create(values)
        env["ir.model.data"].create({"module": "bewell_demo_catalog", "name": key,
                                   "model": model, "res_id": record.id, "noupdate": True})
        return record

    with file_open("bewell_demo_catalog/data/products.json") as source:
        products = json.load(source)
    internal = create_once("internal_category", "product.category", {"name": "Be Well / Demonstration"})
    for index, item in enumerate(products):
        with file_open("bewell_website/static/src/img/" + item["key"] + ".webp", "rb") as image:
            image_data = base64.b64encode(image.read())
        category = create_once("category_" + item["category"].lower().replace(" ", "_"), "product.public.category", {
            "name": item["category"], "website_id": site.id, "sequence": (index + 1) * 10,
            "image_1920": image_data,
        })
        values = {
            "name": item["name"], "type": "consu", "sale_ok": True, "purchase_ok": False,
            "company_id": site.company_id.id, "website_id": site.id,
            "is_published": True, "website_sequence": (index + 1) * 10,
            "list_price": item["price"], "categ_id": internal.id,
            "taxes_id": [Command.clear()], "supplier_taxes_id": [Command.clear()],
            "public_categ_ids": [Command.set(category.ids)], "image_1920": image_data,
            "description_sale": item["description"],
            "website_description": "<p>" + item["description"] + "</p>",
            "description": "<p>DEMONSTRATION PRODUCT: fictional catalogue example. Images, descriptions and prices are illustrative; confirm all specifications before using for real sales.</p>",
        }
        # Standard product.template attribute lines create real Odoo product.product variants.
        if item.get("attribute"):
            attribute = create_once("attribute_" + item["key"], "product.attribute", {
                "name": item["attribute"], "create_variant": "always", "display_type": "radio",
            })
            options = [create_once("value_" + item["key"] + "_" + str(i), "product.attribute.value", {
                "name": name, "attribute_id": attribute.id,
            }) for i, name in enumerate(item["values"])]
            values["attribute_line_ids"] = [Command.create({"attribute_id": attribute.id,
                                                         "value_ids": [Command.set([v.id for v in options])]})]
        existed = bool(env.ref("bewell_demo_catalog.product_" + item["key"], raise_if_not_found=False))
        product = create_once("product_" + item["key"], "product.template", values)
        if not existed:
            for vindex, variant in enumerate(product.product_variant_ids.sorted("id")):
                variant.default_code = "BW-DEMO-%s-%02d" % (item["key"].upper(), vindex + 1)
            if item.get("extra"):
                product.attribute_line_ids.product_template_value_ids.filtered(
                    lambda v: v.name == item["values"][-1]
                ).write({"price_extra": item["extra"]})
