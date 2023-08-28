from __future__ import annotations
import os
import wget
import platform
import zipfile
import tarfile
import py_setenv
import git
import stat
from git import RemoteProgress
from tqdm import tqdm
import shutil


print("---------------")
print("BARAM F/W TOOLS")
print("2023. 8. 26.")
print("---------------\n")

OS_64BIT = 0
OS_32BIT = 1


cmake_file_name = 'tool_cmake.zip'
arm_gcc_file_name = 'tool_arm_gcc.zip'
mingw_gcc_file_name = 'tool_mingw_gcc.zip'
make_file_name = 'tool_make.zip'
openocd_file_name = 'tool_openocd.tar.gz'


os_arch = platform.architecture()

if os_arch[0] == '64bit':
  print("Windows 64Bit")
  OS_BITS = OS_64BIT
else:
  print("Windows 32Bit")
  OS_BITS = OS_32BIT



cur_path = os.getcwd()

# arm_gcc_path = cur_path + "\\arm_gcc\\" + os.listdir(cur_path + "\\arm_gcc")[0] + "\\bin"
# cmake_path = cur_path + "\\cmake\\" + os.listdir(cur_path + "\\cmake")[0] + "\\bin"
# make_path = cur_path + "\\make\\" + os.listdir(cur_path + "\\make")[0] + "\\bin"
# mingw_gcc_path = cur_path + "\\mingw_gcc" + "\\bin"
# openocd_path = cur_path + "\\openocd" 


# PATH_STR = py_setenv.get_variable("PATH", user=True)

class CloneProgress(RemoteProgress):
    def __init__(self):
        super().__init__()
        self.pbar = tqdm()

    def update(self, op_code, cur_count, max_count=None, message=''):
        self.pbar.total = max_count
        self.pbar.n = cur_count
        self.pbar.refresh()

def make_dir_writable(function, path, exception):
    """The path on Windows cannot be gracefully removed due to being read-only,
    so we make the directory writable on a failure and retry the original function.
    """
    os.chmod(path, stat.S_IWRITE)
    function(path)

if os.path.exists("esp/esp-idf-v5.1") == True:
  # os.remove("esp/esp-idf-v5.1")
  shutil.rmtree("esp/esp-idf-v5.1", onerror=make_dir_writable)

# git.Repo.clone_from("https://github.com/espressif/esp-idf.git",
#                     "esp/esp-idf-v5.1",
#                     progress= CloneProgress(),
#                     branch="v5.1", recursive=True,                     
#                     )