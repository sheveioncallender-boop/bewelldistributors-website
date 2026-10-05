from lxml import html
from odoo.tests import HttpCase, tagged


@tagged("post_install", "-at_install")
class TestBeWellWebsite(HttpCase):
    def test_pages_and_native_navigation(self):
        for path in ("/", "/be-well", "/be-well/about", "/be-well/collections",
                     "/be-well/distribution", "/be-well/contact", "/shop", "/shop/cart", "/contactus"):
            response = self.url_open(path)
            self.assertEqual(response.status_code, 200, path)
            tree = html.fromstring(response.content)
            self.assertTrue(tree.xpath("//header"), path)
            self.assertTrue(tree.xpath("//*[@id='wrapwrap'][contains(@class,'bw-site')]"), path)
        self.assertIn("Beautiful spaces.", self.url_open("/").text)

    def test_native_header_contact_and_cart_are_preserved(self):
        response = self.url_open("/shop")
        tree = html.fromstring(response.content)
        header = tree.xpath("//header")[0]
        self.assertNotIn("555-555", html.tostring(header, encoding="unicode"))
        self.assertTrue(header.xpath(".//a[@href='tel:+18682992160']"))
        desktop = tree.xpath("//*[@id='o_main_nav']")[0]
        self.assertTrue(desktop.xpath(".//a[contains(@href, '/shop/cart')]"))
        self.assertTrue(desktop.xpath(".//a[contains(@href, '/web/login')]"))
        self.assertTrue(desktop.xpath(".//a[@href='/contactus']"))
        self.assertTrue(tree.xpath("//*[@id='top_menu_collapse_mobile']//a[@href='tel:+18682992160']"))
        # The same native templates must still render on an unbranded website.
        site = self.env["website"].search([("bewell_enabled", "=", True)], limit=1)
        site.bewell_enabled = False
        other_response = self.url_open("/shop")
        self.assertEqual(other_response.status_code, 200)
        other = html.fromstring(other_response.content)
        self.assertFalse(other.xpath("//*[@id='wrapwrap'][contains(@class,'bw-site')]"))
        self.assertTrue(other.xpath("//header//a[starts-with(@href,'tel:')][contains(@href,'555')]"))

    def test_setup_preserves_editor_changes_and_other_websites(self):
        site = self.env["website"].search([("bewell_enabled", "=", True)], limit=1)
        site.write({"name": "Edited company website", "homepage_url": "/shop"})
        other = self.env["website"].create({"name": "Unrelated website", "homepage_url": "/contactus"})
        self.env["website"]._bewell_setup()
        self.assertEqual(site.name, "Edited company website")
        self.assertEqual(site.homepage_url, "/shop")
        self.assertFalse(other.bewell_enabled)
        self.assertEqual(other.homepage_url, "/contactus")
