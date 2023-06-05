import os
import shutil
import datetime
import random
import string


def create_file_name(ext: str) -> str:
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    random_string = ''.join(random.sample(timestamp + string.ascii_letters, k=20))

    return f"{random_string}.{ext}"


def check_directories(path: dict) -> dict:
    if not os.path.exists(path['base']):
        return {'status': 'error', 'text': 'Дериктория отсутствует'}

    if not os.path.exists(path['photo']):
        os.makedirs(path['photo'])

    if not os.path.exists(path['video']):
        os.makedirs(path['video'])

    return {'status': 'ok'}


def copying_files(path: dict) -> dict:
    errors: str = ''
    input_dir_path: str = path['card_path']
    output_dir_path: dict = {
        'base': path['save_path'],
        'photo': os.path.join(path['save_path'], 'photo'),
        'video': os.path.join(path['save_path'], 'video')
    }

    check_result = check_directories(output_dir_path)

    if check_result['status'] == 'error':
        return check_result

    for root, directories, files in os.walk(input_dir_path):
        for file in files:
            try:
                file_path = os.path.join(root, file)
                file_parts = file.split('.')

                if len(file_parts) <= 1:
                    continue

                ext = file_parts[1].lower()

                if ext == 'jpg':
                    output_file_path = os.path.join(output_dir_path['photo'], create_file_name(ext))
                elif ext == 'mp4':
                    output_file_path = os.path.join(output_dir_path['video'], create_file_name(ext))
                else:
                    continue

                shutil.copy(file_path, output_file_path)

            except Exception as error:
                errors += f"Error: {error}\n"

    if len(errors) != 0:
        return {'status': 'error', 'text': errors}
    else:
        return {'status': 'ok', 'text': 'Файлы успешно перенесены'}

