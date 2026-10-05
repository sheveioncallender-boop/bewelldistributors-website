import json

from odoo.tests import HttpCase, tagged
from odoo.addons.bewell_demo_catalog.hooks import post_init_hook


@tagged("post_install", "-at_install")
class TestBeWellCatalogue(HttpCase):
    def test_native_variants_cart_and_checkout(self):
        product = self.env.ref("bewell_demo_catalog.product_calacatta")
        self.assertEqual(len(product.product_variant_ids), 2)
        response = self.url_open(product.website_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("600 × 1200 mm", response.text)
        variant = product.product_variant_ids.filtered(
            lambda p: "600 × 1200 mm" in p.product_template_attribute_value_ids.mapped("name"))
        response = self.url_open("/shop/cart/add", data=json.dumps({
            "jsonrpc": "2.0", "method": "call", "id": 1,
            "params": {"product_template_id": product.id, "product_id": variant.id, "quantity": 2},
        }), headers={"Content-Type": "application/json"})
        result = response.json()
        self.assertNotIn("error", result, result)
        cart = self.url_open("/shop/cart")
        self.assertEqual(cart.status_code, 200)
        self.assertIn("600 × 1200 mm", cart.text)
        self.assertIn("Calacatta", cart.text)
        self.assertEqual(self.url_open("/shop/checkout").status_code, 200)

    def test_unpublished_products_and_other_site_products_stay_private(self):
        product = self.env.ref("bewell_demo_catalog.product_galaxy")
        product.is_published = False
        home = self.url_open("/be-well").text
        self.assertNotIn(product.name, home)
        other = self.env["website"].create({"name": "Other storefront"})
        product.write({"website_id": other.id, "is_published": True})
        self.assertNotIn(product.name, self.url_open("/be-well").text)

    def test_repeat_loader_preserves_prices_and_does_not_duplicate(self):
        product = self.env.ref("bewell_demo_catalog.product_calacatta")
        product.list_price = 77
        count = self.env["product.template"].search_count([("categ_id", "=", product.categ_id.id)])
        post_init_hook(self.env)
        self.assertEqual(product.list_price, 77)
        self.assertEqual(count, self.env["product.template"].search_count([("categ_id", "=", product.categ_id.id)]))
