program testfifoa
    implicit none

    integer(4), dimension(2500) :: array
    integer :: length, i
    length = 2500

    open(1, file="test1.pipe", form="formatted", status="old", action="write")
    open(2, file="test2.pipe", form="formatted", status="old", action="read")

    do i=1,length
        array(i) = i
    end do

    write(1,*) array
    flush(1)

    read(2,*) array

    close(1)
    close(2)

end program testfifoa

