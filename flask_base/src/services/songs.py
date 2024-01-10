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
    song_schema = SongSchema().loads(json.dumps(song_data), unknown=EXCLUDE)
    response = requests.request(method="POST", url=songs_url, json=song_schema)
    if response.status_code != 201:
        return {"message": "Song created successfully"}, 201
    try:
        song_model = SongModel.from_dict(song_data)  
        songs_repository.add_song(song_model)  
    except Exception :
       return {"message": "Failed to create song"}, response.status_code


def get_song_from_db(song_id):
    return songs_repository.get_song(song_id)


def song_exists(song_id):
    return get_song_from_db(song_id) is not None

def modify_song(id, song_update):
    song_schema = SongSchema().loads(json.dumps(song_update), unknown=EXCLUDE)
    response = requests.request(method="PUT", url=songs_url + id, json=song_schema)

    if response.status_code == 200:
        return {"message": "Song updated successfully"}, 200
    try :
        song_model = SongSchema().loads(response.json())
        songs_repository.update_song(song_model)
    except Exception :
        return {"message": "Failled to update song"}, response.status_code


def delete_song(id):
    response = requests.request(method="DELETE", url=songs_url + id)
    
    if response.status_code != 200:
        return response.json(), response.status_code

    #try:
    #    songs_repository.delete_song(id)
    #    return {"message": "Song deleted successfully"}, 200
    #except Exception:
    #    return {"message": "Failed to delete the song to database"}, 500

    