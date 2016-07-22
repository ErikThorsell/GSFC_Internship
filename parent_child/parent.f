! ########################################################################### !
! parent.f                                                                    !
!                                                                             !
! test the 7 (of which 5 are used) functions that is implemented in the       !
! parent/child communication                                                  !
!                                                                             !
! Written by:                                                                 !
!   Erik Thorsell                                                             !
!   Lina Olandersson                                                          !
!   Simon Strandberg                                                          !
!   2016-07-12                                                                !
! ########################################################################### !
program parent
    implicit none

    include 'solve.i'             ! Includes parameters used by oborg.i
    include 'oborg.i'             ! Includes the common block used for testing
    include 'f77_zmq.h'           ! Includes the ZMQ binding

    integer(ZMQ_PTR)        context
    integer(ZMQ_PTR)        responder
    character*(64)          address
    integer, dimension(22) :: i_buffer ! Buffer for data tranmsmition
    integer, dimension(20) :: i_array, i_array1, i_array2, i_array3 ! Generic arrays
    integer                   i_rc ! if >= 0: the number of bytes sent or received, else: error
    integer                   i, i_lbuf, c, i_sbuf, i_blocksize, i_sizeLastVariable
    character * 48            string

    ! Set up the communication.
    address   = 'tcp://*:55555'                    ! Address to listen to.
    context   = f77_zmq_ctx_new()                  ! Create new context
    responder = f77_zmq_socket(context, ZMQ_REP)   ! Use the REP protocol
    i_rc      = f77_zmq_bind(responder,address) ! Declare the client as a responder
    print *,  "Checking that everything was initialized correctly. RC: ", i_rc

    i=00001
    print *, i
    string = '00001'
    read (string, '(I5)') i

    print *, i

    ! Clear the buffer and fill the arrays with numbers.
    i_lbuf = size(i_buffer)
    i_sbuf = i_lbuf*4

    do i=1, i_lbuf
        i_buffer(i) = 0
    enddo

    do i=1,(i_lbuf-2)
        i_array1(i) = 11
        i_array2(i) = 12
        i_array3(i) = 13
    enddo

    ! Find size of the common block, add 2 for size of ILAST_OBORG_I2
    i_sizeLastVariable = 2
    i_blocksize = loc(ILAST_OBORG_I2)-loc(FJD) + i_sizeLastVariable
    print *, "Size of OBORG.i is equal to: ", i_blocksize
    ! If parent is to call (spawn) its own child, use the line below.
    ! call execute_command_line("./child", wait=.false.)

    ! The parent waits for the child to connect.
    print *,  "Waiting for Child to ack its existence. i_rc: ", i_rc
    i_rc = f77_zmq_recv(responder, i_buffer, i_sbuf, 0) ! 2
    print *,  'Received ack from Child. i_rc: ', i_rc

    ! i_buffer(1) = 9 will be used as an ack throughout the program.
    ! ZeroMQ does not allow consecuetive sends/recvs, why each send has to
    ! be followed by a recv as seen below.
    i_buffer(1) = 9
    i_rc = f77_zmq_send(responder, i_buffer, i_sbuf, 0) ! 4

    ! The parent will listen to the child's communication until the child
    ! chooses to terminate the connection.
    do while(.true.)
        print *,  'Waiting for Child to perform operation. i_rc: ', i_rc
        i_rc = f77_zmq_recv(responder, i_buffer, i_sbuf, 0) ! 6
        print *, "Received operation code: ", (i_buffer(1:2))

        ! Depending on the content of i_buffer(1) the server will do different
        ! things.
        select case (i_buffer(1))
            case (1) ! Corresponds to the subroutine send
                print *, "Child asked for Parent to send i_array: ", i_buffer(2)
                c = i_buffer(2)
                i_buffer(1) = 9
                i_buffer(2) = 9
                select case (c)
                    case (1)
                        i_buffer(3:i_lbuf) = i_array1
                    case (2)
                        i_buffer(3:i_lbuf) = i_array2
                    case (3)
                        i_buffer(3:i_lbuf) = i_array3
                end select
                i_rc = f77_zmq_send(responder, i_buffer, i_sbuf, 0)
                print *, "Sending i_array. i_rc: ", i_rc

            case (2) ! Corresponds to the subroutine get
                print *, "Child asked Parent to get i_array", i_buffer(2)
                c = i_buffer(2)
                i_buffer(1) = 9
                i_rc = f77_zmq_send(responder, i_buffer, i_sbuf, 0)
                print *, "Parent acked that data can be sent. i_rc: ", i_rc
                i_rc = f77_zmq_recv(responder, i_buffer, i_sbuf, 0)
                select case (c)
                    case (1)
                        i_array1 = i_buffer(3:i_lbuf)
                        do i=1,(i_lbuf-2)
                            print *, i_array1(i)
                        enddo
                    case (2)
                        i_array2 = i_buffer(3:i_lbuf)
                        do i=1,(i_lbuf-2)
                            print *, i_array2(i)
                        enddo
                    case (3)
                        i_array3 = i_buffer(3:i_lbuf)
                        do i=1,(i_lbuf-2)
                            print *, i_array3(i)
                        enddo
                end select
                i_buffer(1) = 9
                i_rc = f77_zmq_send(responder, i_buffer, i_sbuf, 0)
                print *, "Parent acked that it got the data!"

            case(3) ! Corresponds to the subroutine sendObsName
                print *, "Child asked parent to send commonblock for obs:",&
                & i_buffer(2)
                c=i_buffer(2)
                i_buffer(1) = 9

                ! Send commonblock to child
                i_rc = f77_zmq_send(responder, FJD, i_blocksize, 0)

            case(4) ! Corresponds to the subroutine getObsName
                print *, "Child wants to send common block for obs:"
                print *, i_buffer(2)
                c=i_buffer(2)
                i_buffer(1) = 9

                ! Acknomledgement, ready to receive again
                i_rc = f77_zmq_send(responder, i_buffer, i_sbuf, 0)

                ! Receive commonblock
                i_rc = f77_zmq_recv(responder, FJD, i_blocksize, 0)

                ! Acknowledge that transfer is done.
                i_buffer(1) = 9
                i_rc = f77_zmq_send(responder, i_buffer, i_sbuf, 0)

            case(5)
            case(6)
            case(7) ! Corresponds to the subroutine closeParent
                i_buffer(1) = 9
                print *, "Child is done with its operations."
                i_rc = f77_zmq_send(responder, i_buffer, i_sbuf, 0 )
                
                ! Close and destroy connection to child
                i_rc = f77_zmq_close(responder)
                i_rc = f77_zmq_ctx_destroy(context)
                exit
        end select
    enddo

end





