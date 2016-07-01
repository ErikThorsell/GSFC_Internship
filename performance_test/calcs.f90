
program calculator_server
! 
! Authors:
!   Lina Olandersson, Simon Strandberg, Erik Thorsell
! Date:
!   2016-06-21
!
! Calculator at the server side of the client/server calculator
! Responsible for starting up the server server.c

use iso_c_binding, only: C_CHAR, C_NULL_CHAR, C_INT, C_PTR
implicit none

    ! type declaration statements
    integer calc, ans, portnum, calculate

    ! Interface that ensures type compatibility between Fortran and C
    interface
        subroutine server(portnum) bind(C, name="server")
            use iso_c_binding, only: c_int
            integer(kind=c_int), value :: portnum
        end subroutine server
        subroutine square(intarray) bind(C, name="square")
            use iso_c_binding
            type(c_ptr), value :: intarray
        end subroutine square
    end interface

    ! Start the server with portnumber read from standard in
    !print *, "Please provide me with a port number."
    !read "(1i9)", portnum
    portnum = 55555
    call server(portnum)

end program calculator_server


! **********************************************************************
subroutine square(cptr) bind(C, name="square")
    use iso_c_binding
    implicit none

    ! Variable declarations
    type(c_ptr) :: cptr
    integer*8 :: iptr
    integer :: length, i
    integer pointee(100000)
    pointer(iptr, pointee)
    iptr = loc(cptr)
    length = 100000

    ! Execution
    do i = 1, length
        pointee(i)= pointee(i)**2
    end do
end subroutine square

