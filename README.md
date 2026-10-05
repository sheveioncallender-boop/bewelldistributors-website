# Be Well Distributors — Odoo 19 Enterprise

Branded tile, granite and stone website for Be Well Distributors Limited, prepared for Git-based deployment on Cloudpepper.

## Modules

| Module | Purpose |
| --- | --- |
| `bewell_website` | Five designed pages, original logo and teal branding, responsive layouts, native Odoo navigation and eCommerce. |
| `bewell_demo_catalog` | Optional six-product showcase with four public categories and real size, finish and thickness variants. |

Install the website module first, then the demonstration catalogue if wanted. Both appear in Apps. This is a standard addons repository, not an Odoo.sh project or a static website deployment.

## Cloudpepper installation

1. Add `https://github.com/sheveioncallender-boop/bewelldistributors-website.git` to the Odoo 19 Enterprise instance's custom Git addons, branch `main`.
2. Use Cloudpepper's rebuild/deploy action. Its Odoo addons path must include the repository root containing the two module folders.
3. Activate developer mode in Odoo, open Apps and select Update Apps List.
4. Install **Be Well Distributors Website**.
5. Install **Be Well Demonstration Catalogue** to load the examples.
6. Open the website at `/`. The homepage is configured as `/be-well` automatically on the unambiguous target website.

### Multiple websites

The installer selects exactly one website already marked for Be Well, named Be Well, or using `/be-well` as its homepage. If no website matches and only one exists, that website is used. If the selection is ambiguous, it changes no websites. Set the intended site's homepage URL to `/be-well`, then upgrade `bewell_website`. Demo installation refuses an ambiguous target.

Initial setup sets only the chosen website's name, logo, homepage and navigation. It does not change company/accounting details, stock, taxes, payment providers, SMTP or existing products. Existing unrelated menu entries are retained. Once configured, future module updates preserve site and navigation edits. Editable page templates are `noupdate` so content edited with Website's editor is preserved.

## Native Odoo behaviour

- Odoo owns the desktop header, mobile menu, search, account menu and cart badge. The default desktop header groups search, account and cart before Contact Us, with the phone in the announcement strip. Mobile and alternative headers use the real Be Well phone/email. Native buttons and variant selections use the teal palette.
- `/shop`, product pages, category filters, variants, cart, checkout and `/my` are standard Odoo.
- Homepage product cards read published, saleable products for the current website and company. They use Odoo's current pricelist, tax and fiscal-position calculation.
- Cards link to the native product page for size/finish/thickness selection and Add to Cart.
- Restricted-shop access and zero-price contact rules are respected.
- Prices, descriptions, photos, categories and variants are editable through normal Odoo product records.
- The contact page links to Odoo's native `/contactus` enquiry form. Configure the website company's contact recipient and outgoing mail in Odoo and test delivery before launch.
- No custom payment processing, cart state or checkout JavaScript is installed.

## Demonstration catalogue

The product range was confirmed by the user as **tiles, granite and stone**. The old live site's About page and product page conflicted, so the food/wellness content was not carried into this build.

All six products, dimensions, descriptions, imagery and prices are illustrative. They are not an import of a verified Be Well price list or stock file. No actual brand representation, origin, certification, slip rating, durability specification or inventory quantity is asserted.

| Product | Starting example price | Native variants |
| --- | ---: | --- |
| Calacatta Ivory Porcelain Tile | 95 per tile | 600 × 600 mm / 600 × 1200 mm (+85) |
| Sand Beige Porcelain Tile | 88 per tile | Single selection |
| Ivory Ceramic Wall Tile | 35 per tile | Gloss / Matt |
| Black Galaxy Granite Slab | 3,200 per slab | 20 mm / 30 mm (+800) |
| Ivory Grey Granite Slab | 3,600 per slab | Single selection |
| Silver Travertine Tile | 145 per tile | Single selection |

Amounts use the website company's existing currency. Set up the intended Trinidad company and TTD currency through Odoo before the showcase; this module never changes accounting currency. Product quantities use native units, with the per-tile or per-slab basis explained in descriptions. Area/box conversions are not implemented. Configure those against real pack coverage and sales units if needed.

Demo products are goods without stock tracking quantities. They use no customer or supplier taxes, are assigned to the Be Well website/company, and use internal references beginning `BW-DEMO-`. They are published by installing the optional app. No payment provider is enabled and no real stock or accounting balances are created. Existing payment providers remain unchanged; use a staging/demo website for demonstrations.

For launch, archive the demo products and replace them with verified products, prices, technical specifications, units, stock, tax rules and genuine photographs. Archive rather than uninstall if demonstration orders already refer to them. Confirm delivery charges, returns terms, payment settings and enquiry email delivery before enabling real sales.

## Validation

The GitHub workflow installs the modules on the official Odoo 19 image, checks page rendering, native cart and checkout, variant creation, website/publication filtering, setup idempotence and module upgrades. This verifies the shared Odoo 19 website/eCommerce engine. The Enterprise instance's own theme, optional apps, checkout configuration and Cloudpepper deployment still require a staging check.

Local validation covers Python syntax, XML structure, assets, manifest references and route consistency. See GitHub Actions for the actual runtime test result; a source check is not an installation test.

## Website pages

- `/be-well` — homepage (also reached from `/`)
- `/be-well/collections` — material collections
- `/be-well/about` — company and founder
- `/be-well/distribution` — project, retailer and supplier enquiries
- `/be-well/contact` — contact and practical FAQs

## Design preview

`docs/preview.html` is an offline design review with simulated products and basket interactions. It is not an Odoo server and cannot validate native checkout or send enquiries. Real deployment uses only the two addons folders. The preview uses the same page markup, CSS and image assets as the module; its navigation is a visual stand-in for Odoo's native header.

## Credits

Original leaf logo and Sharleen Pariag's portrait were retrieved from the live Be Well website on 5 October 2026 for this authorised rebuild. Original teal: `#069083`. Architectural and material imagery is AI-generated for this showcase. See `docs/ASSETS.md` for sources and prompts.

## Update 19.0.1.0.1

Corrected the native placeholder phone/email, arranged the default header controls and applied the teal palette to native buttons, selected variants and badges. Rebuild from main in Cloudpepper, then upgrade **Be Well Distributors Website** in Odoo Apps. This update does not reinstall or reload demo products.
