package users

import (
    "encoding/json"
    "net/http"
    "github.com/sirupsen/logrus"
    "github.com/gofrs/uuid"
    "middleware/example/internal/repositories/users"
    "middleware/example/internal/models"
)
func DeleteUser(w http.ResponseWriter, r *http.Request) {
    ctx := r.Context()
    userID, _ := ctx.Value("userId").(uuid.UUID)

    err := users.DeleteUser(userID)
    if err != nil {
        logrus.Errorf("Error deleting user: %s", err.Error())
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
