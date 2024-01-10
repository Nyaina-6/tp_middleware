package users

import (
    "encoding/json"
    "net/http"
    "github.com/sirupsen/logrus"
    "github.com/gofrs/uuid"
    "middleware/example/internal/repositories/users"
    "middleware/example/internal/models"
    "io/ioutil"
)

func UpdateUser(w http.ResponseWriter, r *http.Request) {
    ctx := r.Context()
    userId, _ := ctx.Value("userId").(uuid.UUID)
    
    var updatedUser models.User

    reqBody , _ := ioutil.ReadAll(r.Body)
    err := json.Unmarshal(reqBody , &updatedUser)

    if err != nil {
        logrus.Errorf("Error decoding request body: %s", err.Error())
        w.WriteHeader(http.StatusBadRequest)
        return
    }
    
    user, err := users.UpdateUser(userId, updatedUser)
    if err != nil {
        logrus.Errorf("Error updating user: %s", err.Error())
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

    
    w.WriteHeader(http.StatusOK)
    body , _ := json.Marshal(user)
    _, _ = w.Write(body)
    return
}
