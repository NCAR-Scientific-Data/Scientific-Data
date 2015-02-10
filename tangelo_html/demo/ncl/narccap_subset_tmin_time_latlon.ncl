;----------------------------------------------------------------------
; narccap_subset_tmin_time_latlon.ncl
;
; This script is a combination of the two scripts:
;    narccap_subset_tmin_time.ncl
;    narccap_subset_tmin_latlon.ncl
;
;  It subsets "tmin" across both time and a lat/lon box.
;
;   1. Opens a NARR NetCDF file.
;   2. Reads tmin, lat, lon off the file.
;   3. Subsets all three variables based on a time range and
;      a lat/lon rectangle.
;   4. Writes subsetted data to a new NetCDF file.
;----------------------------------------------------------------------

begin
  ;dir      = "/glade/p/image/narccap/summaries/daily/"
  ;filename = "tmin.CRCM.ncep.dayavg.native.nc"
  f        = addfile(filename,"r")

;---Read tmin, lat, lon off the file
  tmin  = f->tmin             ; 8766 x 115 x 140 (time x lat x lon)
  lat2d = f->lat              ; 115 x 140
  lon2d = f->lon              ; 115 x 140

  printVarSummary(tmin)       ; Print some info about "tmin"
  printMinMax(tmin,0)

;---Convert "time" array into something we can more easily understand.
  opt      = 0
  new_time = cd_calendar(tmin&time,opt)    ; ntime x 6

;---SW and NE corners of a lat/lon area of interest.
  sw_lat =  swLat    
  sw_lon = swLon
  ne_lat =  neLat
  ne_lon = neLon

;---Start and end year of interest (Jan 1 SY to Dec 31 EY)
  start_year  = startYear
  end_year    = endYear

;---Call function to get indexes closest to the SW and NE corners
  ii_sw = getind_latlon2d (lat2d, lon2d, sw_lat, sw_lon)
  ii_ne = getind_latlon2d (lat2d, lon2d, ne_lat, ne_lon)

;---Call function to get year range of interest
  years   = new_time(:,0)
  ii_time = ind(years.ge.start_year.and.years.le.end_year)

;---Subset the variables with calculated indexes
  tmin_sub =  tmin(ii_time,ii_sw(0,0):ii_ne(0,0),ii_sw(0,1):ii_ne(0,1))
  lat_sub  = lat2d(        ii_sw(0,0):ii_ne(0,0),ii_sw(0,1):ii_ne(0,1))
  lon_sub  = lon2d(        ii_sw(0,0):ii_ne(0,0),ii_sw(0,1):ii_ne(0,1))

  printVarSummary(tmin_sub)    ; Note metadata still attached
  printMinMax(tmin_sub,0)

;----------------------------------------------------------------------
; Write subsetted data to a file, using inefficient (lazy) method.
;----------------------------------------------------------------------

;---Remove file first, if it exists.
  filename_out = "tmin_subset_time_latlon.nc"
  if(isfilepresent(filename_out)) then
    system("rm -rf " + filename_out)
  end if

;---Open NetCDF file to write to.
  fout = addfile(filename_out,"c")

;---Write three variables to file. Metadata will be written automatically.
  fout->tmin = tmin_sub
  fout->lat  = lat_sub
  fout->lon  = lon_sub
  time_bnd = fout->time
  delete(time_bnd@bounds)
;----------------------------------------------------------------------
; When script is finished, type:
;
;  ncl_filedump tmin_subset_time_latlon.nc
;
; Note that some of the metadata (like "actual_range") may
; be incorrect. This script should be updated to fix this.
;----------------------------------------------------------------------
end
