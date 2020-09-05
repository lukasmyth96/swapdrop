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
    PRIMARY_WOMENS_S = 9
    PRIMARY_WOMENS_M = 10
    PRIMARY_WOMENS_L = 11
    PRIMARY_WOMENS_XL = 12
    PRIMARY_WOMENS_XXL = 13
    PRIMARY_WOMENS_4 = 14
    PRIMARY_WOMENS_6 = 15
    PRIMARY_WOMENS_8 = 16
    PRIMARY_WOMENS_10 = 17
    PRIMARY_WOMENS_12 = 18
    PRIMARY_WOMENS_14 = 19
    PRIMARY_WOMENS_16 = 20
    PRIMARY_WOMENS_18 = 21
    WAIST_20 = 22
    WAIST_21 = 23
    WAIST_22 = 24
    WAIST_23 = 25
    WAIST_24 = 26
    WAIST_25 = 27
    WAIST_26 = 28
    WAIST_27 = 29
    WAIST_28 = 30
    WAIST_29 = 31
    WAIST_30 = 32
    WAIST_31 = 33
    WAIST_32 = 34
    WAIST_33 = 35
    WAIST_34 = 36
    WAIST_35 = 37
    WAIST_36 = 38
    WAIST_37 = 39
    WAIST_38 = 40
    WAIST_39 = 41
    WAIST_40 = 42
    SHOE_2 = 43
    SHOE_2_5 = 44
    SHOE_3 = 45
    SHOE_3_5 = 46
    SHOE_4 = 47
    SHOE_4_5 = 48
    SHOE_5 = 49
    SHOE_5_5 = 50
    SHOE_6 = 51
    SHOE_6_5 = 52
    SHOE_7 = 53
    SHOE_7_5 = 54
    SHOE_8 = 55
    SHOE_8_5 = 56
    SHOE_9 = 57
    SHOE_9_5 = 58
    SHOE_10 = 59
    SHOE_10_5 = 60
    SHOE_11 = 61
    SHOE_11_5 = 62
    SHOE_12 = 63
    SHOE_12_5 = 64
    SHOE_13 = 65
