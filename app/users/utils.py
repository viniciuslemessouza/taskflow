import os, secrets
from PIL import Image, ImageOps
from flask import current_app
from app import login_manager
from app.users.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



def save_picture(form_picture):
    random_hex = secrets.token_hex(8)

    _, file_extension = os.path.splitext(form_picture.filename)

    picture_filename = random_hex + file_extension.lower()

    picture_path = os.path.join(current_app.root_path, 'static/profile_pictures', picture_filename)

    image = Image.open(form_picture)

    image = ImageOps.exif_transpose(image)

    image.thumbnail((128, 128))

    image.save(picture_path)

    return picture_filename


def delete_picture(filename):
    if not filename:
        return

    if filename == 'default.png':
        return

    picture_path = os.path.join(current_app.root_path, 'static/profile_pictures', filename)

    if os.path.exists(picture_path):
        os.remove(picture_path)