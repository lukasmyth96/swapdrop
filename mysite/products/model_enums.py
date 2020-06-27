from django_enumfield import enum
from django.utils.translation import ugettext_lazy


class ProductStatus(enum.Enum):
    LIVE = 0  # live on site - visible for new offers
    PENDING_CHECKOUT = 1  # successfully matched - pending product owners checkout checkout
    CHECKOUT_COMPLETE = 2  # product owner has checkout out
    COLLECTED = 3  # successfully picked up from owner
    DELIVERED = 4  # delivered to new owner

    __default__ = LIVE

    # InvalidStatusOperationError exception will be raised if we attempt an invalid transition
    __transitions__ = {
        LIVE: (PENDING_CHECKOUT, CHECKOUT_COMPLETE),  # Can only transition to live from PENDING_CHECKOUT and CHECKOUT_COMPLETE
        PENDING_CHECKOUT: (LIVE,),  # Can only transition to PENDING_CHECKOUT from LIVE
        CHECKOUT_COMPLETE: (PENDING_CHECKOUT,),  # Can only transition to CHECKOUT_COMPLETE from PENDING_CHECKOUT
        COLLECTED: (CHECKOUT_COMPLETE,),  # Can only transition to COLLECTED from CHECKOUT_COMPLETE
        DELIVERED: (COLLECTED,)  # Can only transition to DELIVERED from COLLECTED
    }

    __labels__ = {
        LIVE: ugettext_lazy("Live"),
        PENDING_CHECKOUT: ugettext_lazy("Pending Checkout"),
        CHECKOUT_COMPLETE: ugettext_lazy("Checkout Complete"),
        COLLECTED: ugettext_lazy("Collected"),
        DELIVERED: ugettext_lazy("Delivered"),
    }


class ClothingType(enum.Enum):

    T_SHIRT = 0
    TOP = 1
    SHIRT = 2
    BLOUSE = 3
    JUMPER = 4
    JACKET = 5
    COAT = 6
    TROUSERS = 7
    JEANS = 8
    SHORTS = 9
    SKIRT = 10
    DRESS = 12
    SHOES = 13
    ACCESSORIES = 14
    OTHER = 15

    @property
    def label(self):
        """ Override default label property - saves writing them all out"""
        return '-'.join([text.capitalize() for text in self.name.split('_')])


