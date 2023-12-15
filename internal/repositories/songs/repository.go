package songs

import (
	"github.com/gofrs/uuid"
	"middleware/example/internal/helpers"
	"middleware/example/internal/models"

)

func GetAllSongs() ([]models.Song, error) {
	db, err := helpers.OpenDB()
	if err != nil {
		return nil, err
	}
	rows, err := db.Query("SELECT * FROM songs")
	helpers.CloseDB(db)
	if err != nil {
		return nil, err
	}

	// parsing datas in object slice
	songs := []models.Song{}
	for rows.Next() {
		var data models.Song
		err = rows.Scan(&data.Id, &data.Artist,&data.Album,&data.Title,&data.Realease_year,&data.Genre)
		if err != nil {
			return nil, err
		}
		songs = append(songs, data)
	}
	// don't forget to close rows
	_ = rows.Close()

	return songs, err
}

func GetSongById(id uuid.UUID) (*models.Song, error) {
	db, err := helpers.OpenDB()
	if err != nil {
		return nil, err
	}
	row := db.QueryRow("SELECT * FROM songs WHERE id=?", id.String())
	helpers.CloseDB(db)

	var song models.Song
	err = row.Scan(&song.Id, &song.Artist, &song.Album, &song.Title, &song.Realease_year, &song.Genre)
	if err != nil {
		return nil, err
	}
	return &song, err
}


func CreateSong(song models.Song) (error) {
    db, err := helpers.OpenDB()
    if err != nil {
        return err
    }

	newUUID , err := uuid.NewV4()
	if err != nil {
		return err
	}

	_, err = db.Exec("INSERT INTO songs (id, artist, album, title, realease_year, genre) VALUES (?, ?, ?, ?, ?, ?)",
    newUUID.String() , song.Artist, song.Album, song.Title, song.Realease_year, song.Genre)
	helpers.CloseDB(db) 
    if err != nil {
        return err
    }
    return nil
}

func UpdateSong(id uuid.UUID ,song models.Song) (models.Song, error) {
    db, err := helpers.OpenDB()
    if err != nil {
        return models.Song{}, err
    }

    _, err = db.Exec("UPDATE songs SET artist = ?, album = ?, title = ?, release_year = ?, genre = ? WHERE id = ?",
        song.Artist, song.Album, song.Title, song.Realease_year, song.Genre, id.String())
	helpers.CloseDB(db)

    if err != nil {
        return models.Song{}, err
    }

    return song, nil
}
func DeleteSong(id uuid.UUID) error {
    db, err := helpers.OpenDB()
    if err != nil {
        return err
    }
    
    _, err = db.Exec("DELETE FROM songs WHERE id = ?", id)
	helpers.CloseDB(db)
    if err != nil {
        return err
    }

    return nil
}