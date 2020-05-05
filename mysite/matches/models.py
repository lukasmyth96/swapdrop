from django.db import models
from django_enumfield import enum
from django.contrib.auth.models import User
from products.models import Product


class Like(models.Model):

    liked_by = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        abbreviated_product_name = self.product.__str__()[:20]
        return f'{self.liked_by}  *LIKED*  {abbreviated_product_name}  *OWNED BY*  {self.product.owner}'


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


class Offer(models.Model):

    desired_product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='offers_desired')
    offered_product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='offers_offered')
    status = enum.EnumField(OfferStatus, default=OfferStatus.PENDING)

    def __str__(self):
        abbreviated_desired_product_name = self.desired_product.__str__()[:20]  # just truncating.
        abbreviated_offered_product_name = self.offered_product.__str__()[:20]
        return f'{self.offered_product.owner.username} *OFFERED* {abbreviated_offered_product_name} ' \
               f' *FOR* {abbreviated_desired_product_name}  *OWNED BY* {self.desired_product.owner.username}  *STATUS: {self.status.name}*'
