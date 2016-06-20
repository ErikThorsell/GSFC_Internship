program name
implicit none

    ! type declaration statements
    character indata, ipaddr, ans, calc
    integer portno
    indata = "INDATA"
    ipaddr = "localhost"
    portno = 55555

    ! executable statements
    print *, indata
    ans = calc(indata, ipaddr, portno)
    print *, ans

end program name

