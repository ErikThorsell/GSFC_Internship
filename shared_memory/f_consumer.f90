program f_consumer
use iso_c_binding
implicit none

    ! variables
    character*256 c_name 
    !character*256 ::  base
    !character(kind=C_CHAR, len=1), dimension(256) :: base
    type(c_ptr) base
    integer i_fd, i_size
    character pointee(256)
    character*256 cptr
    pointer(cptr, pointee)

    interface
    ! Initialize Consumer
        subroutine initConsumer(c_name) bind (C, name="initConsumer")
            use iso_c_binding
            character(kind=c_char):: c_name
        end subroutine
        subroutine mapConsumer(i_size) bind (C, name="mapConsumer")
            use iso_c_binding
            integer(kind=c_int) :: i_size
        end subroutine
        subroutine terminateConsumer(i_size, c_name) bind (C, name="terminateConsumer")
            use iso_c_binding
            character(kind=c_char) :: c_name
            integer(kind=c_int) :: i_size
        end subroutine
        function readFromMem() bind (C, name="readFromMem") result(base)
            use iso_c_binding
            type(c_ptr) base
            !character(kind=c_char) :: base
        end function

    end interface

    ! executable statements
    c_name = "/shm-example"//c_null_char
    i_size = 4096
    call initConsumer(c_name)
    print *, "Fortran: File descriptor: ", i_fd
    call mapConsumer(i_size)
    print *, "Fortran: Base before read: ", base
    base = readFromMem()
    cptr = loc(base)
    !base = "Hej"
    print *, "Fortran: Base after read: ", pointee
    call terminateConsumer(i_size, c_name)
    print *, "Fortran: Consumer terminated."

end program f_consumer

