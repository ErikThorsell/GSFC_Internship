program calculator_server
! 
! Authors:
!   Lina Olandersson, Simon Strandberg, Erik Thorsell
! Date:
!   2016-06-21
!
! Calculator at the server side of the client/server calculator
! Responsible for starting up the server server.c

use iso_c_binding, only: C_CHAR, C_NULL_CHAR, C_INT
implicit none

    ! type declaration statements
    character(255) query
    integer calc, ans, portnum, calculate

    ! Interface that ensures type compatibility between Fortran and C
    interface
        subroutine server(portnum) bind(C, name="server")
            use iso_c_binding, only: c_int
            integer(kind=c_int), value :: portnum
        end subroutine server
    end interface

    ! Start the server with portnumber read from standard in
    print *, "Please provide me with a port number."
    read "(1i9)", portnum
    call server(portnum)

end program calculator_server


! **********************************************************************

integer(kind=c_int) function calculate(query) bind (C, name="calculate")
! Authors:
!   Lina Olandersson, Simon Strandberg, Erik Thorsell
! Date:
!   2016-06-21
!
! Calculator function. Takes two numbers, an operator and does the calculation

use iso_c_binding, only: C_CHAR, C_NULL_CHAR, C_INT
    implicit none

    ! Variable declarations
    character(kind = C_CHAR, len=1), dimension(255) :: query
    integer length, i, nargs, len, arraysize,k,tmp
    character(255) operator
    character(255), dimension (255) :: inputarray
    nargs = 0
    len = 0
    calculate = 0

    ! Call the parse subroutine to parse the string and put it in an array
    call parse(query, inputarray, nargs)

    ! Check which operator was sent (last part of the input string)
    ! Then choose accordingly and calculate

    operator = inputarray(nargs)

    if (index(operator, "add") /= 0) then
        do k=1, 2
            read (inputarray(k),*) tmp
            calculate = calculate + tmp
        end do
    end if

    if (index(operator, "sub") /= 0) then
        read (inputarray(1),*) tmp
        calculate = tmp
        read (inputarray(2),*) tmp
        calculate = calculate - tmp
    end if

    if (index(operator, "mul") /= 0) then
        calculate = 1
        do k=1, 2
            read (inputarray(k),*) tmp
            calculate = calculate * tmp
        end do
    end if

    if (index(operator, "div") /= 0) then
        read (inputarray(1),*) tmp
        calculate = tmp
        read (inputarray(2),*) tmp
        calculate = calculate/tmp
    end if


end function calculate


! ****************************************************************

subroutine parse(indata, inputarray, nargs)
!
! Author:
!   Simon Strandberg
! Date:
!   2016-06-21
!
! Subroutine to parse a string

implicit none

! Variable declarations
    character(255) :: indata, string1, string2, delim
    character(255), dimension (255) :: inputarray
    integer :: count, length, nargs, pos, i
    count = 1
    nargs = 1
    pos = 1
    delim = ' '

! Check actual length of indata. Not interested in blanks at the end
    length = len_trim(indata)

    indata = (indata(1:length))

! Scan the string for blankspaces to check total number of arguments. 
    do i=1,length
        pos = SCAN(indata(i:length), delim)
        if (pos==1) then
            nargs=nargs+1
        end if
    end do

! Split the indata into an array. All data is still formated as type character.
    do i=1,nargs
        if (SCAN(indata,' ')/=0) then
            call split_string(indata, string1, string2, delim)
            inputarray(count) = string1
            inputarray(count) = trim(inputarray(count))
            indata = string2
            count=count + 1
        end if
    end do

end subroutine parse


! ******************************************************************

SUBROUTINE split_string(instring, string1, string2, delim)
!
! Split function made by ponderomotion
! URL: https://gist.github.com/ponderomotion/3833266

implicit none
    CHARACTER(255) :: instring,delim
    CHARACTER(255),INTENT(OUT):: string1,string2
    INTEGER :: index

    instring = TRIM(instring)

    index = SCAN(instring,delim)
    string1 = instring(1:index-1)
    string2 = instring(index+1:)

END SUBROUTINE split_string

