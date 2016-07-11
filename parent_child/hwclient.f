! ************************ Pre program ******************* !!
      program server
        implicit none
!        include 'solve.i'
!        include 'oborg.i'
        include 'f77_zmq.h'
        integer(ZMQ_PTR)        context
        integer(ZMQ_PTR)        requester
        character*(64)          address
        integer, dimension(22) :: buffer
        integer, dimension(20) :: array, array1, array2, array3
        integer                 rc
        integer                 i, lbuf, c, sbuf, buffNumber, iobsNumber

        address = 'tcp://localhost:55555'

        context   = f77_zmq_ctx_new()
        requester = f77_zmq_socket(context, ZMQ_REQ)
        rc        = f77_zmq_connect(requester,address)

        lbuf = size(buffer)
        sbuf = lbuf * 4

!! Time to start declaring !!

        do i=1, lbuf
          buffer(i) = 0
        enddo

        do i=1, (lbuf-2)
            array1(i) = 21
            array2(i) = 22
            array3(i) = 23
        enddo

!! Aaand go program, go !!
        call init(buffer, rc)
      
      do while (.true.)
        if ((buffer(1) .eq. 9) .and. (rc .ge. 0)) then
          print *, "All is good, please chose between the options below"
          print *, "Choose what you want to do:"
          print *, "(1) Send"
          print *, "(2) Get"
          print *, "(3) Send Obs"
          print *, "n/a (4) Get Obs"
          print *, "n/a (5) Get Size"
          print *, "n/a (6) Done"
          print *, "(7) Exit"
          read(*,*) c

          select case (c)
            case (1)
              print *, "Which array do you want (1-3)?"
              read(*,*) buffNumber
              call send(buffNumber, buffer)
              print *, "Control data: ", buffer(1), buffer(2)
              print *, "Actual data: "
              do i=3,lbuf
                print *, buffer(i)
              enddo


            case (2)
              print *, "Which array do you want to Parent to get? (1-3)"
              read(*,*) buffNumber
              print *, "Child wants parent to get array: ", buffNumber
              select case (buffNumber)
                case (1)
                  array = array1
                case (2)
                  array = array2
                case (3)
                  array = array3
                end select
              call get(buffNumber, buffer, array)

            case (3)
!              print *,"Which observation's common block would you like?"
!              print *, "Must choose 1 for now"
!              read(*,*) iobsNumber
!              call sendObsN(buffer, iobsNumber)

            case (4)
            case (5)
            case (6)
            case (7)
              call closeParent(buffer)
              print *, "Exiting program"
              exit
          end select
        else
          print *, "Something went wrong."
        endif
      enddo

        !rc = f77_zmq_send(requester, "end", 3, 0)
        !rc = f77_zmq_recv(requester, buffer, 20, 0)

        rc = f77_zmq_close(requester)
        rc = f77_zmq_ctx_destroy(context)

      end

!! Subroutines

! *********************************************************************
      subroutine init(buffer, rc)
        implicit none
        include 'f77_zmq.h'
        integer(ZMQ_PTR)        context
        integer(ZMQ_PTR)        requester
        character*(64)          address
        integer, dimension(22) :: buffer
        integer, dimension(20) :: array1, array2, array3
        integer                 rc
        integer                 i, lbuf, c, sbuf, buffNumber

        address = 'tcp://localhost:55555'

        context   = f77_zmq_ctx_new()
        requester = f77_zmq_socket(context, ZMQ_REQ)
        rc        = f77_zmq_connect(requester,address)

        lbuf = size(buffer)
        sbuf = lbuf * 4

       ! Child is born and acknoweldges its existens to its parent.
        print *,  "Awaken! Sending ack to Parent! RC: ", rc
        rc = f77_zmq_send(requester, buffer, sbuf, 0)
        print *,  "Sent ack, RC: ", rc

        ! Due to ZeroMQ's implementation you cannot send twice in a row,
        ! but the Parent needs to ack each send (and vice versa).
        rc = f77_zmq_recv(requester, buffer, sbuf, 0)
        print *,  "Received dummy. RC: ", rc
      end

      subroutine send(buffNumber, buffer)
        implicit none
        include 'f77_zmq.h'
        integer(ZMQ_PTR)        context
        integer(ZMQ_PTR)        requester
        character*(64)          address
        integer, dimension(22) :: buffer
        integer                 rc
        integer                 i, lbuf, c, sbuf, buffNumber
        
        address = 'tcp://localhost:55555'

        context   = f77_zmq_ctx_new()
        requester = f77_zmq_socket(context, ZMQ_REQ)
        rc        = f77_zmq_connect(requester,address)

        lbuf = size(buffer)
        sbuf = lbuf * 4

        buffer(1) = 1
        buffer(2) = buffNumber

        print *, "Ask Parent to send array."
        rc = f77_zmq_send(requester, buffer, sbuf, 0)

        print *, "Waiting for Parent to send array. RC: ", rc

        rc = f77_zmq_recv(requester, buffer, sbuf, 0)
        print *, "Parent sent back the data. RC: ", rc
      end
! *********************************************************************
      subroutine get(buffNumber, buffer, array)
        implicit none
        include 'f77_zmq.h'
        integer(ZMQ_PTR)        context
        integer(ZMQ_PTR)        requester
        character*(64)          address
        integer, dimension(22) :: buffer
        integer, dimension(20) :: array
        integer                 rc
        integer                 i, lbuf, c, sbuf, buffNumber

        address = 'tcp://localhost:55555'

        context   = f77_zmq_ctx_new()
        requester = f77_zmq_socket(context, ZMQ_REQ)
        rc        = f77_zmq_connect(requester,address)

        lbuf = size(buffer)
        sbuf = lbuf * 4

!! Actual function !!

        buffer(1) = 2
        buffer(2) = buffNumber
        rc = f77_zmq_send(requester, buffer, sbuf, 0)

        !print *, "Parent acked that it's ready."
        rc = f77_zmq_recv(requester, buffer, sbuf, 0)

        buffer(3:lbuf) = array

        !print *, "Sending data to parent."
        rc = f77_zmq_send(requester, buffer, sbuf, 0)

        !print *, "Waiting for Parent to ack. RC: ", rc
        rc = f77_zmq_recv(requester, buffer, sbuf, 0)
      end
! *********************************************************************
      subroutine closeParent(buffer)

        implicit none
        include 'f77_zmq.h'
        integer(ZMQ_PTR)        context
        integer(ZMQ_PTR)        requester
        character*(64)          address
        integer, dimension(22) :: buffer
        integer                 rc, lbuf, sbuf, i
        integer, dimension(8) :: t
        integer                 ms1, ms2
        real                    dt

        address = 'tcp://localhost:55555'

        context   = f77_zmq_ctx_new()
        requester = f77_zmq_socket(context, ZMQ_REQ)
        rc        = f77_zmq_connect(requester,address)
        
        lbuf = size(buffer)
        sbuf = lbuf * 4

        buffer(1) = 7
        
        rc = f77_zmq_send(requester, buffer, sbuf, 0)
        rc = f77_zmq_recv(requester, buffer, sbuf ,0)

      ! Sleep for dt milliseconds
!      call date_and_time(values=t)
!      ms1=(t(5)*3600+t(6)*60+t(7))*1000+t(8)
!
!      dt = 1
!
!      do ! check time:
!       call date_and_time(values=t)
!       ms2=(t(5)*3600+t(6)*60+t(7))*1000+t(8)
!       if(ms2-ms1>=dt)exit
!      enddo

     end

! *********************************************************************
      subroutine sendobsN(buffer, iobsNumber)
        
!        implicit none
!        include 'f77_zmq.h'
!        include 'oborg.i'
!        include 'solve.i'
!        integer(ZMQ_PTR)        context
!        integer(ZMQ_PTR)        requester
!        character*(64)          address
!        integer, dimension(22) :: buffer
!        integer                 rc, lbuf, sbuf, i, iobsNumber
!
!        address = 'tcp://localhost:55555'
!
!        context   = f77_zmq_ctx_new()
!        requester = f77_zmq_socket(context, ZMQ_REQ)
!        rc = f77_zmq_connect(requester, address)
!
!
!        lbuf = size(buffer)
!        sbuf = lbuf * 4
!        
!        print *, ""
!
!        buffer(1) = 3
!        buffer(2) = iobsNumber
!        rc = f77_zmq_send(requester, buffer, sbuf, 0)
!        rc = f77_zmq_recv(requester, FJD, 830, 0)
!        buffer(1) = 9
!        print *, FJD,FRACT
!

      end
