program name
use iso_c_binding, only: C_CHAR, C_NULL_CHAR, C_INT
implicit none

    ! type declaration statements
    character(255) query
    integer calc, ans, portnum, calculate

    interface
        subroutine server(portnum) bind(C, name="server")
            use iso_c_binding, only: c_int
            integer(kind=c_int), value :: portnum
        end subroutine server
    end interface

    ! executable statements
    print *, "Please provide me with a port number. Plz. <3"
    read "(1i9)", portnum
    call server(portnum)

end program name

function calculate(query)
implicit none

    character(255) query, op
    integer length, i, calculate
    integer, dimension (:,:), allocatable :: inputarray

    call parse(query, ' ', inputarray, length)

    do i=1,size(inputarray)
        print *, inputarray(i)
    end do

    calculate = 5

end function calculate


subroutine parse(str, delims, args, nargs)
implicit none

    character(len=*) :: str, delims
    character(len=len_trim(str)) :: strsav
    character(len=*),dimension(:) :: args
    integer na, nargs, i, lenstr, k

    strsav=str
    call compact(str)
    na=size(args)
    do i=1,na
      args(i)=' '
    end do  
    nargs=0
    lenstr=len_trim(str)
    if(lenstr==0) return
    k=0

    do
       if(len_trim(str) == 0) exit
       nargs=nargs+1
       call split(str,delims,args(nargs))
       call removebksl(args(nargs))
    end do
    str=strsav

end subroutine parse


