from odoo import http
from odoo.fields import Domain
from odoo.http import request


class BeWellWebsite(http.Controller):
    def _render(self, page, title, description, catalogue=False):
        website = request.website
        if not website.bewell_enabled:
            return request.not_found()
        Product = request.env["product.template"]
        Category = request.env["product.public.category"]
        can_shop = website.has_ecommerce_access()
        products = Product.search(
            Domain(website.sale_product_domain()) & Domain("is_published", "=", True),
            order="website_sequence, name, id", limit=6,
        ) if can_shop and catalogue else Product
        # Do not sudo: respect native public catalogue visibility and website scope.
        categories = Category.search(
            Domain(website.website_domain()) & Domain("parent_id", "=", False),
            order="sequence, name, id", limit=8,
        ) if can_shop and catalogue else Category
        return request.render("bewell_website." + page, {
            "website": website, "products": products, "categories": categories,
            "can_shop": can_shop,
            "product_prices": products._get_sales_prices(website) if products else {},
            "title": title + " | Be Well Distributors",
            "website_meta_description": description,
        })

    @http.route("/be-well", type="http", auth="public", website=True, sitemap=True)
    def home(self, **kw):
        return self._render("home", "Tiles, Granite & Stone",
                            "Explore tiles, granite and natural stone from Be Well Distributors in Trinidad and Tobago.", True)

    @http.route("/be-well/collections", type="http", auth="public", website=True, sitemap=True)
    def collections(self, **kw):
        return self._render("collections", "Our Collections", "Explore Be Well’s tile, granite and natural stone collections.", True)

    @http.route("/be-well/about", type="http", auth="public", website=True, sitemap=True)
    def about(self, **kw):
        return self._render("about", "Our Story", "Meet Be Well Distributors and founder Sharleen Pariag. Local understanding, global connections.")

    @http.route("/be-well/distribution", type="http", auth="public", website=True, sitemap=True)
    def distribution(self, **kw):
        return self._render("distribution", "Retailer & Supplier Partnerships", "Connect with Be Well for wholesale enquiries, product sourcing and Caribbean distribution partnerships.")

    @http.route("/be-well/contact", type="http", auth="public", website=True, sitemap=True)
    def contact(self, **kw):
        return self._render("contact", "Let's Connect", "Contact Be Well Distributors in Chaguanas, Trinidad. Call (868) 299-2160 or email info@bewelldistributorsltd.com.")
