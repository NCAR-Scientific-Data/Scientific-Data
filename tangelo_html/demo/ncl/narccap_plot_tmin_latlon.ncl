;----------------------------------------------------------------------
; narccap_plot_tmin_latlon.ncl
;
;  1. Opens a NARR NetCDF file
;  2. Reads "tmin" off the file
;  3. Plots "tmin" for the first time step, using lat/lon projection.
;----------------------------------------------------------------------

begin
  f        = addfile(filename,"r")

;---Read some data off the file, including map projection information.
  tm       = f->tmin
  tm@lat2d = f->lat
  tm@lon2d = f->lon

  dims = dimsizes(tm)
  ntime = dims(0)        ; Leftmost dimension is "time")
  print("tmin has " + ntime + " time steps.")

  nt = timeindex    ; which time index to plot

;---The graphics section
  directory = "/data/" + wid + "/"
  echo = systemfunc("[ -d " + directory + " ] && echo 'found' || echo 'notfound'")
  if (echo .eq. "notfound") then
      system("mkdir " + directory)
  end if

  filename_out = directory + tid + "_plot"
  if(isfilepresent(filename_out)) then
    system("rm -rf " + filename_out)
  end if

  wks = gsn_open_wks("png",filename_out)    ; "png", "x11", "ps", "pdf"
    
  res                      = True

  res@gsnAddCyclic         = False           ; regional data
  
  res@cnFillOn             = True            ; turn on color contours
  res@mpFillOn             = False           ; turn off map fill
  
  res@mpMinLatF            = min(tm@lat2d)      ; range to zoom in on
  res@mpMaxLatF            = max(tm@lat2d)
  res@mpMinLonF            = min(tm@lon2d)
  res@mpMaxLonF            = max(tm@lon2d)
    
  res@tiMainString = filename + " (nt=" + nt + ")"

  plot = gsn_csm_contour_map(wks,tm(nt,:,:),res) 
end
