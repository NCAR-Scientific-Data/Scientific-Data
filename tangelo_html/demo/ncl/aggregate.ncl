;;; Aggregates 3-hourly NARCCAP data to averages over daily and longer periods

load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/contrib/ut_string.ncl"


;; This stuff is localized into functions so that seasons or their
;; ordering can be redefined.  Functions could be rewritten to take an
;; optional argument for whether you wanted monsoons, etc.  May move
;; into a separate file at some point.

function getnames(interval)
begin
  if (interval .eq. "season") then
    return((/"error","DJF","MAM","JJA","SON"/))
  end if
  if (interval .eq. "month") then
    return((/"error","Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"/))
  end if
  return("getnames() error: unrecognized interval")
end


function mon2seas(month:numeric)
local season
begin
  season = new(dimsizes(month),"integer")
  season = where(month.eq.12 .or. month.eq. 1 .or. month.eq. 2, 1, season)  ;; DJF
  season = where(month.eq. 3 .or. month.eq. 4 .or. month.eq. 5, 2, season)  ;; MAM
  season = where(month.eq. 6 .or. month.eq. 7 .or. month.eq. 8, 3, season)  ;; JJA
  season = where(month.eq. 9 .or. month.eq.10 .or. month.eq.11, 4, season)  ;; SON
  return(season)
end


;;  For converting times to dates

format = "%Y-%N-%D %H:%M:%S"


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;


;; Command-line inputs:
;; filename
;; variable
;; interval: day, month, season, or year (no default)
;; method:  mean, min, max (defaults to mean)
;; outtime: start, mid, end  (defaults to end)
;; cyclic  (boolean option: average over multiple years?)

if (.not. isvar("cyclic")) then
  cyclic = False
end if

if (.not.isvar("outtime")) then
  outtime = "end"
end if
if (outtime.ne."start" .and. outtime.ne."mid" .and. outtime.ne."end") then
  print("Invalid outtime: '"+outtime+"'.  Use start, mid, or end.")
  exit
end if

if (.not.isvar("method")) then
  method = "mean"
end if

if (method.ne."mean" .and. method.ne."min" .and. method.ne."max") then
  print("Invalid method: '"+method+"'.  Use mean, min, or max.")
  exit
end if

if (method .eq. "max") then
  mstring = "maximum"
else if (method .eq. "min") then
    mstring = "minimum"
  else
    mstring = method
  end if
end if

if (.not.isvar("interval")) then
  print("Specify interval: day, month, season, or year")
  exit
end if
if (interval.ne."day" .and. interval.ne."month" .and. interval.ne."season" .and. interval.ne."year") then
  print("Invalid interval: '"+interval+"'.  Use day, month, season, or year.")
  exit
end if

if(cyclic .and. interval .eq. "year") then
  print("Error: annual interval not allowed with cyclic option.")
  ;; actually, this is just averaging over all time.  The only reason to
  ;; disallow it is clarity.  If we add an "all" option, we can make
  ;; this case synonymous with that and implement it with just a
  ;; dim_avg_n shortcut.
  exit
end if

if(cyclic .and. interval .eq. "day") then
  print("Error: day interval not allowed with cyclic option (due to leap days).")
  ;; once NCL v.6.1.0 is readily available, this is actually an
  ;; allowable option.  Use day_of_year() to convert from Y/M/D output
  ;; of cd_calendar to julian day, and just discard day 366 in leap
  ;; years.  (day_of_year doesn't recognize calendars before v.6.1.0)
  exit
end if

fin = addfile(filename, "r")

time = fin->time
nt = dimsizes(time)

if(.not. any(typeof(time).eq.(/"float","double"/))) then
  print("Error: time is not floating-point.")
  exit
end if


;; get or create time@bounds as appropriate

if (isatt(time,"bounds")) then
  tbname = time@bounds
  time_bnds = fin->$tbname$
else
  time_bnds = transpose(onedtond(time,(/2,nt/)))
end if

 
;; Extract month & year using ut_calendar

utc = ut_calendar(time, 0)

year  = floattointeger(utc(:,0))
month = floattointeger(utc(:,1))
day   = floattointeger(utc(:,2))

if(interval .eq. "day") then
  tunits = str_get_field(time@units,1," ")
  if (tunits .eq. "days") then
      jday  = doubletointeger(time)
    else if (tunits .eq. "hours") then
      jday  = doubletointeger(time/24)
    else
      print("Error: don't know how to convert time unit '"+tunits+"'into julian day.")
      exit
    end if
  end if
end if


season = mon2seas(month)
names =  getnames(interval)


;; Construct mapping info:

;; oci == output cell index array

oci = new(nt,"integer")

if (cyclic) then
  ;; climatology - multi-year averages

  if(interval .eq. "month") then 
    nout = dimsizes(names) - 1
    bin = month
  end if

  if (interval .eq. "season") then
    nout = dimsizes(names) - 1
    bin = season   
  end if

  ;; The -1 is because January = month 1 goes in array position time(0), etc.
  do i = 1, nout
    oci(ind(bin .eq. i)) = i-1
  end do

else
  ;; normal (linear/non-cyclic) intervals
  
 if(interval .eq. "day"   ) then bin = jday   end if
 if(interval .eq. "month" ) then bin = month  end if
 if(interval .eq. "season") then bin = season end if
 if(interval .eq. "year"  ) then bin = year   end if
 
 nout = 0
 oci(0) = 0 
 do i = 1, nt-1
   if (bin(i) .ne. bin(i-1)) then
     nout = nout + 1
   end if
   oci(i) = nout
 end do
 nout = nout + 1
end if



;; And now for the actual averaging of data

;; This is a cheap way to get metadata from a non-copied var
outdata = fin->$variable$(0:nout-1,:,:)
outdata(:,:,:) = outdata@_FillValue
odim = dimsizes(outdata)

misscount = new(nout,"integer")
stepcount = new(nout,"integer")
cell_bnds = new((/nout,2/), "double","No_FillValue") ;; will become time_bnds; follows CF rules
date = new (nout, "string")                          ;; plain-text version of output time coordinate


;; so the deletes don't error...
map  = 0
slab = 0 

;; Note that we dodge around reading in fin->$variable$ so that we
;; don't crash in cases where it's too big to fit into memory.

do i=0, nout-1

  delete(map)
  map = ind(oci .eq. i)

  if(dimsizes(map) .eq. 1) then

    ;; A little kludgey.  Probably ought to do something with expected
    ;; of timesteps and a threshold for allowable %missing instead of
    ;; simple yes-no tainting by missing value...

    outdata(i,:,:) = fin->$variable$(map(0):map(0),:,:)
    misscount(i) = num(ismissing(outdata(i,:,:)))
    stepcount(i) = 1
    cell_bnds(i,0) = time_bnds(map(0),0)
    cell_bnds(i,1) = time_bnds(map(0),1)

  else 

    delete(slab)
    slab = fin->$variable$(map,:,:)
  
    if(method.eq."mean") then
      outdata(i,:,:) = dim_avg_n(slab,0)
    end if
    if(method.eq."min") then
      outdata(i,:,:) = dim_min_n(slab,0)
    end if
    if(method.eq."max") then
      outdata(i,:,:) = dim_max_n(slab,0)
    end if
  
    nmap = dimsizes(map)
    misscount(i) = num(ismissing(slab))
    stepcount(i) = nmap
    cell_bnds(i,0) = time_bnds(map(0),0)
    cell_bnds(i,1) = time_bnds(map(nmap-1),1)

  end if

  if(cyclic) then
    date(i) = names(i+1)
  else
    if (interval .eq. "day") then
      date(i) = ""+year(map(0))+"-"+month(map(0))+"-"+day(map(0))
    else 
      if (interval .eq. "year") then
        date(i) = year(map(0))
      else
        date(i) = names(bin(map(0)))+" "+year(map(0))
      end if
    end if
  end if
end do

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;; Done with the actual aggregation.  From here on out, we're just
;; generating output

;; Add appropriate metadata to output variables

delete(time)
delete(time_bnds)

if(outtime.eq."start") then
    time = cell_bnds(:,0)
end if
if(outtime.eq."mid") then
  if(cyclic) then
    if(interval.eq."month") then
      z0 = new(12,"integer")
      mout = ispan(1,12,1)
    end if
    if(interval.eq."season") then
      z0 = new(4,"integer")
      mout = (/1,4,7,10/)
    end if
    z0 = 0
    z0@calendar = fin->time@calendar
    outyear = tointeger((year(0)+year(nt-1))/2)
    time = ut_inv_calendar(z0+outyear,mout,z0+15,z0+12,z0,z0,fin->time@units, z0(0))
  else
    time = cell_bnds(:,1)
    time = (time + cell_bnds(:,0))/2
  end if
end if
if(outtime.eq."end") then
  time = cell_bnds(:,1)
end if
if (cyclic) then
time@climatology = "time_bnds"
else
time@bounds = "time_bnds"
end if
time@axis = "T"
time@calendar = fin->time@calendar
time@units = fin->time@units
time@standard_name = "time"
time@long_name = "time"
time!0 = "time"
time&time = time

time_bnds = cell_bnds
time_bnds!0 = "time"
time_bnds!1 = "bnds"


if (cyclic) then
  cmstring = "time: "+mstring+" within years time: "+mstring+" over years"
else
  cmstring = "time: "+mstring+" (interval: 1 "+interval+"s)"
end if
if (isatt(outdata, "cell_methods")) then
  cmstring = outdata@cell_methods + " " + cmstring
end if
outdata@cell_methods = cmstring


;; Create output file
;;Check if workflow directory exists, if not create one
directory = "/data/" + wid + "/"
echo = systemfunc("[ -d " + directory + " ] && echo 'found' || echo 'notfound'")
if (echo .eq. "notfound") then
  system("mkdir " + directory)
end if

;Uniquely name output file by task id
filename_out = directory + tid + "_aggregate.nc"
if(isfilepresent(filename_out)) then
  system("rm -rf " + filename_out)
end if

fout = addfile(filename_out, "c")
filedimdef(fout,"time",-1,True)  ;; make time dimension unlimited

;; copy global attributes

att_names = getvaratts(fin) 

do i = 0,dimsizes(att_names)-1
  fout@$att_names(i)$ = fin@$att_names(i)$
end do

;; copy over other variables

var_names = getfilevarnames(fin) ;

do i = 0,dimsizes(var_names)-1      

  if (var_names(i) .eq. "time")      then continue end if
  if (var_names(i) .eq. "time_bnds") then continue end if
  if (var_names(i) .eq. variable)     then continue end if
  if (var_names(i) .eq. "date")      then continue end if
  if (var_names(i) .eq. "date_bnds") then continue end if

  fout->$var_names(i)$ = fin->$var_names(i)$
end do

;; add our data

fout->time_bnds = time_bnds
fout->$variable$ = outdata
fout->time      = time
; For some reason, time needs to come *last* or it gets values from fin instead
delete(fout->time@_FillValue)  ;; coming from filedimdf call to make it unlimited, I think
exit