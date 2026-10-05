import base64
import logging

from odoo import api, fields, models
from odoo.tools import file_open

_logger = logging.getLogger(__name__)


class Website(models.Model):
    _inherit = "website"

    bewell_enabled = fields.Boolean("Be Well branding", copy=False)
    bewell_setup_done = fields.Boolean(copy=False)

    @api.model
    def _bewell_setup(self):
        """Set up a clearly identified site once, preserving subsequent editor changes."""
        sites = self.search([])
        targets = sites.filtered(lambda s: s.bewell_enabled or s.homepage_url == "/be-well"
                                 or "bewell" in s.name.lower().replace(" ", "").replace("-", ""))
        if not targets and len(sites) == 1:
            targets = sites
        if len(targets) != 1:
            _logger.warning("Be Well: set the target website homepage to /be-well and upgrade the module; no unique target found.")
            return
        site = targets
        if site.bewell_setup_done:
            return
        with file_open("bewell_website/static/src/img/logo.png", "rb") as image:
            site.write({"bewell_enabled": True, "name": "Be Well Distributors",
                        "homepage_url": "/be-well", "logo": base64.b64encode(image.read())})
        Menu = self.env["website.menu"]
        if not site.menu_id:
            Menu.create({"name": "Main Menu", "website_id": site.id})
            site.invalidate_recordset(["menu_id"])
        links = [("Home", "/", 10), ("Shop", "/shop", 20),
                 ("Collections", "/be-well/collections", 30),
                 ("Our Story", "/be-well/about", 40),
                 ("For Business", "/be-well/distribution", 50),
                 ("Contact", "/be-well/contact", 60)]
        existing = Menu.search([("website_id", "=", site.id), ("parent_id", "=", site.menu_id.id)])
        for name, url, sequence in links:
            match = existing.filtered(lambda m: m.url == url or (name == "Contact" and m.url == "/contactus"))[:1]
            if match:
                match.write({"name": name, "url": url, "sequence": sequence})
            else:
                Menu.create({"name": name, "url": url, "sequence": sequence,
                             "website_id": site.id, "parent_id": site.menu_id.id})
        site.bewell_setup_done = True
