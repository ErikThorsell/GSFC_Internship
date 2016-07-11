      program server
        implicit none
        include 'solve.i'
        include 'oborg.i'
        include 'f77_zmq.h'
        integer(ZMQ_PTR)        context
        integer(ZMQ_PTR)        responder
        character*(64)          address
        integer, dimension(22) :: buffer
        integer, dimension(20) :: array1, array2, array3
        integer                 rc, sbuf, i, lbuf, c


        !allocate(buffer(3))
        lbuf = size(buffer)
        sbuf = lbuf*4
        do i=1,(lbuf-2)
            array1(i) = 11
            array2(i) = 12
            array3(i) = 13
        enddo

        address = 'tcp://*:55555'

        context   = f77_zmq_ctx_new()
        responder = f77_zmq_socket(context, ZMQ_REP)
        rc        = f77_zmq_bind(responder,address)
        
        print *, OBORG_IFILL_LEN
        print *,  "Waiting for Child to ack its existence. RC: ", rc
        rc = f77_zmq_recv(responder, buffer, sbuf, 0) ! 2
        print *,  'Received ack from Child. RC: ', rc

        ! buffer(1) = 9 will be used as an ack throughout the program.
        ! ZeroMQ does not allow consecuetive sends/recvs, why each send has to
        ! be followed by a recv as seen below.
        buffer(1) = 9
        rc = f77_zmq_send(responder, buffer, sbuf, 0) ! 4
      
      do while(.true.)   
        print *,  'Waiting for Child to perform operation. RC: ', rc
        rc = f77_zmq_recv(responder, buffer, sbuf, 0) ! 6
        print *, "Received operation code: ", (buffer(1:2))

        select case (buffer(1))
          case (1)
            print *, "Child asked for Parent to send array: ", buffer(2)
            c = buffer(2)
            buffer(1) = 9
            buffer(2) = 9
            select case (c)
              case (1)
                  buffer(3:lbuf) = array1
              case (2)
                  buffer(3:lbuf) = array2
              case (3)
                  buffer(3:lbuf) = array3
            end select
            rc = f77_zmq_send(responder, buffer, sbuf, 0)
            print *, "Sending array. RC: ", rc

          case (2)
            print *, "Child asked Parent to get array", buffer(2)
            c = buffer(2)
            buffer(1) = 9
            rc = f77_zmq_send(responder, buffer, sbuf, 0)
            print *, "Parent acked that data can be sent. RC: ", rc
            rc = f77_zmq_recv(responder, buffer, sbuf, 0)
            !do i=3,(lbuf)
            !  print *, buffer(i)
            !enddo
            select case (c)
              case (1)
                array1 = buffer(3:lbuf)
                do i=1,(lbuf-2)
                  print *, array1(i)
                enddo
              case (2)
                array2 = buffer(3:lbuf)
                do i=1,(lbuf-2)
                  print *, array2(i)
                enddo
              case (3)
                array3 = buffer(3:lbuf)
                do i=1,(lbuf-2)
                  print *, array3(i)
                enddo
            end select
            buffer(1) = 9
            rc = f77_zmq_send(responder, buffer, sbuf, 0)
            print *, "Parent acked that it got the data!"

          case(3)
            print *, "Child asked parent to send commonblock for obs:"
            print *, buffer(2)
            c=buffer(2)
            buffer(1) = 9
            buffer(2) = 9
            FJD = 3
            FRACT = 9
            rc = f77_zmq_send(responder, FJD, 830, 0)
            print *, FJD, FRACT
          case(4)
          case(5)
          case(6)
          case(7)
            buffer(1) = 9
            print *, "Child is done with its operations."
            rc = f77_zmq_send(responder, buffer, sbuf, 0 )
            exit
        end select
      enddo

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


