package tests

import (
	"context"
	pb "github.com/wcodesoft/user-management-service/grpc/go/user-management.proto"
	"google.golang.org/protobuf/types/known/emptypb"
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
	"service/database"
	"service/routes"
	"testing"
)

func localDatabase() database.Database {
	db, err := gorm.Open(sqlite.Open("file::memory:?cache=shared"), &gorm.Config{})
	if err != nil {
		panic("Failed to connect to database.")
	}
	db.AutoMigrate(&database.User{})
	return database.Database{
		Database: db,
	}
}

func TestCreateUserRPC(t *testing.T) {
	db := localDatabase()
	ctx := context.Background()
	defer db.CloseDatabase()

	server := routes.NewRouteServer(db)
	name := "John"
	lastName := "Doe"
	user := pb.User{Username: "johndoe", FirstName: &name, LastName: &lastName}
	resp, err := server.CreateUser(ctx, &user)

	if !resp.Success {
		t.Errorf("Error when creating user %s", err.Error())
	}
}

func TestDeleteUserRPC(t *testing.T) {
	db := localDatabase()
	ctx := context.Background()
	defer db.CloseDatabase()

	server := routes.NewRouteServer(db)
	name := "John"
	lastName := "Doe"
	username := "johndoe"
	user := pb.User{Username: username, FirstName: &name, LastName: &lastName}
	server.CreateUser(ctx, &user)
	resp, err := server.DeleteUser(ctx, &pb.RequestId{
		Username: username,
	})

	if !resp.Success {
		t.Errorf("Error when deleting user %s", err.Error())
	}
}

func TestGetUsersRPC(t *testing.T) {
	db := localDatabase()
	ctx := context.Background()
	defer db.CloseDatabase()

	server := routes.NewRouteServer(db)
	name := "John"
	lastName := "Doe"
	username := "johndoe"
	user := pb.User{Username: username, FirstName: &name, LastName: &lastName}
	user2 := pb.User{Username: username + "2", FirstName: &name, LastName: &lastName}

	server.CreateUser(ctx, &user)
	server.CreateUser(ctx, &user2)
	users, err := server.GetUsers(ctx, &emptypb.Empty{})

	if len(users.Users) != 2 {
		t.Errorf("Error when getting all users %s", err.Error())
	}
}

func TestUpdateUserRPC(t *testing.T) {
	db := localDatabase()
	ctx := context.Background()
	defer db.CloseDatabase()

	server := routes.NewRouteServer(db)
	name := "John"
	lastName := "Doe"
	username := "johndoe"
	user := pb.User{Username: username, FirstName: &name, LastName: &lastName}
	server.CreateUser(ctx, &user)

	newName := "Atualizado"
	resp, err := server.UpdateUser(ctx, &pb.User{
		Username:  username,
		FirstName: &newName,
	})

	if !resp.Success {
		t.Errorf("Error when updating user %s", err.Error())
	}

	users, errGet := server.GetUsers(ctx, &emptypb.Empty{})

	if len(users.Users) != 1 && users.Users[0].FirstName != &newName {
		t.Errorf("Error when updating user %s", errGet.Error())
	}
}
