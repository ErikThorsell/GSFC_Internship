program name
implicit none

    ! type declaration statements
    integer, pointer :: p1, p2
    integer, target :: t

    ! executable statements
    p1 => t
    p2 => t
    p1 = 1
    print *, p1, p2, t

    p1 = p1 + 1
    print *, p1, p2, t

    t = 3
    print *, p1, p2, t

end program name

