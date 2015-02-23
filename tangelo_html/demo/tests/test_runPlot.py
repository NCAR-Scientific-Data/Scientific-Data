import sys
import unittest
sys.path.insert(0,'/usr/local/CUProject/Scientific-Data/tangelo_html/demo/python')
import runPlot

class TestPlot(unittest.TestCase):
    def setUp(self):
        self.aggregateFile = "tmin_aggregate_monthly.nc"
        self.goodPlot = { "image": "tmin_latlon.png" }
    def testPlot(self):
        plot = runPlot.run(self.aggregateFile, 1, False)
        self.assertEqual(plot, self.goodPlot)
    def testNoTimeIndex(self):
        noIndex = runPlot.run(self.aggregateFile, '', False)
        self.assertEqual(noIndex, self.goodPlot)
    def testNativeFails(self):
        nativeFail = runPlot.run(self.aggregateFile, 1, True)
        self.assertNotEqual(nativeFail,self.goodPlot)

if __name__ == '__main__':
        unittest.main()
