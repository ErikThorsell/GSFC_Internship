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
    character(255) query
    integer calc, ans, portno

    ! Interfaces that ensure type compatability between Fortran and C.
    interface
        subroutine client(ipaddr, portnum) bind(C, name="client")
            use iso_c_binding, only: c_char, c_int
            character(kind=c_char) :: ipaddr(*)
            integer(kind=c_int), value :: portnum
        end subroutine client
    end interface

    interface
        function calc(indata) bind(C, name="calc") result (ans)
            use iso_c_binding, only: c_char
            character(kind=c_char) :: indata(*)
        end function calc
    end interface

    ! executable statements
    ans = 0
    print *, "Please enter the same port number as for the server (e.g. 55555)."
    read *, portno
    ! Call client.c and connect to localhost on port number `portno'.
    call client(C_CHAR_"localhost"//C_NULL_CHAR, portno)
    print *, "Usage: Write two numbers followed by an operator (add, sub, mul, div)."
    print *, "Only integer answers are supported. (2 4 div will return 0)"
    read (*,'(A)') query
    ! Call client.c and pass the query on towards calcs.f90.
    ans = calc(query//C_NULL_CHAR)
    print *, "The answer is: ", ans

end program calculator_client

