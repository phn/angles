from angles import (
    normalize, deci2sexa, sexa2deci, fmt_angle, phmsdms, pposition
)
import pytest


def test_normalize_proper_input_range():
    """Normalize must be called with proper range limits must be"""
    with pytest.raises(ValueError):
        normalize(10, 0, 360, b=True)

    with pytest.raises(ValueError):
        normalize(10, -89, 90, b=True)

    with pytest.raises(ValueError):
        normalize(10, 1, 90)

    # both shouldn't raise any exception
    assert normalize(10, 0, 360) == 10
    assert normalize(10, -90, 90) == 10


def test_normalize_b_false_sanity_check():
    """Values at extremes and in the middle must be handled."""
    L, U = 0, 360
    assert normalize(10, L, U) == 10
    assert normalize(L, L, U) == L
    assert normalize(U, L, U) == L

    L, U = -90, 90
    assert normalize(10, L, U) == 10
    assert normalize(L, L, U) == L
    assert normalize(U, L, U) == L


def test_normalize_b_true_sanity_check():
    """Values at extremes and in the middle must be handled."""
    L, U = -180, 180
    assert normalize(10, L, U, b=True) == 10
    assert normalize(L, L, U, b=True) == L
    assert normalize(U, L, U, b=True) == U

    L, U = -90, 90
    assert normalize(10, L, U, b=True) == 10
    assert normalize(L, L, U, b=True) == L
    assert normalize(U, L, U, b=True) == U


def test_normalize_b_false_outside_right_limit():
    """Values to the right of the right limit must be handled properly."""
    L, U = 0, 360
    assert normalize(U+1, L, U) == L + 1
    assert normalize(U*2+1, L, U) == L + 1
    assert normalize(U*100+(U-L)/2.0, L, U) == L + (U-L)/2.0

    L, U = -90, 90
    assert normalize(U+1, L, U) == L + 1
    assert normalize(181, L, U) == 1
    assert normalize(361, L, U) == 1


def test_normalize_b_true_outside_right_limit():
    """Values to the right of the right limit must be handled properly."""
    L, U = -180, 180
    assert normalize(U+1, L, U, b=True) == U - 1
    assert normalize(181, L, U, b=True) == U - 1
    assert normalize(361, L, U, b=True) == -1

    L, U = -90, 90
    assert normalize(U+1, L, U, b=True) == U - 1
    assert normalize(181, L, U, b=True) == -1
    assert normalize(361, L, U, b=True) == 1


def test_normalize_b_false_outside_left_limit():
    """Values to the left of the left limit must be handled properly."""
    L, U = 0, 360
    assert normalize(L-1, L, U) == U - 1
    assert normalize(-360, L, U) == 0
    assert normalize(-361, L, U) == 359
    assert normalize(-721, L, U) == 359

    L, U = -90, 90
    assert normalize(L-1, L, U) == U - 1
    assert normalize(-180, L, U) == 0
    assert normalize(-181, L, U) == -1
    assert normalize(-361, L, U) == -1


def test_normalize_b_true_outside_left_limit():
    """Values to the left of the left limit must be handled properly."""
    L, U = -180, 180
    assert normalize(-181, L, U, b=True) == -179
    assert normalize(-361, L, U, b=True) == 1
    assert normalize(-721, L, U, b=True) == -1

    L, U = -90, 90
    assert normalize(-91, L, U, b=True) == -89
    assert normalize(-181, L, U, b=True) == 1
    assert normalize(-361, L, U, b=True) == -1


def test_deci2sexa_pre_should_work_as_expected():
    """The pre keyword should round decimal places to required values."""
    assert deci2sexa(-11.2345678) == (-1, 11, 14, 4.444)
    assert deci2sexa(-11.2345678, pre=5) == (-1, 11, 14, 4.44408)
    assert deci2sexa(-11.2345678, pre=2) == (-1, 11, 14, 4.44)
    assert deci2sexa(-11.2345678, pre=0) == (-1, 11, 14, 4.0)
    assert deci2sexa(-11.2345678, pre=-1) == (-1, 11, 14, 0.0)


def test_deci2sexa_pre_should_handle_nines():
    """deci2sexa pre should recover nines."""
    x = 23+59/60.0+59.99999/3600.0
    assert deci2sexa(x, pre=3) == (1, 24, 0.0, 0.0)
    assert deci2sexa(x, pre=4) == (1, 24, 0.0, 0.0)
    assert deci2sexa(x, pre=5) == (1, 23, 59, 59.99999)


def test_deci2sexa_normalize_should_work_as_expected():
    """deci should get properly normlized when lower and upper bounds are given."""
    assert deci2sexa(10, lower=0, upper=360) == (1, 10, 0.0, 0.0)
    assert deci2sexa(361, lower=0, upper=360) == (1, 1, 0.0, 0.0)
    assert deci2sexa(-2, lower=0, upper=360) == (1, 358, 0.0, 0.0)

    assert deci2sexa(10, lower=-90, upper=90) == (1, 10, 0.0, 0.0)
    assert deci2sexa(-91, lower=-90, upper=90) == (1, 89, 0.0, 0.0)
    assert deci2sexa(-91, lower=-90, upper=90, b=True) == (-1, 89, 0.0, 0.0)


def test_deci2sexa_trunc_should_truncate_values():
    """trunc should truncate values."""
    x = 23+59/60.0+59.99999/3600.0
    assert deci2sexa(x, pre=3, trunc=True) == (1, 23, 59, 59.999)
    assert deci2sexa(x, pre=4, trunc=True) == (1, 23, 59, 59.9999)


def test_deci2sexa_upper_trim_should_trim_upper_limit():
    assert deci2sexa(24, upper_trim=True) == (1, 24, 0.0, 0.0)
    assert deci2sexa(24, lower=0, upper=24, upper_trim=True) == (1, 0.0, 0.0, 0.0)

    x = 23+59/60.0+59.99999/3600.0
    assert deci2sexa(x, lower=0, upper=24, pre=3, upper_trim=True) == (1, 0, 0, 0)
    assert deci2sexa(x, lower=0, upper=24, pre=5, upper_trim=True) == (1, 23, 59, 59.99999)


def test_sexa2deci():
    assert sexa2deci(1, 1, 0, 0) == 1
    assert sexa2deci(-1, 1, 0, 0) == -1

    assert sexa2deci(1, 23, 59, 59.99999) == 23+59/60.0+59.99999/3600.0
    assert sexa2deci(-1, 23, 59, 59.99999) == -1 * (23+59/60.0+59.99999/3600.0)


def test_fmt_angle():
    assert fmt_angle(1.9999, pre=3, trunc=True) == '+01 59 59.639'
    assert fmt_angle(1.9999, pre=0, trunc=True) == '+01 59 59'

    assert fmt_angle(12.348978659, pre=4, trunc=True) == '+12 20 56.3231'
    assert fmt_angle(12.348978659, pre=5) == '+12 20 56.32317'
    assert fmt_angle(12.348978659, s1='HH ', s2='MM ', s3='SS', pre=5) == '+12HH 20MM 56.32317SS'

    x = 23+59/60.0+59.99999/3600.0
    assert fmt_angle(x) == '+24 00 00.000'
    assert fmt_angle(x, lower=0, upper=24, upper_trim=True) == '+00 00 00.000'
    assert fmt_angle(x, pre=5) == '+23 59 59.99999'
    assert fmt_angle(-x, lower=0, upper=24, upper_trim=True) == '+00 00 00.000'
    assert fmt_angle(-x) == '-24 00 00.000'


def test_phmsdms():
    """Parse reasonably formatted hms dms strings."""
    assert phmsdms("12") == {'parts': [12.0, None, None],
                             'sign': 1,
                             'units': 'degrees',
                             'vals': [12.0, 0.0, 0.0]}

    assert phmsdms("12h") == {'parts': [12.0, None, None],
                              'sign': 1,
                              'units': 'hours',
                              'vals': [12.0, 0.0, 0.0]}

    assert phmsdms("12d13m14.56") == {'parts': [12.0, 13.0, 14.56],
                                      'sign': 1,
                                      'units': 'degrees',
                                      'vals': [12.0, 13.0, 14.56]}

    assert phmsdms("12d13m14.56") == {'parts': [12.0, 13.0, 14.56],
                                      'sign': 1,
                                      'units': 'degrees',
                                      'vals': [12.0, 13.0, 14.56]}

    assert phmsdms("12d14.56ss") == {'parts': [12.0, None, 14.56],
                                     'sign': 1,
                                     'units': 'degrees',
                                     'vals': [12.0, 0.0, 14.56]}

    assert phmsdms("14.56ss") == {'parts': [None, None, 14.56],
                                  'sign': 1,
                                  'units': 'degrees',
                                  'vals': [0.0, 0.0, 14.56]}

    assert phmsdms("12h13m12.4s") == {'parts': [12.0, 13.0, 12.4],
                                      'sign': 1,
                                      'units': 'hours',
                                      'vals': [12.0, 13.0, 12.4]}

    assert phmsdms("12:13:12.4s") == {'parts': [12.0, 13.0, 12.4],
                                      'sign': 1,
                                      'units': 'degrees',
                                      'vals': [12.0, 13.0, 12.4]}

    assert phmsdms("-12:13:12.4s") == {'parts': [-12.0, 13.0, 12.4],
                                       'sign': -1,
                                       'units': 'degrees',
                                       'vals': [12.0, 13.0, 12.4]}

    with pytest.raises(ValueError):
        phmsdms("12:13mm:12.4s")

    assert phmsdms("-13m12s") == {'parts': [None, -13.0, 12.0],
                                  'sign': -1,
                                  'units': 'degrees',
                                  'vals': [0.0, 13.0, 12.0]}

    assert phmsdms("-12s") == {'parts': [None, None, -12.0],
                               'sign': -1,
                               'units': 'degrees',
                               'vals': [0.0, 0.0, 12.0]}

    with pytest.raises(ValueError):
        phmsdms("-12:-13:12.4s")


def test_pposition():
    ra, de = pposition("12 22 54.899 +15 49 20.57")
    assert ra == 12+(22/60.0)+(54.899/3600.0)
    assert de == 15+(49/60.0)+(20.57/3600.0)
