from http.client import BAD_REQUEST
import json
from flask import Blueprint, jsonify, request
from flask_login import login_required
from marshmallow import ValidationError

from src.models.http_exceptions import *
from src.schemas.user import UserUpdateSchema
from src.schemas.user import UserCreateSchema

from src.schemas.errors import *
import src.services.users as users_service

# from routes import users
users = Blueprint(name="users", import_name=__name__)


@users.route('/<id>', methods=['GET'])
@login_required
def get_user(id):
    """
    ---
    get:
      description: Getting a user
      parameters:
        - in: path
          name: id
          schema:
            type: uuidv4
          required: true
          description: UUID of user id
      responses:
        '200':
          description: Ok
          content:
            application/json:
              schema: User
            application/yaml:
              schema: User
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
          - users
    """
    return users_service.get_user(id)


@users.route('/<id>', methods=['PUT'])
@login_required
def put_user(id):
    """
    ---
    put:
      description: Updating a user
      parameters:
        - in: path
          name: id
          schema:
            type: uuidv4
          required: true
          description: UUID of user id
      requestBody:
        required: true
        content:
            application/json:
                schema: UserUpdate
      responses:
        '200':
          description: Ok
          content:
            application/json:
              schema: User
            application/yaml:
              schema: User
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
          - users
    """
    # parser le body
    try:
        user_update = UserUpdateSchema().loads(json_data=request.data.decode('utf-8'))
    except ValidationError as e:
        error = UnprocessableEntitySchema().loads(json.dumps({"message": e.messages.__str__()}))
        return error, error.get("code")

    # modification de l'utilisateur (username, nom, mot de passe, etc.)
    try:
        return users_service.modify_user(id, user_update)
    except Conflict:
        error = ConflictSchema().loads(json.dumps({"message": "User already exists"}))
        return error, error.get("code")
    except UnprocessableEntity:
        error = UnprocessableEntitySchema().loads(json.dumps({"message": "One required field was empty"}))
        return error, error.get("code")
    except Forbidden:
        error = ForbiddenSchema().loads(json.dumps({"message": "Can't manage other users"}))
        return error, error.get("code")
    except Exception:
        error = SomethingWentWrongSchema().loads("{}")
        return error, error.get("code")
    
@users.route('/', methods=['GET'])
@login_required
def get_all_users():
    """
    ---
    get:
      description: Get all users
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: UsersList
            application/yaml:
              schema: UsersList
        '401':
          description: Unauthorized
          content:
            application/json:
              schema: Unauthorized
            application/yaml:
              schema: Unauthorized
      tags:
          - users
    """
    users = users_service.get_all_users()  
    return jsonify(users), 200

@users.route('', methods=['POST'])
@login_required  
def create_user():
    """
    ---
    post:
      description: Insert a new user
      requestBody:
        required: true
        content:
            application/json:
                schema: UserInsertSchema 
            application/yaml:
                schema: UserInsertSchema
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: SuccessMessage
            application/yaml:
              schema: SuccessMessage
        '500':
          description: Internal Server Error
          content:
            application/json:
              schema: ErrorMessage
            application/yaml:
              schema: ErrorMessage
      tags:
          - users
    """
    try:
        user_data = UserCreateSchema().loads(json_data=request.data.decode('utf-8'))
    except ValidationError as e:
        error = UnprocessableEntitySchema().loads(json.dumps({"message": e.messages.__str__()}))
        return error, error.get("code")
    try : 
        result, status_code = users_service.create_user(user_data)
        return jsonify(result), status_code
    except Exception as e:
        error = SomethingWentWrongSchema().loads("{}")
        return error, error.get("code")
    
    

@users.route('/<id>', methods=['DELETE'])
@login_required
def delete_user(id):
    """
    ---
    delete:
      description: Delete a user
      parameters:
        - in: path
          name: id
          schema:
            type: uuidv4
          required: true
          description: UUID of user id to delete
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: DeletedUser
            application/yaml:
              schema: DeletedUser
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
          - users
    """
    try:
        result ,deleted_user = users_service.delete_user(id)  
        if not deleted_user:
            return jsonify({"message": "User not found"}), 404
        else:
             return jsonify(result), deleted_user

    except BAD_REQUEST as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        return jsonify({"message": "An error occurred: {}".format(str(e))}), 500