; Class: Subset
; A NCL script that uses OPeNDAP to pull NARCCAP data, subset, and output a subsetted NetCDF file.
;
; Attributes:
;
;     filename - The OPeNDAP url for the netCDF file to subset.
;     variable - The variable to subset
;     swlat - The southwest latitude coordinate of the bounding box to subset.
;     swlon - The southwest longitude coordinate of the bounding box to subset.
;     nelat - The northeast latitude coordinate of the bounding box to subset.
;     nelon - The northeast longitude coordinate of the bounding box to subset.
;     startdate - The beginning date to subset data over.
;     enddate - The final date to subset data over.

begin

; Function: Add File
; Calls the OPeNDAP url and returns the file metadata
;
; Parameters:
;
;      filename - the OPeNDAP url for file to pull data form
;
; Returns:
;
;       The metadata of the corresponding NetCDF file.

  f        = addfile(filename, "r")

;---Read variable, lat, lon off the file
  if (.not. isfilevar(f, variable)) then
    status_exit(5)
  end if

  lat2d = f->lat
  lon2d = f->lon
  tbnds = f->time_bnds

; Function: Initial US Subset
; Initially subsets data to US in order to meet the NARCCAP download size limit
; 
; Parameters:
;
;       lat2d - the latitude array pulled from the NetCDF file.
;       lon2d - the longitude array pulled from the NetCDF file.
;       variable - the variable of the file
;
; Returns:
;
;       varname - the main variable subsetted to the US

  sw = getind_latlon2d (lat2d, lon2d, 24, 246)
  ne = getind_latlon2d (lat2d, lon2d, 44, 286)
;  varname = f->$variable$(:,sw(0,0):ne(0,0),sw(0,1):ne(0,1))

;---Convert "time" array into something we can more easily understand.
  opt      = -2
  new_time = cd_calendar(f->$variable$&time,opt)    ; ntime x 6
  stDate = str_split(startDate, "-")
  edDate = str_split(endDate, "-")

  latmin = min(lat2d)
  latmax = max(lat2d)
  lonmin = min(lon2d)
  lonmax = max(lon2d)

  if (swLat .lt. latmin .or. swLat .gt. latmax .or. neLat .lt. latmin .or. neLat .gt. latmax) then
    status_exit(3)
  else if (swLon .lt. lonmin .or. swLon .gt. lonmax .or. neLon .lt. lonmin .or. neLon .gt. lonmax) then
    status_exit(3)
  end if
  end if

; Function: Subset Data
; Uses the time range selected by the user to further subset the NetCDF file.
;
; Parameters:
;     swlat - The southwest latitude coordinate of the bounding box to subset.
;     swlon - The southwest longitude coordinate of the bounding box to subset.
;     nelat - The northeast latitude coordinate of the bounding box to subset.
;     nelon - The northeast longitude coordinate of the bounding box to subset.
;     startdate - The beginning date to subset data over.
;     enddate - The final date to subset data over.
;
; Returns:
;
;     The variable array subsetted by the input time and boundaries.


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

  if (startTime .lt. min(new_time) .or. startTime .gt. max(new_time) .or. endTime .lt. min(new_time) .or. endTime .gt. max(new_time)) then
    status_exit(4)
  end if

;---Call function to get indexes closest to the SW and NE corners
  ii_sw = getind_latlon2d (lat2d, lon2d, swLat, swLon)
  ii_ne = getind_latlon2d (lat2d, lon2d, neLat, neLon)

;---Call function to get date range of interest
 
  ii_time = ind(new_time.ge.startTime.and.new_time.le.endTime)

;---Subset the variables with calculated indexes
  var_sub =  f->$variable$(ii_time,ii_sw(0,0):ii_ne(0,0),ii_sw(0,1):ii_ne(0,1))
  lat_sub  = lat2d(        ii_sw(0,0):ii_ne(0,0),ii_sw(0,1):ii_ne(0,1))
  lon_sub  = lon2d(        ii_sw(0,0):ii_ne(0,0),ii_sw(0,1):ii_ne(0,1))
  tb_sub   = tbnds(ii_time,:)


; Function: Output Subset
; Creates the output NetCDF file in the corresponding workflow folder.
;
; Parameters:
;
;     wid - The workflow id, passed from the python task.
;     tid - The task id, passed from the python task.
;
; Returns:
;
;      A subset NetCDF file in the workflow folder with the name tid_subset.nc. The subsetted file contains a new attribute with the variable being analyzed.

;---Remove file first, if it exists.
  ; Check if workflow directory exists, if not create one
  directory = "data/" + wid + "/"
  echo = systemfunc("[ -d " + directory + " ] && echo 'found' || echo 'notfound'")
  if (echo .eq. "notfound") then
    system("mkdir " + directory)
  end if

  ; Uniquely name output file by task id
  filename_out = directory + tid + "_subset.nc"
  if(isfilepresent(filename_out)) then
    system("rm -rf " + filename_out)
  end if

;---Open NetCDF file to write to.
  fout = addfile(filename_out,"c")
  print("----------------------------------------")
  print(fout)
  att_names = getvaratts(f)
  do i=0, dimsizes(att_names)-1
    fout@$att_names(i)$ = f@$att_names(i)$
  end do
  fout@MainVariable = variable
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
  fout->time_bnds = tb_sub
end
