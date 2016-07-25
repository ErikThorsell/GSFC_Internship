program f_producer
use iso_c_binding
implicit none

    interface
    ! Initialize Producer
        function initProducer(c_name, i_size) bind (C, name="initProducer") result (i_fd)
            use iso_c_binding
            character(kind=c_char):: c_name
            integer(kind=c_int), value :: i_size
            integer(kind=c_int) :: i_fd
        end function
        function mapProducer(i_fd, i_size) bind (C, name="mapProducer") result (c_base)
            use iso_c_binding
            integer(kind=c_int), value :: i_fd
            integer(kind=c_int), value :: i_size
            character(kind=c_char) :: c_base
        end function
        subroutine terminateProducer(c_base, i_fd, i_size) bind (C, name="terminateProducer")
            use iso_c_binding
            character(kind=c_char) :: c_base(*)
            integer(kind=c_int), value :: i_fd
            integer(kind=c_int), value :: i_size
        end subroutine
        subroutine writeToMem(c_base, c_msg) bind (C, name="writeToMem")
            use iso_c_binding
            character(kind=c_char) :: c_base(*)
            character(kind=c_char) :: c_msg(*)
        end subroutine
    end interface

    ! variables
    character c_name, c_base, c_msg
    integer i_fd, i_size

    ! executable statements
    c_name = "/shm-example"//c_null_char
    c_msg = "This is an example message."//c_null_char
    i_size = 4096
    i_fd = initProducer(c_name, i_size)
    print *, "File descriptor: ", i_fd
    c_base = mapProducer(i_fd, i_size)
    print *, "Base address: ", c_base
    call writeToMem(c_base, c_msg)
    call terminateProducer(c_base, i_fd, i_size)
    print *, "Producer terminated."

end program f_producer

