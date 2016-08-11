program master
! Master writes a 10 000 bytes matrix to a file, then slave
! squares all numbers and writes it back to the file.
! Author: Lina Olandersson  
! Date: 2016-06-22
implicit none

integer*4, dimension (2000000/4) :: matrix
integer :: length, i, j, exitstatus, cmdstatus, count1, count2
real :: start_time, stop_time
logical :: waistatus

! put integers in matrix and output data into a file 
do j=1,1000
open(1, file='matrixdata.dat', status='old')

length = size(matrix)

do i=1,length
    matrix(i) = 2
    write(1,*) matrix(i)
end do

close(1)

call execute_command_line("./slave.out", wait = .true., exitstat=exitstatus)

if(exitstatus .eq. 0) then
    ! open and read the file changed by subroutine slave
    open(1, file= 'matrixdata.dat', status='old')
    do i = 1, length
        read(1,*) matrix(i)
    end do
    close(1)
endif

enddo

end program master

! ********************************************************************

