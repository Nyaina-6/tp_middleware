import json
from flask import Blueprint, jsonify, request
from flask_login import login_required
from marshmallow import ValidationError

from src.models.http_exceptions import *
from src.schemas.songs import SongUpdateSchema  
from src.schemas.songs import SongSchema
from src.schemas.songs import SongCreateSchema
from src.schemas.errors import *
import src.services.songs as songs_service

songs = Blueprint(name="songs", import_name=__name__)

@songs.route('/<id>', methods=['GET'])
@login_required
def get_song(id):
    """
    ---
    get:
      description: Getting a song
      parameters:
        - in: path
          name: id
          schema:
            type: uuidv4
          required: true
          description: UUID of song id
      responses:
        '200':
          description: Ok
          content:
            application/json:
              schema: Song
            application/yaml:
              schema: Song
        '401':
          description: Unauthorized
          content:
            application/json:
              schema: Unauthorized
            application/yaml:
              schema: Unauthorized
        '404':
          description: Not found
          content:
            application/json:
              schema: NotFound
            application/yaml:
              schema: NotFound
      tags:
          - songs
    """
    return songs_service.get_song(id)

@songs.route('/<id>', methods=['PUT'])
@login_required
def put_song(id):
    """
    ---
    put:
      description: Updating a song
      parameters:
        - in: path
          name: id
          schema:
            type: uuidv4
          required: true
          description: UUID of song id
      requestBody:
        required: true
        content:
            application/json:
                schema: SongUpdateSchema  
      responses:
        '200':
          description: Ok
          content:
            application/json:
              schema: Song
            application/yaml:
              schema: Song
        '401':
          description: Unauthorized
          content:
            application/json:
              schema: Unauthorized
            application/yaml:
              schema: Unauthorized
        '404':
          description: Not found
          content:
            application/json:
              schema: NotFound
            application/yaml:
              schema: NotFound
        '422':
          description: Unprocessable entity
          content:
            application/json:
              schema: UnprocessableEntity
            application/yaml:
              schema: UnprocessableEntity
      tags:
          - songs
    """
    try:
        song_update = SongUpdateSchema().loads(json_data=request.data.decode('utf-8'))
    except ValidationError as e:
        error = UnprocessableEntitySchema().loads(json.dumps({"message": e.messages.__str__()}))
        return error, error.get("code")

    try:
        return songs_service.modify_song(id, song_update)
    except Exception :
        error = SomethingWentWrongSchema().loads("{}")
        return error, error.get("code")

@songs.route('/', methods=['GET'])
@login_required
def get_all_songs():
    """
    ---
    get:
      description: Getting all songs
      responses:
        '200':
          description: Ok
          content:
            application/json:
              schema: List[Song]
            application/yaml:
              schema: List[Song]
        '401':
          description: Unauthorized
          content:
            application/json:
              schema: Unauthorized
            application/yaml:
              schema: Unauthorized
      tags:
          - songs
    """
    return songs_service.get_all_songs()

@songs.route('', methods=['POST'])
@login_required
def create_song():
    """
    ---
    post:
      description: Adding a new song
      parameters:
        - in : path
          name : id
          schema :
            type : uuidv4
          required : true
          description : UUID of Song id
      requestBody:
        required: true
        content:
            application/json:
                schema: SongCreateSchema  
            application/yaml:
                schema : SongCreateSchema
      responses:
        '201':
          description: Created
          content:
            application/json:
              schema: Song
            application/yaml:
              schema: Song
        '401':
          description: Unauthorized
          content:
            application/json:
              schema: Unauthorized
            application/yaml:
              schema: Unauthorized
        '422':
          description: Unprocessable entity
          content:
            application/json:
              schema: UnprocessableEntity
            application/yaml:
              schema: UnprocessableEntity
      tags:
          - songs
    """
    try:
        new_song_data = SongCreateSchema().loads(json_data=request.data.decode('utf-8'))
    except ValidationError as e:
        error = UnprocessableEntitySchema().loads(json.dumps({"message": e.messages.__str__()}))
        return error, error.get("code")
    try:
        result, status_code = songs_service.create_song(new_song_data)
        return jsonify(result), status_code
 
    except Exception as e:
        # Gérer d'autres exceptions en fonction de votre logique
        error = SomethingWentWrongSchema().loads("{}")
        
        return error, error.get("code")
    
      
    
@songs.route('/<id>', methods=['DELETE'])
@login_required
def delete_song(id):
    """
    ---
    delete:
      description: Deleting a song
      parameters:
        - in: path
          name: id
          schema:
            type: uuidv4
          required: true
          description: UUID of song id to be deleted
      responses:
        '200':
          description: Ok
          content:
            application/json:
              schema: Song
            application/yaml:
              schema: Song
        '401':
          description: Unauthorized
          content:
            application/json:
              schema: Unauthorized
            application/yaml:
              schema: Unauthorized
        '404':
          description: Not found
          content:
            application/json:
              schema: NotFound
            application/yaml:
              schema: NotFound
      tags:
          - songs
    """
    try:
        return songs_service.delete_song(id)
    except NotFound:
        error = NotFoundSchema().loads(json.dumps({"message": "Song not found"}))
        return error, 404
    except Exception as e:
        # Handle other exceptions based on your application's logic
        error = SomethingWentWrongSchema().loads("{}")
        return error, error.get("code")

