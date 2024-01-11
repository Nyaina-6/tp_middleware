package songs

import (
    "encoding/json"
    "net/http"
    "github.com/sirupsen/logrus"
    "github.com/gofrs/uuid"
    "middleware/example/internal/repositories/songs"
    "middleware/example/internal/models"
)
func DeleteSong(w http.ResponseWriter, r *http.Request) {
    ctx := r.Context()
    songID, _ := ctx.Value("songId").(uuid.UUID)

    err := songs.DeleteSong(songID)
    if err != nil {
        logrus.Errorf("Error deleting song: %s", err.Error())
        customError, isCustom := err.(*models.CustomError)
		if isCustom {
			w.WriteHeader(customError.Code)
			body, _ := json.Marshal(customError)
			_, _ = w.Write(body)
		} else {
			w.WriteHeader(http.StatusInternalServerError)
		}
		return
    }

    w.WriteHeader(http.StatusNoContent)
}
