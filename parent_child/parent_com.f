subroutine zmq_com()
 
       use obs_buffer
       use vgosDB_solve

implicit none

! 1. ZMQ_COM PROGRAM SPECIFICATION
!
!
!**********************************************************************  
!*                                                                    *
!* Routine ZMQ_COM is used for communication between programs using   *
!* the ZeroMQ library. Used on the parent side of communication       *
!*                                                                    * 
!* Beginns with initiating the connection to the child program and    *
!* then listens for commands sent in c_buffer. Parent is of type      *
!* ZMQ_REP and must start with a receive command. Then alternating    *
!* between send and receive.                                          *
!*                                                                    *
!* Can listen for commands:                                           *
!*                                                                    * 
!* send: sends specified common block to child                        *
!*                                                                    * 
!* recv: receives specified common block from child                   *
!*                                                                    *
!* stop: closes and destroys connection                               *
!*                                                                    *
!**********************************************************************
!
! 2. ZMQ_COM Program Interface
! 
! 2.1 Parameter File

INCLUDE  'f77_zmq.h'  !Enable ZMQ funcionality

! 2.2 Input Variables
! 
! 2.3 Output variables
!
! 2.4 Common Blocks used

INCLUDE  'solve.i'
INCLUDE  'precm.i'
INCLUDE  'erm.i'
INCLUDE  'socom.i'
INCLUDE  'socom_plus.i'
INCLUDE  'batcm.i'
INCLUDE  'ba2cm.i'
INCLUDE  'glbcm.i'
INCLUDE  'glbc3.i'
INCLUDE  'glbc4.i'
INCLUDE  'dmapp.i'
INCLUDE  'prfil.i'
INCLUDE  'glbp.i'
INCLUDE  'cnstr.i'
INCLUDE  'fast.i'
INCLUDE  'gvh.i'

! 3.Local Variables

! ZMQ Functions
integer(ZMQ_PTR) context, parent
integer f77_zmq_ctx_new_
integer f77_zmq_socket_
integer f77_zmq_bind_
integer f77_zmq_recv_
integer f77_zmq_send_
integer f77_zmq_close_
integer f77_zmq_ctx_destroy_

! Variables
character*64 address
integer i_rc, i_lengthbuff, i_sizebuff, i_blocksize, obsNum, i_obssize, i_buffer(3), i_oborg_vert, i_oborg_hor
character*48 c_buffer, sink

! 4. History
!  WHO      WHEN        WHAT
!  interns  2016-07-22  Wrote program

! 5.ZMQ_COM Program Structure


! Initializing communication between child and
! parent. Child started with "call system(...)"
! outside of this file. 

    address = 'tcp://*:55556'
    context = f77_zmq_ctx_new_()
    parent  = f77_zmq_socket_(context, ZMQ_REP)
    i_rc    = f77_zmq_bind_(parent, address)
    i_sizebuff = len(c_buffer)

    !print *, "Waiting for child to ack its existence"
    i_rc = f77_zmq_recv_(parent, sink, i_sizebuff, 0)
    !print *, "Received akc from Child. i_rc: ", i_rc
    i_rc = f77_zmq_send_(parent, "Parent is ready", i_sizebuff, 0)

    i_obssize = sizeof(iobs_buffer)
    i_oborg_hor  = size(iobs_buffer, 1)
    i_oborg_vert  = size(iobs_buffer, 2)
    i_buffer(1) = i_obssize
    i_buffer(2) = i_oborg_hor
    i_buffer(3) = i_oborg_vert

    !print *, i_buffer

    ! Parent receivs action from child.
    do while(.true.)
    i_rc = f77_zmq_recv_(parent, c_buffer, i_sizebuff, 0)
    !print *, "Received ", c_buffer

    ! Depending on the content of c_buffer parent will do different things.
    select case (c_buffer(1:4))

    case('send') ! Corresponds to the subroutine sendObsName
    !print *, "Child asked parent to send commonblock:",&
    !             & c_buffer(6:10)

                 select case (c_buffer(6:10))
                    case('oborg')
                     ! read obsNum from c_buffer to obsNum. Only done for block oborg.i   
                     !print *, "Child asked parent to send obsNum", obsNum
                     i_rc = f77_zmq_send_(parent, i_buffer, sizeof(i_buffer), 0)
                     i_rc = f77_zmq_recv_(parent, sink, i_sizebuff, 0)
                     i_rc = f77_zmq_send_(parent, iobs_buffer, i_obssize, 0)

                     case('prfil')
                     ! Find size of the common block, add 2 for size of ILAST_PRFIL_I2
                     i_blocksize = loc(ILAST_PRFIL_I2)-loc(VAXOF) + 2
                     i_rc = f77_zmq_send_(parent, VAXOF, i_blocksize, 0)

                     case('socom')
                     ! Find size of the common block, add 2 for size of SOCOM_LAST_I2
                     i_blocksize = loc(SOCOM_LAST_I2)-loc(PI_VAR) + 2
                     i_rc = f77_zmq_send_(parent, PI_VAR, i_blocksize, 0)

                     case('glbc4')
                     ! Find size of the common block, add 4 for size of ENDMARK_GLBC4_I4
                     i_blocksize = loc(ENDMARK_GLBC4_I4)-loc(BEGMARK_GLBC4_I4) + 4
                     i_rc = f77_zmq_send_(parent, BEGMARK_GLBC4_I4, i_blocksize, 0)

                     case('precm')
                     ! Find size of the common block, add 4 for size of TEST_FIELD
                     i_blocksize = loc(TEST_FIELD)-loc(DBH_PROG) + 4
                     i_rc = f77_zmq_send_(parent, DBH_PROG, i_blocksize, 0)

                     ! Acknowledgement: Child ready to receive second commonblock from precm
                     i_rc = f77_zmq_recv_(parent, c_buffer, i_sizebuff, 0)

                     ! Find size of second block and send that
                     i_blocksize = loc(PRE_SPL_NAM)-loc(PRE_SCR_DIR) + 128
                     i_rc = f77_zmq_send_(parent, PRE_SCR_DIR, i_blocksize, 0)

             end select

             case('recv') ! Corresponds to the subroutine getCommon
                 !print *, "Child to send common block: ",&
                 !& c_buffer(6:10)
                 !print *, c_buffer(6:10)

                 ! Acknomledgement, ready to receive again
                 i_rc = f77_zmq_send_(parent, "Parent ready to recieve", i_sizebuff, 0)

                 ! Receive commonblock
                 select case (c_buffer(6:10))
                     ! Will not use case oborg. Not interested in sending oborg to parent. oborg only used in child.
                     case('oborg')
                     read(c_buffer(12:16),'(I5)')  obsNum
                     !print *, "OBSNUM IN PARENT", obsNum
                     i_blocksize = 2550
                     ! FUNGERAR INTE ATT LAGRA IN I ARRAY SA HAR!!
                     i_rc = f77_zmq_recv_(parent, iobs_buffer(1,obsNum), i_blocksize, 0)
                     !print *, "PARENTS OBORG VARIABLES", iobs_buffer(1,1), &
                     !& iobs_buffer(1,2)

                     case('prfil')
                     ! Find size of the common block, add 2 for size of ILAST_PRFIL_I2
                     i_blocksize = loc(ILAST_PRFIL_I2)-loc(VAXOF) + 2
                     i_rc = f77_zmq_recv_(parent, VAXOF, i_blocksize, 0)

                     case('socom')
                     ! Find size of the common block, add 2 for size of SOCOM_LAST_I2
                     i_blocksize = loc(SOCOM_LAST_I2)-loc(PI_VAR) + 2
                     i_rc = f77_zmq_recv_(parent, PI_VAR, i_blocksize, 0)

                     case('glbc4')
                     ! Find size of the common block, add 4 for size of ENDMARK_GLBC4_I4
                     i_blocksize = loc(ENDMARK_GLBC4_I4)-loc(BEGMARK_GLBC4_I4) + 4
                     i_rc = f77_zmq_recv_(parent, BEGMARK_GLBC4_I4, i_blocksize, 0)

                     case('precm')
                     ! Find size of the common block, add 4 for size of TEST_FIELD
                     i_blocksize = loc(TEST_FIELD)-loc(DBH_PROG) + 4
                     i_rc = f77_zmq_recv_(parent, DBH_PROG, i_blocksize, 0)

                     ! Acknowledgement: Parent ready to receive second commonblock in precm
                     i_rc = f77_zmq_send_(parent, c_buffer, i_sizebuff, 0)

                     ! Find size of the commonblock, add 128 for the size of last element, and receive it from child.
                     i_blocksize = loc(PRE_SPL_NAM)-loc(PRE_SCR_DIR) + 128
                     i_rc = f77_zmq_recv_(parent, PRE_SCR_DIR, i_blocksize, 0)

                     !print *,'Received elements: ', PRE_SPL_NAM, TEST_FIELD
             end select

                 ! Acknowledge that transfer is done.
                 i_rc = f77_zmq_send_(parent, "Transfer is done", i_sizebuff, 0)

             case('stop') ! Corresponds to the subroutine closeParent
                 !print *, "Child is done."
                 i_rc = f77_zmq_send_(parent, "Parent closing connection", i_sizebuff, 0 )

                 ! Close and destroy connection to child
                 i_rc = f77_zmq_close_(parent)
                 i_rc = f77_zmq_ctx_destroy_(context)
                 exit
         end select
       enddo
 end

