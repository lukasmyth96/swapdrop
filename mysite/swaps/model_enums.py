from django_enumfield import enum


class SwapStatus(enum.Enum):
    PENDING_REVIEW = 0
    REJECTED = 1
    PENDING_CHECKOUT = 2
    TIMED_OUT = 3
    CANCELLED = 4
    CHECKOUT_COMPLETE = 5
    SWAP_COMPLETE = 6

    __default__ = PENDING_REVIEW


