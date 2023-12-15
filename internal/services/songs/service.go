package songs

import (
	"database/sql"
	"errors"
	"github.com/gofrs/uuid"
	"github.com/sirupsen/logrus"
	"middleware/example/internal/models"
	repository "middleware/example/internal/repositories/songs"
	"net/http"
)

func GetAllSongs() ([]models.Song, error) {
	var err error
	// calling repository
	songs, err := repository.GetAllSongs()
	// managing errors
	if err != nil {
		logrus.Errorf("error retrieving collections : %s", err.Error())
		return nil, &models.CustomError{
			Message: "Something went wrong",
			Code:    500,
		}
	}

	return songs, nil
}

func GetSongById(id uuid.UUID) (*models.Song, error) {
	song, err := repository.GetSongById(id)
	if err != nil {
		if errors.As(err, &sql.ErrNoRows) {
			return nil, &models.CustomError{
				Message: "song not found",
				Code:    http.StatusNotFound,
			}
		}
		logrus.Errorf("error retrieving songs : %s", err.Error())
		return nil, &models.CustomError{
			Message: "Something went wrong",
			Code:    500,
		}
	}

	return song, err
}
func CreateSong (song models.Song) (error) {
	err := repository.CreateSong(song)
	if err != nil {
		return &models.CustomError{
			Message : "Something went wrong" , 
			Code : 500,
		}
	}
	return nil
}

func UpdateSong(id uuid.UUID, song models.Song) (models.Song, error) {
    updatedSong, err := repository.UpdateSong(id, song)
    if err != nil {
        return models.Song{}, &models.CustomError{
            Message: "Failed to update the song",
            Code:   500,
        }
    }
    return  updatedSong , nil
}
func DeleteSong(id uuid.UUID) error {
    // Vérifie si la chanson existe avant de la supprimer
    _, err := repository.GetSongById(id)
    if err != nil {
        return &models.CustomError{
            Message: "La chanson n'existe pas",
            Code:    http.StatusNotFound,
        }
    }

    err = repository.DeleteSong(id)
    if err != nil {
        return &models.CustomError{
            Message: "Erreur lors de la suppression de la chanson",
            Code:    http.StatusInternalServerError,
        }
    }

    return nil
}