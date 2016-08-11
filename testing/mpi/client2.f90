program name
use mpi
implicit none

    ! type declaration statements
    integer :: ierr, parent, my_id, n_procs, i, j, siz, array(4000000/4), ctag, csource, intercomm, siffra
    logical :: flag

    siz = size(array)

    ! executable statements
    call MPI_Init(ierr)
    call MPI_Initialized(flag, ierr)
    call MPI_Comm_get_parent(parent, ierr)
    call MPI_Comm_rank(MPI_COMM_WORLD, my_id, ierr)
    call MPI_Comm_size(MPI_COMM_WORLD, n_procs, ierr)

    csource = 0 !rank of source
    ctag = 1 !message tag

    do j=1,1000
    call MPI_Recv(array(1), siz, MPI_INTEGER, csource, j, parent, MPI_STATUS_IGNORE, ierr)

    do i=1,size(array)
        array(i) = array(i)**2
    enddo

    !do i=1,10
    !    print *, "C.Array(",i,"): ", array(i)
    !enddo

    call MPI_Send(array(1), siz, MPI_INTEGER, csource, j, parent, ierr)
    enddo

    call MPI_Finalize(ierr)
end program name

