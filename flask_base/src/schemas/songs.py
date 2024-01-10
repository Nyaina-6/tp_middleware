from marshmallow import Schema, fields, validates_schema, ValidationError

# Schéma de sortie pour une chanson (renvoyé au front)
class SongSchema(Schema):
    id = fields.String(description="UUID")
    artist = fields.String(description="Artist")
    album = fields.String(description="Album")
    title = fields.String(description="Title")
    genre = fields.String(description="Genre")
    
    @staticmethod
    def is_empty(obj):
        return (not obj.get("id") or obj.get("id") == "") and \
               (not obj.get("artist") or obj.get("artist") == "") and \
               (not obj.get("album") or obj.get("album") == "") and \
               (not obj.get("title") or obj.get("title") == "") and \
               (not obj.get("genre") or obj.get("genre") == "")


class SongUpdateSchema(Schema):
    # Champs pour la mise à jour d'une chanson
    artist = fields.String(description="Artist")
    album = fields.String(description="Album")
    title = fields.String(description="Title")
    genre = fields.String(description="Genre")

    # Fonction de validation pour s'assurer qu'au moins un champ est spécifié pour la mise à jour
    @validates_schema
    def validates_schema_for_update(self, data, **kwargs):
        # Vérification qu'au moins un champ est spécifié pour la mise à jour
        fields_to_check = ['artist', 'album', 'title', 'genre']
        for field in fields_to_check:
            if field in data and data[field]:
                return  # Au moins un champ non vide est trouvé
        raise ValidationError("At least one of ['artist', 'album', 'title', 'genre'] must be specified")


class SongCreateSchema(Schema):
    # Champs pour la création d'une chanson
    artist = fields.String(required=True, description="Artist")
    album = fields.String(required=True, description="Album")
    title = fields.String(required=True, description="Title")
    genre = fields.String(required=True, description="Genre")

    # Validation pour s'assurer qu'au moins un champ est spécifié
    @validates_schema
    def validate_field(self, data, **kwargs):
        fields_to_check = ['artist', 'album', 'title', 'genre']
        for field in fields_to_check:
            if field in data and data[field]:
                return  # Au moins un champ non vide est trouvé
        raise ValidationError("All of ['artist', 'album', 'title', 'genre'] must be specified")
