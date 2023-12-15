package models

import (
	"github.com/gofrs/uuid"
)

type Song struct {
	Id      *uuid.UUID `json:"id"`
	Artist string     `json:"artist"`
	Album string     `json:"album"`
	Title string     `json:"title"`
	Realease_year string     `json:"realease_year"`
	Genre string     `json:"genre"`
	
}
