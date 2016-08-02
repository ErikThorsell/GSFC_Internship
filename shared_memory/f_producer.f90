program f_producer
use iso_c_binding
implicit none

character*256  c_name, c_msg
integer i_size, i, i_test
character*400 :: c_array
integer*4, dimension(100) :: i_array
integer*4, dimension(100) :: i_array_2
integer*4, dimension(100) :: i_array_mold
equivalence(i_array,c_array)

    interface
    ! Initialize Producer
        subroutine initProducer(c_name, i_size) bind (C, name="initProducer")
            use iso_c_binding
            character(kind=c_char):: c_name
            integer(kind=c_int), value :: i_size
        end subroutine
        subroutine mapProducer(i_size) bind (C, name="mapProducer")
            use iso_c_binding
            integer(kind=c_int), value :: i_size
        end subroutine
        subroutine terminateProducer(i_size) bind (C, name="terminateProducer")
            use iso_c_binding
            integer(kind=c_int), value :: i_size
        end subroutine
        subroutine writeToMem(c_msg) bind (C, name="writeToMem")
            use iso_c_binding
            character(kind=c_char) :: c_msg(*)
        end subroutine
    end interface

    ! variables
    
    ! executable statements
    c_name = "/shm-example"//c_null_char
    c_msg = "Banana. This is an example message."//c_null_char
    i_size = 4096

    do i=1,100
        i_array(i) = 2
    enddo
    
    print *, "Fortran: This is c_array: ", c_array(1:4)
    i_array_2 = transfer(c_array, i_array_mold)
    print *, "Fortran: This is i_array_2: ", i_array_2(1)
    
    print *, "Fortran: Initializing producer" 
    call initProducer(c_name, i_size)
    print *, "Fortran: Mapping memory"
    call mapProducer(i_size)
    print *, "Fortran: Writing msg to memory: ", c_msg
    call writeToMem(c_msg)
    print *, "Fortran: Terminating producer"
    call terminateProducer(i_size)
    print *, "Fortran: Producer terminated."

end program f_producer
