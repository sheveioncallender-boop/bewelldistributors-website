{
    "name": "Be Well Distributors Website",
    "version": "19.0.1.0.0",
    "summary": "Be Well's branded website with native Odoo eCommerce",
    "category": "Website",
    "author": "Spxcorp Limited",
    "license": "LGPL-3",
    "depends": ["website_sale"],
    "data": ["views/layout.xml", "views/pages.xml", "data/setup.xml"],
    "assets": {"web.assets_frontend": ["bewell_website/static/src/css/bewell.css"]},
    "application": True,
    "installable": True,
}
