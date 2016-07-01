program master
use mpi
implicit none

    integer :: ierr, num_procs, my_id, intercomm, i, array(10), s_tag, s_dest, siffra

    CALL MPI_INIT(ierr)

    CALL MPI_COMM_RANK(MPI_COMM_WORLD, my_id, ierr)
    CALL MPI_COMM_SIZE(MPI_COMM_WORLD, num_procs, ierr)

    print *, "S.Rank =", my_id
    print *, "S.Size =", num_procs

    if (.not. (ierr .eq. 0)) then
        print*, "S.Unable to initilaize bös!"
        stop
    endif

    do i=1,10
        array(i) = 99
    enddo

    if (my_id .eq. 0) then
        call MPI_Comm_spawn("./client2.out", MPI_ARGV_NULL, 1, MPI_INFO_NULL, my_id, &
        & MPI_COMM_WORLD, intercomm, MPI_ERRCODES_IGNORE, ierr)


        s_dest = 0 !rank of destination (integer)
        s_tag =  1 !message tag (integer)
        call MPI_Send(array(1), 10, MPI_INTEGER, s_dest, s_tag, intercomm, ierr)

        call MPI_Recv(array(1), 10, MPI_INTEGER, s_dest, s_tag, intercomm, MPI_STATUS_IGNORE, ierr)

        do i=1,10
           print *, "S.Array(",i,"): ", array(i)
        enddo

    endif

    call MPI_Finalize(ierr)

end program master
