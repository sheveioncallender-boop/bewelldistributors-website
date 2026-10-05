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

    def test_setup_preserves_editor_changes_and_other_websites(self):
        site = self.env["website"].search([("bewell_enabled", "=", True)], limit=1)
        site.write({"name": "Edited company website", "homepage_url": "/shop"})
        other = self.env["website"].create({"name": "Unrelated website", "homepage_url": "/contactus"})
        self.env["website"]._bewell_setup()
        self.assertEqual(site.name, "Edited company website")
        self.assertEqual(site.homepage_url, "/shop")
        self.assertFalse(other.bewell_enabled)
        self.assertEqual(other.homepage_url, "/contactus")
