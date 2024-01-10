package users

import (
	"github.com/gofrs/uuid"
	"middleware/example/internal/helpers"
	"middleware/example/internal/models"
)

func GetAllUsers() ([]models.User, error) {
	db, err := helpers.OpenDB()
	if err != nil {
		return nil, err
	}
	rows, err := db.Query("SELECT * FROM users")
	helpers.CloseDB(db)
	if err != nil {
		return nil, err
	}

	// parsing datas in object slice
	users := []models.User{}
	for rows.Next() {
		var data models.User
		err = rows.Scan(&data.Id, &data.Name,&data.Username,&data.Password,&data.Email)
		if err != nil {
			return nil, err
		}
		users = append(users, data)
	}
	// don't forget to close rows
	_ = rows.Close()

	return users, err
}

func GetUserById(id uuid.UUID) (*models.User, error) {
	db, err := helpers.OpenDB()
	if err != nil {
		return nil, err
	}
	row := db.QueryRow("SELECT * FROM users WHERE id=?", id.String())
	helpers.CloseDB(db)

	var user models.User
	err = row.Scan(&user.Id, &user.Name,&user.Username,&user.Password,&user.Email,)
	if err != nil {
		return nil, err
	}
	return &user, err
}

func InsertUser(user models.User) (error) {
	db, err := helpers.OpenDB()
	if err != nil {
		return err
	}
	newUUID, err := uuid.NewV4()
	if err != nil {
		return err
	}
	//defer helpers.CloseDB(db)


	// Insérer l'utilisateur dans la base de données
	_, err = db.Exec("INSERT INTO users (id, name, username, password, email) VALUES (?, ?, ?, ?, ?)",
		newUUID.String(), user.Name, user.Username, user.Password, user.Email)
		helpers.CloseDB(db)
	if err != nil {
		return err
	}

	return nil
}

func DeleteUser(id uuid.UUID) error {
    db, err := helpers.OpenDB()
    if err != nil {
        return err
    }
    
    _, err = db.Exec("DELETE FROM users WHERE id = ?", id)
	helpers.CloseDB(db)
    if err != nil {
        return err
    }

    return nil
}
func UpdateUser(id uuid.UUID ,user models.User) (models.User, error) {
    db, err := helpers.OpenDB()
    if err != nil {
        return models.User{}, err
    }

    _, err = db.Exec("UPDATE users SET name = ?, username = ?, password = ?, email = ?  WHERE id = ?",
        user.Name, user.Username, user.Password, user.Email, id.String())
	helpers.CloseDB(db)

    if err != nil {
        return models.User{}, err
    }

    return user, nil
}