import subprocess
import sys

def run(filename):
	status = subprocess.call(["ncl 'filename=\"{}\"' narccap_plot_tmin_latlon.ncl".format(filename)], shell=True)
	if status < 0:
		print "Error plotting data"
		return { "alert": "Error plotting data" }
        else:
		return { "image": "tmin_latlon.png" }

