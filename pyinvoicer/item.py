from abc import ABC, abstractmethod
from decimal import Decimal


class BaseItem(ABC):
    def __init__(self, content):
        self.name = ""
        self.units = Decimal(0)
        self.unit_price = Decimal(0)

        self._content = content

        self._content_sanity_check()
        self._parse_content()

    @property
    def amount(self):
        return self.units * self.unit_price

    @abstractmethod
    def _content_sanity_check(self):
        pass

    def _parse_content(self):
        content = self._content

        self.name = content["name"]
        # fool-proof. no matter what type of the number users input, for example, 12.34 or "12.34", convert them into
        # string for decimal later to keep the calculation precision.
        self.units = Decimal(str(content["units"]))
        self.unit_price = Decimal(str(content["unit_price"]))


class SimpleItem(BaseItem):
    def _content_sanity_check(self):
        pass
