; Class: Unit Conversion
; A NCL script that converts the units of temperature data and outputs an updated NetCDF file.
;
; Attributes:
;
;     filename - The name of the NetCDF file to plot.
;     outunit - The unit to convert the data to.


begin

; Function: Add File
; Opens the file for converting and returns the metadata.
;
; Parameters:
;
;     filename - The filename of the NetCDF file.
;
; Returns:
;
;     The metadata of the corresponding NetCDF file.

    f = addfile(filename,"r")
    variable = f@MainVariable

    if (.not. isfilevar(f, variable)) then
        status_exit(5)
    end if

    var = f->$variable$

    if (.not.isvar("unit")) then
        status_exit(2)
    end if

    if (unit.ne."degC" .and. unit.ne."degF" .and. unit.ne."degK") then
        status_exit(5)
    end if

    vunits = str_get_field(var@units,1," ")
    if (vunits.ne."degC" .and. vunits.ne."degF" .and. vunits.ne."degK") then
        if (vunits.ne."C" .and. vunits.ne."F" .and. vunits.ne."K") then
		if (vunits.ne."C " .and. vunits.ne."F " .and. vunits.ne."K ") then
            		status_exit(5)
		end if
        end if
    end if

; Function: Unit Conversion
; Converts temperature data between Celcius, Fahrenheit, and Kelvin and creates an output NetCDF file in the corresponding workflow folder.
;
; Parameters:
;
;     outunit - The unit to convert the data to.
;     wid - The workflow id, passed from the python task.
;     tid - The task id, passed from the python task.
;
; Returns:
;
;     An updated NetCDF file in the workflow folder with the name tid_unitconv.nc. The metadata of the output file contains the new unit.

    if (vunits.ne.unit) then
        if (vunits.eq."degC" .or. vunits.eq."C" .or. vunits.eq."C ") then
            if (unit.eq."degF") then
                var = (var * (9./5.)) + 32
                var@units = "degF"
            else
                var = var + 273.15
                var@units = "degK"
            end if
        else if (vunits.eq."degF" .or. vunits.eq."F" .or. vunits.eq."F ")then
            if (unit.eq."degC") then
                var = ((var - 32) * (5./9.))
                var@units = "degC"
            else
                var = ((var - 32) * (5./9.)) + 273.15
                var@units = "degK"
            end if
        else
            if (unit.eq."degC") then
                var = var - 273.15
                var@units = "degC"
            else
                var = ((var - 273.15) * (9./5.)) + 32
                var@units = "degF"
            end if
        end if
        end if
    end if

    ;Check if workflow directory exists, if not create one
    directory = "data/" + wid + "/"
    echo = systemfunc("[ -d " + directory + " ] && echo 'found' || echo 'notfound'")
    if (echo .eq. "notfound") then
        system("mkdir " + directory)
    end if

    ;Uniquely name output file by task id
    filename_out = directory + tid + "_unitconv.nc"
    if(isfilepresent(filename_out)) then
        system("rm -rf " + filename_out)
    end if
    
    fout = addfile(filename_out,"c")
    
    ; copy global attributes
    att_names = getvaratts(f)
    
    do i = 0, dimsizes(att_names)-1
        fout@$att_names(i)$ = f@$att_names(i)$
    end do
    fout@MainVariable = variable
    
    ; copy over other variables
    var_names = getfilevarnames(f)

    do i = 0,dimsizes(var_names) -1
        if (var_names(i) .eq. variable) then
            continue
        end if

        fout->$var_names(i)$ = f->$var_names(i)$
    end do

    fout->$variable$ = var
end
