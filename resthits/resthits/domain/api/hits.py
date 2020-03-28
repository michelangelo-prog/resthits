from flask import Blueprint, abort, jsonify
from marshmallow import Schema, fields, validate

from resthits.domain.decorators import request_schema
from resthits.domain.models.hits import Hit

hit_blueprint = Blueprint("hit", __name__)


class CreateHitRequestSchema(Schema):
    artistId = fields.Integer(required=True)
    title = fields.Str(required=True, validate=validate.Length(min=1, max=200))


class UpdateHitRequestSchema(Schema):
    artistId = fields.Integer(required=True)
    title = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    titleUrl = fields.Str(required=True, validate=validate.Length(min=1, max=300))


def hit_to_dict(hit):
    return {
        "id": hit.id,
        "title": hit.title,
        "titleUrl": hit.title_url,
        "createdAt": hit.created_at.strftime("%Y-%m-%dT%H:%M:%S%Z"),
        "artist": {
            "id": hit.artist_id,
            "firstName": hit.artist.first_name,
            "lastName": hit.artist.last_name,
        },
    }


@hit_blueprint.route("/hits", methods=["GET"])
def get_twenty_recent_hits():
    try:
        hits = Hit.get_twenty_recent_hits()
    except:
        abort(500)
    else:
        if len(hits):
            return (
                jsonify(
                    [
                        {"id": hit.id, "title": hit.title, "titleUrl": hit.title_url}
                        for hit in hits
                    ]
                ),
                200,
            )
        return {}, 204


@hit_blueprint.route("/hits/<string:title_url>", methods=["GET"])
def get_hit_details(title_url):
    try:
        hit = Hit.get_hit_by_title_url(title_url)
    except:
        abort(500)
    else:
        if hit:
            return jsonify(hit_to_dict(hit)), 200
        abort(404)


@hit_blueprint.route("/hits", methods=["POST"])
@request_schema(CreateHitRequestSchema)
def add_hit(json_data):
    try:
        hit = Hit.add_hit_from_json_data(json_data)
    except:
        abort(500)
    else:
        if hit:
            return {}, 201
        abort(400)


@hit_blueprint.route("/hits/<string:title_url>", methods=["PUT"])
@request_schema(UpdateHitRequestSchema)
def update_hit(json_data, title_url):
    try:
        hit = Hit.update_hit_by_title_url_from_json_data(title_url, json_data)
    except:
        abort(500)
    else:
        if hit:
            return {}, 204
        abort(400)


@hit_blueprint.route("/hits/<string:title_url>", methods=["DELETE"])
def delete_hit(title_url):
    try:
        if_deleted = Hit.delete_hit_by_title_url(title_url)
    except:
        abort(500)
    else:
        if if_deleted:
            return {}, 204
        abort(400)
