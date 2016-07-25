program fortran_c
use iso_c_binding
implicit none

    ! variables
    character c_name, c_base
    integer i_fd, i_size

    interface
    ! Initialize Consumer
        function initConsumer(c_name) bind (C, name="initConsumer") result (i_fd)
            use iso_c_binding
            character(kind=c_char):: c_name
            integer(kind=c_int) :: i_fd
        end function
        function mapConsumer(i_fd, i_size) bind (C, name="mapConsumer") result (c_base)
            use iso_c_binding
            integer(kind=c_int) :: i_fd
            integer(kind=c_int) :: i_size
            character(kind=c_char) :: c_base
        end function
        subroutine terminateConsumer(c_base, i_fd, i_size, c_name) bind (C, name="terminateConsumer")
            use iso_c_binding
            character(kind=c_char) :: c_base
            character(kind=c_char) :: c_name
            integer(kind=c_int) :: i_fd
            integer(kind=c_int) :: i_size
        end subroutine
        subroutine readFromMem(c_base) bind (C, name="readFromMem")
            use iso_c_binding
            character(kind=c_char) :: c_base
        end subroutine

    end interface

    ! executable statements
    c_name = "/shm-example"//c_null_char
    i_size = 4096
    i_fd = initConsumer(c_name)
    print *, "File descriptor: ", i_fd
    c_base = mapConsumer(i_fd, i_size)
    print *, "Base address: ", c_base
    call readFromMem(c_base)
    call terminateConsumer(c_base, i_fd, i_size, c_name)
    print *, "Consumer terminated."

end program fortran_c

