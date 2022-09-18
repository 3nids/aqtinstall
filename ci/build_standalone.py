import argparse

import gravitybee


VENV_BIN_PATH="venv/Scripts/"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("arch", nargs="?")
    args = parser.parse_args()

    # generate pseudo script
    # pip does not generate console_script any more but gravitybee expect it.
    with open(VENV_BIN_PATH + "aqtinstall.py", "w") as f:
        f.write("import aqt\nif __name__ == \"__main__\":\n    aqt.main()\n")

    # generate setup.py
    # pyppyn build wheel with deprecated setup.py bdist_wheel
    # so fake it with dummy setup.py
    with open("setup.py", "w") as f:
        f.write("import setuptools\nsetuptools.setup(name='aqtinstall', packages='aqt', package_data={'aqt': ['*.ini', '*.json']})\n")

    gbargs = gravitybee.Arguments(
        app_name="aqtinstall",
        pkg_name="aqt",
        script_path="venv/Scripts/aqtinstall.py",
        src_dir=".",
        pkg_dir=".",
        clean=False,
        with_latest=True,
        name_format="aqt" if args.arch is None else "aqt-" + args.arch,
    )

    pg = gravitybee.PackageGenerator(gbargs)
    pg.generate()
