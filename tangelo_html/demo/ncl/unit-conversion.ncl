;Inputs
;filename
;variable
;outunit

begin
    f = addfile(filename,"r")

    if (.not.isvar("variable")) then
        print("fatal: Please specify variable for conversion.")
        exit
    end if
    var = f->$variable$

    if (.not.isvar("outunit")) then
        print("fatal: Please specify variable from unit.")
        exit
    end if
    if (outunit.ne."degC" .and. outunit.ne."degF" .and. outunit.ne."degK") then
        print("fatal: Units must be either celcius, fahrenheit, or kelvin")
        exit
    end if

    vunits = str_get_field(var@units,1," ")
    if (vunits.ne."degC" .and. vunits.ne."degF" .and. vunits.ne."degK") then
        print("fatal: Conversion from variable unit not supported.")
        exit
    end if

    if (vunits.ne.outunit) then
        if (vunits.eq."degC") then
            if (outunit.eq."degF") then
                var = var * 9 / 5 + 32
                var@units = "degF"
            else
                var = var + 273.15
                var@units = "degK"
            end if
        else if (vunits.eq."degF")then
            if (outunit.eq."degC") then
                var = var - 32 * 5 / 9
                var@units = "degC"
            else
                var = var - 32 * 5 / 9 + 273.15
                var@units = "degK"
            end if
        else
            if (outunit.eq."degC") then
                var = var - 273.15
                var@units = "degC"
            else
                var = var - 273.15 * 9 / 5 + 32
                var@units = "degF"
            end if
        end if
        end if
    end if

    outfile = "conversion_subset.nc"

    if(isfilepresent(outfile)) then
        system("rm -rf "+outfile)
    end if

    fout = addfile(outfile,"c")
    
    att_names = getvaratts(f)
    
    do i = 0, dimsizes(att_names)-1
        fout@$att_names(i)$ = f@$att_names(i)$
    end do

    var_names = getfilevarnames(f)

    do i = 0,dimsizes(var_names) -1
        if (var_names(i) .eq. variable) then
            continue
        end if

        fout->$var_names(i)$ = f->$var_names(i)$
    end do

    fout->$variable$ = var
end