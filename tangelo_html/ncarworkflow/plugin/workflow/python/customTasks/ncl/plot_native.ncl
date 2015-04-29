; Class: Plot Native
; A NCL script that plots data using the data's native projection.
;
; Attributes:
;
;     filename - The name of the NetCDF file to plot.
;     timeindex - The time index of which to plot.

begin

; Function: Add file
; Opens the file for plotting and returns the metadata.
;
; Parameters:
;
;     filename - The filename of the NetCDF file.
;
; Returns:
;
;     The metadata of the corresponding NetCDF file.

  f        = addfile(filename,"r")
  variable = f@MainVariable

;---Read some data off the file, including map projection information.
  varname  = f->$variable$
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
    status_exit(5)
  end if

  ; Function: Natvie Plot
  ; Plots the data using the data's native projection.
  ;
  ; Parameters:
  ;
  ;     timeindex - The timeindex of which to plot.
  ;     wid - The workflow id, passed from the python task.
  ;     tid - The task id, passed from the python task.
  ; Returns:
  ;
  ;     The .png image of the plot.

  ;Check if workflow directory exists, if not create one
  directory = "data/" + wid + "/"
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
