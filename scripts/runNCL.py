import subprocess

def runNCL():
    status = subprocess.call(["ncl", "narccap_subset_tmin_time_latlon.ncl"])
    if status < 0:
        print "Error running ncl"
    else:
        print "Success"
