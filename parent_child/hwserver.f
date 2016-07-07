      program server
        implicit none
        include 'f77_zmq.h'
        integer(ZMQ_PTR)        context
        integer(ZMQ_PTR)        responder
        character*(64)          address
        !integer, dimension(:), allocatable :: buffer
        integer, dimension(20) :: buffer
        integer, dimension(20) :: array1, array2, array3
        integer                 rc, sbuf, i, lbuf


        !allocate(buffer(3))
        lbuf = size(buffer)
        sbuf = lbuf*4
        do i=1,lbuf
            array1(i) = 1
            array2(i) = 2
            array3(i) = 3
        enddo

        address = 'tcp://*:55555'

        context   = f77_zmq_ctx_new()
        responder = f77_zmq_socket(context, ZMQ_REP)
        rc        = f77_zmq_bind(responder,address)

        print *,  "Waiting for Child to acknowledge existence. RC: ", rc
        rc = f77_zmq_recv(responder, buffer, sbuf, 0) ! 2
        print *,  'Received ack from Child. RC: ', rc

        ! buffer(1) = 9 will be used as an ack throughout the program.
        ! ZeroMQ does not allow consecuetive sends/recvs, why each send has to
        ! be followed by a recv as seen below.
        buffer(1) = 9
        rc = f77_zmq_send(responder, buffer, sbuf, 0) ! 4
        print *,  'Waiting for Child. RC: ', rc
        rc = f77_zmq_recv(responder, buffer, sbuf, 0) ! 6
        print *, "Received: ", (buffer(1:3))

        select case (buffer(1))
          case (1)
            print *, "Child asked for Parent to send array: ", buffer(2)
            select case (buffer(2))
              case (1)
                  buffer = array1
              case (2)
                  buffer = array2
              case (3)
                  buffer = array3
            end select
            rc = f77_zmq_send(responder, buffer, sbuf, 0)
            print *, "Sending array. RC: ", rc
        end select


        !if (buffer(1:rc) /= 'end') then
        !  print *, "Child asked for: ",
        !  rc = f77_zmq_send (responder, "world", 5, 0)
        !else
        !  rc = f77_zmq_send (responder, "end", 3, 0)
        !  exit
        !endif
      !enddo

        rc = f77_zmq_close(responder)
        rc = f77_zmq_ctx_destroy(context)
        !deallocate(buffer)
      end


