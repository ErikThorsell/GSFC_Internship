program name
use strings
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
        print *, inputarray(i, 1)
    end do

    calculate = 5

end function calculate

