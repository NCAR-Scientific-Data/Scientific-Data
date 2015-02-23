import unittest
import sys
sys.path.insert(1,'/usr/local/CUProject/Scientific-Data/tangelo_html/demo/tests')
import test_runSubset
import test_runAggregate
import test_runPlot

loader = unittest.TestLoader()

suite = loader.loadTestsFromModule(test_runSubset)
suite.addTests(loader.loadTestsFromModule(test_runAggregate))
suite.addTests(loader.loadTestsFromModule(test_runPlot))

runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(suite)
