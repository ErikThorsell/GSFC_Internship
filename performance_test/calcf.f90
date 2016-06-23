program calculator_client
!
! Client side of the Server/Client calculator, written in Fortran and C
! Authors:
!   Lina Olandersson, Simon Strandberg, Erik Thorsell
!   2016-06-21
!
use iso_c_binding, only: C_CHAR, C_NULL_CHAR, C_INT
implicit none

    ! type declaration statements
    integer(4), dimension(2500) :: array, ans
    integer portno, i

    ! Interfaces that ensure type compatability between Fortran and C.
    interface
        subroutine client(ipaddr, portnum) bind(C, name="client")
            use iso_c_binding, only: c_char, c_int
            character(kind=c_char) :: ipaddr(*)
            integer(kind=c_int), value :: portnum
        end subroutine client
    end interface

    interface
        function calc(indata, length) bind(C, name="calc") result (ans)
            use iso_c_binding, only: c_int
            integer(kind=c_int), dimension(2500) :: indata
            integer(kind=c_int) :: length
        end function calc
    end interface

    ! executable statements
    print *, "Please enter the same port number as for the server (e.g. 55555)."
    read "(1i9)", portno
    ! Call client.c and connect to localhost on port number `portno'.
    call client(C_CHAR_"localhost"//C_NULL_CHAR, portno)

    ! Put numbers int the matrix
    do i=1,2500
        array(i) = i
    end do

    ! Call client.c and pass the query on towards calcs.f90.

    print *, "KOM HIT"

    array = calc(array, 2500)

    print *, "KOM DIT"

end program calculator_client

