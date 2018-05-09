from enum import Enum


class ConfidenceLevel(Enum):
    NONE = -1
    LOW = 0
    MEDIUM = 5
    HIGH = 10
    VERY_HIGH = 15


class Homeowner:
    def __init__(self, name=None, indirect_name=None, address=None, mortgage_amount=None, property_sale=None,
                 bookpage=None, date_time=None, confidence_level=ConfidenceLevel.NONE, deed_item=None,
                 mortgage_item=None, legal_description=None):
        if deed_item and mortgage_item:
            # [entry[0], item[5], entry[2], entry[8], item[8], "", entry[6], item[0]]
            # name from M, bookpage from D, date/time from M, mortgage amount from M, saleprice from D
            # placeholder for confidence level, legal descr, counterparty name
            self.name = mortgage_item[0]
            self.bookpage = deed_item[5]
            self.date_time = mortgage_item[2]
            self.mortgage_amount = mortgage_item[8]
            self.property_sale = deed_item[8]
            self.legal_description = mortgage_item[6]
            self.counterparty_name = deed_item[0]
            self.address = None
        else:
            self.name = name
            self.address = address
            self.bookpage = bookpage
            self.date_time = date_time
            self.mortgage_amount = mortgage_amount
            self.property_sale = property_sale
            self.indirect_name = indirect_name
            self.legal_description = legal_description

        self.confidence_level = confidence_level

    def to_dictionary(self):
        return {
                "name": self.name,
                "address": self.address,
                "confidence_level": self.confidence_level,
                "mortgage_amount": self.mortgage_amount,
                "property_sale": self.property_sale
        }

    def to_list(self):
        return [self.name, self.address, self.date_time, self.mortgage_amount, self.property_sale]
