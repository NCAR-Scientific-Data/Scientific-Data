load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"

begin
  f = addfile(filename, "r")
  var = f->$variable$

  dimx = dimsizes(var)
  print(dimx)
  ntim = dimx(0)

  nmos  = 12
  modCheck ("clmMonTLL", ntim, nmos)   ; error check
      
  nlat = dimx(1)
  mlon = dimx(2)
;
; Compute all 12 monthly averages first. 
;
   aveMonth = new((/nmos,nlat,mlon/),typeof(var),getFillValue(var))

   do nmo=0,nmos-1
      aveMonth(nmo,:,:) = dim_avg_n( var(nmo:ntim-1:nmos,:,:), 0 )
   end do

; copy attributes and add a couple of informational attributes
; only need to do this if plotting or writing to netCDF file

   copy_VarAtts (var,aveMonth)
   aveMonth@time_op_ncl = "Climatology: "+ (ntim/nmos) +" years"
   aveMonth@info    = "function clmMonLLT: contributed.ncl"

; copy spatial (eg, lat/lon) coordinate variables

   do i=1,2
      if (.not.ismissing(var!i)) then
          aveMonth!i = var!i
          if (iscoord(var,var!i)) then
              aveMonth&$aveMonth!i$ = var&$var!i$
          end if
      end if
   end  do

   aveMonth!0     = "month"           ; create a "month" named dim
   aveMonth&month = ispan(0,nmos-1,1) ; create a month coord var

   return (aveMonth)
end