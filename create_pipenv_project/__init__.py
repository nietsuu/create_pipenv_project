__version__ = "0.1"

import os
import shutil
import create_pipenv_project
from create_pipenv_project.terminal import ANSICodes as ansi, print_error


class FileOperations:
    @staticmethod
    def insert_text(filename: str, line: int, *texts: str) -> None:
        with open(filename, "r") as file:
            contents = file.readlines()

        contents.insert(line - 1, "\n".join(texts) + "\n")

        with open(filename, "w") as file:
            file.write("".join(contents))


class Inputs:
    def __init__(self) -> None:
        self.project_name = self.get_project_name()

    def input(self, prompt: str) -> str:
        return input(f"{ansi.BOLD_PURPLE}{prompt}:{ansi.END} ").strip()

    def get_project_name(self) -> str:
        while True:
            project_name = self.input("Project Name")

            if project_name == "":
                print_error("Project name cannot be empty.")
                continue

            if os.path.isdir(project_name):
                print_error(f"Directory '{project_name}' already exists.")
                continue

            return project_name


class Outputs:
    def __init__(self, inputs: Inputs) -> None:
        self.create_project(inputs.project_name)

    def _copy_user_files(self, project_name: str) -> None:
        mapping = {
            "env": ".env",
            ".gitignore": ".",
            "run.py": ".",
            "run_tests.sh": ".",
            "__init__.py": project_name,
            "logging.py": project_name,
        }

        cpp_dirpath = os.path.dirname(create_pipenv_project.__file__)
        user_files_dirpath = os.path.join(cpp_dirpath, "user_files")

        for filename in os.listdir(user_files_dirpath):
            paste_dir = mapping[filename]
            shutil.copy(
                os.path.join(user_files_dirpath, filename),
                paste_dir,
            )

    def create_project(self, name: str) -> None:
        os.mkdir(name)
        os.chdir(name)
        os.mkdir(name)
        os.mkdir("tests")

        self._copy_user_files(name)
        FileOperations.insert_text(
            "run.py",
            66,
            f"    from {name} import main",
            f"    from {name}.logging import get_logger",
            "",
        )

        os.system("pipenv install --dev --skip-lock mypy black coverage pytest")
        FileOperations.insert_text(
            "Pipfile",
            5,
            "\n[scripts]",
            'app = "python run.py"',
            'tests = "./run_tests.sh"',
            'format = "black ."',
        )
        FileOperations.insert_text(
            "Pipfile",
            12,
            'uvloop = {version = "*", sys_platform = "== \'linux\'"}',
        )
        os.system("pipenv install")


def main() -> int:
    Outputs(Inputs())
    return 0
