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
	s.database.AddUser(user.GetUsername(), user.GetFirstName(), user.GetLastName())
	return &pb.Response{Success: true}, nil
}

func (s *routeServer) GetUsers(context.Context, *emptypb.Empty) (*pb.GetUsersResponse, error) {
	l := s.database.GetUsers()
	var array []*pb.User

	for _, s := range l {
		var user = pb.User{
			Username:  s.Username,
			FirstName: &s.FirstName,
			LastName:  &s.LastName,
		}
		array = append(array, &user)
	}

	return &pb.GetUsersResponse{
		Users: array,
	}, nil
}

func (s *routeServer) UpdateUser(_ context.Context, user *pb.User) (*pb.Response, error) {
	ok := s.database.UpdateUser(user.GetUsername(), user.GetFirstName(), user.GetLastName())
	return &pb.Response{Success: ok}, nil
}

func (s *routeServer) DeleteUser(_ context.Context, request *pb.RequestId) (*pb.Response, error) {
	ok := s.database.DeleteUser(request.GetUsername())
	return &pb.Response{Success: ok}, nil
}
