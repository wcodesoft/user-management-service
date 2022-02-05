package main

import (
	"github.com/rs/cors"
	"log"
	"net"
	"net/http"
	"service/database"
	"service/routes"

	"github.com/improbable-eng/grpc-web/go/grpcweb"

	uManagement "github.com/wcodesoft/user-management-service/grpc/go/user-management.proto"
	"google.golang.org/grpc"
)

func main() {
	port := ":9000"
	webPort := ":9001"

	lis, err := net.Listen("tcp", port)
	if err != nil {
		log.Fatalf("Failed to listen: %v", err)
	}

	log.Print("Server running gRPC at port " + port)

	gRPCServer := grpc.NewServer()

	db := database.NewDatabase()
	uManagement.RegisterUserManagementServer(gRPCServer, routes.NewRouteServer(db))

	go func() {
		if err := gRPCServer.Serve(lis); err != nil {
			log.Fatalf("Failed to serve: %v", err)
		}
	}()

	wrappedServer := grpcweb.WrapServer(gRPCServer)
	handler := func(resp http.ResponseWriter, req *http.Request) {
		if wrappedServer.IsGrpcWebRequest(req) {
			wrappedServer.ServeHTTP(resp, req)
			return
		}
		http.DefaultServeMux.ServeHTTP(resp, req)
	}

	httpServer := http.Server{
		Addr:    webPort,
		Handler: cors.AllowAll().Handler(http.HandlerFunc(handler)),
	}

	log.Printf("Starting gRPC Web server. http port %s\n", webPort)

	if err := httpServer.ListenAndServe(); err != nil {
		log.Fatalf("failed starting http server: %v", err)
	}
}
