;----------------------------------------------------------------------
; narccap_plot_tmin_latlon.ncl
;
;  1. Opens a NARR NetCDF file
;  2. Reads "tmin" off the file
;  3. Plots "tmin" for the first time step, using lat/lon projection.
;----------------------------------------------------------------------

begin
  f        = addfile(filename,"r")

  if (.not. isfilevar(f, variable)) then
    status_exit(5)
  end if
;---Read some data off the file, including map projection information.
  varname       = f->$variable$
  varname@lat2d = f->lat
  varname@lon2d = f->lon

  dims = dimsizes(varname)
  ntime = dims(0)        ; Leftmost dimension is "time")

  nt = timeindex    ; which time index to plot

  if (nt .ge. ntime ) then
    status_exit(5)
  end if

;---The graphics section
  ;Check if workflow directory exists, if not create one
  directory = "/data/" + wid + "/"
  echo = systemfunc("[ -d " + directory + " ] && echo 'found' || echo 'notfound'")
  if (echo .eq. "notfound") then
      system("mkdir " + directory)
  end if

  ;Uniquely name output file by task id
  filename_out = directory + tid + "_plot"
  if(isfilepresent(filename_out)) then
    system("rm -rf " + filename_out)
  end if

  wks = gsn_open_wks("png",filename_out)    ; "png", "x11", "ps", "pdf"
    
  res                      = True

  res@gsnAddCyclic         = False           ; regional data
  
  res@cnFillOn             = True            ; turn on color contours
  res@mpFillOn             = False           ; turn off map fill
  
  res@mpMinLatF            = min(varname@lat2d)      ; range to zoom in on
  res@mpMaxLatF            = max(varname@lat2d)
  res@mpMinLonF            = min(varname@lon2d)
  res@mpMaxLonF            = max(varname@lon2d)
    
  res@tiMainString = filename + " (nt=" + nt + ")"

  plot = gsn_csm_contour_map(wks,varname(nt,:,:),res) 
end
