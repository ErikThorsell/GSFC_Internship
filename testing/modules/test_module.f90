module test_module
implicit none

    real :: array(10)

    contains

        subroutine show_array()
            integer :: i
            do i=1,size(array)
                print *, array(i)
            enddo
        end subroutine show_array

end module test_module
