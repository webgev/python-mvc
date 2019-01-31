from PIL import Image
import glob, os

def SaveImage(image, path, size=(128, 128)):
    image_type = get_image_type(image.content_type)
    if not image_type:
        raise Warning("Bed type image")
    im = Image.open(image)
    im.thumbnail(size)
    im.save(path, image_type)


def get_image_type(image_type):
    image_type = image_type.lower()
    if image_type == "image/png":
        return "png"
    if image_type == "image/jpg":
        return "jpg"
    if image_type == "image/jpeg":
        return "jpeg"
    if image_type == "image/gif":
        return "gif"

    return False