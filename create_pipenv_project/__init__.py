__version__ = "0.10"

import os
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
        self.package_name = self.get_package_name()
        self.git_init = self.get_git_init()
        print()

    def input(self, prompt: str) -> str:
        return input(f"{ansi.BOLD_PURPLE}{prompt}{ansi.END} ").strip()

    def get_project_name(self) -> str:
        while True:
            project_name = self.input("Project Name (ex: MyApp, CoolCalc):")

            if project_name == "":
                print_error("Project name cannot be empty.")
                continue

            if os.path.isdir(project_name):
                print_error(f"Directory '{project_name}' already exists.")
                continue

            return project_name

    def get_package_name(self) -> str:
        while True:
            package_name = self.input("Package Name (ex: my_app, cool_calc):")

            if package_name == "":
                print_error("Package name cannot be empty.")
                continue

            return package_name

    def get_git_init(self) -> bool:
        while True:
            is_git_init = self.input("Initialize Git repository?").lower()

            if is_git_init in ("y", "yes", "1"):
                return True

            if is_git_init in ("n", "no", "0"):
                return False

            print_error("Please specify if yes or no.")


class Outputs:
    def __init__(self, inputs: Inputs) -> None:
        self.create_project(inputs.project_name, inputs.package_name)

        if inputs.git_init:
            self.git_init()

        print(f"\n{ansi.GREEN}Project successfully created.{ansi.END}")
        print(
            f"Start writing your code at {ansi.YELLOW}"
            f"{os.path.join(inputs.project_name, inputs.package_name, '__init__.py')}"
            f"{ansi.END}.\n"
            f"Run with {ansi.YELLOW}pipenv run main{ansi.END}.\n"
        )

    def _copy_user_files(self, package_name: str) -> None:
        mapping = {
            "env": (".env", ".env.example"),
            ".gitignore": ".gitignore",
            "run.py": "run.py",
            "mypy.ini": "mypy.ini",
            "__init__.py": os.path.join(package_name, "__init__.py"),
            "entry_point.py": os.path.join(package_name, "entry_point.py"),
            "environ.py": os.path.join(package_name, "environ.py"),
            "logging.py": os.path.join(package_name, "logging.py"),
        }

        cpp_dirpath = os.path.dirname(create_pipenv_project.__file__)
        user_files_dirpath = os.path.join(cpp_dirpath, "user_files")

        for filename in os.listdir(user_files_dirpath):
            try:
                paste_path = mapping[filename]
            except KeyError:
                continue

            with open(os.path.join(user_files_dirpath, filename)) as file:
                content = file.read().replace("PACKAGE_NAME", package_name)

            paste_paths = [paste_path] if isinstance(paste_path, str) else paste_path

            for path in paste_paths:
                with open(path, "w") as file:
                    file.write(content)

    def create_project(self, project_name: str, package_name: str) -> None:
        os.mkdir(project_name)
        os.chdir(project_name)
        os.mkdir(package_name)

        self._copy_user_files(package_name)

        os.system("pipenv install --dev --skip-lock mypy black coverage pytest")
        FileOperations.insert_text(
            "Pipfile",
            5,
            "\n[scripts]",
            'main = "python run.py"',
            'tests = "coverage run -m pytest"',
            "check = \"bash -c 'black . && mypy . && mypy --install-types'\"",
        )
        FileOperations.insert_text(
            "Pipfile",
            12,
            'uvloop = {version = "*", markers = "sys_platform == \'linux\'"}',
        )
        os.system("pipenv install")

    def git_init(self) -> None:
        os.system("git init")
        os.system("git branch -m main")
        os.system("git add .")
        os.system('git commit -m "Create Pipenv project"')


def main() -> int:
    try:
        inputs = Inputs()
    except KeyboardInterrupt:
        print()
        return 0

    Outputs(inputs)

    return 0
