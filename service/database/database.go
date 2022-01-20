package database

type Database struct {
	memoryDatabase map[string]user
}

type user struct {
	Username  string
	FirstName string
	LastName  string
}

func NewDatabase() Database {
	return Database{
		memoryDatabase: make(map[string]user),
	}
}

func (d *Database) AddUser(username string, firstName string, lastName string) bool {
	if d.GetUser(username) != nil {
		return false
	}
	d.memoryDatabase[username] = user{username, firstName, lastName}
	return true
}

func (d *Database) UpdateUser(username string, firstName string, lastName string) bool {
	if d.GetUser(username) == nil {
		return false
	}
	d.memoryDatabase[username] = user{username, firstName, lastName}
	return true
}

func (d *Database) DeleteUser(username string) bool {
	if d.GetUser(username) == nil {
		return false
	}
	delete(d.memoryDatabase, username)
	return true
}

func (d *Database) GetUser(username string) *user {
	if val, ok := d.memoryDatabase[username]; ok {
		return &val
	} else {
		return nil
	}
}

func (d *Database) GetUsers() []user {
	var l []user
	for _, v := range d.memoryDatabase {
		l = append(l, v)
	}
	return l
}
