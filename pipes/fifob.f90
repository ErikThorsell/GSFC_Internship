program testfifoa
    implicit none

    integer(4), dimension(400000/4) :: array
    integer :: length, i, exitstatus, j
    length = size(array)

    call execute_command_line("./fifoa.out", wait=.false., exitstat=exitstatus)

    open(1, file="test1.pipe", form="formatted", status="old", action="write")
    open(2, file="test2.pipe", form="formatted", status="old", action="read")

do j=1,1000

    read(2,*) array

    do i=1,length
        array(i)=array(i)**2
    end do

    !do i=1,length
    !    print *, array(i)+1
    !enddo

    write(1,*) array
    flush(1)

enddo

    close(2)
    close(1)

end program testfifoa

