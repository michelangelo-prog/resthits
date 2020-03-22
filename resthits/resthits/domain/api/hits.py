from flask import Blueprint, abort, jsonify

from resthits.domain.models.hits import Hit

hit_blueprint = Blueprint("hit", __name__)


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
    hits = Hit.get_twenty_recent_hits()
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
    hit = Hit.get_hit_by_title_url(title_url)
    if hit:
        return jsonify(hit_to_dict(hit)), 200
    abort(404)
