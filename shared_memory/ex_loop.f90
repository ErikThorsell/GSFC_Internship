program name
    use omp_lib
    implicit none

    ! type declaration statements
    integer :: i
    real    :: a(1000000), b(1000000)

    ! executable statements
    do i=1,1000000
        a(i)=i
    enddo
    call loop(a,b)

    do i=1,10
        print *,(b(i))
    enddo
    do i=1000,1010
        print *,(b(i))
    enddo
    do i=99990,100000
        print *,(b(i))
    enddo

end program name

subroutine loop(a, b)

    integer :: i, n
    real    :: a(1000000), b(1000000)

    !$omp parallel do
        do i=2,1000000
            b(i) = (a(i)+a(i-1))/2.0
        enddo
    !$omp end parallel do

end subroutine loop
