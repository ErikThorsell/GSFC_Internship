! ########################################################################### !
! child.f                                                                    !
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
program child
    implicit none

    include 'solve.i'             ! Includes parameters used by oborg.i
    include 'oborg.i'             ! Includes the common block used for testing
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
        i_buffer(i) = 0
    enddo

    ! Fill the arrays with arbitrary numbers. The arrays hold two less elements
    ! since the buffer carries two control bits (buffer(1), buffer(2)).
    do i=1, (i_lbuf-2)
        i_array1(i) = 21
        i_array2(i) = 22
        i_array3(i) = 23
    enddo

    ! Invoke the program, l 121
    call init(i_buffer, i_rc)

    ! Due to the nature of the program, a loop is used to provide the opportunity
    ! to test all functions. When used in production, a program would be written
    ! that makes use of the subroutines, with no need for human interaction.
    do while (.true.)
        if ((i_buffer(1) .eq. 9) .and. (i_rc .ge. 0)) then
            print *, "All is good, please chose between the options below:"
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
                    print *, "Which array do you want parent to send (1-3)?"
                    read(*,*) buffNumber
                    call send(buffNumber, i_buffer)
                    print *, "Control data: ", i_buffer(1), i_buffer(2)
                    print *, "Actual data: "
                    do i=3,i_lbuf
                        print *, i_buffer(i)
                    enddo

                case (2)
                    print *,"Which array do you want to Parent to recieve (1-3)?"
                    read(*,*) buffNumber
                    print *, "Child wants parent to get array: ", buffNumber
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
                    print *,"Which observation's common block would you like parent to send?"
                    print *, "Must choose 1 for now"
                    read(*,*) i_obsNumber
                    call sendObsN(i_buffer, i_obsNumber)

                case (4)
                    print *, "Which observation's common block would you like parent to recieve?"
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
            print *, "Something went wrong. i_buffer(1) = ", i_buffer(1), ", i_rc: ", i_rc
        endif
    enddo

    i_rc = f77_zmq_close(requester)
    i_rc = f77_zmq_ctx_destroy(context)

end


! ############################## Subroutines ################################ !
! The general subroutine works as follows:
! The child will call a subroutine which is associated with some functionality
! provided by the parent. The number associated with the subroutine will be put
! in buffer(1) and possibly buffer(2) and the parent will parse the buffer in
! order to determine how to respond to the data.
!
! It's basically just a big case select.

! *************************************************************************** !
! Establish the connection between the child and its parent.
!
subroutine init(i_buffer, i_rc)
  implicit none
  include 'f77_zmq.h'
  include 'variables_client.i'
  integer, dimension(22) :: i_buffer
  integer, dimension(20) :: i_array1, i_array2, i_array3
  integer                 i_rc
  integer                 i, i_lbuf, c, i_sbuf, buffNumber

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

! *************************************************************************** !
! Tell parent to send buffNumber to the child. buffNumber is an integer [1,3]
! and tells the parent which of three arrays to send the child.
!
subroutine send(buffNumber, i_buffer)
  implicit none
  include 'f77_zmq.h'
  include 'variables_client.i'
  integer, dimension(22) :: i_buffer
  integer                 i_rc
  integer                 i, i_lbuf, c, i_sbuf, buffNumber

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

!*****************************************************************
! Tell parent that the child will send i_array.
!
subroutine get(buffNumber, i_buffer, i_array)
  implicit none
  include 'f77_zmq.h'
  include 'variables_client.i'
  integer, dimension(22) :: i_buffer
  integer, dimension(20) :: i_array
  integer                 i_rc
  integer                 i, i_lbuf, c, i_sbuf, buffNumber

  i_lbuf = size(i_buffer)
  i_sbuf = i_lbuf * 4

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

! *************************************************************************** !
! Tell parent to send the common block associated with i_obsNumber to the child.
!
subroutine sendObsN(i_buffer, i_obsNumber) ! CASE 3
  implicit none
  include 'solve.i'
  include 'oborg.i'
  include 'f77_zmq.h'
  include 'variables_client.i'
  integer, dimension(22) :: i_buffer
  integer                  i_rc
  integer                  i_lbuf, i_sbuf, i, i_obsNumber, i_blocksize

  i_lbuf = size(i_buffer)
  i_sbuf = i_lbuf * 4


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

! *************************************************************************** !
! Tell the parent that the common block associated with i_obsNumber will be sent.
!
subroutine getobsN(i_buffer, i_obsNumber)
  implicit none
  include 'solve.i'
  include 'oborg.i'
  include 'f77_zmq.h'
  include 'variables_client.i'
  integer, dimension(22) :: i_buffer
  integer                  i_rc
  integer                  i_lbuf, i_sbuf, i, i_obsNumber, i_blocksize


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

!*****************************************************************
! Tell parent that child wants to terminate the connection.
!
subroutine closeParent(i_buffer)

  implicit none
  include 'f77_zmq.h'
  include 'variables_client.i'
  integer, dimension(22) :: i_buffer
  integer                 i_rc
  integer, dimension(8) :: t
  integer                 ms1, ms2, i_lbuf, i_sbuf, i
  real                    dt

  i_lbuf = size(i_buffer)
  i_sbuf = i_lbuf * 4

  i_buffer(1) = 7

  ! Tell parent that child is done
  i_rc = f77_zmq_send(requester, i_buffer, i_sbuf, 0)
  ! Receive confirmation from parent
  i_rc = f77_zmq_recv(requester, i_buffer, i_sbuf ,0)

end

