from app.models import Article, Cover
from app import db


def cover_inserter(cover_image_destination, cover_image_name, input_journal):
    cover = Cover(
        cover_url=cover_image_destination,
        cover_name=cover_image_name,
        journal=input_journal,
    )
    db.session.add(cover)
    db.session.commit()
    print("cover uploaded")
