import contextlib
from contextlib import ExitStack
import os
from pathlib import Path
from tempfile import TemporaryDirectory
import shutil
import subprocess
import sys
import urllib.request

import setuptools.command.build_ext


@contextlib.contextmanager
def patched_path(path, old, new):
    contents = path.read_text("latin-1")
    if old not in contents:
        raise Exception(f"Invalid patch: {old}")
    try:
        path.write_text(contents.replace(old, new), "utf-8")
        yield
    finally:
        path.write_text(contents, "latin-1")


patches = [
    ("TransTableL.cpp",
     "const unsigned char lengths[][DDS_SUITS]) const",
     "const unsigned char lengths[DDS_SUITS][DDS_SUITS]) const"),
    ("Moves.cpp", "", ""),  # Only for reencoding.
]


class build_ext(setuptools.command.build_ext.build_ext):
    def finalize_options(self):
        super().finalize_options()
        # Needs to be computed here because setuptools patches out inplace.
        self.__dest_dir = Path(self.get_ext_fullpath("redeal._")).parent

    def build_extensions(self):
        self.distribution.ext_modules[:] = []
        super().build_extensions()
        if os.name == "posix":
            dds_src = Path(__file__).resolve().parent / "dds"
            if not dds_src.exists():
                sys.exit("DDS sources are missing.")
            with ExitStack() as stack:
                for name, old, new in patches:
                    if old:
                        stack.enter_context(patched_path(dds_src / name, old, new))
                
                # Use the existing Makefile in dds/
                subprocess.check_call(["make", "clean"], cwd=dds_src)
                subprocess.check_call(["make"], cwd=dds_src)
                
                if sys.platform == "darwin":
                    shutil.copy2(dds_src / "libdds.dylib", self.__dest_dir / "libdds.so")
                else:
                    # On Linux it might produce libdds.so or we might need to adjust the Makefile
                    # For now, let's assume it might produce libdds.so
                    so_path = dds_src / "libdds.so"
                    if not so_path.exists():
                        # Fallback if the Makefile produced something else
                        dylib_path = dds_src / "libdds.dylib"
                        if dylib_path.exists():
                            shutil.copy2(dylib_path, self.__dest_dir / "libdds.so")
                        else:
                            raise Exception("Could not find libdds.so or libdds.dylib")
                    else:
                        shutil.copy2(so_path, self.__dest_dir)
                        
        elif os.name == "nt":
            url = "https://privat.bahnhof.se/wb758135/bridge/dds290-dll.zip"
            with TemporaryDirectory() as tmpdir:
                tmppath = Path(tmpdir)
                zip_path = tmppath / "dds290-dll.zip"
                with urllib.request.urlopen(url) as req:
                    zip_path.write_bytes(req.read())
                shutil.unpack_archive(str(zip_path), tmpdir)
                arch = "x64" if sys.maxsize > 2 ** 32 else "win32"
                shutil.unpack_archive(
                    str(tmppath / f"dds290-dll/dds-290-multi-{arch}-dll.zip"),
                    tmppath)
                shutil.copy2(tmppath / "dds.dll", self.__dest_dir)


setuptools.setup(
    cmdclass={"build_ext": build_ext},
    ext_modules=[setuptools.Extension("redeal._", [])],
    packages=["redeal"],
)
