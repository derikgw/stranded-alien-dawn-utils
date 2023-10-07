import subprocess
import sys


def install_and_import(package_name, module_name=None):
    if module_name is None:
        module_name = package_name
    try:
        __import__(module_name)
    except ImportError:
        subprocess.call([sys.executable, "-m", "pip", "install", package_name])
    finally:
        globals()[module_name] = __import__(module_name)


if __name__ == "__main__":
    install_and_import("nltk", "nltk")
    install_and_import("Pillow", "PIL.Image")
    install_and_import("Pillow", "PIL.ImageTk")
    install_and_import("pyperclip", "pyperclip")
