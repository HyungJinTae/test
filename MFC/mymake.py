import argparse
import os
import shutil

pyinstaller_string = "pyinstaller --noconsole Main_INDEGO_MFC.py"
pyrcc5_string = "pyrcc5 -o resources_rc.py resources.qrc"
pyuic5_string = "pyuic5 -x Main_INDEGO_MFC.ui -o Main_INDEGO_MFC_UI.py"
copy1_src_string = "./resources"
copy1_dst_string = "./dist/Main_INDEGO_MFC/resources"
copy2_src_string = "./Main_INDEGO_MFC.ui"
copy2_dst_string = "./dist/Main_INDEGO_MFC/Main_INDEGO_MFC.ui"

help_string = ""
help_string += pyinstaller_string
help_string += " | "
help_string += pyrcc5_string
help_string += " | "
help_string += pyuic5_string
help_string += " | "
help_string += copy1_src_string
help_string += " "
help_string += copy1_dst_string
help_string += " | "
help_string += copy2_src_string
help_string += " "
help_string += copy2_dst_string
help_string += " | "


def parse():
    parser = argparse.ArgumentParser(prog="mymake", description="My Makefile")
    parser.add_argument("--a", type=str, dest="action", action="store",
                        choices=["pyinstaller", "pyrcc5", "pyuic5", "copy"], default="pyuic5",
                        help=help_string)
    parser.add_argument("-action", type=str, dest="action", action="store",
                        choices=["pyinstaller", "pyrcc5", "pyuic5", "copy"], default="pyuic5",
                        help=help_string)
    args = parser.parse_args()
    return args


def my_execute(args):
    if args.action == "pyinstaller":
        os.system(pyinstaller_string)
    elif args.action == "pyrcc5":
        os.system(pyrcc5_string)
    elif args.action == "pyuic5":
        os.system(pyuic5_string)
    elif args.action == "copy":
        shutil.copytree(copy1_src_string, copy1_dst_string)
        shutil.copy2(copy2_src_string, copy2_dst_string)


if __name__ == "__main__":
    args = parse()
    my_execute(args)
