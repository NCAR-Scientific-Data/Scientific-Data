;Inputs
;filename
;variable
;unit

begin
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
    end if

    vunits = str_get_field(var@units,1," ")
    if (vunits.ne."degC" .and. vunits.ne."degF" .and. vunits.ne."degK") then
        if (unit.ne."C" .and. unit.ne."F" .and. unit.ne."K") then
            status_exit(5)
        end if
    end if

    if (vunits.ne.unit) then
        if (vunits.eq."degC" .or. vunits.eq."C") then
            if (unit.eq."degF") then
                var = (var * (9./5.)) + 32
                var@units = "degF"
            else
                var = var + 273.15
                var@units = "degK"
            end if
        else if (vunits.eq."degF" .or. vunits.eq."F")then
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