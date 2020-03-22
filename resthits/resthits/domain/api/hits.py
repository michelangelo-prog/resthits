from flask import Blueprint, jsonify

from resthits.domain.models.hits import Hit

hit_blueprint = Blueprint("hit", __name__)


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
