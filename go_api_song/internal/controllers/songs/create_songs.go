package songs

import (
    "encoding/json"
    "net/http"
    "middleware/example/internal/repositories/songs"
	"middleware/example/internal/models"
    "fmt"
    "github.com/sirupsen/logrus"
    "io/ioutil"

)

func AddSong(w http.ResponseWriter, r *http.Request) {
    reqBody , _ := ioutil.ReadAll(r.Body)
    var song models.Song


    err := json.Unmarshal(reqBody , &song)
    if err != nil {
        fmt.Println("Error decoding request body: ", err)
        return
    }
    err = songs.CreateSong(song)

    if err != nil {
        logrus.Errorf("Error creating song: %s", err.Error())
        customError , isCustom := err.(*models.CustomError)
        if isCustom{ 
            w.WriteHeader(customError.Code)
            body , _ := json.Marshal(customError)
            _, _ = w.Write(body)
        } else {
            w.WriteHeader(http.StatusInternalServerError)
        }
        return
        
    }
    w.WriteHeader(http.StatusOK)
    
}
