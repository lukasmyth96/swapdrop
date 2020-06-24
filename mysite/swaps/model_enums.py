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

    __transitions__ = {
        REJECTED: (PENDING_REVIEW,),  # Can only transition to REJECTED from PENDING_REVIEW
        PENDING_CHECKOUT: (PENDING_REVIEW,),  # Can only transition to PENDING_CHECKOUT from PENDING_REVIEW
        CHECKOUT_COMPLETE: (PENDING_CHECKOUT,),  # Can only transition to CHECKOUT_COMPLETE from PENDING_CHECKOUT
        TIMED_OUT: (PENDING_CHECKOUT),  # Can only transition to TIMED_OUT from PENDING_CHECKOUT
        CANCELLED: (PENDING_REVIEW, PENDING_CHECKOUT, TIMED_OUT)  # Can only transition to CANCELLED from PENDING_REVIEW or PENDING_CHECKOUT
    }


