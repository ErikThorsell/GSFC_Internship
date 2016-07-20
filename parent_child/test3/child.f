program child
    implicit none

    include 'f77_zmq.h'           ! Includes the ZMQ binding
    include 'variables_client.i'  ! Includes a small common block holding the ZMQ related variables
    integer, dimension(22) :: i_buffer ! Buffer for data tranmsmition
    integer, dimension(20) :: i_array, i_array1, i_array2, i_array3 ! Generic arrays
    integer                   i_rc ! if >= 0: the number of bytes sent or received, else: error
    integer                   i, i_lbuf, c, i_sbuf, buffNumber, i_obsNumber

    ! Set up the communication.
    address = 'tcp://localhost:55555'               ! Address to listen to.
    context   = f77_zmq_ctx_new()                   ! Create new context
    requester = f77_zmq_socket(context, ZMQ_REQ)    ! Use the REQ protocol
    i_rc        = f77_zmq_connect(requester,address)! Declare the client as a requester

    i_lbuf = size(i_buffer)
    i_sbuf = i_lbuf * 4

    ! Clear the buffer
    do i=1, i_lbuf
        i_buffer(i) = 1
    enddo

    ! Child is born and acknoweldges its existens to its parent.
    print *,  "CHILD: Awaken! Sending buffer filled with: ", i_buffer(i_lbuf)
    i_rc = f77_zmq_send(requester, i_buffer, i_sbuf, 0)
    print *,  "CHILD: Sent buffer"

  
    i_rc = f77_zmq_recv(requester, i_buffer, i_sbuf, 0)
    print *,  "CHILD: Received buffer with: ", i_buffer(i_lbuf)

    i_rc = f77_zmq_close(requester)
    i_rc = f77_zmq_ctx_destroy(context)
    print *, 'CHILD: Closed and destroyed connection.'


! #########################################################################
!
!    ! Set up the communication.
!    address = 'tcp://localhost:55555'               ! Address to listen to.
!    context   = f77_zmq_ctx_new()                   ! Create new context
!    requester = f77_zmq_socket(context, ZMQ_REQ)    ! Use the REQ protocol
!    i_rc        = f77_zmq_connect(requester,address)! Declare the client as a requester
!
!    i_lbuf = size(i_buffer)
!    i_sbuf = i_lbuf * 4
!
!    ! Clear the buffer
!    do i=1, i_lbuf
!        i_buffer(i) = 1
!    enddo
!
!    ! Child is born and acknoweldges its existens to its parent.
!    print *,  "CHILD: Awaken! Sending buffer filled with: ", i_buffer(i_lbuf)
!    i_rc = f77_zmq_send(requester, i_buffer, i_sbuf, 0)
!    print *,  "CHILD: Sent buffer filled with: ", i_buffer(i_lbuf)
!
!  
!    i_rc = f77_zmq_recv(requester, i_buffer, i_sbuf, 0)
!    print *,  "CHILD: Received buffer with: ", i_buffer(i_lbuf)
!
!    i_rc = f77_zmq_close(requester)
!    i_rc = f77_zmq_ctx_destroy(context)
!    print *, 'CHILD: Closed and destroyed connection. Second time.'
!
end program child
