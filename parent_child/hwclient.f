      program server
        implicit none
        include 'f77_zmq.h'
        integer(ZMQ_PTR)        context
        integer(ZMQ_PTR)        requester
        character*(64)          address
        integer, dimension(20) :: buffer
        integer                 rc
        integer                 i, lbuf, c, sbuf
      
      
        address = 'tcp://localhost:55555'
      
        context   = f77_zmq_ctx_new()
        requester = f77_zmq_socket(context, ZMQ_REQ)
        rc        = f77_zmq_connect(requester,address)
      
        lbuf = size(buffer)
        sbuf = lbuf * 4

        print *, "Size of buffer is: ", sbuf
      
        do i=1, lbuf
          buffer(i) = 0
        enddo
      
        ! Child is born and acknoweldges its existens to its parent.
        print *,  "Awaken! Sending ack to Parent! RC: ", rc
        rc = f77_zmq_send(requester, buffer, sbuf, 0) ! 1
        print *,  "Sent ack, RC: ", rc

        ! Due to ZeroMQ's implementation you need to send/recv 
        rc = f77_zmq_recv(requester, buffer, sbuf, 0) ! 3
        print *,  "3: Received dummy. RC: ", rc
        if ((buffer(1) .eq. 9) .and. (rc .ge. 0)) then
          print *, "All is good, please chose between the options below"
          print *, "Choose what you want to do:"
          print *, "(1) Send"
          print *, "(2) Get"
          print *, "(3) Send Obs"
          print *, "(4) Get Obs"
          print *, "(5) Get Size"
          print *, "(6) Done"
          print *, "(7) Exit"
          read(*,*) c
        
          select case (c)
            case (1)
              print *, "Ask Parent to send array."
              print *, "Which array do you want (1-3)?"
              read(*,*) c
              buffer(1) = 1
              buffer(2) = c
              rc = f77_zmq_send(requester, buffer, sbuf, 0) ! 5
              print *, "Waiting for Parent to send array. RC: ", rc
            case (2)
            case (3)
            case (4)
            case (5)
            case (6)
            case (7)
          end select
        
          !print *,  "rc = f77_zmq_recv(requester, buffer, 20, 0)"
          if (rc .ge. 0) then
            rc = f77_zmq_recv(requester, buffer, sbuf, 0)
            print *, "Parent sent back the data. RC: ", rc
            do i=1,lbuf
                print *, buffer(i)
            enddo
          else
            print *, "Something went wrong. RC: ", rc
          endif
        else
            print *, "Something went wrong. RC: ", rc
        endif
      
        !rc = f77_zmq_send(requester, "end", 3, 0)
        !rc = f77_zmq_recv(requester, buffer, 20, 0)
      
        rc = f77_zmq_close(requester)
        rc = f77_zmq_ctx_destroy(context)
      
      end
 
 
