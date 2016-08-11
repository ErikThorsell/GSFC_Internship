program name
use mpi
implicit none

    ! type declaration statements
    INTEGER :: ierr, buf(255), tag, newcomm
    CHARACTER(MPI_MAX_PORT_NAME) :: port_name
    LOGICAL :: done

    ! executable statements
    call MPI_Init(ierr)
    print *, "Please provide me with the port name: "
    read(*,'(A)') port_name

    call MPI_Comm_connect(port_name, MPI_INFO_NULL, 0, MPI_COMM_WORLD, newcomm, ierr)

    done = .false.
    do while (.not. done)
        tag = 0
        call MPI_Send(buf, 255, MPI_INTEGER, 0, tag, newcomm, ierr)
        done = .true.
    enddo
    call MPI_Send(buf, 0, MPI_INTEGER, 0, 1, newcomm, ierr)
    call MPI_Comm_Disconnect(newcomm, ierr)
    call MPI_Finalize(ierr)

end program name

