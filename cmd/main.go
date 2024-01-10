package main

import (
	"github.com/go-chi/chi/v5"
	"github.com/sirupsen/logrus"
	"middleware/example/internal/controllers/songs"
	"middleware/example/internal/helpers"
	"net/http"
	
)

func main() {
	r := chi.NewRouter()
	

	r.Route("/songs", func(r chi.Router) {
		r.Get("/", songs.GetSongs)
		r.Route("/{id}", func(r chi.Router) {
			r.Use(songs.Ctx)
			r.Get("/", songs.GetSong)
			r.Put("/", songs.UpdateSong)
			r.Delete("/", songs.DeleteSong)

		})
		r.Post("/", songs.AddSong) 

	})
	
	
	logrus.Info("[INFO] Web server started. Now listening on *:8081")
	logrus.Fatalln(http.ListenAndServe(":8081", r))
}

func init() {
	db, err := helpers.OpenDB()
	if err != nil {
		logrus.Fatalf("error while opening database : %s", err.Error())
	}
	schemes := []string{
		`CREATE TABLE IF NOT EXISTS songs (
			id VARCHAR(225) PRIMARY KEY AUTOINCREMENT UNIQUE,
		artist VARCHAR(255) NOT NULL,
			album VARCHAR(255) ,
			title VARCHAR(255) NOT NULL,
			genre VARCHAR(255) NOT NULL


		);`,
	}
	for _, scheme := range schemes {
		if _, err := db.Exec(scheme); err != nil {
			logrus.Fatalln("Could not generate table ! Error was : " + err.Error())
		}
	}

	helpers.CloseDB(db)

}
