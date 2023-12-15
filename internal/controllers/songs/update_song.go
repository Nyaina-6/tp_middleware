package songs

import (
    "encoding/json"
    "net/http"
    "github.com/sirupsen/logrus"
    "github.com/gofrs/uuid"
    "middleware/example/internal/repositories/songs"
    "middleware/example/internal/models"
)

func UpdateSong(w http.ResponseWriter, r *http.Request) {
    ctx := r.Context()
    songId, _ := ctx.Value("songId").(uuid.UUID)


    
    var updatedSong models.Song

    // Convertir le corps de la requête en objet Song
    err := json.NewDecoder(r.Body).Decode(&updatedSong)
    if err != nil {
        logrus.Errorf("Error decoding request body: %s", err.Error())
        w.WriteHeader(http.StatusBadRequest)
        return
    }

    
    song, err := songs.UpdateSong(songId, updatedSong)
    if err != nil {
        logrus.Errorf("Error updating song: %s", err.Error())
        if customError, isCustom := err.(*models.CustomError); isCustom {
            w.WriteHeader(customError.Code)
            body, _ := json.Marshal(customError)
            _, _ = w.Write(body)
        } else {
            w.WriteHeader(http.StatusInternalServerError)
        }
        return
    }

    

    w.WriteHeader(http.StatusOK)
    body , _ := json.Marshal(song)
    _, _ = w.Write(body)
    return
}
