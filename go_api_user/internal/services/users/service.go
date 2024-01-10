package users

import (
	"database/sql"
	"errors"
	"github.com/gofrs/uuid"
	"github.com/sirupsen/logrus"
	"middleware/example/internal/models"
	 "middleware/example/internal/repositories/users"
	
	"net/http"
)

func GetAllUsers() ([]models.User, error) {
	var err error
	// calling repository
	users, err := users.GetAllUsers()
	// managing errors
	if err != nil {
		logrus.Errorf("error retrieving users : %s", err.Error())
		return nil, &models.CustomError{
			Message: "Something went wrong",
			Code:    500,
		}
	}

	return users, nil
}

func GetUserById(id uuid.UUID) (*models.User, error) {
	user, err := users.GetUserById(id)
	if err != nil {
		if errors.As(err, &sql.ErrNoRows) {
			return nil, &models.CustomError{
				Message: "user not found",
				Code:    http.StatusNotFound,
			}
		}
		logrus.Errorf("error retrieving users : %s", err.Error())
		return nil, &models.CustomError{
			Message: "Something went wrong",
			Code:    500,
		}
	}

	return user, err
}
func CreateUser(user models.User) (error) {
	err := users.InsertUser(user)
	if err != nil {
		return &models.CustomError{
			Message : "Something went wrong" , 
			Code : 500,
		}
	}
	return nil
}
func DeleteUser(id uuid.UUID) error {
    // Vérifie si l'utilisateur existe avant de le supprimer
    _, err := users.GetUserById(id)
    if err != nil {
        return &models.CustomError{
            Message: "L'utilisateur n'existe pas",
            Code:    http.StatusNotFound,
        }
    }

    err = users.DeleteUser(id)
    if err != nil {
        return &models.CustomError{
            Message: "Erreur lors de la suppression de l'utilisateur",
            Code:    http.StatusInternalServerError,
        }
    }

    return nil
}
func UpdateUser(id uuid.UUID, user models.User) (models.User, error) {
    updatedUser, err := users.UpdateUser(id, user)
    if err != nil {
        return models.User{}, &models.CustomError{
            Message: "Failed to update the user",
            Code:   500,
        }
    }
    return  updatedUser, nil
}