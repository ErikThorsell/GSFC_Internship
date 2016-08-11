program slave
implicit none

    integer*4, dimension (2000000/4) :: matrix
    integer :: length, i

    ! Open and read the file made by master into a matrix
    open (1, file= 'matrixdata.dat', status = 'old')
    length = size(matrix)

    do i = 1, length
        read(1,*) matrix(i)
    end do
    close(1)

    ! Square all numbers and write over the file with new data
    open(1, file= 'matrixdata.dat', status = 'old')
    do i=1,length
        matrix(i) = matrix(i)**2
        write(1,*) matrix(i)
    end do
    close(1)

end program slave
