import unittest
gymplay = __import__("gym-play1")

class TestAngleFinder(unittest.TestCase):
    
    def test_quad1(self):
        self.assertAlmostEqual(gymplay.findAngle(2,2),45, places = 1)
    
    def test_quad2(self):
        self.assertAlmostEqual(gymplay.findAngle(-2,1),152.43, places = 1)
    
    def test_quad3(self):
        self.assertAlmostEqual(gymplay.findAngle(-3,-1),198.43, places = 1)
    
    def test_quad4(self):
        self.assertAlmostEqual(gymplay.findAngle(1,-2),296.54, places = 1)
        
if __name__ == '__main__':
   unittest.main()