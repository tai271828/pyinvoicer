import base64
import logging
from abc import ABC, abstractmethod

from jinja2 import Environment, PackageLoader

loader = PackageLoader("pyinvoicer", "templates")
# default true for security concern of XSS. See bandit B701.
env = Environment(loader=loader, autoescape=True)


class BaseRenderer(ABC):
    def __init__(self, content_model):
        self.content = content_model
        self.rendered_report = None

        self.rendered = None

        self._render()

    @abstractmethod
    def _render(self):
        pass

    @abstractmethod
    def dump(self, path="/tmp/output.invoice"):
        pass

    @staticmethod
    def get_currency_html_entity(currency_code):
        if currency_code == "EUR":
            return "&euro;"
        elif currency_code == "USD":
            return "&dollar;"
        else:
            return "&euro;"


class HTMLRenderer(BaseRenderer):
    def _render(self):
        html_template = env.get_template("invoice.html")

        content = self.content
        # hosting all tags that will be applied to the jinja2 target string
        tag_all = {
            "company_name": content.company_name,
            "company_detail": content.company_detail,
            "client_name": content.client_name,
            "client_detail": content.client_detail,
            "invoice_id": content.invoice_id,
            "invoice_date": content.invoice_date,
            "invoice_due_date": content.invoice_due_date,
            "footer_note": content.footer_note,
            "currency": self.get_currency_html_entity(content.currency),
        }

        tag_items = {"items": content.items}
        tag_all.update(tag_items)

        tag_total_amounts = {
            "total_excl_tax": content.total_excl_tax,
            "total_vat": content.vat_percentage,
            "total_incl_tax": content.total_incl_tax,
        }
        tag_all.update(tag_total_amounts)

        # embed logo image if available
        try:
            with open(content.company_logo, "rb") as img_file:
                img_data = img_file.read()
                img_data_decoded = (
                    base64.b64encode(img_data).decode("utf-8").replace("\n", "")
                )
                tag_all.update({"logo": img_data_decoded})
        except TypeError as e:
            logging.warning(
                f"Please check your logo_url: logo_url should be a str: {e}"
            )
        except FileNotFoundError as e:
            logging.info(
                f"Please check your logo_url: logo is not available from logo_url: {e}"
            )

        # reuse jinja2 env to get absolute file path of the css
        with open(env.get_template("styles.css").filename, "r") as fhandler:
            css = fhandler.read()
            tag_all.update({"css": css})

        self.rendered = html_template.render(**tag_all)

    def dump(self, path="./invoice.html"):
        with open(path, "w") as fhandler:
            fhandler.write(self.rendered)


class PDFRenderer(BaseRenderer):
    def _render(self):
        self.invoice_rendered_html = HTMLRenderer(self.content)

    def dump(self, path="./invoice.pdf"):
        import weasyprint

        htmldoc = weasyprint.HTML(
            string=self.invoice_rendered_html.rendered, base_url=""
        )
        htmldoc.write_pdf(path)
