from django_enumfield import enum
from django.utils.translation import ugettext_lazy


class ProductStatus(enum.Enum):
    LIVE = 0  # live on site
    MATCHED = 1  # successfully matched
    COLLECTED = 2  # successfully picked up by owner
    DELIVERED = 3  # delivered

    __default__ = LIVE

    # InvalidStatusOperationError exception will be raised if we attempt an invalid transition
    __transitions__ = {
        MATCHED: (LIVE,),  # Can go from LIVE to MATCHED
        COLLECTED: (MATCHED,),  # Can go from MATCHED to COLLECTED
        DELIVERED: (COLLECTED,)  # Can go from collected to delivered
    }

    __labels__ = {
        LIVE: ugettext_lazy("Live"),
        MATCHED: ugettext_lazy("Matched"),
        COLLECTED: ugettext_lazy("Collected"),
        DELIVERED: ugettext_lazy("Delivered"),
    }
