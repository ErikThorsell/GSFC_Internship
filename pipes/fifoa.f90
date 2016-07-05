program testfifoa
    implicit none

    integer(4), dimension(400000/4) :: array
    integer :: length, i, exitstatus, j
    length = size(array)

    open(1, file="test1.pipe", form="formatted", status="old", action="read")
    open(2, file="test2.pipe", form="formatted", status="old", action="write")

do j=1,1000

    do i=1,length
        array(i) = 2
    end do

    write(2,*) array
    flush(2)

    if(exitstatus .eq. 0) then
        read(1,*) array
    endif

   ! do i=1,length
   !     print *, "Print in server:", array(i)
   ! enddo

enddo

    close(2)
    close(1)

end program testfifoa

