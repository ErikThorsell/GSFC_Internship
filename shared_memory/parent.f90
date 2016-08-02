program parent
use iso_c_binding, only: C_CHAR, C_INT, C_PTR, C_NULL_CHAR

implicit none
    
    integer*4, dimension(100)   :: i_array
    character*400               :: c_buffer
    character*60                :: c_memName !, & 
                                 !& mapMemoryProducer, mapMemoryConsumer
    integer                     :: i, i_length, i_memSize
    equivalence(i_array,c_buffer)
    character, pointer          :: c_shm_base_prod_fpoint(:)
    type(C_PTR) :: c_shm_base_prod

! Interface for producer functions
    interface 
        function initProducer(memName, memSize) bind(C, name="initProducer") result(i_shm_fd_prod)
            use iso_c_binding, only: c_char, c_int
            character(kind=c_char) :: memName(*)
            integer(kind=c_int), value ::  memSize
        end function initProducer

        function mapProducer(shm_fd_c, memSize) bind(C, name="mapProducer") result(c_shm_base_prod)
            use iso_c_binding, only: c_int, c_ptr
            integer(kind=c_int), value :: shm_fd_c, memSize
            type(C_PTR) :: c_shm_base_prod
        end function mapProducer

        subroutine terminateProducer(shm_base_c, shm_fd_c, memSize) bind(C, name="terminateProducer")
            use iso_c_binding, only: c_char, c_int
            character(kind=c_char) :: shm_base_c(*)
            integer(kind=c_int), value :: shm_fd_c, memSize
        end subroutine terminateProducer
        
        subroutine writeToMem(base, msg) bind(C, name="writeToMem")
            use iso_c_binding, only: c_char
            character(kind=c_char) :: base(*), msg(*)
        end subroutine writeToMem      
    end interface

! Interface for consumer functions
    interface
        function initConsumer(memName) bind(C, name="initConsumer") result(i_shm_fd_cons)
            use iso_c_binding, only: c_char
            character(kind=c_char) :: memName(*)
        end function initConsumer

        function mapConsumer(shm_fd_c, memSize) bind(C, name="mapConsumer") result(c_shm_base_cons)
            use iso_c_binding, only: c_int
            integer(kind=c_int), value :: shm_fd_c, memSize
        end function mapConsumer

        subroutine terminateConsumer(shm_base_c, shm_fd_c, memSize, memName) bind(C, name="terminateConsumer")
            use iso_c_binding, only: c_char, c_int
            character(kind=c_char) :: shm_base_c(*), memName
            integer(kind=c_int), value :: shm_fd_c, memSize
        end subroutine terminateConsumer
        
        
        subroutine readFromMem(base) bind(C, name="readFromMem")
            use iso_c_binding, only: c_char
            character(kind=c_char) :: base(*)
        end subroutine readFromMem

    end interface

    i_length=size(i_array)
    
    do i=1,i_length
        i_array(i)=2
    enddo
    
    c_memName = "/shm-test"//C_NULL_CHAR
    i_memSize = 4096
    i_shm_fd_prod = initializeProducer(c_memName, i_memSize)
    c_shm_base_prod = mapMemoryProducer(i_shm_fd_prod, i_memSize)
    
    call writeToMem(c_shm_base_prod, C_CHAR_"Hej!!!!"//C_NULL_CHAR)
    call terminateMemProducer(c_shm_base_prod, i_shm_fd_prod, i_memSize)


end program
