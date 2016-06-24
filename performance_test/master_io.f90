program master
! Master writes a 10 000 bytes matrix to a file, then slave
! squares all numbers and writes it back to the file.
! Author: Lina Olandersson  
! Date: 2016-06-22
implicit none

integer*4, dimension (2500) :: matrix     
integer :: length, i

! put integers in matrix and output data into a file 
open(1, file='matrixdata.dat', status='new')

length = 2500

do i=1,length
    matrix(i) = i
    write(1,*) matrix(i)
end do

close(1)

call slave

! open and read the file changed by subroutine slave
open(1, file= 'matrixdata.dat', status='old')
do i = 1, 100
    read(1,*) matrix(i)
end do
close(1)

end program master

! ********************************************************************
subroutine slave
implicit none

integer*4, dimension (2500) :: matrix
integer :: length, i

! Open and read the file made by master into a matrix
open (1, file= 'matrixdata.dat', status = 'old')
length = 2500

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

end subroutine slave
