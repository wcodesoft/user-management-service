package database

import (
	"errors"
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
)

type Database struct {
	database *gorm.DB
}

type User struct {
	gorm.Model
	Username  string `gorm:"primaryKey"`
	FirstName string
	LastName  string
}

func NewDatabase() Database {
	db, err := gorm.Open(sqlite.Open("file::memory:?cache=shared"), &gorm.Config{})
	if err != nil {
		panic("Failed to connect to database.")
	}
	db.AutoMigrate(&User{})
	return Database{
		database: db,
	}
}

func (d *Database) CloseDatabase() {
	db, _ := d.database.DB()
	defer db.Close()
}

func (d *Database) AddUser(username string, firstName string, lastName string) bool {
	if d.GetUser(username) != nil {
		return false
	}
	error := d.database.Create(&User{Username: username, FirstName: firstName, LastName: lastName}).Error
	return !errors.Is(error, gorm.ErrRecordNotFound)
}

func (d *Database) UpdateUser(username string, firstName string, lastName string) bool {
	var user = d.GetUser(username)
	if user == nil {
		return false
	}
	error := d.database.Model(&user).Updates(User{Username: username, FirstName: firstName, LastName: lastName}).Error
	return !errors.Is(error, gorm.ErrRecordNotFound)
}

func (d *Database) DeleteUser(username string) bool {
	var user = d.GetUser(username)
	if user == nil {
		return false
	}
	error := d.database.Delete(&user).Error
	return !errors.Is(error, gorm.ErrRecordNotFound)
}

func (d *Database) GetUser(username string) *User {
	var user User
	error := d.database.First(&user, "username = ?", username).Error
	if errors.Is(error, gorm.ErrRecordNotFound) {
		return nil
	} else {
		return &user
	}
}

func (d *Database) GetUsers() []User {
	var l []User
	d.database.Find(&l)
	return l
}
