from django_enumfield import enum


class OfferStatus(enum.Enum):
    PENDING = 0  # pending review
    REJECTED = 1
    ACCEPTED = 2

    __default__ = PENDING

    # InvalidStatusOperationError exception will be raised if we attempt an invalid transition
    __transitions__ = {
        REJECTED: (PENDING,),  # Can go from PENDING to REJECTED
        ACCEPTED: (PENDING,)  # Can go from PENDING to ACCEPTED
    }
