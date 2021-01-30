import logging
from abc import ABC, abstractmethod
from decimal import Decimal

import yaml

from pyinvoicer.item import SimpleItem


class BaseInvoice(ABC):
    def __init__(self, content_file):
        self.company_name = ""
        self.company_detail = ""
        self.company_logo = ""
        self.invoice_id = ""
        self.invoice_date = ""
        self.invoice_due_date = ""
        self.client_name = ""
        self.client_detail = ""
        self.items = []
        self.footer_note = ""
        self.vat_percentage = Decimal(0)
        self.currency = ""

        self._content = None
        self.read_content_yaml(content_file)

        self._content_sanity_check()
        self._parse_content()

    @property
    def total_excl_tax(self):
        total = 0
        for item in self.items:
            total += item.amount

        return total

    @property
    def total_incl_tax(self):
        total = 0
        for item in self.items:
            total += item.amount + item.amount * self.vat_percentage

        return total

    @abstractmethod
    def _content_sanity_check(self):
        pass

    @abstractmethod
    def _parse_content(self):
        pass

    @abstractmethod
    def _parse_items(self):
        pass

    def read_content_yaml(self, content_file):
        with open(content_file, "r") as stream:
            try:
                self._content = yaml.safe_load(stream)

            except yaml.YAMLError as e:
                logging.critical(e)


class SimpleInvoice(BaseInvoice):
    def _content_sanity_check(self):
        pass

    def _parse_content(self):
        self._parse_items()

        content = self._content
        self.company_name = content["company"]["name"]
        self.company_detail = content["company"]["detail"]
        self.company_logo = content["company"]["logo_url"]
        self.invoice_id = content["invoice"]["id"]
        self.invoice_date = content["invoice"]["date"]
        self.invoice_due_date = content["invoice"]["due_date"]
        self.client_name = content["client"]["name"]
        self.client_detail = content["client"]["detail"]
        self.footer_note = content["footer_note"]
        self.currency = content["currency"]

    def _parse_items(self):
        for item in self._content["items"]:
            simple_item = SimpleItem(item)
            self.items.append(simple_item)

    @property
    def vat(self):
        total = Decimal(0)
        for item in self.items:
            total += item.amount * self.vat_percentage

        return total
