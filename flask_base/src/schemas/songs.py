from marshmallow import Schema, fields, validates_schema, ValidationError

# Schéma de sortie pour une chanson (renvoyé au front)
class SongSchema(Schema):
    id = fields.String(description="UUID")
    artist = fields.String(description="Artist")
    album = fields.String(description="Album")
    title = fields.String(description="Title")
    release_year = fields.String(description="Release year")
    genre = fields.String(description="Genre")
    
    @staticmethod
    def is_empty(obj):
        return (not obj.get("id") or obj.get("id") == "") and \
               (not obj.get("artist") or obj.get("artist") == "") and \
               (not obj.get("album") or obj.get("album") == "") and \
               (not obj.get("title") or obj.get("title") == "") and \
               (not obj.get("realease_year") or obj.get("realease_year") == "") and \
               (not obj.get("genre") or obj.get("genre") == "")


# Schéma pour la modification d'une chanson (artist, album, title, release_year, genre)
class SongUpdateSchema(Schema):
    # Permet de définir dans quelles conditions le schéma est validé ou non
    @validates_schema
    def validates_schemas(self, data, **kwargs):
        if not (("artist" in data and data["artist"] != "") or
                ("album" in data and data["album"] != "") or
                ("title" in data and data["title"] != "") or
                ("realease_year" in data and data["realease_year"] != "") or
                ("genre" in data and data["genre"] != "")):
            raise ValidationError("at least one of ['artist','album','title','realease_year','genre'] must be specified")
        
class SongCreateSchema(Schema):
    artist = fields.String(required=True)
    album = fields.String(required=True)
    title = fields.String(required=True)
    release_year = fields.String(required=True)
    genre = fields.String(required=True)
