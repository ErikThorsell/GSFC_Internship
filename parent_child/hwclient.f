! ************************ Pre program ******************* !
      program server
        implicit none
        include 'solve.i'
        include 'oborg.i'
        include 'f77_zmq.h'
        include 'variables_client.i'
        integer, dimension(22) :: i_buffer
        integer, dimension(20) :: i_array, i_array1, i_array2, i_array3
        integer                   i_rc
        integer                   i, i_lbuf, c, i_sbuf, buffNumber, i_obsNumber

        address = 'tcp://localhost:55555'

        context   = f77_zmq_ctx_new()
        requester = f77_zmq_socket(context, ZMQ_REQ)
        i_rc        = f77_zmq_connect(requester,address)

        i_lbuf = size(i_buffer)
        i_sbuf = i_lbuf * 4

!! Time to start declaring !!

        do i=1, i_lbuf
          i_buffer(i) = 0
        enddo

        do i=1, (i_lbuf-2)
            i_array1(i) = 21
            i_array2(i) = 22
            i_array3(i) = 23
        enddo

!! Aaand go program, go !!
        call init(i_buffer, i_rc)

      do while (.true.)
        if ((i_buffer(1) .eq. 9) .and. (i_rc .ge. 0)) then
          print *, "All is good, please chose between the options below"
          print *, "Choose what you want to do:"
          print *, "(1) Send"
          print *, "(2) Get"
          print *, "(3) Send Obs"
          print *, "(4) Get Obs"
          print *, "n/a (5) Get Size"
          print *, "n/a (6) Done"
          print *, "(7) Exit"
          read(*,*) c

          select case (c)
            case (1)
              print *, "Which i_array do you want (1-3)?"
              read(*,*) buffNumber
              call send(buffNumber, i_buffer)
              print *, "Control data: ", i_buffer(1), i_buffer(2)
              print *, "Actual data: "
              do i=3,i_lbuf
                print *, i_buffer(i)
              enddo

            case (2)
              print *, "Which i_array do you want to Parent to get? (1-3)"
              read(*,*) buffNumber
              print *, "Child wants parent to get i_array: ", buffNumber
              select case (buffNumber)
                case (1)
                  i_array = i_array1
                case (2)
                  i_array = i_array2
                case (3)
                  i_array = i_array3
                end select
              call get(buffNumber, i_buffer, i_array)

            case (3)
              print *,"Which observation's common block would you like?"
              print *, "Must choose 1 for now"
              read(*,*) i_obsNumber
              call sendObsN(i_buffer, i_obsNumber)

            case (4)
              print *, "Which observation's common block shall I send?"
              read(*,*) i_obsNumber
              call getObsN(i_buffer, i_obsNumber)

            case (5)
            case (6)
            case (7)
              call closeParent(i_buffer)
              print *, "Exiting program"
              exit
          end select
        else
          print *, "Something went wrong. i_buffer(1) = ", &
          & i_buffer(1), ", i_rc: ", i_rc
        endif
      enddo

        !i_rc = f77_zmq_send(requester, "end", 3, 0)
        !i_rc = f77_zmq_recv(requester, i_buffer, 20, 0)

        i_rc = f77_zmq_close(requester)
        i_rc = f77_zmq_ctx_destroy(context)

      end

!! Subroutines

! *********************************************************************
      subroutine init(i_buffer, i_rc)
        implicit none
        include 'f77_zmq.h'
        include 'variables_client.i'
        !integer(ZMQ_PTR)        context
        !integer(ZMQ_PTR)        requester
        !character*(64)          address
        integer, dimension(22) :: i_buffer
        integer, dimension(20) :: i_array1, i_array2, i_array3
        integer                 i_rc
        integer                 i, i_lbuf, c, i_sbuf, buffNumber

        !address = 'tcp://localhost:55555'

        !context   = f77_zmq_ctx_new()
        !requester = f77_zmq_socket(context, ZMQ_REQ)
        !i_rc        = f77_zmq_connect(requester,address)

        i_lbuf = size(i_buffer)
        i_sbuf = i_lbuf * 4

       ! Child is born and acknoweldges its existens to its parent.
        print *,  "Awaken! Sending ack to Parent! i_rc: ", i_rc
        i_rc = f77_zmq_send(requester, i_buffer, i_sbuf, 0)
        print *,  "Sent ack, i_rc: ", i_rc

        ! Due to ZeroMQ's implementation you cannot send twice in a row,
        ! but the Parent needs to ack each send (and vice versa).
        i_rc = f77_zmq_recv(requester, i_buffer, i_sbuf, 0)
        print *,  "Received dummy. i_rc: ", i_rc
      end
!*************************************************************************!
      subroutine send(buffNumber, i_buffer)
        !implicit none
        include 'f77_zmq.h'
        include 'variables_client.i'
        !integer(ZMQ_PTR)        context
        !integer(ZMQ_PTR)        requester
        !character*(64)          address
        integer, dimension(22) :: i_buffer
        integer                 i_rc
        integer                 i, i_lbuf, c, i_sbuf, buffNumber

        !address = 'tcp://localhost:55555'

        !context   = f77_zmq_ctx_new()
        !requester = f77_zmq_socket(context, ZMQ_REQ)
        !i_rc        = f77_zmq_connect(requester,address)

        i_lbuf = size(i_buffer)
        i_sbuf = i_lbuf * 4

        i_buffer(1) = 1
        i_buffer(2) = buffNumber

        print *, "Ask Parent to send i_array."
        i_rc = f77_zmq_send(requester, i_buffer, i_sbuf, 0)

        print *, "Waiting for Parent to send i_array. i_rc: ", i_rc

        i_rc = f77_zmq_recv(requester, i_buffer, i_sbuf, 0)
        print *, "Parent sent back the data. i_rc: ", i_rc
      end
! *********************************************************************
      subroutine get(buffNumber, i_buffer, i_array)
        implicit none
        include 'f77_zmq.h'
        include 'variables_client.i'
        !integer(ZMQ_PTR)        context
        !integer(ZMQ_PTR)        requester
        !character*(64)          address
        integer, dimension(22) :: i_buffer
        integer, dimension(20) :: i_array
        integer                 i_rc
        integer                 i, i_lbuf, c, i_sbuf, buffNumber

        !address = 'tcp://localhost:55555'

        !context   = f77_zmq_ctx_new()
        !requester = f77_zmq_socket(context, ZMQ_REQ)
        !i_rc        = f77_zmq_connect(requester,address)

        i_lbuf = size(i_buffer)
        i_sbuf = i_lbuf * 4

!! Actual function !!

        i_buffer(1) = 2
        i_buffer(2) = buffNumber
        i_rc = f77_zmq_send(requester, i_buffer, i_sbuf, 0)

        !print *, "Parent acked that it's ready."
        i_rc = f77_zmq_recv(requester, i_buffer, i_sbuf, 0)

        i_buffer(3:i_lbuf) = i_array

        !print *, "Sending data to parent."
        i_rc = f77_zmq_send(requester, i_buffer, i_sbuf, 0)

        !print *, "Waiting for Parent to ack. i_rc: ", i_rc
        i_rc = f77_zmq_recv(requester, i_buffer, i_sbuf, 0)
      end
! *********************************************************************
      subroutine closeParent(i_buffer)

        implicit none
        include 'f77_zmq.h'
        include 'variables_client.i'
        !integer(ZMQ_PTR)        context
        !integer(ZMQ_PTR)        requester
        !character*(64)          address
        integer, dimension(22) :: i_buffer
        integer                 i_rc
        integer, dimension(8) :: t
        integer                 ms1, ms2, i_lbuf, i_sbuf, i
        real                    dt

        !address = 'tcp://localhost:55555'

        !context   = f77_zmq_ctx_new()
        !requester = f77_zmq_socket(context, ZMQ_REQ)
        !i_rc        = f77_zmq_connect(requester,address)

        i_lbuf = size(i_buffer)
        i_sbuf = i_lbuf * 4

        i_buffer(1) = 7

! Tell parent that child is done
        i_rc = f77_zmq_send(requester, i_buffer, i_sbuf, 0)
! Receive confirmation from parent
        i_rc = f77_zmq_recv(requester, i_buffer, i_sbuf ,0)

     end

! *********************************************************************
      subroutine sendobsN(i_buffer, i_obsNumber) ! CASE 3

        implicit none
        include 'solve.i'
        include 'oborg.i'
        include 'f77_zmq.h'
        include 'variables_client.i'
        !integer(ZMQ_PTR)        context
        !integer(ZMQ_PTR)        requester
        !character*(64)          address
        integer, dimension(22) :: i_buffer
        integer                  i_rc
        integer                  i_lbuf, i_sbuf, i, i_obsNumber, i_blocksize

        !address = 'tcp://localhost:55555'

        !context   = f77_zmq_ctx_new()
        !requester = f77_zmq_socket(context, ZMQ_REQ)
        !i_rc = f77_zmq_connect(requester, address)


        i_lbuf = size(i_buffer)
        i_sbuf = i_lbuf * 4

        print *, ""

        i_buffer(1) = 3
        i_buffer(2) = i_obsNumber
        i_rc = f77_zmq_send(requester, i_buffer, i_sbuf, 0)

! Find size of commonblock. add 2 for  size of ILAST_OBORG_I2
        i_blocksize = loc(ILAST_OBORG_I2)-loc(FJD) + 2

        i_rc = f77_zmq_recv(requester, FJD, i_blocksize, 0)

        FJD = 33
        ILAST_OBORG_I2 = 888

! Assign value 9 to i_buffer(1) so that loop may continue
        i_buffer(1) = 9


      end

! *********************************************************************

      subroutine getobsN(i_buffer, i_obsNumber)
        implicit none
        include 'solve.i'
        include 'oborg.i'
        include 'f77_zmq.h'
        include 'variables_client.i'
        !integer(ZMQ_PTR)        context
        !integer(ZMQ_PTR)        requester
        !character*(64)          address
        integer, dimension(22) :: i_buffer
        integer                  i_rc
        integer                  i_lbuf, i_sbuf, i, i_obsNumber, i_blocksize

        !address = 'tcp://localhost:55555'

        !context   = f77_zmq_ctx_new()
        !requester = f77_zmq_socket(context, ZMQ_REQ)
        !i_rc = f77_zmq_connect(requester, address)


        i_lbuf = size(i_buffer)
        i_sbuf = i_lbuf * 4

        i_buffer(1) =4
        i_buffer(2) = i_obsNumber
        i_rc = f77_zmq_send(requester, i_buffer, i_sbuf, 0)

        ! Find size of commonblock. add 2 for  size of ILAST_OBORG_I2
        i_blocksize = loc(ILAST_OBORG_I2)-loc(FJD) + 2

        ! Receive acknowledgement, now ready to send
        i_rc = f77_zmq_recv(requester, i_buffer, i_sbuf, 0)

        ! Send commonblock
        i_rc = f77_zmq_send(requester, FJD, i_blocksize, 0)

        i_rc = f77_zmq_recv(requester, i_buffer, i_sbuf, 0)

      end
