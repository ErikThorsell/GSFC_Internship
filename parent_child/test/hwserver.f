      program server
        implicit none
        include 'solve.i'
        include 'oborg.i'
        include 'f77_zmq.h'
        integer(ZMQ_PTR)        context
        integer(ZMQ_PTR)        responder
        character*(64)          address
        integer, dimension(22) :: i_buffer
        integer, dimension(20) :: i_array1, i_array2, i_array3
        integer                 i_rc, i_sbuf, i, i_lbuf, c, i_blocksize
        integer, dimension(20) :: x, y, z
        
        !allocate(i_buffer(3))
        i_lbuf = size(i_buffer)
        i_sbuf = i_lbuf*4
!        do i=1,(i_lbuf-2)
!            i_array1(i) = 11
!            i_array2(i) = 12
!            i_array3(i) = 13
!        enddo

        !Make inputfile
        call execute_command_line('rm -- data.dat')

        do i = 1, 20
            x(i)=1
            y(i)=2
            z(i)=3
        enddo


        open(1, file='data.dat', status='new')
        do i=1,20
           write(1,*) x(i), y(i), z(i)
        end do
        close(1)

        open(1, file='data.dat', status='old')
        do i = 1,20
            read(1,*) i_array1(i), i_array2(i), i_array3(i)
        enddo
        close(1)





        address = 'tcp://*:55555'

        context   = f77_zmq_ctx_new()
        responder = f77_zmq_socket(context, ZMQ_REP)
        i_rc        = f77_zmq_bind(responder,address)

        call execute_command_line("./hwclient", wait=.false.)

        ! Find size of commonblock, add 2 for size of ILAST_OBORG_I2
        i_blocksize = loc(ILAST_OBORG_I2)-loc(FJD) + 2

        print *,  "Waiting for Child to ack its existence. i_rc: ", i_rc
        i_rc = f77_zmq_recv(responder, i_buffer, i_sbuf, 0) ! 2
        print *,  'Received ack from Child. i_rc: ', i_rc

        ! i_buffer(1) = 9 will be used as an ack throughout the program.
        ! ZeroMQ does not allow consecuetive sends/recvs, why each send has to
        ! be followed by a recv as seen below.
        i_buffer(1) = 9
        i_rc = f77_zmq_send(responder, i_buffer, i_sbuf, 0) ! 4

      do while(.true.)
        print *,  'Waiting for Child to perform operation. i_rc: ', i_rc
        i_rc = f77_zmq_recv(responder, i_buffer, i_sbuf, 0) ! 6
        print *, "Received operation code: ", (i_buffer(1:2))

        select case (i_buffer(1))
          case (1)
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

          case (2)
            print *, "Child asked Parent to get i_array", i_buffer(2)
            c = i_buffer(2)
            i_buffer(1) = 9
            i_rc = f77_zmq_send(responder, i_buffer, i_sbuf, 0)
            print *, "Parent acked that data can be sent. i_rc: ", i_rc
            i_rc = f77_zmq_recv(responder, i_buffer, i_sbuf, 0)
            !do i=3,(i_lbuf)
            !  print *, i_buffer(i)
            !enddo
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

          case(3)
            print *, "Child asked parent to send commonblock for obs:"
            print *, i_buffer(2)
            c=i_buffer(2)
            i_buffer(1) = 9

            ! Assign values to forst and last entries for sanity check
            FJD = 1
            ILAST_OBORG_I2 = 999

            print *, "FJD: ", FJD
            print *, "ILAST_OBORG_I2: ", ILAST_OBORG_I2

            ! Send commonblock to child
            i_rc = f77_zmq_send(responder, FJD, i_blocksize, 0)

          case(4)
            print *, "Child wants to send common block for obs:"
            print *, i_buffer(2)
            c=i_buffer(2)
            i_buffer(1) = 9

            ! Acknomledgement, ready to receive again
            i_rc = f77_zmq_send(responder, i_buffer, i_sbuf, 0)

            ! Receive commonblock
            i_rc = f77_zmq_recv(responder, FJD, i_blocksize, 0)

            print *, "FJD: ", FJD
            print *, "ILAST_OBORG_I2: ", ILAST_OBORG_I2

            ! Acknowledge that transfer is done.
            i_buffer(1) = 9
            i_rc = f77_zmq_send(responder, i_buffer, i_sbuf, 0)

          case(5)
          case(6)
          case(7)
            i_buffer(1) = 9
            print *, "Child is done with its operations."
            i_rc = f77_zmq_send(responder, i_buffer, i_sbuf, 0 )
            exit
        end select
      enddo

        !if (i_buffer(1:i_rc) /= 'end') then
        !  print *, "Child asked for: ",
        !  i_rc = f77_zmq_send (responder, "world", 5, 0)
        !else
        !  i_rc = f77_zmq_send (responder, "end", 3, 0)
        !  exit
        !endif
      !enddo

        i_rc = f77_zmq_close(responder)
        i_rc = f77_zmq_ctx_destroy(context)
        !deallocate(i_buffer)
      end


