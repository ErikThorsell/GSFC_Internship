program performance_test
!
! Client side of the Server/Client calculator, written in Fortran and C
! Authors:
!   Lina Olandersson, Simon Strandberg, Erik Thorsell
!   2016-06-21
!
use iso_c_binding, only: C_CHAR, C_NULL_CHAR, C_INT, C_PTR, C_LOC
implicit none

    ! Interfaces that ensure type compatability between Fortran and C.
    interface
        subroutine client(ipaddr, portnum) bind(C, name="client")
            use iso_c_binding, only: c_char, c_int
            character(kind=c_char) :: ipaddr(*)
            integer(kind=c_int), value :: portnum
        end subroutine client

        subroutine close_connection() bind(C, name="close_connection")
            use iso_c_binding
            implicit none
        end subroutine close_connection

        subroutine calc(indata, length) bind(C, name="calc")
            use iso_c_binding, only: c_ptr, c_int
            implicit none
            integer(c_int), value :: length
            type(c_ptr), value :: indata
        end subroutine calc

    end interface

    ! type declaration statements
    integer(c_int), allocatable, target :: array(:)
    type(c_ptr) :: cptr
    integer portno, length, i, j

    ! executable statements
    !print *, "Please enter the same port number as for the server (e.g. 55555)."
    !read "(1i9)", portno
    ! Call client.c and connect to localhost on port number `portno'.
    portno=55555
    do j=1,500
        call client(C_CHAR_"localhost"//C_NULL_CHAR, portno)

        ! Put numbers in the array
        length = 100000
        allocate(array(0:length))
        cptr=c_loc(array(1))

        do i=1, length
            array(i) = 2
        end do

        ! Call client.c and pass the query on towards calcs.f90.
        call calc(cptr, length)

       ! do i=1,2
       !     print *, array(i)
       ! end do

!        call close_connection()

        deallocate(array)
    enddo
end program performance_test

