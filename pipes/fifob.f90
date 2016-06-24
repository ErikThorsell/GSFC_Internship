program testfifoa
    implicit none

    integer(4), dimension(2500) :: array
    integer :: length, i
    length = 2500

    open(1, file="test1.pipe", form="formatted", status="old", action="read")
    open(2, file="test2.pipe", form="formatted", status="old", action="write")

    read(1,*) array

    do i=1,length
        array(i)=array(i)**2
    end do

    write(2,*) array
    flush(2)

    close(1)
    close(2)

end program testfifoa

