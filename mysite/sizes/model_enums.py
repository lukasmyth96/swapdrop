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


class SizeTypes(enum.Enum):
    PRIMARY = 0
    WAIST = 1
    SHOE = 2


class SizeOptions(enum.Enum):
    PRIMARY_MENS_XXS = 0
    PRIMARY_MENS_XS = 1
    PRIMARY_MENS_S = 2
    PRIMARY_MENS_M = 3
    PRIMARY_MENS_L = 4
    PRIMARY_MENS_XL = 5
    PRIMARY_MENS_XXL = 6
    PRIMARY_WOMENS_XXS = 7
    PRIMARY_WOMENS_XS = 8
    PRIMARY_WOMENS_M = 9
    PRIMARY_WOMENS_L = 10
    PRIMARY_WOMENS_XL = 11
    PRIMARY_WOMENS_XXL = 12
    PRIMARY_WOMENS_4 = 13
    PRIMARY_WOMENS_6 = 14
    PRIMARY_WOMENS_8 = 15
    PRIMARY_WOMENS_10 = 16
    PRIMARY_WOMENS_12 = 17
    PRIMARY_WOMENS_14 = 18
    PRIMARY_WOMENS_16 = 19
    PRIMARY_WOMENS_18 = 20
    WAIST_20 = 21
    WAIST_21 = 22
    WAIST_22 = 23
    WAIST_23 = 24
    WAIST_24 = 25
    WAIST_25 = 26
    WAIST_26 = 27
    WAIST_27 = 28
    WAIST_28 = 29
    WAIST_29 = 30
    WAIST_30 = 31
    WAIST_31 = 32
    WAIST_32 = 33
    WAIST_33 = 34
    WAIST_34 = 35
    WAIST_35 = 36
    WAIST_36 = 37
    WAIST_37 = 38
    WAIST_38 = 39
    WAIST_39 = 40
    WAIST_40 = 41
    SHOE_2 = 42
    SHOE_2_5 = 43
    SHOE_3 = 44
    SHOE_3_5 = 45
    SHOE_4 = 46
    SHOE_4_5 = 47
    SHOE_5 = 48
    SHOE_5_5 = 49
    SHOE_6 = 50
    SHOE_6_5 = 51
    SHOE_7 = 52
    SHOE_7_5 = 53
    SHOE_8 = 54
    SHOE_8_5 = 55
    SHOE_9 = 56
    SHOE_9_5 = 57
    SHOE_10 = 58
    SHOE_10_5 = 59
    SHOE_11 = 60
    SHOE_11_5 = 61
    SHOE_12 = 62
    SHOE_12_5 = 63
    SHOE_13 = 64
