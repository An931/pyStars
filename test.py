import unittest
from stars import *
from geometry import *
from drawer import *



class TestStar(unittest.TestCase):
    def test_star_with_lable(self):
        line = ' 35  0: 9:10.7 +59: 8:59 117.52 -03.27  V 2.27   F2III-IV           +0.525 -0.181    13 +012    432  11Bet ( 3)'
        s = Star(line)
        self.assertTrue(isinstance(s.ra, RightAscension))
        self.assertTrue(isinstance(s.dec, Declination))
        self.assertEqual(s.mag, 2.27)
        self.assertEqual(s.sp_class, 'F2III-IV')
        self.assertEqual(s.label, 'Bet')

    def test_star_without_lable(self):
        line = ' 36  1:25:49.0 +60:14: 7 127.19 -02.35 WV -2.68   A5III-IV           +0.297 -0.051    27 +007   8538  37  '
        s = Star(line)
        self.assertTrue(isinstance(s.ra, RightAscension))
        self.assertTrue(isinstance(s.dec, Declination))
        self.assertEqual(s.mag, -2.68)
        self.assertEqual(s.sp_class, 'A5III-IV')
        self.assertEqual(s.label, '')

class TestRightAscension(unittest.TestCase):
    def test_right_ascension(self):
        line = '0: 9:10.7'
        ra = RightAscension(line)
        self.assertEqual(ra.hours, 0)
        self.assertEqual(ra.minutes, 9)
        self.assertEqual(ra.seconds, 10.7)
        self.assertEqual(ra.full_sec, 550.7)

    def test_ra_full_sec(self):
        line = '0: 0:0'
        ra = RightAscension(line)
        ra.full_sec = 24*60*60 + 12
        self.assertEqual(ra.full_sec, 12)

    def test_ra_str(self):
        line = '0:9:10.7'
        ra = RightAscension(line)
        self.assertEqual(str(ra), line)


class TestDeclination(unittest.TestCase):
    def test_declination_neg(self):
        line = '+59: 8:59.0'
        d = Declination(line)
        self.assertEqual(d.sign, 1)
        self.assertEqual(d.degrees, 59)
        self.assertEqual(d.minutes, 8)
        self.assertEqual(d.seconds, 59)
        self.assertEqual(d.full_sec, 212939)

    def test_declination_pos(self):
        line = '-49:28: 5.0'
        d = Declination(line)
        self.assertEqual(d.sign, -1)
        self.assertEqual(d.degrees, 49)
        self.assertEqual(d.minutes, 28)
        self.assertEqual(d.seconds, 5)
        self.assertEqual(d.full_sec, -178085)

    def test_dec_str(self):
        line = '+59:8:59.0'
        d = Declination(line)
        self.assertEqual(str(d), line)


class TestGeometry(unittest.TestCase):
    def test_get_ra_coords(self):
        ra1 = RightAscension('0:0:0')
        self.assertEqual(Geom.get_ra_coords(ra1), 0)
        ra2 = RightAscension('12:0:0')
        self.assertEqual(Geom.get_ra_coords(ra2), -1)
        ra3 = RightAscension('24:0:0')
        self.assertEqual(Geom.get_ra_coords(ra3), 0)
        ra4 = RightAscension('3:30:0')
        self.assertTrue(abs(Geom.get_ra_coords(ra4) - 0.2917) < 0.001)

    def test_get_dec_coords(self):
        d1 = Declination('+90:0:0')
        self.assertEqual(Geom.get_dec_coords(d1), 1)
        d2 = Declination('0:0:0')
        self.assertEqual(Geom.get_dec_coords(d2), 0)
        d3 = Declination('-90:0:0')
        self.assertEqual(Geom.get_dec_coords(d3), -1)
        d4 = Declination('45:0:0')
        self.assertEqual(Geom.get_dec_coords(d4), 0.5)
        d5 = Declination('30:0:0')
        self.assertTrue(abs(Geom.get_dec_coords(d5) - 0.333) < 0.001)

    def test_get_coords(self):
        star = Star()
        star.ra = RightAscension('5:0:0')
        star.dec = Declination('+90:0:0')
        self.assertEqual(Geom.get_coords(star), (0, 1))

        star.ra = RightAscension('12:0:0')
        star.dec = Declination('0:0:0')
        self.assertEqual(Geom.get_coords(star), (-1, 0))

        star.ra = RightAscension('11:59:59')
        star.dec = Declination('0:0:0')
        self.assertTrue(abs(Geom.get_coords(star)[0] - 1) < 0.001)

        star.ra = RightAscension('6:0:0')
        star.dec = Declination('+45:0:0')
        x, y = Geom.get_coords(star)
        self.assertTrue(abs(x - 0.433) < 0.001)
        self.assertEqual(y, 0.5)

        star.ra = RightAscension('18:0:0')
        star.dec = Declination('-45:0:0')
        x, y = Geom.get_coords(star)
        self.assertTrue(abs(x + 0.433) < 0.001)
        self.assertEqual(y, -0.5)

    def test_image_coords(self):
        size = 100
        star = Star()
        star.ra = RightAscension('5:0:0')
        star.dec = Declination('+90:0:0')
        self.assertEqual(Geom.get_image_coords(star, size), (50, 0))

        star.ra = RightAscension('12:0:0')
        star.dec = Declination('0:0:0')
        self.assertEqual(Geom.get_image_coords(star, size), (100, 50))

        star.ra = RightAscension('11:59:59')
        star.dec = Declination('0:0:0')
        x, y = Geom.get_image_coords(star, size)
        self.assertTrue(abs(x - 0.001) < 0.001)
        self.assertEqual(y, 50)


class TestDrawer(unittest.TestCase):
    def test_get_color(self):
    	star = Star()
    	star.sp_class = 'M'
    	self.assertEqual(Drawer.get_color(star), '#ff8f8f')

    def test_get_radius(self):
    	star = Star()
    	star.mag = 1
    	self.assertEqual(Drawer.get_radius(star, 1000), 5)



if __name__ == '__main__':
    unittest.main()