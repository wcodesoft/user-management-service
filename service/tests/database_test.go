package tests

import (
	"service/database"
	"testing"
)

func TestAddDatabase(t *testing.T) {
	db := database.NewDatabase()
	defer db.CloseDatabase()
	ans := db.AddUser("johndoe", "John", "Doe")
	if !ans {
		t.Errorf("Fail when adding user.")
	}
}

func TestAddDatabaseDuplicatedUserFail(t *testing.T) {
	db := database.NewDatabase()
	defer db.CloseDatabase()
	_ = db.AddUser("johndoe", "John", "Doe")
	ans := db.AddUser("johndoe", "John", "Doe2")
	if ans {
		t.Errorf("Fail because user is being duplicated added.")
	}
}

func TestGetUsers(t *testing.T) {
	db := database.NewDatabase()
	defer db.CloseDatabase()
	db.AddUser("johndoe", "John", "Doe")
	users := db.GetUsers()
	if len(users) != 1 {
		t.Errorf("Wrong number of users, %d", len(users))
	}
	db.AddUser("johndoe2", "John2", "Doe")
	users = db.GetUsers()
	if len(users) != 2 {
		t.Errorf("Wrong number of users, %d", len(users))
	}
}

func TestDeleteUser(t *testing.T) {
	username := "johndoe"
	db := database.NewDatabase()
	defer db.CloseDatabase()

	db.AddUser(username, "John", "Doe")
	ans := db.DeleteUser(username)
	if !ans {
		t.Errorf("Unable to delete user %s", username)
	}
}

func TestDeleteUserFail(t *testing.T) {
	db := database.NewDatabase()
	defer db.CloseDatabase()
	ans := db.DeleteUser("johndoe")
	if ans {
		t.Errorf("Was able to delete inexistent user")
	}
}

func TestUpdateUser(t *testing.T) {
	db := database.NewDatabase()
	defer db.CloseDatabase()

	username := "johndoe"
	db.AddUser(username, "John", "Doe")

	ans := db.UpdateUser(username, "John", "Updated")
	if !ans {
		t.Errorf("Unable to update user %s data", username)
	}

	user := db.GetUser(username)
	if user == nil || user.LastName != "Updated" {
		t.Errorf("Unable to update user %s data", username)
	}
}

func TestUpdateUserFail(t *testing.T) {
	db := database.NewDatabase()
	defer db.CloseDatabase()

	username := "johndoe"
	ans := db.UpdateUser("johndoe", "John", "Updated")
	if ans {
		t.Errorf("Able to update user %s data", username)
	}
}
