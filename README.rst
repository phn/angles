Angles
======

.. _TPM: http://www.sal.wisc.edu/~jwp/astro/tpm/tpm.html
.. _Jeffrey W. Percival: http://www.sal.wisc.edu/~jwp/
.. _pip: http://pypi.python.org/pypi/pip
.. _easy_install: packages.python.org/distribute/easy_install.html


Angles module defines several classes for representing angles, and
positions on a unit sphere. It also has several functions for
performing common operations on angles, such as unit conversion,
normalization, creating string representations and others.

Examples
--------

Some examples are given below. For more information see
http://oneau.wordpress.com/angles/.

Unit conversion::

    >>> import math
    >>> angles.r2d(math.pi)
    180.0
    >>> angles.r2arcs(math.pi)
    648000.0
    >>> angles.h2r(12.0)
    3.1415926535897931
    >>> angles.h2d(12.0)
    180.0
    >>> angles.d2arcs(1.0)
    3600.0

Normalizing angles::

    >>> normalize(-270,-180,180)
    90.0
    >>> import math
    >>> math.degrees(normalize(-2*math.pi,-math.pi,math.pi))
    0.0
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

Sexagesimal representation::

    >>> x = 23+59/60.0+59.99999/3600.0
    >>> deci2sexa(x, pre=3, lower=0, upper=24, upper_trim=True)
    (1, 0, 0, 0.0)
    >>> deci2sexa(x, pre=3, lower=0, upper=24, upper_trim=False)
    (1, 24, 0, 0.0)
    >>> deci2sexa(x, pre=5, lower=0, upper=24, upper_trim=True)
    (1, 23, 59, 59.99999)

Formatting angles::

    >>> x = 23+59/60.0+59.99999/3600.0
    >>> fmt_angle(x)
    '+24 00 00.000 '
    >>> fmt_angle(x, lower=0, upper=24, upper_trim=True)
    '+00 00 00.000 '
    >>> fmt_angle(x, pre=5)
    '+23 59 59.99999 '
    >>> fmt_angle(-x, lower=0, upper=24, upper_trim=True)
    '+00 00 00.000 '
    >>> fmt_angle(-x)
    '-24 00 00.000 '

Parsing sexagesimal strings::

    >>> phmsdms("12d14.56ss")

    {'parts': [12.0, None, 14.56],
     'sign': 1,
     'units': 'degrees',
     'vals': [12.0, 0.0, 14.56]}
    >>> phmsdms("14.56ss")

    {'parts': [None, None, 14.56],
     'sign': 1,
     'units': 'degrees',
     'vals': [0.0, 0.0, 14.56]}

    >>> phmsdms("12h13m12.4s")

    {'parts': [12.0, 13.0, 12.4],
     'sign': 1,
     'units': 'hours',
     'vals': [12.0, 13.0, 12.4]}


Separation angle along a great circle, using vectors::

    >>> r2d(sep(0, d2r(45.0), d2r(90.0), d2r(45.0)))
    60.00000000000001
    >>> import math
    >>> 90.0 * math.cos(d2r(45.0))  # Distance along latitude circle.
    63.63961030678928

    >>> r2d(sep(0, d2r(45.0), 0, d2r(90.0)))
    45.00000000000001

Bearing between two points, using vectors::

    >>> angles.bear(0, 0, 0, -angles.d2r(90.0))
    3.141592653589793
    >>> angles.bear(0, -angles.d2r(90.0), 0, 0)
    0.0
    >>> angles.bear(0, -angles.d2r(45.0), 0, 0)
    0.0
    >>> angles.bear(0, -angles.d2r(89.678), 0, 0)
    0.0

    >>> r2d(bear(angles.d2r(45.0), angles.d2r(45.0),
        angles.d2r(60.0), angles.d2r(45.0)))
    84.68152816060062


Angle class::

    >>> a = Angle(sg="12h34m16.592849219")
    >>> print a.r, a.d, a.h, a.arcs
    3.29115230606 188.569136872 12.5712757914 678848.892738
    >>> print a.ounit
    hours
    >>> print a
    +12 34 16.593
    >>> print a.pre, a.trunc
    3 False
    >>> a.pre = 4
    >>> print a
    +12 34 16.5928
    >>> a.pre = 3
    >>> a.trunc = True
    >>> print a
    +12 34 16.592

    >>> a.ounit = "degrees"
    >>> print a
    +188 34 08.8927
    >>> a.ounit = "radians"
    >>> print a
    3.29115230606

    >>> a.ounit = "degrees"
    >>> a.s1 = "DD "
    >>> a.s2 = "MM "
    >>> a.s3 = "SS"
    >>> print a
    +188DD 34MM 08.892SS

Class for longitudinal angles::

    >>> a = AlphaAngle(d=180.5)
    >>> print a
    +12HH 02MM 00.000SS
    >>> a = AlphaAngle(h=12.0)
    >>> print a
    +12HH 00MM 00.000SS

    >>> a = AlphaAngle(h=-12.0)
    >>> a.hms
    (1, 12, 0, 0.0)
    >>> a = AlphaAngle(h=12.54678345)
    >>> a.hms
    (1, 12, 32, 48.42)
    >>> a.sign, a.hh, a.mm, a.ss
    (1, 12, 32, 48.42)
    >>> print a
    +12HH 32MM 48.420SS
    >>> a.pre = 5
    >>> a.hms
    (1, 12, 32, 48.42042)
    >>> print a
    +12HH 32MM 48.42042SS

    >>> a = AlphaAngle(h=25.0)
    >>> print a
    +01HH 00MM 00.000SS
    >>> a = AlphaAngle(h=-1.0)
    >>> print a
    +23HH 00MM 00.000SS


Class for latitudinal angles::

    >>> a = DeltaAngle(d=-45.0)
    >>> print a
    -45DD 00MM 00.000SS
    >>> a = DeltaAngle(h=12.0)
    >>> print a
    +00DD 00MM 00.000SS
    >>> a = DeltaAngle(sg="91d")
    >>> print a
    +89DD 00MM 00.000SS

    >>> a = DeltaAngle("12d23m14.2s")
    >>> print a
    +12DD 23MM 14.200SS
    >>> print a.r, a.d, a.h, a.arcs
    0.216198782581 12.3872777778 0.825818518519 44594.2

    >>> a = DeltaAngle(d=12.1987546)
    >>> a.dms
    (1, 12, 11, 55.517)
    >>> a.pre = 5
    >>> a.dms
    (1, 12, 11, 55.51656)
    >>> a.dd, a.mm, a.ss
    (12, 11, 55.51656)
    >>> a.pre = 0
    >>> a.dms
    (1, 12, 11, 56.0)

    >>> a.dd = 89
    >>> a.mm = 59
    >>> a.ss = 59.9999
    >>> print a
    +90DD 00MM 00.000SS
    >>> a.pre = 5
    >>> print a
    +89DD 59MM 59.99990SS
    >>> a.dd = 89
    >>> a.mm = 60
    >>> a.ss = 60
    >>> print a
    +89DD 59MM 00.000SS

Class for points on a unit sphere::

    >>> pos1 = AngularPosition(alpha=12.0, delta=90.0)
    >>> pos2 = AngularPosition(alpha=12.0, delta=0.0)
    >>> angles.r2d(pos2.bear(pos1))
    0.0
    >>> angles.r2d(pos1.bear(pos2))
    0.0
    >>> angles.r2d(pos1.sep(pos2))
    90.0
    >>> pos1.alpha.h = 0.0
    >>> pos2.alpha.h = 0.0
    >>> angles.r2d(pos1.sep(pos2))
    90.0
    >>> angles.r2d(pos2.bear(pos1))
    0.0
    >>> angles.r2d(pos1.bear(pos2))
    0.0

    >>> pos2.delta.d = -90
    >>> angles.r2d(pos1.bear(pos2))
    0.0
    >>> angles.r2d(pos1.sep(pos2))
    180.0


Installation
------------

Use `pip`_ or `easy_install`_::

  $ pip install angles

or,

::

  $ easy_install angles

  
Details
-------

This module provides three classes for representing angles: ``Angle``,
``AlphaAngle`` and ``DeltaAngle``, and one class for representing a point
on a unit sphere, ``AngularPosition``.

``Angle`` is for representing generic angles. ``AlphaAngle`` is for
representing longitudinal angles such as geographic longitude, right
ascension and others. ``DeltaAngle`` is for representing latitudinal
angles such as geographic latitude, declination and others.

An angle object can be initialized with value in various units, it can
normalize its value into an appropriate range. The value can be
retrieved in various units, using appropriately named attributes.

Sexagesimal representation of an angle can be obtained through
appropriate attributes of the angle object. The number of decimal
places in the final part of a sexagesimal representation, and whether
rounding or truncation is used to produce these many decimal places,
can be customized.

An angle object can provide string representation of itself. The
delimiters used in the string representation can be customized. The
string representation is based on the sexagesimal value and hence it
also reflects the precision and truncation settings.

The ``AngularPosition`` class can be used for representing points on a
sphere. It uses an ``AlphaAngle`` instance for storing the longitudinal
angle, and a ``DeltaAngle`` instance for storing the latitudinal angle.
It can calcuate the separation and bearing, also called position angle,
to another point on the sphere. The results for separation and
bearing agree with those from the SLALIB (pyslalib) library (see the
function ``_test_with_slalib()``).

The separation and bearing calculations do not use spherical
trignometry. They involve Cartesian vectors, and objects of the class
``CartesianVector`` are used for these calculations.

Almost all the methods of the classes call functions for performing
calculations. If needed these functions can be used directly.

Functions include those for converting angles between different units,
parsing sexagesimal strings, creating string representations of angles,
converting angles between various units, normalizing angles into a
given range, finding separation and bearing bewteen two points and
others. Normalization of angles can be performed in two different
ways. One method normalizes angles in the manner that longitudinal
angles are normalized i.e., [0, 360.0) or [0, 2π) or [0, 24.0). The
other method normalizes angles in the manner that latitudinal angles
are normalized i.e., [-90, 90] or [-π/2, π/2].

See docstrings of classes and functions for documentation and
examples. Also see http://oneau.wordpress.com/angles/.

Credits
--------

Some of the functions are adapted from the `TPM`_ C library by `Jeffrey
W. Percival`_. A Python interface to this C library is available at
http://github.com/phn/pytpm.

License
-------

Released under BSD; see
http://www.opensource.org/licenses/bsd-license.php.

For comments and suggestions, email to user `prasanthhn` in the `gmail.com`
domain.

