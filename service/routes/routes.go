package routes

import (
	"context"
	"log"
	"service/database"

	pb "github.com/wcodesoft/user-management-service/grpc/go/user-management.proto"
)

type routeServer struct {
	pb.UnimplementedUserManagementServer
	database database.Database
}

func NewRouteServer() *routeServer {
	s := &routeServer{
		database: database.NewDatabase(),
	}
	return s
}

func (s *routeServer) CreateUser(ctx context.Context, user *pb.User) (*pb.Response, error) {
	log.Printf("Name received: " + user.FirstName)
	s.database.AddUser(user.FirstName, user.SecondName)
	return &pb.Response{Success: true}, nil
}
