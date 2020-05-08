from django.core.exceptions import ValidationError


def is_square_image(image):
    """
    Check uploaded product image is square
    TODO temporary solution - in future we will ask users to simply crop non-square images
    Parameters
    ----------
    image: django.db.models.fields.files.ImageFieldFile

    Raises
    -------
    ValidationError
    """
    if image.width != image.height:
        raise ValidationError('you must upload a square image')
