from django.core.exceptions import ValidationError


def is_square_image(image):
    """
    Check uploaded product image isn't almost square
    TODO temporary solution - in future we will ask users to simply crop non-square images
    Parameters
    ----------
    image: django.db.models.fields.files.ImageFieldFile

    Raises
    -------
    ValidationError
    """
    ratio = image.height / image.width
    if (ratio < 0.95) or (ratio > 1.05):
        raise ValidationError('you must upload a square image')
