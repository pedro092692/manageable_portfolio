import os


def get_avatar_extension():
    for file in os.listdir('static/images'):
        if file.split('.')[0] == 'avatar':
            return file

