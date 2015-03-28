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
;---Get NetCDF file
  f        = addfile(filename,"r")

;---Read variable, lat, lon off the file
  varname  = f->$variable$
  lat2d = f->lat
  lon2d = f->lon
  tbnds = f->time_bnds


;---Convert "time" array into something we can more easily understand.
  opt      = -2
  new_time = cd_calendar(varname&time,opt)    ; ntime x 6
  stDate = str_split(startDate, "-")
  edDate = str_split(endDate, "-")
  
;---SW and NE corners of a lat/lon area of interest.
  sw_lat =  swLat    
  sw_lon = swLon
  ne_lat =  neLat
  ne_lon = neLon

;---Start and end date of interest
  start_year  = stringtointeger(stDate(0))
  end_year    = stringtointeger(edDate(0))
  start_month = stringtointeger(stDate(1))
  end_month   = stringtointeger(edDate(1))
  start_day   = stringtointeger(stDate(2))
  end_day     = stringtointeger(edDate(2))
  
  startTime = start_year*100 + start_month
  startTime = startTime*100 + start_day
  endTime   = end_year*100 + end_month
  endTime   = endTime*100 + end_day

;---Call function to get indexes closest to the SW and NE corners
  ii_sw = getind_latlon2d (lat2d, lon2d, sw_lat, sw_lon)
  ii_ne = getind_latlon2d (lat2d, lon2d, ne_lat, ne_lon)

;---Call function to get date range of interest
 
  ii_time = ind(new_time.ge.startTime.and.new_time.le.endTime)

;---Subset the variables with calculated indexes
  var_sub =  varname(ii_time,ii_sw(0,0):ii_ne(0,0),ii_sw(0,1):ii_ne(0,1))
  lat_sub  = lat2d(        ii_sw(0,0):ii_ne(0,0),ii_sw(0,1):ii_ne(0,1))
  lon_sub  = lon2d(        ii_sw(0,0):ii_ne(0,0),ii_sw(0,1):ii_ne(0,1))
  tb_sub   = tbnds(ii_time,:)
;----------------------------------------------------------------------
; Write subsetted data to a file, using inefficient (lazy) method.
;----------------------------------------------------------------------

;---Remove file first, if it exists.
  directory = "/data/" + wid + "/"
  echo = systemfunc("[ -d " + directory + " ] && echo 'found' || echo 'notfound'")
  if (echo .eq. "notfound") then
    system("mkdir " + directory)
  end if

  filename_out = directory + tid + "_subset.nc"
  if(isfilepresent(filename_out)) then
    system("rm -rf " + filename_out)
  end if

;---Open NetCDF file to write to.
  fout = addfile(filename_out,"c")
  att_names = getvaratts(f)
  do i=0, dimsizes(att_names)-1
    fout@$att_names(i)$ = f@$att_names(i)$
  end do

  var_names = getfilevarnames(f)

  do i=0, dimsizes(var_names)-1
    if (var_names(i) .eq. "lat") then continue end if
    if (var_names(i) .eq. "lon") then continue end if
    if (var_names(i) .eq. "time") then continue end if
    if (var_names(i) .eq. "xc") then continue end if
    if (var_names(i) .eq. "yc") then continue end if
    if (var_names(i) .eq. "time_bnds") then continue end if
    if (var_names(i) .eq. variable) then continue end if
    fout->$var_names(i)$ = f->$var_names(i)$
  end do


;---Write three variables to file. Metadata will be written automatically.
  fout->$variable$ = var_sub
  fout->lat  = lat_sub
  fout->lon  = lon_sub
  ;fout->time = time
  fout->time_bnds = tb_sub
  ;delete(time_bnd@bounds)
;----------------------------------------------------------------------
; When script is finished, type:
;
;  ncl_filedump tmin_subset_time_latlon.nc
;
; Note that some of the metadata (like "actual_range") may
; be incorrect. This script should be updated to fix this.
;----------------------------------------------------------------------
end