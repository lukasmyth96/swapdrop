from django_enumfield import enum


class Slot(enum.Enum):
    
    SLOT_00_01 = 0
    SLOT_01_02 = 1
    SLOT_02_03 = 2
    SLOT_03_04 = 3
    SLOT_04_05 = 4
    SLOT_05_06 = 5
    SLOT_06_07 = 6
    SLOT_07_08 = 7
    SLOT_08_09 = 8
    SLOT_09_10 = 9
    SLOT_10_11 = 10
    SLOT_11_12 = 11
    SLOT_12_13 = 12
    SLOT_13_14 = 13
    SLOT_14_15 = 14
    SLOT_15_16 = 15
    SLOT_16_17 = 16
    SLOT_17_18 = 17
    SLOT_18_19 = 18
    SLOT_19_20 = 19
    SLOT_20_21 = 20
    SLOT_21_22 = 21
    SLOT_22_23 = 22
    SLOT_23_24 = 23

    __labels__ = {
        SLOT_00_01: '00:00-01:00',
        SLOT_01_02: '01:00-02:00',
        SLOT_02_03: '02:00-03:00',
        SLOT_03_04: '03:00-04:00',
        SLOT_04_05: '04:00-05:00',
        SLOT_05_06: '05:00-06:00',
        SLOT_06_07: '06:00-07:00',
        SLOT_07_08: '07:00-08:00',
        SLOT_08_09: '08:00-09:00',
        SLOT_09_10: '09:00-10:00',
        SLOT_10_11: '10:00-11:00',
        SLOT_11_12: '11:00-12:00',
        SLOT_12_13: '12:00-13:00',
        SLOT_13_14: '13:00-14:00',
        SLOT_14_15: '14:00-15:00',
        SLOT_15_16: '15:00-16:00',
        SLOT_16_17: '16:00-17:00',
        SLOT_17_18: '17:00-18:00',
        SLOT_18_19: '18:00-19:00',
        SLOT_19_20: '19:00-20:00',
        SLOT_20_21: '20:00-21:00',
        SLOT_21_22: '21:00-22:00',
        SLOT_22_23: '22:00-23:00',
        SLOT_23_24: '23:00-24:00',
    }


class BookingType(enum.Enum):

    COLLECTION = 0
    DELIVERY = 1
    RETURN = 2

    __labels__ = {
        COLLECTION: 'Collection',
        DELIVERY: 'Delivery',
        RETURN: 'Return'
    }


class BookingStatus(enum.Enum):
    PENDING = 0
    COMPLETE = 1
    CANCELLED = 2

