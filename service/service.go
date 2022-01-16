package main

import (
	"log"
	"net"
	"service/routes"

	uManagement "github.com/wcodesoft/user-management-service/grpc/go/user-management.proto"
	"google.golang.org/grpc"
)

func main() {
	port := ":9000"
	lis, err := net.Listen("tcp", port)
	if err != nil {
		log.Fatalf("Failed to listen: %v", err)
	}

	log.Print("Server running at port " + port)

	gRPCServer := grpc.NewServer()

	uManagement.RegisterUserManagementServer(gRPCServer, routes.NewRouteServer())

	if err := gRPCServer.Serve(lis); err != nil {
		log.Fatalf("Failed to serve: %v", err)
	}
}
