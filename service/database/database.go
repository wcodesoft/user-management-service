package database

import (
	"errors"
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
)

type Database struct {
	Database *gorm.DB
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
		Database: db,
	}
}

func (d *Database) CloseDatabase() {
	db, _ := d.Database.DB()
	defer db.Close()
}

func (d *Database) AddUser(username string, firstName string, lastName string) bool {
	if d.GetUser(username) != nil {
		return false
	}
	err := d.Database.Create(&User{Username: username, FirstName: firstName, LastName: lastName}).Error
	return !errors.Is(err, gorm.ErrRecordNotFound)
}

func (d *Database) UpdateUser(username string, firstName string, lastName string) bool {
	var user = d.GetUser(username)
	if user == nil {
		return false
	}
	err := d.Database.Model(&user).Updates(User{Username: username, FirstName: firstName, LastName: lastName}).Error
	return !errors.Is(err, gorm.ErrRecordNotFound)
}

func (d *Database) DeleteUser(username string) bool {
	var user = d.GetUser(username)
	if user == nil {
		return false
	}
	err := d.Database.Delete(&user).Error
	return !errors.Is(err, gorm.ErrRecordNotFound)
}

func (d *Database) GetUser(username string) *User {
	var user User
	err := d.Database.First(&user, "username = ?", username).Error
	if errors.Is(err, gorm.ErrRecordNotFound) {
		return nil
	} else {
		return &user
	}
}

func (d *Database) GetUsers() []User {
	var l []User
	d.Database.Find(&l)
	return l
}
