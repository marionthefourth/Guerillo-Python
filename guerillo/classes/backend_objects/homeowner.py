from enum import Enum

from guerillo.classes.backend_objects.backend_object import BackendType, BackendObject
from guerillo.classes.backend_objects.result_item import ResultItem


class ConfidenceLevel(Enum):
    NONE = -1
    LOW = 0
    MEDIUM = 5
    HIGH = 10
    VERY_HIGH = 15


class Homeowner(ResultItem):

    b_type = BackendType.HOMEOWNER

    def __init__(self, name=None, counterparty_name=None, address=None, mortgage_amount=None, property_sale=None,
                 bookpage=None, date_time=None, confidence_level=ConfidenceLevel.NONE, deed_item=None,
                 mortgage_item=None, legal_description=None, uid=None, pyres=None, pyre=None, message_data=None):
        super().__init__(uid)
        if not pyres and not pyre and not message_data:
            if deed_item and mortgage_item:
                # [entry[0], item[5], entry[2], entry[8], item[8], "", entry[6], item[0]]
                # name from M, bookpage from D, date/time from M, mortgage amount from M, saleprice from D
                # placeholder for confidence level, legal descr, counterparty name
                self.address = None
                self.name = mortgage_item[0]
                self.bookpage = deed_item[5]
                self.date_time = mortgage_item[2]
                self.property_sale = deed_item[8]
                self.counterparty_name = deed_item[0]
                self.mortgage_amount = mortgage_item[8]
                self.legal_description = mortgage_item[6]
            else:
                self.name = name
                self.address = address
                self.bookpage = bookpage
                self.date_time = date_time
                self.property_sale = property_sale
                self.mortgage_amount = mortgage_amount
                self.legal_description = legal_description
                self.counterparty_name = counterparty_name

            self.confidence_level = confidence_level
        else:
            self.from_dictionary(pyres=pyres, pyre=pyre, message_data=message_data)

    def has_all_attributes(self):
        return self.name and self.address and self.date_time and self.address and self.bookpage \
                and self.mortgage_amount and self.property_sale and self.counterparty_name and self.legal_description

    def __eq__(self, other):
        if self.has_all_attributes() and other.has_all_attributes():
            name_match = self.name == other.name
            address_match = self.address == other.address
            bookpage_match = self.bookpage == other.bookpage
            date_time_match = self.date_time == other.date_time
            mortgage_match = self.mortgage_amount == other.mortgage_amount
            property_sale_match = self.property_sale == other.property_sale
            counterparty_match = self.counterparty_name == other.counterparty_name
            legal_description_match = self.legal_description == other.legal_description

            return name_match and address_match and date_time_match \
                and bookpage_match and mortgage_match and property_sale_match and counterparty_match \
                and legal_description_match
        return False

    def should_remove(self):
        if not self.address:
            return True
        try:
            float(self.mortgage_amount)
            float(self.property_sale)
        except ValueError:
            return True

        return False

    def from_dictionary(self, pyres=None, pyre=None, message_data=None):
        dictionary = super().from_dictionary(pyres=pyres, pyre=pyre, message_data=message_data)
        self.name = dictionary["name"]
        self.address = dictionary["address"]
        self.bookpage = dictionary["bookpage"]
        self.date_time = dictionary["date_time"]
        self.property_sale = dictionary["property_sale"]
        self.mortgage_amount = dictionary["mortgage_amount"]
        # self.confidence_level = dictionary["confidence_level"]
        self.legal_description = dictionary["legal_description"]
        self.counterparty_name = dictionary["counterparty_name"]

    def to_dictionary(self):
        return {
                ** super().to_dictionary(),
                "name": self.name,
                "address": self.address,
                "bookpage": self.bookpage,
                "date_time": self.date_time,
                "property_sale": self.property_sale,
                "mortgage_amount": self.mortgage_amount,
                # "confidence_level": self.confidence_level,
                "legal_description": self.legal_description,
                "counterparty_name": self.counterparty_name,
        }

    def to_list(self):
        return [self.name, self.address, self.date_time, self.mortgage_amount, self.property_sale]
