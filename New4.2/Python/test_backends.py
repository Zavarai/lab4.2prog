from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent))

from app import build_cpp_modules, CppListModule, DYNAMIC_DLL, STL_DLL
from python_list import PythonListModule


def check_module(module):
    assert not module.add_end(1.0, "a")
    assert module.create_structure()
    assert module.add_end(1.0, "a")
    assert module.add_beg(0.0, "b")
    assert module.count() == 2
    assert module.search_by_first_value(1.0)
    assert module.delete_element(0.0, "b")
    assert module.count() == 1


def main():
    build_cpp_modules()
    check_module(PythonListModule())
    check_module(CppListModule(DYNAMIC_DLL))
    check_module(CppListModule(STL_DLL))
    print("Проверка пройдена.")


if __name__ == "__main__":
    main()
