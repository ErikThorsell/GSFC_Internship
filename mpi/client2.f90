program name
use mpi
implicit none

    ! type declaration statements
    integer :: ierr, parent, my_id, n_procs, i, array(10), ctag, csource, intercomm, siffra
    logical :: flag

    ! executable statements
    call MPI_Init(ierr)
    call MPI_Initialized(flag, ierr)
    call MPI_Comm_get_parent(parent, ierr)
    call MPI_Comm_rank(MPI_COMM_WORLD, my_id, ierr)
    call MPI_Comm_size(MPI_COMM_WORLD, n_procs, ierr)

    print *, "Initilaized? ", flag
    print *, "My mommy is: ", parent
    print *, "My rank is:", my_id

    csource = 0 !rank of source
    ctag = 1 !message tag

    call MPI_Recv(array(1), 10, MPI_INTEGER, csource, ctag, parent, MPI_STATUS_IGNORE, ierr)
    print *, "Client received array."

    do i=1,10
        print *, "C.Array(",i,"): ", array(i)
    enddo

    do i=1,10
        array(i) = i
    enddo

    do i=1,10
        print *, "C.Array(",i,"): ", array(i)
    enddo

    call MPI_Send(array(1), 10, MPI_INTEGER, csource, ctag, parent, ierr)

    call MPI_Finalize(ierr)
end program name

