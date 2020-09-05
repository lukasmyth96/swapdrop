from django.core.exceptions import ValidationError


def is_in_chichester(postcode):
    """
    Check that given postcode is in Chichester area

    Parameters
    ----------
    postcode: str

    Raises
    -------
    ValidationError
    """
    if not postcode.startswith('PO19'):
        raise ValidationError('Sorry - we are currently only open in Chichester')
