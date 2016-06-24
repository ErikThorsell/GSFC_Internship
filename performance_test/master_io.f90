program master
! Master writes a 10 000 bytes matrix to a file, then slave
! squares all numbers and writes it back to the file.
! Author: Lina Olandersson	
! Date: 2016-06-22
implicit none

integer*2, dimension (100,50) :: matrix     
integer :: i, j

! put integers in matrix and output data into a file 
open(1, file='matrixdata.dat', status='new')  
do i=1,100
	do j = 1, 50
	 	matrix(i, j) = i+j
		write(1,*) matrix(i, j) 
    end do   
end do     
close(1) 

call slave

! open and read the file changed by subroutine slave
open(1, file= 'matrixdata.dat', status='old')
do i = 1, 100
	do j = 1, 50
		read(1,*) matrix(i,j)
	end do
end do
close(1)

end program master

! ********************************************************************
subroutine slave
implicit none

integer*2, dimension (100,50) :: matrix
integer :: i,j

! Open and read the file made by master into a matrix
open (1, file= 'matrixdata.dat', status = 'old')
do i = 1, 100
	do j = 1, 50
		read(1,*) matrix(i,j)
	end do
end do
close(1)

! Square all numbers and write over the file with new data
open(1, file= 'matrixdata.dat', status = 'old')
do i=1,100
	do j = 1, 50
		matrix(i,j) = matrix(i,j)**2
		write(1,*) matrix(i, j) 	
   end do   
end do     
close(1) 

end subroutine slave
