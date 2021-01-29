from abc import ABC, abstractmethod
from jinja2 import Environment, Markup, PackageLoader

loader = PackageLoader("pyinvoicer", "templates")
env = Environment(loader=loader)


class BaseRenderer(ABC):
    def __init__(self, content_model):
        self.content = content_model
        self.rendered_report = None

        self.rendered = None

        self._render()

    @abstractmethod
    def _render(self):
        self.rendered_report = "rendered_report"

    @abstractmethod
    def dump(self, path="/tmp/"):
        return self.rendered_report


class HTMLRenderer(BaseRenderer):
    def _render(self):
        def include_file(name):
            # This helper function insert static files literally into Jinja
            # templates without parsing them.
            return Markup(loader.get_source(env, name)[0])

        env.globals["include_file"] = include_file
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
            "footer_note": content.footer_note
        }

        tag_items = {
            "items": content.items
        }
        tag_all.update(tag_items)

        tag_total_amounts = {
            "total_excl_tax": content.total_excl_tax,
            "total_vat": content.vat_percentage,
            "total_incl_tax": content.total_incl_tax
        }
        tag_all.update(tag_total_amounts)

        self.rendered = html_template.render(**tag_all)

    def dump(self, path="/tmp/invoice.html"):
        with open(path, "w") as fhandler:
            fhandler.write(self.rendered)


class PDFRenderer(BaseRenderer):
    def __init__(self, content_model):
        self.invoice_rendered_html = HTMLRenderer(content_model)
