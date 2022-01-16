package routes

import (
	"context"
	"service/database"

	"google.golang.org/protobuf/types/known/emptypb"

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

func (s *routeServer) CreateUser(_ context.Context, user *pb.User) (*pb.Response, error) {
	s.database.AddUser(user.GetUsername(), user.GetFirstName(), user.GetSecondName())
	return &pb.Response{Success: true}, nil
}

func (s *routeServer) GetUsers(context.Context, *emptypb.Empty) (*pb.GetUsersResponse, error) {
	l := s.database.GetUsers()
	var array []*pb.User

	for _, s := range l {
		var user = pb.User{
			Username:   s.Username,
			FirstName:  &s.FirstName,
			SecondName: &s.SecondName,
		}
		array = append(array, &user)
	}

	return &pb.GetUsersResponse{
		Users: array,
	}, nil
}
