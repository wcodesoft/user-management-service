package database

import "container/list"

type Database struct {
	memoryDatabase *list.List
}

type user struct {
	firstName  string
	secondName string
}

func NewDatabase() Database {
	return Database{
		memoryDatabase: list.New(),
	}
}

func (d *Database) AddUser(firstName string, secondName string) bool {
	d.memoryDatabase.PushBack(user{firstName, secondName})
	return true
}
