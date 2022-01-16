package main

import (
	"log"
	"net"
	"service/usermanagement/definitions"

	usermanagement "../grpc/go/user-management.proto"
	"google.golang.org/grpc"
)

func main() {
	lis, err := net.Listen("tcp", ":9000")
	if err != nil {
		log.Fatalf("Failed to listen: %v", err)
	}

	s := definitions.Server{}

	gRPCServer := grpc.NewServer()

	usermanagement.RegisterUserManagementServer(gRPCServer, &s)

	if err := gRPCServer.Serve(lis); err != nil {
		log.Fatalf("Failed to serve: %v", err)
	}
}
