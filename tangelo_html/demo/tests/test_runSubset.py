import unittest
import sys
sys.path.insert(0,'/usr/local/CUProject/Scientific-Data/tangelo_html/demo/python')
import runSubset

class TestSubset(unittest.TestCase):            
	def setUp(self):
                self.testSubset = { "subset": "tmin_subset_time_latlon.nc" }
	def testSubset(self):
                goodSubset = runSubset.run("tmin.CRCM.ncep.dayavg.native.nc","tmin",37.5,255.0,45.0,265.0,"\"1990-10-29\"","\"2000-04-17\"")
                self.assertEqual(goodSubset,self.testSubset)
        def testSubsetError(self):
                badSubset = runSubset.run("tmin.CRCM.ncep.dayavg.native.nc","tmins",37.5,255.0,45.0,265.0,"\"1990-10-29\"","\"2000-04-17\"")
                self.assertNotEqual(badSubset,self.testSubset)
             
if __name__ == '__main__':
        unittest.main()
