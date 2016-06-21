program name
use iso_c_binding, only: C_CHAR, C_NULL_CHAR, C_INT
implicit none

    ! type declaration statements
    character*255 query
    integer calc, ans

    interface
        subroutine client(ipaddr, portnum) bind(C, name="client")
            use iso_c_binding, only: c_char, c_int
            character(kind=c_char) :: ipaddr(*)
            integer(kind=c_int), value :: portnum
        end subroutine client
    end interface

    interface
        function calc(indata) bind(C, name="calc") result (ans)
            use iso_c_binding, only: c_char
            character(kind=c_char) :: indata(*)
        end function calc
    end interface

    ! executable statements
    ans = 0
    call client(C_CHAR_"localhost"//C_NULL_CHAR,55555)
    print *, "What would you like to sum? (Usage: m n ... add)"
    read (*,'(A)') query
    ans = calc(query//C_NULL_CHAR)
    print *, ans
    print *, "The answer is: ", ans+1

end program name

