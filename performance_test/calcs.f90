
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
    character(255) query
    integer calc, ans, portnum, calculate

    ! Interface that ensures type compatibility between Fortran and C
    interface
        subroutine server(portnum) bind(C, name="server")
            use iso_c_binding, only: c_int
            integer(kind=c_int), value :: portnum
        end subroutine server
    end interface

    ! Start the server with portnumber read from standard in
    print *, "Please provide me with a port number."
    read "(1i9)", portnum
    call server(portnum)

end program calculator_server


! **********************************************************************

type(c_ptr) function square(iptr) bind(C, name="square")
    use iso_c_binding, only: C_PTR, C_INT, C_LOC
    implicit none

    ! Variable declarations
    type(c_ptr), pointer :: iptr
    integer(c_int), allocatable, target :: intarray(:)
    integer :: i, length

    length = 2500
    allocate(intarray(0:length))
    intarray = c_loc(iptr(1))

    do i=1,3
        print *, intarray(i)
    end do
    
    do i=1,length
        intarray(i)=intarray(i)**2
    end do

    do i=1,3
        print *, intarray(i)
    end do

end function square

