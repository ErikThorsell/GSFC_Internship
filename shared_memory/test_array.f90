program name
    use omp_lib
    implicit none

    ! type declaration statements
    real :: d(1000000)
    integer :: flag, i, n
    n = 1000000

    ! executable statements
    do i=1,size(d)
        d(i) = 9
    enddo
    flag = 0

    !$omp parallel num_threads(3)
        if(omp_get_thread_num() .eq. 0) then
            !$omp atomic update
                flag = flag + 1
                call c0(d,n)
        else if(omp_get_thread_num() .eq. 1) then
            !$omp flush(flag, d)
            do while(flag .lt. 1)
                !$omp flush(flag, d)
            enddo

            print *, "Thread 1 awoken."
            call c1(d,n)

            !$omp atomic update
                flag = flag + 1
        else if(omp_get_thread_num() .eq. 2) then
            !$omp flush(flag, d)
            do while(flag .lt. 2)
                !$omp flush(flag, d)
            enddo

            print *, "Thread 2 awoken."
            call c2(d,n)

        end if
    !$omp end parallel

    do i=1,10
        print *, d(i)
    enddo

    do i=10000,10010
        print *, d(i)
    enddo

end program name

subroutine c0(array, n)
    implicit none

    integer :: i, n
    real    :: array(n)

    do i=1,size(array)
        array(i) = 0
    enddo

end subroutine c0

subroutine c1(array, n)
    implicit none

    integer :: i, n
    real    :: array(n)

    do i=1,size(array)
        array(i) = 1
    enddo

end subroutine c1

subroutine c2(array, n)
    implicit none

    integer :: i, n
    real    :: array(n)

    do i=1,size(array)
        array(i) = 2
    enddo

end subroutine c2

