import subprocess
import platform


def for_windows(path_to_card: str) -> dict:
    try:
        if path_to_card[-1:] == '/':
            path_to_card = path_to_card[0:-1]

        format_command = f'format {path_to_card} /FS:exFAT /Q /V:Card'
        process = subprocess.Popen(format_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, shell=True)
        process.communicate(input=b'\n')
        process.wait()

        if process.returncode == 0:
            return {'status': 'ok', 'text': f'Карта памяти успешно отформатирована'}
        else:
            return {'status': 'error', 'text': f'Произошла ошибка при форматировании карты памяти.\n{process.returncode}'}
    except Exception as error:
        return {'status': 'error', 'text': f'Произошла ошибка при форматировании карты памяти:\n{str(error)}'}


def for_linux() -> dict:
    try:
        subprocess.run(['sudo', '-S', 'umount', '/dev/mmcblk0p1'])
        subprocess.run(['sudo', '-S', 'mkfs.exfat', '/dev/mmcblk0p1', '-n', 'Card'])

        return {'status': 'ok', 'text': 'Карта памяти успешно отформатирована.'}
    except Exception as error:
        return {'status': 'error', 'text': f'Произошла ошибка при форматировании карты памяти:\n{str(error)}'}


def format_card(path_to_card: str) -> dict:
    system = platform.system()

    if system == 'Windows':
        return for_windows(path_to_card)
    elif system == 'Linux':
        return for_linux()
