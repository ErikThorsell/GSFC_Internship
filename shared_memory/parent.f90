program parent
use iso_c_binding, only: C_CHAR, C_INT, C_NULL_CHAR

implicit none
    
    integer*4, dimension(100)   :: i_array
    character*400               :: c_buffer
    integer                     :: i, length, ans
    equivalence(i_array,c_buffer)

    interface
        function initializeMem(base, memSize) bind(C, name="initializeMem") result(ans)
            use iso_c_binding, only: c_char, c_int
            character(kind=c_char) :: base(*)
            integer(kind=c_int), value ::  memSize
        end function initializeMem

        
    end interface

    
    length=size(i_array)
    
    do i=1,length
        i_array(i)=2
    enddo
    



end program
