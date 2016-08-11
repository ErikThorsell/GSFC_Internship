program calling_func
implicit none

   integer*8 :: i, f, myfactorial
   print *, "Enter your number please:"
   read *, i

   print *, "The value of factorial", i, "is"
   f = myfactorial(i)
   Print *, f

end program calling_func

! computes the factorial of n (n!)
recursive function myfactorial (n) result (fac)
! function result
implicit none

   ! dummy arguments
   integer*8 :: fac
   integer*8, intent (in) :: n

   select case (n)
      case (0:1)
         fac = 1
      case default
         fac = n * myfactorial (n-1)
   end select

end function myfactorial
