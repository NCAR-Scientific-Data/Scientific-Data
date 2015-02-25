import unittest
import sys
sys.path.insert(1,'/usr/local/CUProject/Scientific-Data/tangelo_html/demo/python')
import runCalculation

class TestAggregate(unittest.TestCase):
    def setUp(self):
        self.subsetFile = "tmin_subset_time_latlon.nc"
        self.goodAggregate = { "result" : "tmin_aggregate_monthly.nc" }
    def testAggregate(self):
        aggregate = runCalculation.run(self.subsetFile, 'month','mean','start')
        self.assertEqual(aggregate, self.goodAggregate)
    def testAggregateError(self):
        badAggregate = runCalculation.run(self.subsetFile, 'moth', 'mean','start')
        self.assertNotEqual(badAggregate, self.goodAggregate)
    def testNoMethod(self):
        noMethod = runCalculation.run(self.subsetFile, 'month','', 'start')
        self.assertEqual(noMethod, self.goodAggregate)
    def testNoOuttime(self):
        noOuttime = runCalculation.run(self.subsetFile, 'month', 'mean', '')
        self.assertEqual(noOuttime, self.goodAggregate)
    def testNoMethodOut(self):
        noMethodOut = runCalculation.run(self.subsetFile, 'month', '', '')
        self.assertEqual(noMethodOut, self.goodAggregate)

if __name__ == '__main__':
        unittest.main()
