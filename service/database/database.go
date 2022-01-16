package database

type Database struct {
	memoryDatabase []user
}

type user struct {
	Username   string
	FirstName  string
	SecondName string
}

func NewDatabase() Database {
	return Database{}
}

func (d *Database) AddUser(username string, firstName string, secondName string) bool {
	d.memoryDatabase = append(d.memoryDatabase, user{username, firstName, secondName})
	return true
}

func (d *Database) GetUsers() []user {
	return d.memoryDatabase
}
