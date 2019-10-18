import unittest
import common

class TestAngleFinder(unittest.TestCase):

    def setUp(self):
        self.state = common.AgentState()
    
    def test_quad1(self):
        self.assertAlmostEqual(self.state.findAngle(2,2),45, places = 1)
    
    def test_quad2(self):
        self.assertAlmostEqual(self.state.findAngle(-2,1),152.43, places = 1)
    
    def test_quad3(self):
        self.assertAlmostEqual(self.state.findAngle(-3,-1),198.43, places = 1)
    
    def test_quad4(self):
        self.assertAlmostEqual(self.state.findAngle(1,-2),296.54, places = 1)
        
if __name__ == '__main__':
   unittest.main()