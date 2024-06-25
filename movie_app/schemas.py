from marshmallow import Schema, fields, validate

class MovieSchema(Schema):
    title = fields.String(required=True, validate=validate.Length(min=1))
    poster = fields.String(required=True, validate=validate.Length(min=1))
    description = fields.String(required=True, validate=validate.Length(min=1))

movie_schema = MovieSchema()
