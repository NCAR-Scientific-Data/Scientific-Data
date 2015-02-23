import sys
#sys.path.insert(0,'/usr/local/CUProject/Scientific-Data/tangelo_html/demo/python')
sys.path.insert(0,'C:/Users/Hannah/Documents/Scientific-Data/tangelo_html/demo/python')
import runAggregate
import runSubset
import runPlot

def main():
   """
   #try:
   subset =  runSubset.run("tmin.CRCM.ncep.dayavg.native.nc","tmin",37.5,255.0,45.0,265.0,"\"1990-10-29\"","\"2000-01-17\"")
   subsetFile = subset["subset"]   
   except KeyError as e:
      print "Problem with subset key: Key {0}".format(e)
   except OSError as e:
      print "Problem executing process: Error {0}".format(e.strerror)
   except ValueError as e:
      print "Process called with invalid options: Error {0} - {1}".format(e.errno,e.strerror)
   except:
      print "Unexpected error:", sys.exc_info()[0]

   aggregate = runAggregate.run("tmin_subset_time_latlon.nc",'month','', '')
   print aggregate
   aggregateFile = aggregate["result"]
   print aggregateFile
   """
   plot = runPlot.run("tmin_aggregate_monthly.nc",1,False)
   print plot
  
if __name__ == "__main__":
     main()
