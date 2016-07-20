      integer(ZMQ_PTR)       context
      integer(ZMQ_PTR)       requester
      character*(64)         address

      COMMON /client_variables/ &
      !integer(ZMQ_PTR)
      & context, &
      !integer(ZMQ_PTR)
      & requester, &
      !character*(64)
      & address

