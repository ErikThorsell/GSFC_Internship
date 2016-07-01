program name
use mpi
implicit none

    ! type declaration statements
    INTEGER :: ierr, size, newcomm, loop, buf(255), status(MPI_STATUS_SIZE)
    CHARACTER(MPI_MAX_PORT_NAME) :: port_name

    ! executable statements
    call MPI_Init(ierr)
    call MPI_Comm_size(MPI_COMM_WORLD, size, ierr)
    call MPI_Open_port(MPI_INFO_NULL, port_name, ierr)
    print *, "Port name is: ", port_name

    do while (.true.)
        call MPI_Comm_accept(port_name, MPI_INFO_NULL, 0, MPI_COMM_WORLD, newcomm, ierr)

        loop = 1
        do while (loop .eq. 1)
            call MPI_Recv(buf, 255, MPI_INTEGER, MPI_ANY_SOURCE, MPI_ANY_TAG, newcomm, status, ierr)
            print *, "Inne och loopar i loop."
            loop = 0
        enddo

        call MPI_Comm_free(newcomm, ierr)
        call MPI_Close_port(port_name, ierr)
        call MPI_Finalize(ierr)

    enddo

end program name

