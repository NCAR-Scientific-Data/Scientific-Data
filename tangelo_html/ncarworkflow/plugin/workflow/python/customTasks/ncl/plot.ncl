; Class: Plot
; A NCL script that plots data using a standard projection.
;
; Attributes:
;
;     filename - The name of the NetCDF file to plot.
;     timeindex - The time index of which to plot.

begin

; Function: Add File
; Opens the file for plotting and returns the metadata.
;
; Parameters:
;
;       filename - The filename of the NetCDF file.
;
; Returns:
;
;       The metadata of the corresponding NetCDF file.

  f        = addfile(filename,"r")
  variable = f@MainVariable
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

; Function: Plot
; Plots the data using a standard projection.
;
; Parameters:
;
;     timeindex - The timeindex of which to plot.
;     wid - The workflow id, passed from the python task.
;     tid - The task id, passed from the python task.
;
; Returns:
;
;     The .png image of the plot.

;---The graphics section
  ;Check if workflow directory exists, if not create one
  directory = "data/" + wid + "/"
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
