import math
import pytest
from angles import (
    r2d, d2r, h2d, d2h, r2h, h2r, arcs2r, arcs2h, h2arcs, d2arcs, arcs2d,
    normalize, deci2sexa, sexa2deci, fmt_angle, phmsdms, pposition, sep, bear,
    Angle, AlphaAngle, DeltaAngle, CartesianVector, normalize_sphere,
    AngularPosition
)


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


def test_sep_against_slalib_dsep():
    """Results from sep should match those from slalib.dsep"""
    # Random positions.
    import random
    import math
    random.seed(12345)
    alpha = [random.uniform(0, 2 * math.pi) for i in range(100)]
    delta = [random.uniform(-math.pi / 2, math.pi / 2)
             for i in range(100)]

    alpha1 = [random.uniform(0, 2 * math.pi) for i in range(100)]
    delta1 = [random.uniform(-math.pi / 2, math.pi / 2)
              for i in range(100)]

    # Code used to generate result from pyslalib:
    # s = [slalib.sla_dsep(alpha[i], delta[i], alpha1[i], delta1[i])
    #      for i in range(100)]
    s = [2.3488832415605776,
         1.1592942993972908,
         1.6727782224088137,
         1.9310273037619246,
         1.961534390837681,
         1.5150119839396818,
         1.8524526916856978,
         2.116947088206131,
         0.9750943461637399,
         0.8331152895856854,
         2.4690444308150243,
         0.8640444988019701,
         1.041460475452765,
         1.9245098805162162,
         2.7727507743449507,
         1.1760229988483686,
         1.6418575515189582,
         1.0798127458770757,
         2.705734045454533,
         2.711202832152844,
         2.4387778718976763,
         0.1675761464872016,
         0.7614806222975763,
         1.7781491597763561,
         2.029672021455121,
         2.4349201303097403,
         1.2603565818807192,
         2.05499965347367,
         0.6224811898002452,
         0.8126836325942026,
         0.7539982342941834,
         1.6809458707673535,
         1.975972151791415,
         0.7115429070168364,
         1.8079386355215084,
         0.7830659699492306,
         1.233553087948177,
         2.08588792306906,
         0.2779525335855478,
         1.458433197949138,
         1.2964042308707935,
         1.117425142370921,
         1.6383665060581982,
         0.21787615812753383,
         1.6859098755220057,
         1.2253004206853584,
         1.472817142187865,
         0.6648294675219921,
         2.982945161877018,
         0.45704974384275243,
         1.1584539180661326,
         2.8484175031722643,
         1.0402706684988297,
         0.7079258905264588,
         0.7808758533750498,
         0.5608700573233222,
         1.8505539643075692,
         2.494182944528214,
         0.8296145526473544,
         2.2901089789186297,
         1.7477923358131886,
         2.1499080375112816,
         1.1529753011873909,
         1.807265859808323,
         2.5770854449349865,
         1.172037115203078,
         2.7438561146081937,
         0.2216663532818151,
         1.4502352305471127,
         2.2334298247493645,
         1.9946613229884687,
         1.1362010677143621,
         0.9530063759328101,
         0.6782653608813761,
         0.9421358945224116,
         1.970340302154089,
         0.31583484463019296,
         0.5945806070431309,
         1.9894690263497685,
         0.5114702873070847,
         3.059530134272125,
         0.09988794964432562,
         2.1732721685109437,
         2.054896439114964,
         1.0130957019858804,
         1.6899941268950893,
         1.4002698103226345,
         1.3736478209061835,
         1.7281316524003778,
         1.7041224372124824,
         2.7245561902753233,
         1.676900403298997,
         0.5940433957880709,
         2.4371934329915814,
         2.189360172634095,
         1.127368860507556,
         0.49285131033236657,
         2.6159861791852204,
         0.878592556336548,
         2.875063431097953]

    s1 = [sep(a1, b1, a2, b2) for a1, b1, a2, b2 in zip(alpha, delta, alpha1, delta1)]
    d = [i - j for i, j in zip(s, s1)]

    assert abs(min(d)) <= 1e-8
    assert abs(max(d)) <= 1e-8


def test_bear_against_slalib_dbear():
    # Random positions.
    import random
    import math
    random.seed(12345)
    alpha = [random.uniform(0, 2 * math.pi) for i in range(100)]
    delta = [random.uniform(-math.pi / 2, math.pi / 2)
             for i in range(100)]

    alpha1 = [random.uniform(0, 2 * math.pi) for i in range(100)]
    delta1 = [random.uniform(-math.pi / 2, math.pi / 2)
              for i in range(100)]

    # Code used to genereate bearing using slalib dbear:
    # s = [slalib.sla_dbear(alpha[i], delta[i], alpha1[i], delta1[i]) for i in range(100)]
    b = [-2.802730180048627,
         -1.8282705266673154,
         -0.8229162360615494,
         -1.50561816706146,
         0.6169694662032101,
         -0.6505136095824406,
         -0.6237949122875199,
         -2.0768579807928913,
         0.00027549548902526105,
         1.6142044071114134,
         3.0878895670973243,
         -0.47320706830317716,
         0.06190481660259022,
         -1.03007008188762,
         0.775717143305989,
         -2.7067016680966023,
         2.1224548117790047,
         -1.030175664056971,
         -1.8233618083982595,
         1.3802949430521891,
         1.32600595175508,
         1.9161324814685965,
         -1.257992384533619,
         -1.8923575750450647,
         -2.849982502670024,
         -1.4815085590837829,
         1.2338318984498888,
         0.9700753149536098,
         -3.050268462926681,
         -0.1318582353729857,
         0.18967227270953274,
         -2.6611041651816594,
         -3.0926331594553336,
         -2.9552961803695688,
         -1.0552664256955493,
         -0.3182126662842619,
         1.74355265166135,
         1.9194408827882212,
         -2.23431073776154,
         2.141981338795311,
         3.0955846805455725,
         -2.2600451709070986,
         1.0631812721303564,
         1.911640561253558,
         2.3958324854466624,
         -1.5143325847489462,
         2.946174804550307,
         -1.6912405026872621,
         -0.11786194597447722,
         1.0089300595551698,
         2.8464370317469925,
         -1.6337200759200259,
         -0.6680723541395739,
         -2.471721062395574,
         1.4597475588846283,
         3.0792251024082278,
         -0.8057020486292137,
         -1.510207534571296,
         -0.08775316083954136,
         2.0988637247219883,
         2.2504551423501837,
         2.107601630440999,
         0.34039601061617075,
         1.0418765214809675,
         0.688747369384069,
         -2.3296409687097386,
         2.5897193899922506,
         -2.393153809329422,
         -3.0541885602740177,
         -1.8139247745212312,
         -1.0210832104840029,
         0.6899945557674444,
         -0.8891455292741541,
         3.130046300550455,
         2.908952782394968,
         0.6550522788979163,
         -3.134605151198775,
         -0.12475321919475321,
         -1.6656194717624897,
         -0.9677173412992314,
         -2.9207577062998094,
         2.4110029136060587,
         -0.03098323339310322,
         1.9470847586196487,
         1.7443120546722641,
         3.0823235581938064,
         2.9447500058858602,
         -1.9083517971200812,
         1.1505416723252806,
         -2.3991117480912285,
         -2.8752727323013234,
         0.07055989389651941,
         0.6806493576133517,
         -1.2279992966931366,
         2.649711406235304,
         -3.0212965774564386,
         2.81575992838288,
         0.5727515440160112,
         -0.17589890559662485,
         3.1252650751263333]

    b1 = [bear(a1, b1, a2, b2) for a1, b1, a2, b2 in zip(alpha, delta, alpha1, delta1)]
    d = [i - j for i, j in zip(b, b1)]

    assert abs(min(d)) <= 1e-8
    assert abs(max(d)) <= 1e-8


def test_angle_class_must_initialize_properly():
    a = Angle(sg="12h14m13.567s")
    val = 12 + 14/60.0 + 13.567 / 3600.0
    assert a.h == val
    assert a.ounit == 'hours'
    assert a.r == h2r(val)
    assert a.d == h2d(val)
    assert a.arcs == h2arcs(val)

    # ignore r
    with pytest.warns(UserWarning):
        Angle(sg="12h14m13.567s", r=10)

    a = Angle(sg="12h14m13.567s", r=10)
    assert a.r == h2r(val)
    assert a.ounit == 'hours'

    # ignore h and mm
    with pytest.warns(UserWarning):
        a = Angle(r=10, h=20)

    a = Angle(r=10, h=20)
    assert a.r == 10
    assert a.ounit == 'radians'
    assert a.h == r2h(10)

    a = Angle(h=20, d=10)
    assert a.d == 10
    assert a.ounit == 'degrees'
    assert a.h == d2h(10)


def test_angle_class_must_handle_assignments():
    a = Angle(d=10.5)
    a.r = d2r(45.0)

    v = 45.0
    assert a.r == d2r(v)
    assert a.h == d2h(v)
    assert a.arcs == d2arcs(v)
    assert a.ounit == 'degrees'

    v = 46.0
    # assignment
    a.r = d2r(v)
    assert a.r == d2r(v)
    assert a.h == d2h(v)
    assert a.d == v
    assert a.arcs == d2arcs(v)
    assert a.ounit == 'degrees'  # no change

    v = 49.0
    a.d = v
    assert a.r == d2r(v)
    assert a.h == d2h(v)
    assert a.d == v
    assert a.arcs == d2arcs(v)
    assert a.ounit == 'degrees'  # no change

    v = 10
    a.h = v
    assert a.r == h2r(v)
    assert a.h == v
    assert a.d == h2d(v)
    assert a.arcs == h2arcs(v)
    assert a.ounit == 'degrees'  # no change

    v = 3600.0
    a.arcs = v
    assert a.r == arcs2r(v)
    assert a.h == arcs2h(v)
    assert a.d == arcs2d(v)
    assert a.arcs == v
    assert a.ounit == 'degrees'  # no change


def test_angle_class_getting_hms_property_must_work():
    a = Angle(d=45.0)

    assert a.hms.sign == 1
    assert a.hms.hh == 3.0
    assert a.hms.mm == 0.0
    assert a.hms.ss == 0.0
    assert a.hms.hms == (1, 3, 0.0, 0.0)
    assert str(a.hms) == ("+03HH 00MM 00.000SS")

    a = Angle(sg="-12h14m13.567s")

    assert a.hms.sign == -1
    assert a.hms.hh == 12
    assert a.hms.mm == 14
    assert a.hms.ss == 13.567
    assert a.hms.hms == (-1, 12, 14, 13.567)
    assert str(a.hms) == "-12HH 14MM 13.567SS"


def test_angle_class_setting_hms_property_must_work():
    a = Angle(d=0.0)

    a.hms = (1, 12, 14, 13.567)
    v = 12 + 14/60.0 + 13.567/3600.0
    assert a.h == v
    assert a.hms.sign == 1
    assert a.hms.hh == 12
    assert a.hms.mm == 14
    assert a.hms.ss == 13.567
    assert str(a.hms) == "+12HH 14MM 13.567SS"

    a.hms.hh = 15
    assert a.h == 15 + 14/60.0 + 13.567/3600.0

    a.hms.mm = 15
    assert a.h == 15 + 15/60.0 + 13.567/3600.0

    a = Angle(d=0.0)
    a.hms.mm = 12
    assert round(a.h, 15) == 12/60.0


def test_angle_class_getting_dms_property_must_work():
    a = Angle(d=45.0)

    assert a.dms.sign == 1
    assert a.dms.dd == 45.0
    assert a.dms.mm == 0.0
    assert a.dms.ss == 0.0
    assert a.dms.dms == (1, 45, 0.0, 0.0)
    assert str(a.dms) == ("+45DD 00MM 00.000SS")

    a = Angle(sg="-12h14m13.567s")

    assert a.dms.sign == -1
    assert a.dms.dd == 183
    assert a.dms.mm == 33
    assert a.dms.ss == 23.505
    assert a.dms.dms == (-1, 183, 33, 23.505)
    assert str(a.dms) == "-183DD 33MM 23.505SS"


def test_angle_class_setting_dms_property_must_work():
    a = Angle(d=0.0)

    a.dms = (-1, 183, 33, 23.505)
    v = -1 * (183 + 33/60.0 + 23.505/3600.0)
    assert a.d == v
    assert a.dms.sign == -1
    assert a.dms.dd == 183
    assert a.dms.mm == 33
    assert a.dms.ss == 23.505
    assert str(a.dms) == "-183DD 33MM 23.505SS"

    a.dms.dd = 101
    assert a.d == -101.55652916666668

    a.dms.mm = 15
    assert a.d == -101.25652916666667

    a = Angle(d=0.0)
    a.dms.mm = 12
    assert round(a.d, 15) == 12/60.0


def test_angle_class_hms_and_dms_must_be_consistent():
    a = Angle(d=1)

    a.dms = (1, 1, 0, 0)
    assert a.hms.hms == (1, 0, 4, 0.0)

    a.hms = (1, 1, 0, 0)
    assert a.dms.dms == (1, 15, 0, 0.0)


def test_alpha_angle():
    a = AlphaAngle(h=-12)
    assert a.h == 12
    assert a.ounit == "hours"
    with pytest.raises(AttributeError):
        a.ounit = "degrees"

    a = AlphaAngle(h=12.527)

    assert round(a.h, 14) == 12.527
    a.hms.hms == (1, 12, 31, 37.2)
    a.dms.dms == (1, 12/15.0, 31/60.0/15.0, 37.2/3600.0/15.0)


def test_delta_angle():
    a = DeltaAngle(d=-91)
    assert a.d == -89
    assert a.ounit == "degrees"
    with pytest.raises(AttributeError):
        a.ounit = "hours"

    a = DeltaAngle(d=45.678)

    assert round(a.d, 12) == 45.678
    a.dms.dms == (1, 45, 40, 40.80)
    a.hms.hms == (1, 45/15.0, 40/60.0/15.0, 40.80/3600.0/15.0)


def test_cartesian_vector():
    v = CartesianVector()
    assert v.x == 0.0
    assert v.y == 0.0
    assert v.z == 0.0

    v = CartesianVector(x=10, y=10, z=10)
    assert v.mod == math.sqrt(3 * 10**2)
    assert v.spherical_coords == (v.mod, math.atan2(10, 10), math.asin(10/v.mod))

    a = math.atan2(10, 10)
    d = math.asin(10/v.mod)
    v = CartesianVector.from_spherical(r=1.0, alpha=a, delta=d)
    assert v.mod == 1.0
    assert round(v.x, 15) == round(math.cos(d)*math.sin(a), 15)
    assert round(v.y, 15) == round(math.cos(d)*math.cos(a), 15)
    assert round(v.z, 15) == round(math.sin(d), 15)
    r1, a1, d1 = v.spherical_coords
    assert r1 == 1.0
    assert round(a1, 15) == round(a, 15)
    assert round(d1, 15) == round(d, 15)


def test_cartesian_vector_normalize_sphere():
    a = (180, 91)
    r = (0, 89)
    v = CartesianVector.from_spherical(r=1.0, alpha=d2r(a[0]), delta=d2r(a[1]))
    x = [r2d(i) for i in v.normalized_angles]
    assert (round(x[0], 12), round(x[1], 12)) == r

    a = (180, -91)
    r = (0, -89)
    v = CartesianVector.from_spherical(r=1.0, alpha=d2r(a[0]), delta=d2r(a[1]))
    x = [r2d(i) for i in v.normalized_angles]
    assert (round(x[0], 12), round(x[1], 12)) == r

    a = (0, 91)
    r = (180, 89)
    v = CartesianVector.from_spherical(r=1.0, alpha=d2r(a[0]), delta=d2r(a[1]))
    x = [r2d(i) for i in v.normalized_angles]
    assert (round(x[0], 12), round(x[1], 12)) == r

    a = (0, -91)
    r = (180, -89)
    v = CartesianVector.from_spherical(r=1.0, alpha=d2r(a[0]), delta=d2r(a[1]))
    x = [r2d(i) for i in v.normalized_angles]
    assert (round(x[0], 12), round(x[1], 12)) == r

    a = (120, 280)
    r = (120, -80)
    v = CartesianVector.from_spherical(r=1.0, alpha=d2r(a[0]), delta=d2r(a[1]))
    x = [r2d(i) for i in v.normalized_angles]
    assert (round(x[0], 12), round(x[1], 12)) == r

    a = (375, 45)  # 25 hours, 45 degrees
    r = (15, 45)
    v = CartesianVector.from_spherical(r=1.0, alpha=d2r(a[0]), delta=d2r(a[1]))
    x = [r2d(i) for i in v.normalized_angles]
    assert (round(x[0], 12), round(x[1], 12)) == r

    a = (-375, -45)
    r = (345, -45)
    v = CartesianVector.from_spherical(r=1.0, alpha=d2r(a[0]), delta=d2r(a[1]))
    x = [r2d(i) for i in v.normalized_angles]
    assert (round(x[0], 12), round(x[1], 12)) == r

    a = (-375, -91)
    r = (165, -89)
    v = CartesianVector.from_spherical(r=1.0, alpha=d2r(a[0]), delta=d2r(a[1]))
    x = [r2d(i) for i in v.normalized_angles]
    assert (round(x[0], 12), round(x[1], 12)) == r


def test_normalize_sphere():
    x = normalize_sphere(180, 91)
    r = (0, 89)
    assert (round(x[0], 12), round(x[1], 12)) == r

    x = normalize_sphere(180, -91)
    r = (0, -89)
    assert (round(x[0], 12), round(x[1], 12)) == r

    x = normalize_sphere(0, 91)
    r = (180, 89)
    assert (round(x[0], 12), round(x[1], 12)) == r

    x = normalize_sphere(0, -91)
    r = (180, -89)
    assert (round(x[0], 12), round(x[1], 12)) == r

    x = normalize_sphere(120, 280)
    r = (120, -80)
    assert (round(x[0], 12), round(x[1], 12)) == r

    x = normalize_sphere(375, 45)  # 25 hours ,45 degrees
    r = (15, 45)
    assert (round(x[0], 12), round(x[1], 12)) == r

    x = normalize_sphere(-375, -45)
    r = (345, -45)
    assert (round(x[0], 12), round(x[1], 12)) == r


def test_angular_position():
    # should get converted to (345, -89)
    ap = AngularPosition(alpha=165, delta=-91)
    assert round(ap.alpha.d, 12) == 345
    assert round(ap.delta.d, 12) == -89

    # changing delta to -91 again should switch alpha back to 165
    ap.delta.d = -91
    assert round(ap.alpha.d, 12) == 165
    assert round(ap.delta.d, 12) == -89

    # changing to 89 shouldn't change alpha
    ap.delta.d = 89
    assert round(ap.alpha.d, 12) == 165
    assert round(ap.delta.d, 12) == 89

    # changing alpha shouldn't change delta
    ap.alpha.d = -180
    assert round(ap.alpha.d, 12) == 180
    assert round(ap.delta.d, 12) == 89


def test_angular_position_from_hd():
    a = AngularPosition.from_hd("19 16 35.57 +30 11 00.5")
    assert round(a.alpha.h, 12) == round(19 + 16/60.0 + 35.57/3600.0, 12)
    assert round(a.delta.d, 12) == round(30 + 11/60.0 + 0.5/3600.0, 12)

    a = AngularPosition.from_hd("19d 16 35.57 +30 11 00.5")
    assert round(a.alpha.d, 12) == round(19 + 16/60.0 + 35.57/3600.0, 12)
    assert round(a.delta.d, 12) == round(30 + 11/60.0 + 0.5/3600.0, 12)


def test_angular_position_sep():
    a = AngularPosition(45.0, 45.0)
    b = AngularPosition(45.0, -45.0)

    assert round(a.sep(b), 12) == round(d2r(90), 12)


def test_angular_position_bear():
    a = AngularPosition(45.0, 45.0)
    b = AngularPosition(45.0, -45.0)

    assert round(a.bear(b), 12) == round(d2r(180), 12)
