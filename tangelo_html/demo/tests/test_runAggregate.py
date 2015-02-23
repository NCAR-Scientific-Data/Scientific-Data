import unittest
import sys
sys.path.insert(0,'/usr/local/CUProject/Scientific-Data/tangelo_html/demo/python')
import runAggregate

class TestAggregate(unittest.TestCase):
    def setUp(self):
        self.subsetFile = "tmin_subset_time_latlon.nc"
        self.goodAggregate = { "result" : "tmin_aggregate_monthly.nc" }
    def testAggregate(self):
        aggregate = runAggregate.run(self.subsetFile, 'month','mean','start')
        self.assertEqual(aggregate, self.goodAggregate)
    def testAggregateError(self):
        badAggregate = runAggregate.run(self.subsetFile, 'moth', 'mean','start')
        self.assertNotEqual(badAggregate, self.goodAggregate)
    def testNoMethod(self):
        noMethod = runAggregate.run(self.subsetFile, 'month','', 'start')
        self.assertEqual(noMethod, self.goodAggregate)
    def testNoOuttime(self):
        noOuttime = runAggregate.run(self.subsetFile, 'month', 'mean', '')
        self.assertEqual(noOuttime, self.goodAggregate)
    def testNoMethodOut(self):
        noMethodOut = runAggregate.run(self.subsetFile, 'month', '', '')
        self.assertEqual(noMethodOut, self.goodAggregate)

if __name__ == '__main__':
        unittest.main()
