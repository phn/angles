Angles
======

.. _TPM: http://www.sal.wisc.edu/~jwp/astro/tpm/tpm.html
.. _Jeffrey W. Percival: http://www.sal.wisc.edu/~jwp/
.. _pip: http://pypi.python.org/pypi/pip
.. _easy_install: packages.python.org/distribute/easy_install.html

.. image:: https://travis-ci.org/phn/angles.svg?branch=master
    :target: https://travis-ci.org/phn/angles

The Angles module defines several classes for representing angles, and positions
on a sphere. It also has several functions for performing common operations
on angles, such as unit conversion, normalization, creating string
representations and others.

The position of M100 reported by SIMBAD is "12 22 54.899 +15 49 20.57". We can
easily parse these coordinates as follows:

.. code-block:: python

    >>> from __future__ import print_function    
    >>> from angles import AngularPosition

    >>> a = AngularPosition.from_hd("12 22 54.899 +15 49 20.57")
    >>> a.alpha
    3.24157813039
    >>> a.delta
    0.276152636198

    >>> print(a.alpha)
    +12HH 22MM 54.899SS
    >>> print(a.delta)
    +15DD 49MM 20.570SS

    >>> a.alpha.hms.hms
    (1, 12, 22, 54.899)
    >>> a.delta.dms.dms
    (1, 15, 49, 20.57)
    >>> a.alpha.dms.dms
    (1, 185, 43, 43.485)
    >>> a.delta.hms.hms
    (1, 1, 3, 17.371)

    >>> a.alpha.r, a.alpha.d, a.alpha.h, a.alpha.arcs
    (3.2415781303913653, 185.72874583333328, 12.381916388888886, 668623.4849999998)
    >>> a.delta.r, a.delta.d, a.delta.h, a.delta.arcs
    (0.27615263619797403, 15.822380555555556, 1.0548253703703705, 56960.57)


Installation
------------

Use `pip`_ or `easy_install`_::

  $ pip install angles

or,

::

  $ easy_install angles


Tests are in the file ``test_angles.py``.

Examples
--------

Some examples are given below. For more details see docstrings of functions and
classes.

Unit conversion
~~~~~~~~~~~~~~~

Convert between radians, degrees, hours and arc-seconds.

.. code-block:: python

    >>> import math
    >>> from angles import r2d, r2arcs, h2r, h2d, d2arcs

    >>> r2d(math.pi)
    180.0
    >>> r2arcs(math.pi)
    648000.0
    >>> h2r(12.0)
    3.141592653589793
    >>> h2d(12.0)
    180.0
    >>> d2arcs(1.0)
    3600.0

Normalizing angles
~~~~~~~~~~~~~~~~~~

Normalize value between two limits using ``normalize``.

.. code-block:: python

    >>> from angles import normalize

    >>> normalize(-180, -180, 180)
    -180.0
    >>> normalize(180, -180, 180)
    -180.0
    >>> normalize(180, -180, 180, b=True)
    180.0
    >>> normalize(181,-180,180)
    -179.0
    >>> normalize(181, -180, 180, b=True)
    179.0
    >>> normalize(-180,0,360)
    180.0
    >>> normalize(36,0,24)
    12.0
    >>> normalize(368.5,-180,180)
    8.5
    >>> normalize(-100, -90, 90)
    80.0
    >>> normalize(-100, -90, 90, b=True)
    -80.0
    >>> normalize(100, -90, 90, b=True)
    80.0
    >>> normalize(181, -90, 90, b=True)
    -1.0
    >>> normalize(270, -90, 90, b=True)
    -90.0
    >>> normalize(271, -90, 90, b=True)
    -89.0

Normalizing angles on a sphere
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Simplify point on sphere to simplest representation using ``normalize_sphere``.

.. code-block:: python

    >>> from angles import normalize_sphere

    >>> normalize_sphere(180, 91)
    (0.0, 89.0000000000001)

    >>> normalize_sphere(180, -91)
    (0.0, -89.0000000000001)

    >>> normalize_sphere(0, 91)
    (180.0, 89.0000000000001)

    >>> normalize_sphere(0, -91)
    (180.0, -89.0000000000001)

    >>> normalize_sphere(120, 280)
    (119.99999999999999, -80.00000000000003)

    >>> normalize_sphere(375, 45)  # 25 hours ,45 degrees
    (14.999999999999966, 44.99999999999999)

    >>> normalize_sphere(-375, -45)
    (345.00000000000006, -44.99999999999999)

Sexagesimal representation
~~~~~~~~~~~~~~~~~~~~~~~~~~

Convert decimal value into sexagesimal representation.

.. code-block:: python

    >>> from angles import deci2sexa

    >>> deci2sexa(-11.2345678)
    (-1, 11, 14, 4.444)
    >>> deci2sexa(-11.2345678, pre=5)
    (-1, 11, 14, 4.44408)
    >>> deci2sexa(-11.2345678, pre=4)
    (-1, 11, 14, 4.4441)
    >>> deci2sexa(-11.2345678, pre=4, trunc=True)
    (-1, 11, 14, 4.444)

    >>> deci2sexa(-11.2345678, pre=1)
    (-1, 11, 14, 4.4)
    >>> deci2sexa(-11.2345678, pre=0)
    (-1, 11, 14, 4.0)
    >>> deci2sexa(-11.2345678, pre=-1)
    (-1, 11, 14, 0.0)

    >>> x = 23+59/60.0+59.99999/3600.0
    
    >>> deci2sexa(x, pre=3, lower=0, upper=24)
    (1, 24, 0, 0.0)
    >>> deci2sexa(x, pre=3, lower=0, upper=24, upper_trim=True)
    (1, 0, 0, 0.0)
    
    >>> deci2sexa(x, pre=5, lower=0, upper=24, upper_trim=True)
    (1, 23, 59, 59.99999)

Formatting angles
~~~~~~~~~~~~~~~~~

Format an angle into various string representations using ``fmt_angle``.

.. code-block:: python

    >>> from angles import fmt_angle

    >>> fmt_angle(12.348978659, pre=4, trunc=True)
    '+12 20 56.3231'
    >>> fmt_angle(12.348978659, pre=5)
    '+12 20 56.32317'
    >>> fmt_angle(12.348978659, s1='HH ', s2='MM ', s3='SS', pre=5)
    '+12HH 20MM 56.32317SS'

    >>> x = 23+59/60.0+59.99999/3600.0
    >>> fmt_angle(x)
    '+24 00 00.000'
    >>> fmt_angle(x, lower=0, upper=24, upper_trim=True)
    '+00 00 00.000'
    >>> fmt_angle(x, pre=5)
    '+23 59 59.99999'
    >>> fmt_angle(-x, lower=0, upper=24, upper_trim=True)
    '+00 00 00.000'
    >>> fmt_angle(-x)
    '-24 00 00.000'


Parsing sexagesimal strings
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Parse a sexagesimal number from a string using ``phmsdms``.

.. code-block:: python

    >>> from angles import phmsdms

    >>> phmsdms("12") == {
    ... 'parts': [12.0, None, None],
    ... 'sign': 1,
    ... 'units': 'degrees',
    ... 'vals': [12.0, 0.0, 0.0]
    ... }
    True

    >>> phmsdms("12h") == {
    ... 'parts': [12.0, None, None],
    ... 'sign': 1,
    ... 'units': 'hours',
    ... 'vals': [12.0, 0.0, 0.0]
    ... }
    True

    >>> phmsdms("12d13m14.56") == {
    ... 'parts': [12.0, 13.0, 14.56],
    ... 'sign': 1,
    ... 'units': 'degrees',
    ... 'vals': [12.0, 13.0, 14.56]
    ... }
    True

    >>> phmsdms("12d14.56ss") == {
    ... 'parts': [12.0, None, 14.56],
    ... 'sign': 1,
    ... 'units': 'degrees',
    ... 'vals': [12.0, 0.0, 14.56]
    ... }
    True

    >>> phmsdms("14.56ss") == {
    ... 'parts': [None, None, 14.56],
    ... 'sign': 1,
    ... 'units': 'degrees',
    ... 'vals': [0.0, 0.0, 14.56]
    ... }
    True

    >>> phmsdms("12h13m12.4s") == {
    ... 'parts': [12.0, 13.0, 12.4],
    ... 'sign': 1,
    ... 'units': 'hours',
    ... 'vals': [12.0, 13.0, 12.4]
    ... }
    True

    >>> phmsdms("12:13:12.4s") == {
    ... 'parts': [12.0, 13.0, 12.4],
    ... 'sign': 1,
    ... 'units': 'degrees',
    ...  'vals': [12.0, 13.0, 12.4]
    ... }
    True


Parse string containing angular position
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Parse coordinates of a point on sphere using ``pposition``.

.. code-block:: python

    >>> from angles import pposition

    >>> ra, de = pposition("12 22 54.899 +15 49 20.57")
    >>> ra
    12.38191638888889
    >>> de
    15.822380555555556

    >>> pposition("12 22 54.899 +15 49 20.57", details=True)  # doctest: +SKIP
    {'y': 15.822380555555556, 
     'x': 12.38191638888889, 
     'numvals': 6, 
     'raw_x': {
        'vals': [12.0, 22.0, 54.899],
        'units': 'degrees', 
        'parts': [12.0, 22.0, 54.899], 
        'sign': 1
      }, 
     'raw_y': {
        'vals': [15.0, 49.0, 20.57], 
        'units': 'degrees', 
        'parts': [15.0, 49.0, 20.57], 
        'sign': 1
      }
    }

Separation angle along a great circle
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Find angular separation along a great circle using ``sep``. This function
uses vectors to find the angle of separation.

.. code-block:: python

    >>> from angles import r2d, d2r, sep

    >>> r2d(sep(0, 0, 0, d2r(90.0)))
    90.0
    >>> r2d(sep(0, d2r(45.0), 0, d2r(90.0)))
    45.00000000000001
    >>> r2d(sep(0, d2r(-45.0), 0, d2r(90.0)))
    135.0

    >>> r2d(sep(0, d2r(-90.0), 0, d2r(90.0)))
    180.0
    >>> r2d(sep(d2r(45.0), d2r(-90.0), d2r(45.0), d2r(90.0)))
    180.0
    >>> r2d(sep(0, 0, d2r(90.0), 0))
    90.0

    >>> r2d(sep(0, d2r(45.0), d2r(90.0), d2r(45.0)))
    60.00000000000001
    >>> import math
    >>> 90.0 * math.cos(d2r(45.0))  # Distance along latitude circle.
    63.63961030678928

Bearing between two points
~~~~~~~~~~~~~~~~~~~~~~~~~~

Find bearing of one point with respect to another using ``bear``. Like ``sep``
this function uses vectors.

.. code-block:: python

    >>> from angles import bear, r2d, d2r
    >>> bear(0, 0, 0, -d2r(90.0))
    3.141592653589793
    >>> bear(0, -d2r(90.0), 0, 0)
    0.0
    >>> bear(0, -d2r(45.0), 0, 0)
    0.0
    >>> bear(0, -d2r(89.678), 0, 0)
    0.0

    >>> r2d(bear(d2r(45.0), d2r(45.0), d2r(46.0), d2r(45.0)))
    89.64644212193384

    >>> r2d(bear(d2r(45.0), d2r(45.0), d2r(44.0), d2r(45.0)))
    -89.64644212193421


Angle class
~~~~~~~~~~~

Class for representing an angle, conversion between different 
units, generating string representations.

.. code-block:: python

    >>> from __future__ import print_function
    >>> from angles import Angle

    >>> a = Angle(sg="12h34m16.592849219")
    >>> a.r, a.d, a.h, a.arcs  # doctest: +NORMALIZE_WHITESPACE
    (3.291152306055805, 188.56913687174583, 12.571275791449722, 678848.892738285)

    >>> a.hms.sign, a.hms.hh, a.hms.mm, a.hms.ss
    (1, 12, 34, 16.593)
    >>> a.hms.hms
    (1, 12, 34, 16.593)
    >>> a.h
    12.571275791449722

    >>> a.dms.sign, a.dms.dd, a.dms.mm, a.dms.ss
    (1, 188, 34, 8.893)
    >>> a.dms.dms
    (1, 188, 34, 8.893)
    >>> a.d
    188.56913687174583

    >>> print(a.ounit)
    hours
    >>> print(a)
    +12 34 16.593
    >>> a.pre, a.trunc
    (3, False)
    >>> a.pre = 4
    >>> print(a)
    +12 34 16.5928
    >>> a.pre = 3
    >>> a.trunc = True
    >>> print(a)
    +12 34 16.592

    >>> a.ounit = "degrees"
    >>> print(a)
    +188 34 08.892
    >>> a.ounit = "radians"
    >>> print(a)  # doctest: +SKIP
    3.29115230606

    >>> a.ounit = "degrees"
    >>> a.s1 = "DD "
    >>> a.s2 = "MM "
    >>> a.s3 = "SS"
    >>> print(a)
    +188DD 34MM 08.892SS

    >>> a = Angle(r=10)
    >>> a.d, a.h, a.r, a.arcs, a.ounit  # doctest: +NORMALIZE_WHITESPACE
    (572.9577951308232, 38.197186342054884, 10, 2062648.0624709637, 'radians')

    >>> a.d = 10
    >>> a.d, a.h, a.r, a.arcs, a.ounit  # doctest: +NORMALIZE_WHITESPACE
    (10.0, 0.6666666666666666, 0.17453292519943295, 36000.0, 'radians')

    >>> a.dms.mm = 60
    >>> a.d, a.h, a.r, a.arcs, a.ounit  # doctest: +NORMALIZE_WHITESPACE
    (11.0, 0.7333333333333333, 0.19198621771937624, 39600.0, 'radians')

    >>> a.dms.dms = (1, 12, 10, 5.234)
    >>> a.d, a.h, a.r, a.arcs, a.ounit  # doctest: +NORMALIZE_WHITESPACE
    (12.168120555555557, 0.8112080370370371, 0.21237376747404604,
    43805.234000000004, 'radians')

    >>> a.hms.hms = (1, 1, 1, 1)
    >>> a.d, a.h, a.r, a.arcs, a.ounit  # doctest: +NORMALIZE_WHITESPACE
    (15.254166666666668, 1.0169444444444444, 0.2662354329813017,
    54915.00000000001, 'radians')

    >>> print(a)  # doctest: +SKIP
    0.266235432981
    >>> a.ounit = 'hours'
    >>> print(a)
    +01 01 01.000
    >>> a.ounit = 'degrees'
    >>> print(a)
    +15 15 15.000


Class for longitudinal angles
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A subclass of ``Angle`` that is normalized to the range ``[0, 24)``, i.e., a
Right Ascension like angle. The ``ounit`` attribute is always "hours".

.. code-block:: python

    >>> from __future__ import print_function
    >>> from angles import AlphaAngle
    
    >>> a = AlphaAngle(d=180.5)
    >>> print(a)
    +12HH 02MM 00.000SS
    >>> a = AlphaAngle(h=12.0)
    >>> print(a)
    +12HH 00MM 00.000SS
    >>> a = AlphaAngle(h=-12.0)

    >>> a = AlphaAngle("12h14m23.4s")
    >>> print(a)
    +12HH 14MM 23.400SS
    >>> a.r, a.d, a.h, a.arcs
    (3.204380873430289, 183.5975, 12.239833333333333, 660951.0)

    >>> a = AlphaAngle(h=12.54678345)
    >>> a.hms.hms
    (1, 12, 32, 48.42)
    >>> a.hms.sign, a.hms.hh, a.hms.mm, a.hms.ss
    (1, 12, 32, 48.42)
    >>> print(a)
    +12HH 32MM 48.420SS
    >>> a.pre = 5
    >>> a.hms.hms
    (1, 12, 32, 48.42042)
    >>> print(a)
    +12HH 32MM 48.42042SS

    >>> a.s1 = " : "
    >>> a.s2 = " : "
    >>> a.s3 = ""
    >>> print(a)
    +12 : 32 : 48.42042

    >>> a.pre = 3
    >>> a.dms.dms
    (1, 188, 12, 6.306)

    >>> a = AlphaAngle(h=25.0)
    >>> print(a)
    +01HH 00MM 00.000SS
    >>> a = AlphaAngle(h=-1.0)
    >>> print(a)
    +23HH 00MM 00.000SS

    >>> a.hms.hh = 23
    >>> a.hms.mm = 59
    >>> a.hms.ss = 59.99999
    >>> a.hms.hms
    (1, 0, 0, 0.0)
    >>> print(a)
    +00HH 00MM 00.000SS
    >>> a.pre = 5
    >>> a.hms.hms
    (1, 23, 59, 59.99999)
    >>> print(a)
    +23HH 59MM 59.99999SS

Class for latitudinal angles
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A subclass of ``Angle`` that is normalized to the range ``[-90, 90]``, i.e., a
Declination like angle. The ``ounit`` attribute is always "degrees".


.. code-block:: python

    >>> from __future__ import print_function
    >>> from angles import DeltaAngle

    >>> a = DeltaAngle(d=-45.0)
    >>> print(a)
    -45DD 00MM 00.000SS
    >>> a = DeltaAngle(d=180.0)
    >>> print(a)
    +00DD 00MM 00.000SS
    >>> a = DeltaAngle(h=12.0)
    >>> print(a)
    +00DD 00MM 00.000SS
    >>> a = DeltaAngle(sg="91d")
    >>> print(a)
    +89DD 00MM 00.000SS

    >>> a = DeltaAngle("12d23m14.2s")
    >>> print(a)
    +12DD 23MM 14.200SS
    >>> a.r, a.d, a.h, a.arcs
    (0.2161987825813487, 12.387277777777777, 0.8258185185185185, 44594.2)

    >>> a = DeltaAngle(d=12.1987546)
    >>> a.dms.dms
    (1, 12, 11, 55.517)
    >>> a.pre = 5
    >>> a.dms.dms
    (1, 12, 11, 55.51656)
    >>> a.dms.dd, a.dms.mm, a.dms.ss
    (12, 11, 55.51656)
    >>> a.pre = 0
    >>> a.dms.dms
    (1, 12, 11, 56.0)

    >>> a = DeltaAngle(d=12.3459876)
    >>> a.s1 = " : "
    >>> a.s2 = " : "
    >>> a.s3 = ""
    >>> print(a)
    +12 : 20 : 45.555

    >>> a = DeltaAngle(d=-91.0)
    >>> print(a)
    -89DD 00MM 00.000SS
    >>> a = DeltaAngle(d=91.0)
    >>> print(a)
    +89DD 00MM 00.000SS

    >>> a.dms.sign = 1
    >>> a.dms.dd = 89
    >>> a.dms.mm = 59
    >>> a.dms.ss = 59.9999
    >>> a.pre = 3
    >>> print(a)
    +90DD 00MM 00.000SS
    >>> a.pre = 5
    >>> print(a)
    +89DD 59MM 59.99990SS

    >>> a.dms.dms = (1, 0, 0, 0.0)
    >>> a.dms.dd = 89
    >>> a.dms.mm = 60
    >>> a.dms.ss = 60
    >>> a.pre = 3
    >>> print(a)
    +89DD 59MM 00.000SS

Class for points on a unit sphere
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A class for representing a point on a sphere. The input angle values are 
normalized to get the simplest representation of the coordinates of the point.

.. code-block:: python

   >>> from __future__ import print_function
    >>> from angles import AngularPosition, r2d

    >>> a = AngularPosition.from_hd("12 22 54.899 +15 49 20.57")
    >>> print(a)
    +12HH 22MM 54.899SS +15DD 49MM 20.570SS
    >>> a = AngularPosition.from_hd("12dd 22 54.899 +15 49 20.57")
    >>> print(a)
    +00HH 49MM 31.660SS +15DD 49MM 20.570SS
    >>> a = AngularPosition.from_hd("12d 22 54.899 +15 49 20.57")
    >>> print(a)
    +00HH 49MM 31.660SS +15DD 49MM 20.570SS

    >>> a = AngularPosition(alpha=165, delta=-91)  # alpha should flip by 180 degrees
    >>> round(a.alpha.d , 12), round(a.delta.d, 12)
    (345.0, -89.0)

    >>> a.delta.d = -91 # alpha should now do another 180 flip and come back to 165
    >>> round(a.alpha.d, 12), round(a.delta.d, 12)
    (165.0, -89.0)
    
    >>> a.delta.d = 89  # there should be no change in normalized angles
    >>> round(a.alpha.d, 12), round(a.delta.d, 12)
    (165.0, 89.0)
    
    >>> a.alpha.d = -180  # alpha should normalize to 180 delta shouldn't change
    >>> round(a.alpha.d, 12), round(a.delta.d, 12)
    (180.0, 89.0)

    >>> pos1 = AngularPosition(alpha=12.0, delta=90.0)
    >>> pos2 = AngularPosition(alpha=12.0, delta=0.0)
    >>> r2d(pos2.bear(pos1))
    0.0
    >>> r2d(pos1.bear(pos2))
    0.0
    >>> r2d(pos1.sep(pos2))
    90.0
    >>> pos1.alpha.h = 0.0
    >>> pos2.alpha.h = 0.0
    >>> r2d(pos1.sep(pos2))
    90.0
    >>> r2d(pos2.bear(pos1))
    0.0
    >>> r2d(pos1.bear(pos2))
    0.0

Credits
--------

Some of the functions are adapted from the `TPM`_ C library by `Jeffrey
W. Percival`_.

License
-------

Released under BSD; see LICENSE.txt.

For comments and suggestions, email to user `prasanthhn` in the `gmail.com`
domain.

