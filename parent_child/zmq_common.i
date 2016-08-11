!   COMMON BLOCK SPECIFICATON
! ZMQ_COMMON is included in the child part of a communication
! that uses the ZeroMQ library.
! Used in child_com.f  

!   Connection initiating variables
integer(ZMQ_PTR)    context
integer(ZMQ_PTR)    child
character*(64)      address

!   child_com variables 
character*(128)     validCommonBlocks

!   ZMQ functions 
integer f77_zmq_ctx_new_
integer f77_zmq_socket_
integer f77_zmq_connect_
integer f77_zmq_recv_
integer f77_zmq_send_
integer f77_zmq_close_
integer f77_zmq_ctx_destroy_

!   Common block
COMMON /zmq_common/ context, child, address, &
       & validCommonBlocks
