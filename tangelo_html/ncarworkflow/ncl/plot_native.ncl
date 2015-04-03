;----------------------------------------------------------------------
; narccap_plot_tmin_native.ncl
;
;  1. Opens a NARR NetCDF file
;  2. Reads "tmin" off the file
;  3. Plots "tmin" for the first time step, using native map 
;     projection defined on file.
;----------------------------------------------------------------------

begin
  f        = addfile(filename,"r")

;---Read some data off the file, including map projection information.
  varname       = f->$variable$
  proj     = f->polar_stereographic
  lat2d    = f->lat
  lon2d    = f->lon
  pname    = varname@grid_mapping

  dims = dimsizes(varname)
  ntime = dims(0)        ; Leftmost dimension is "time"
  nlat  = dims(1)
  nlon  = dims(2)

  nt = timeindex    ; which time index to plot
  if (nt .ge. ntime ) then
    print("Error: Time index out of range.")
    exit
  end if

  ;Check if workflow directory exists, if not create one
  directory = "/data/" + wid + "/"
  echo = systemfunc("[ -d " + directory + " ] && echo 'found' || echo 'notfound'")
  if (echo .eq. "notfound") then
      system("mkdir " + directory)
  end if
  
  ;Uniquely name output file by task id
  filename_out = directory + tid + "_nativeplot"
  if(isfilepresent(filename_out)) then
    system("rm -rf " + filename_out)
  end if

;---The graphics section
  wks = gsn_open_wks("png",filename_out)          
    
  res                   = True

  res@gsnMaximize       = True         ; maximize plot in frame

  res@gsnAddCyclic      = False        ; regional data
  
  res@cnFillOn          = True         ; turn on color
  res@mpFillOn          = False        ; turn off map fill
;  
; These next 8 resources necessary for plotting tmin 
; in its native projection.
;
  res@tfDoNDCOverlay    = True         ; important for native projection

  res@mpProjection      = "Stereographic"
  res@mpCenterLonF      = proj@straight_vertical_longitude_from_pole - 360
  res@mpCenterLatF      = proj@latitude_of_projection_origin

  res@mpLimitMode       = "Corners"
  res@mpLeftCornerLatF  = lat2d(0,0)             ; SW corner
  res@mpLeftCornerLonF  = lon2d(0,0)
  res@mpRightCornerLatF = lat2d(nlat-1,nlon-1)   ; NE corner
  res@mpRightCornerLonF = lon2d(nlat-1,nlon-1)

  res@tiMainString      = filename + " (nt=" + nt + ")"

  res@pmTickMarkDisplayMode = "Always"    ; add tickmarks and labels

  plot = gsn_csm_contour_map(wks,varname(nt,:,:),res) 
end
