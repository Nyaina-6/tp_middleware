import json
import requests
from marshmallow import EXCLUDE
from src.schemas.songs import SongSchema
from src.schemas.songs import SongCreateSchema
from src.schemas.songs import SongUpdateSchema
from src.models.songs import Song as SongModel
from src.models.http_exceptions import *
import src.repositories.songs as songs_repository


songs_url = "http://localhost:8081/songs/"  # URL de l'API songs (golang)


def get_song(id):
    response = requests.request(method="GET", url=songs_url + id)
    return response.json(), response.status_code

def get_all_songs():
    response = requests.request(method ="GET" , url=songs_url)
    return response.json(), response.status_code

def create_song(song_data):
    song_model = SongModel.from_dict(song_data)
    song_schema = SongSchema().loads(json.dumps(song_data), unknown=EXCLUDE)

    response = requests.request(method="POST", url=songs_url, json=song_schema)
    if response.status_code != 201:
        return response.json(), response.status_code

    try:
        #song_model.id = response.json()["id"]
        songs_repository.add_song(song_model)
    except Exception:
        raise SomethingWentWrong

    return response.json(), response.status_code


def get_song_from_db(song_id):
    return songs_repository.get_song(song_id)


def song_exists(song_id):
    return get_song_from_db(song_id) is not None

def modify_song(id, song_update):
    song_schema = SongSchema().loads(json.dumps(song_update), unknown=EXCLUDE)
    response = requests.request(method="PUT", url=songs_url + id, json=song_schema)

    if not SongSchema.is_empty(song_schema):
        if response.status_code != 200:
            return response.json(), response.status_code

    song_model = SongModel.from_dict(song_update)
    if not song_model.is_empty():
        song_model.id = id
        found_song = songs_repository.get_song_from_id(id)
        
        # Mise à jour des attributs de la chanson en fonction des données fournies
        if not song_model.artist:
            song_model.artist = found_song.artist
        if not song_model.album:
            song_model.album = found_song.album
        if not song_model.title:
            song_model.title = found_song.title
        if not song_model.release_year:
            song_model.release_year = found_song.release_year
        if not song_model.genre:
            song_model.genre = found_song.genre

        try:
            songs_repository.update_song(song_model)
        except Exception as e:
            # Gérez les exceptions selon la logique de votre application
            return {"message": "Failed to update song"}, 500

    return (response.json(), response.status_code) if response else songs_repository.get_song(id)
