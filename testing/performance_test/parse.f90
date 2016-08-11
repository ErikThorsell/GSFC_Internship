program parse
implicit none

	character*30 :: testString, string1, string2, delim
	character*30, dimension (:), allocatable :: ansArray
	integer :: count, length, nargs, pos, i
	count = 1
	nargs = 1
	pos = 1
	delim = ' ' 
	testString = "1 2 3     hej 8 9 6 add"

	length = LEN_Trim(testString)

	do i=1,length
		pos = SCAN(testString(i:length), delim)
			if (pos==1) then
				nargs=nargs+1
			end if
	end do

	print *, "Succes! nargs equals: ", nargs

	allocate(ansArray(nargs))

	do i=1,nargs

		if (SCAN(testString,' ')/=0) then
			call split_string(testString, string1, string2, delim)
			ansArray(count) = string1
			testString = string2
			count=count + 1
		end if
		print *, ansArray(i)
	end do



	

end program parse

! Subroutine for splitting a string into two parts at first occurance of delimeter
SUBROUTINE split_string(instring, string1, string2, delim)
    CHARACTER(30) :: instring,delim
    CHARACTER(30),INTENT(OUT):: string1,string2
    INTEGER :: index

    instring = TRIM(instring)

    index = SCAN(instring,delim)
    string1 = instring(1:index-1)
    string2 = instring(index+1:)

END SUBROUTINE split_string