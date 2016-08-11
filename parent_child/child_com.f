module child_com
implicit none

    integer*2, allocatable :: iobs_buffer(:,:)

! BEGINNING OF FILE child_com.f !
!
! Contains subroutines: connectToParent()
!                       sendCommon()
!                       getCommon()
!                       sendOborg()
!                       getOborg() - not functional
!                       closeChild()
!
! Written by the Swedish interns: 2016-07-22 (yes, it only took us one day)
!
!
!
contains
!*****************************************************************
! Open connection to parent.
subroutine connectToParent()
    implicit none
    include '/home/erik/f77_zmq.h'
    include 'zmq_common.i'
    integer i_rc, i_buffsize
    character*48 sink

    ! Declare ZMQ related variables.
    ! address contains the address user_part wants to connect to.
    !
    ! f77_zmq_ctx_new_() returns a context, which acts as the container
    ! for all connections between the processes.
    !
    ! f77_zmq_socket_() returns a socket of type REQUESTER, contained in
    ! the context. The requester (as opposed to the RESPONDER in
    ! prces.f) must start by sending a message (as opposed to receiving)
    !
    ! f77_zmq_connect_() connects the child to the parent and returns 0
    ! if all went well.
    !
    address = 'tcp://localhost:55556'
    context = f77_zmq_ctx_new_()
    child   = f77_zmq_socket_(context, ZMQ_REQ)
    i_rc    = f77_zmq_connect_(child, address)
    !print *, "Initialization in parent completed."

    if(.not. (i_rc .eq. 0)) then
        print *, "ZMQ failed to establish connection! i_rc = ", i_rc
    endif

    i_buffsize = len(sink)

    !print *, "Sending ack to parent."
    i_rc = f77_zmq_send_(child, "ack", i_buffsize, 0)
    i_rc = f77_zmq_recv_(child, sink, i_buffsize, 0)
    !print *, "Child received: ", sink
end subroutine


! *************************************************************************** !
! Tell parent to send the common block associated with i_obsNumber to the child.

subroutine sendCommon(name)
    implicit none
    include 'solve.i'
    include 'oborg.i'
    include 'prfil.i'
    include 'socom.i'
    include 'glbc4.i'
    include 'precm.i'
    include '/home/erik/f77_zmq.h'
    include 'zmq_common.i'
    character*(48)           c_buffer
    character*(5)            name
    integer                  i_rc
    integer                  i_buffsize, i_obsNumber, i_blocksize

    validCommonBlocks = "prfil socom glbc4 precm"

    if( index (validCommonBlocks,  name) .eq. 0) then
        return
    endif

    i_buffsize = len(c_buffer)
    c_buffer = "send "//name
    !print *, "c_buffer before send to parent: ", c_buffer
    i_rc = f77_zmq_send_(child, c_buffer, i_buffsize, 0)

    select case (c_buffer(6:10))

        case('prfil')
            ! Find size of commonblock. add 2 for  size of ILAST_PRFIL_I2
            i_blocksize = loc(ILAST_PRFIL_I2)-loc(VAXOF) + 2
            i_rc = f77_zmq_recv_(child, VAXOF, i_blocksize, 0)
            !PRINT *, 'prfil variables:', VREL, PWCFNAME

        case('socom')
            ! Find size of commonblock. add 2 for  size of SoCOM_LAST_I2
            i_blocksize = loc(SOCOM_LAST_I2)-loc(PI_VAR) + 2
            i_rc = f77_zmq_recv_(child, PI_VAR, i_blocksize, 0)
            !PRINT *, 'socom variables:', LOGBCL, PI_VAR

        case('glbc4')
            ! Find size of commonblock. add 4 for  size of ENDMARK_GLBC4_I4
            i_blocksize = loc(ENDMARK_GLBC4_I4)-loc(BEGMARK_GLBC4_I4) + 4
            i_rc = f77_zmq_recv_(child, BEGMARK_GLBC4_I4, i_blocksize, 0)
            !print *, 'glbc4 variables', endmark_glbc4_i4!, sitdif

        case('precm')
            ! Find size of commonblock. add 4 for  size of TEST_FIELD
            i_blocksize = loc(TEST_FIELD)-loc(DBH_PROG) + 4
            i_rc = f77_zmq_recv_(child, DBH_PROG, i_blocksize, 0)

            i_rc = f77_zmq_send_(child, c_buffer, i_buffsize, 0)

            ! Find size of commonblock. add 128 for  size of PRE_SPL_NAM
            i_blocksize = loc(PRE_SPL_NAM)-loc(PRE_SCR_DIR) + 128
            i_rc = f77_zmq_recv_(child, PRE_SCR_DIR, i_blocksize, 0)

            !print *, 'precm variables:', pre_sv_len, pre_scr_dir

    end select
end subroutine

! *************************************************************************** !
! Tell the parent that the common block associated with i_obsNumber will be sent.
!
subroutine getCommon(name)
  implicit none
  include 'solve.i'
  include 'oborg.i'
  include 'prfil.i'
  include 'socom.i'
  include 'glbc4.i'
  include 'precm.i'
  include '/home/erik/f77_zmq.h'
  include 'zmq_common.i'
  character*(48)           c_buffer, sink
  character*(5)            name
  integer                  i_rc
  integer                  i_buffsize, i_obsNumber, i_blocksize

  validCommonBlocks = "prfil socom glbc4 precm"

  if( index (validCommonBlocks,  name) .eq. 0) then
      return
  endif

  i_buffsize = len(c_buffer)
  c_buffer = "recv "//name
  print *, "c_buffer before send to parent: ", c_buffer

  i_rc = f77_zmq_send_(child, c_buffer, i_buffsize, 0)

  ! Receive acknowledgement, now  ready to send
  i_rc = f77_zmq_recv_(child, sink, i_buffsize, 0)

    select case (c_buffer(6:10))
        case('prfil')
            ! Find size of commonblock. add 2 for  size of ILAST_PRFIL_I2
            i_blocksize = loc(ILAST_PRFIL_I2)-loc(VAXOF) + 2
            i_rc = f77_zmq_send_(child, VAXOF, i_blocksize, 0)

        case('socom')
            ! Find size of commonblock. add 2 for  size of SOCOM_LAST_I2
            i_blocksize = loc(SOCOM_LAST_I2)-loc(PI_VAR) + 2
            i_rc = f77_zmq_send_(child, PI_VAR, i_blocksize, 0)

        case('glbc4')
            ! Find size of commonblock. add 4 for  size of ENDMARK_GLBC4_I4
            i_blocksize = loc(ENDMARK_GLBC4_I4)-loc(BEGMARK_GLBC4_I4) + 4
            i_rc = f77_zmq_send_(child, BEGMARK_GLBC4_I4, i_blocksize, 0)

        case('precm')
            TEST_FIELD = 555
            PRE_SPL_NAM = 'This is a message!!'
            ! Find size of commonblock. add 4 for  size of TEST_FIELD
            i_blocksize = loc(TEST_FIELD)-loc(DBH_PROG) + 4
            i_rc = f77_zmq_send_(child, DBH_PROG, i_blocksize, 0)

            i_rc = f77_zmq_recv_(child, c_buffer, i_buffsize, 0)

            ! Find size of commonblock. add 128 for  size of PRE_SPL_NAM
            i_blocksize = loc(PRE_SPL_NAM)-loc(PRE_SCR_DIR) + 128
            i_rc = f77_zmq_send_(child, PRE_SCR_DIR, i_blocksize, 0)

        case default
            i_rc = f77_zmq_send_(child, "invalid input to getCommon()", i_buffsize, 0)

      end select

  i_rc = f77_zmq_recv_(child, sink, i_buffsize, 0)

end subroutine

!****************************************************************
! Tells parent to send observation number obsNum to child
subroutine sendOborg()
    implicit none
    include 'solve.i'
    include 'oborg.i'
    include 'prfil.i'
    include 'socom.i'
    include 'glbc4.i'
    include 'precm.i'
    include '/home/erik/f77_zmq.h'
    include 'zmq_common.i'
    character*(48)           c_buffer
    integer                  obsNum
    integer                  i_rc
    integer                  i_buffsize, i_obsNumber, i_blocksize, i_buffer(3), i_obssize, i_oborg_hor, i_oborg_vert
    !integer*2, allocatable :: iobs_buffer(:,:)

    i_buffsize = len(c_buffer)
    write(c_buffer, '(A11, I5)') 'send oborg '

    i_rc = f77_zmq_send_(child, c_buffer, i_buffsize, 0)
    !print *, "Sent -send oborg- to parent."

    if(allocated(iobs_buffer)) then
        deallocate(iobs_buffer)
    endif

    i_rc = f77_zmq_recv_(child, i_buffer, sizeof(i_buffer), 0)

    i_obssize = i_buffer(1)
    i_oborg_hor  = i_buffer(2)
    i_oborg_vert = i_buffer(3)

    allocate(iobs_buffer(i_oborg_hor, i_oborg_vert))

    i_rc = f77_zmq_send_(child, "dummy", i_buffsize, 0)

    i_rc = f77_zmq_recv_(child, iobs_buffer, i_obssize, 0)
    !print *, 'oborg variables:', FJD, FRACT
end subroutine

!***********************************************************
! Sends observation number obsNum to parent
 subroutine getOborg(obsNum)
    implicit none
    include 'solve.i'
    include 'oborg.i'
    include 'prfil.i'
    include 'socom.i'
    include 'glbc4.i'
    include 'precm.i'
    include '/home/erik/f77_zmq.h'
    include 'zmq_common.i'
    character*(48)           c_buffer, sink
    integer                  obsNum
    integer                  i_rc
    integer                  i_buffsize, i_obsNumber, i_blocksize

    i_buffsize = len(c_buffer)
    write(c_buffer, '(A11,I5)') 'recv oborg ', obsNum

    ! Find size of commonblock. add 2 for  size of ILAST_OBORG_I2
    i_blocksize = loc(ILAST_OBORG_I2)-loc(FJD) + 2

    ! Make parent ready to recieve oborg obsNum
    i_rc = f77_zmq_send_(child, c_buffer, i_buffsize, 0)
    i_rc = f77_zmq_recv_(child, sink, i_buffsize, 0)

    !print *, "OBORG BEFORE SENDING PARENT", FJD, FRACT
    ! Send observation obsNum to parent
    i_rc = f77_zmq_send_(child, FJD, i_blocksize, 0)
    ! Parent recieved observation
    i_rc = f77_zmq_recv_(child, sink, i_buffsize, 0)

 end subroutine

!****************************************************************
! Tell parent that child wants to terminate the connection and
! close the child.

subroutine closeChild()
    implicit none
    include '/home/erik/f77_zmq.h'
    include 'zmq_common.i'
    integer i_rc, i_buffsize
    character*(48) c_buffer, sink

    i_buffsize = len(c_buffer)
    c_buffer = 'stop'

    ! Tell parent that child is done
    i_rc = f77_zmq_send_(child, c_buffer, i_buffsize, 0)
    ! Receive confirmation from parent
    i_rc = f77_zmq_recv_(child, sink, i_buffsize ,0)

    i_rc = f77_zmq_close_(child)
    i_rc = f77_zmq_ctx_destroy_(context)
end subroutine
!
!
! END OF child_com.f !
end module
