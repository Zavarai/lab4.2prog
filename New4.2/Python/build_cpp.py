import subprocess
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
C_DIR = BASE_DIR.parent / "C"
BUILD_DIR = C_DIR / "build"


def build_one(source_name, dll_name):
    BUILD_DIR.mkdir(exist_ok=True)
    command = [
        "g++",
        "-std=c++17",
        "-shared",
        "-O2",
        "-static-libgcc",
        "-static-libstdc++",
        "-o",
        str(BUILD_DIR / dll_name),
        str(C_DIR / source_name),
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr or result.stdout or "Ошибка сборки.")


def main():
    build_one("list_dynamic.cpp", "list_dynamic.dll")
    build_one("list_stl.cpp", "list_stl.dll")
    print("C++ модули собраны.")


if __name__ == "__main__":
    main()

