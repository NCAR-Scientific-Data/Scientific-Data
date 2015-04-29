;; Template
;; A template for writing NCL analysis scripts
;;
;; Attributes
;;
;;     filename
;;     input1 
;;	   input2

begin
; Read variable off the file
f        = addfile(filename, "r")

if (.not. isfilevar(f, variable)) then
    status_exit(5)
end if

; Read variables needed for the calculations
varname1 = f->$input1$
varname2 = f->$input2$

;--------------------------------------------
; Calculations
;--------------------------------------------

; Check if the workflow folder has been created already, it not create one and name it the unique wid.
directory = "data/" + wid + "/"
echo = systemfunc("[ -d " + directory + " ] && echo 'found' || echo 'notfound'")
if (echo .eq. "notfound") then
    system("mkdir " + directory)
end if

; Uniquely name output file by task id and task name
filename_out = directory + tid + "_task.nc"
if(isfilepresent(filename_out)) then
    system("rm -rf " + filename_out)
end if

; Open NetCDF file to write to.
fout = addfile(filename_out,"c")
; Copy the file attributes from the original file
att_names = getvaratts(f)
do i=0, dimsizes(att_names)-1
  fout@$att_names(i)$ = f@$att_names(i)$
end do

; Create an attribute called MainVariable to cascade the variable throughout the workflow.
fout@MainVariable = variable

; Get the original variables.
var_names = getfilevarnames(f)

; Skip over the variables that have been updated.
do i=0, dimsizes(var_names)-1
  if (var_names(i) .eq. input1) then continue end if
  if (var_names(i) .eq. input2) then continue end if
  fout->$var_names(i)$ = f->$var_names(i)$
end do

; Write the updated variables to the output file. Metadata will be written automatically.
  fout->$input1$ = varname1
  fout->$input1$ = varname1
end