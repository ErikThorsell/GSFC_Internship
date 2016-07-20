program parent
    implicit none

    include 'f77_zmq.h'
    
    integer(ZMQ_PTR)    context
    integer(ZMQ_PTR)    responder
    character*(64)      adress
    integer, dimension(22) :: i_buffer ! Buffer for data tranmsmition
    integer             i_rc
    integer             j, i, i_lbuf, c, i_sbuf, i_blocksize, i_sizeLastVariable

do j=1,10
    ! Set up the communication.
    adress   = 'tcp://*:55555'                    ! Address to listen to.
    context   = f77_zmq_ctx_new()                  ! Create new context
    responder = f77_zmq_socket(context, ZMQ_REP)   ! Use the REP protocol
    i_rc      = f77_zmq_bind(responder,adress) ! Declare the client as a responder
    print *,  "PARENT: Checking that everything was initialized correctly. RC: ", i_rc

    print *, 'PARENT: Parent starts child with ECECUTE_COMMAND_LINE'

    call execute_command_line('./child',wait=.false.)
    
    print *, 'PARENT: started child and continous with whatever parents does all day'

    ! Clear the buffer and fill the arrays with numbers.
    i_lbuf = size(i_buffer)
    i_sbuf = i_lbuf*4

    do i=1, i_lbuf
        i_buffer(i) = 0
    enddo

    ! The parent waits for the child to connect.
    print *,  "PARENT: Waiting for Child to ack its existence. i_rc: ", i_rc
    i_rc = f77_zmq_recv(responder, i_buffer, i_sbuf, 0) ! 2
    print *,  'PARENT: Received ack from Child. i_rc: ', i_rc    
    
    print *, 'PARENT: Received buffer filled with: ', i_buffer(i_lbuf)

    do i=1, i_lbuf
        i_buffer(i) = 2
    enddo
    
    print *, 'PARENT: Sending buffer filled with: ', i_buffer(i_lbuf)

    i_rc = f77_zmq_send(responder, i_buffer, i_sbuf, 0)
    
    i_rc = f77_zmq_close(responder)
    i_rc = f77_zmq_ctx_destroy(context)
    print *, 'PARENT: Closed and destroyed connection.', j
end do


end program parent
