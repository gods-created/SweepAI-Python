from sys import executable
from subprocess import run, TimeoutExpired
from uuid import uuid4
from os import makedirs, path, remove

def runCodeService(
    code: str
) -> dict:
    TEMPORARY_FILES_STORE = './assets/temporary_files'
    makedirs(TEMPORARY_FILES_STORE, exist_ok=True)

    temporary_filename = uuid4().hex + '.py'
    path_to_temporary_file = path.join(TEMPORARY_FILES_STORE, temporary_filename)

    try:
        with open(path_to_temporary_file, mode='w', encoding='utf-8') as f:
            f.write(code)

        result = run(
            args=[executable, path_to_temporary_file],
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=10,
            check=False
        )

        return {
            'returncode': result.returncode,
            'stdout': result.stdout,
            'srderr': result.stderr
        }

    except (OSError, UnicodeError, TimeoutExpired, ) as e:
        err = f'Task time running expired: {str(e)}' if e.__class__.__name__ == 'TimeoutExpired' \
            else f'Unexpected error (run_code): {str(e)}'

        return {
            'returncode': 1,
            'stdout': None,
            'srderr': err
        } 

    finally:
        if path.exists(path_to_temporary_file):
            try:
                remove(path_to_temporary_file)
            except OSError:
                pass
