import runAggregate
import runSubset
import runPlot

def main():
   #subset =  runSubset.run("",37.5,255.0,45.0,265.0,1990,2000)
   #subsetFile = subset["subset"]
   #print subsetFile
   #aggregate = runAggregate.run(subsetFile,'month', 'mean', 'start')
   #aggregateFile = aggregate["result"]
   #print aggregateFile
   plot = runPlot.run("../tmin_aggregate_monthly.nc",1,True)
   print plot

if __name__ == "__main__":
     main()
