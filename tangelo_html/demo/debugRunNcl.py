import sys
sys.path.insert(0,'/usr/local/CUProject/Scientific-Data/tangelo_html/demo/python')
import runAggregate
import runSubset
import runPlot

def main():
   subset =  runSubset.run("tmin.CRCM.ncep.dayavg.native.nc",37.5,255.0,45.0,265.0,"1990-10-29","2000-04-17")
   subsetFile = subset["subset"]
   print subsetFile
   #aggregate = runAggregate.run(subsetFile,'month', 'mean', 'start')
   #aggregateFile = aggregate["result"]
   #print aggregateFile
   #plot = runPlot.run("../tmin.CRCM.ncep.dayavg.native.nc",1,True)
  # print plot

if __name__ == "__main__":
     main()
