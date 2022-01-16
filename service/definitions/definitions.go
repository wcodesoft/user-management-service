package definitions

import (
	"log"

	"golang.org/x/net/context"
)

type Server struct {
}

func (s *Server) CreateUser(ctx context.Context, in *User) (*Response, error) {
	log.Printf("Receive message body from client: %s", in.Body)
	return &Response{Success: true}, nil
}
