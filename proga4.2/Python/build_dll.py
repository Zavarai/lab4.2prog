import subprocess
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
C_DIR = BASE_DIR.parent / "C"
BUILD_DIR = C_DIR / "build"


def main():
    BUILD_DIR.mkdir(exist_ok=True)
    command = [
        "g++",
        "-std=c++17",
        "-shared",
        "-O2",
        "-static-libgcc",
        "-static-libstdc++",
        "-o",
        str(BUILD_DIR / "list.dll"),
        str(C_DIR / "list.cpp"),
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr or result.stdout or "Ошибка сборки.")
    print("DLL собрана.")


if __name__ == "__main__":
    main()

