program name
use iso_c_binding, only: C_CHAR, C_NULL_CHAR, C_INT
implicit none

    ! type declaration statements
    character query
    integer calc, ans

    interface
        subroutine client(ipaddr, portnum) bind(C, name="client")
            use iso_c_binding, only: c_char, c_int
            character(kind=c_char) :: ipaddr(*)
            integer(kind=c_int), value :: portnum
        end subroutine client
    end interface

    interface
        integer(c_int) function calc(indata) bind(C, name="calc")
            use iso_c_binding, only: c_char
            character(kind=c_char) :: indata(*)
        end function calc
    end interface

    ! executable statements
    call client(C_CHAR_"localhost"//C_NULL_CHAR,55555)
    ans = calc(C_CHAR_"1 2 add"//C_NULL_CHAR)
    print *, ans

end program name

