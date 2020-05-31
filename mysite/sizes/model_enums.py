from django_enumfield import enum


class GenderOptions(enum.Enum):
    MENSWEAR = 0
    WOMENSWEAR = 1
    UNISEX = 2

    __labels__ = {
        MENSWEAR: 'Menswear',
        WOMENSWEAR: 'Womenswear',
        UNISEX: 'Unisex'
    }


class PrimarySizeOptions(enum.Enum):
    MENS_XXS = 0
    MENS_XS = 1
    MENS_S = 2
    MENS_M = 3
    MENS_L = 4
    MENS_XL = 5
    MENS_XXL = 6
    WOMENS_XXS = 7
    WOMENS_XS = 8
    WOMENS_M = 9
    WOMENS_L = 10
    WOMENS_XL = 11
    WOMENS_XXL = 12
    WOMENS_4 = 13
    WOMENS_6 = 14
    WOMENS_8 = 16
    WOMENS_10 = 17
    WOMENS_12 = 18
    WOMENS_14 = 20
    WOMENS_16 = 21
    WOMENS_18 = 22


class WaistSizeOptions(enum.Enum):
    """ Inches """
    INCH_20 = 0
    INCH_21 = 1
    INCH_22 = 2
    INCH_23 = 3
    INCH_24 = 4
    INCH_25 = 5
    INCH_26 = 6
    INCH_27 = 7
    INCH_28 = 8
    INCH_29 = 9
    INCH_30 = 10
    INCH_31 = 11
    INCH_32 = 12
    INCH_33 = 13
    INCH_34 = 14
    INCH_35 = 15
    INCH_36 = 16
    INCH_37 = 17
    INCH_38 = 19
    INCH_39 = 20
    INCH_40 = 20



class ShoeSizeOptions(enum.Enum):
    UK_2 = 0
    UK_3 = 1
    UK_4 = 2
    UK_5 = 3
    UK_6 = 4
    UK_7 = 5
    UK_8 = 6
    UK_9 = 7
    UK_10 = 8
    UK_11 = 9
    UK_12 = 10
