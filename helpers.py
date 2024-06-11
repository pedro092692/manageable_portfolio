import os


def get_avatar_extension(file_name):
    for file in os.listdir('static/images'):
        if file.split('.')[0] == file_name:
            return file


def get_info_page(db, type_info):
    value = ''
    info = db.check_page_info_type(type_info)
    if info:
        value = info.value
    return value


def save_img_file(img_type, img):
    # check if img exist
    file = get_avatar_extension(file_name=img_type)
    if file:
        os.remove(f'static/images/{file}')
    # save image
    new_img = img
    extension = new_img.filename.split('.')[1]
    new_img.filename = f'{img_type}.{extension}'
    new_img.save(os.path.join('static/images', new_img.filename))
