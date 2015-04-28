import subprocess
import sys

def run():
    args = ['ncl', 'filename=\"tmin_aggregate_monthly.nc\"', '../tangelo_html/demo/ncl/narccap_plot_tmin_native.ncl']
    p = subprocess.Popen(args)

if __name__ == "__main__":
    run()
