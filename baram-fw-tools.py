import os
import wget
import platform
import zipfile
import tarfile
import py_setenv
import git
import stat
import shutil
import json
import subprocess
import sys
import ssl

from git import RemoteProgress
from tqdm import tqdm
from utils import *


print("---------------")
print("BARAM F/W TOOLS")
print("2023. 11. 8.")
print("---------------\n")

OS_64BIT = 0
OS_32BIT = 1

ssl._create_default_https_context = ssl._create_unverified_context

os_arch = platform.architecture()
cur_path = os.getcwd()
down_path = cur_path + "\\downloads"
arm_tool_path = cur_path + "\\arm_toolchain"

cmake_file_name     = down_path + "\\" + 'tool_cmake.zip'
arm_gcc_file_name   = down_path + "\\" + 'tool_arm_gcc.zip'
mingw_gcc_file_name = down_path + "\\" + 'tool_mingw_gcc.zip'
make_file_name      = down_path + "\\" + 'tool_make.zip'
openocd_file_name   = down_path + "\\" + 'tool_openocd.tar.gz'


if os_arch[0] == '64bit':
  print("Windows 64Bit")
  OS_BITS = OS_64BIT
else:
  print("Windows 32Bit")
  OS_BITS = OS_32BIT
print()

if os.path.exists(down_path) == False:
  os.mkdir(down_path)
  
if os.path.exists(arm_tool_path) == False:
  os.mkdir(arm_tool_path)


def download_ARM_TOOL_CHAIN():
    
  print('Download - CMAKE')
  cmake_down_url = ['https://github.com/Kitware/CMake/releases/download/v3.27.1/cmake-3.27.1-windows-x86_64.zip', 
                    'https://github.com/Kitware/CMake/releases/download/v3.27.1/cmake-3.27.1-windows-i386.zip']
  if os.path.exists(cmake_file_name) == False:
    # os.remove(cmake_file_name)
    wget.download(cmake_down_url[OS_BITS], out=cmake_file_name)

  print("\nDownload - MAKE")
  make_down_url = ['https://github.com/xpack-dev-tools/windows-build-tools-xpack/releases/download/v4.4.0-1/xpack-windows-build-tools-4.4.0-1-win32-x64.zip',
                  'https://github.com/xpack-dev-tools/windows-build-tools-xpack/releases/download/v4.4.0-1/xpack-windows-build-tools-4.4.0-1-win32-x64.zip']
  if os.path.exists(make_file_name) == False:
    wget.download(make_down_url[OS_BITS], out=make_file_name)
  
  print('\nDownload - ARM_GCC')
  arm_gcc_down_url = ['https://developer.arm.com/-/media/Files/downloads/gnu-rm/10.3-2021.10/gcc-arm-none-eabi-10.3-2021.10-win32.zip',
                      'https://developer.arm.com/-/media/Files/downloads/gnu-rm/10.3-2021.10/gcc-arm-none-eabi-10.3-2021.10-win32.zip']
  if os.path.exists(arm_gcc_file_name) == False:
    wget.download(arm_gcc_down_url[OS_BITS], out=arm_gcc_file_name)

  print('\nDownload - MINGW_GCC')
  mingw_gcc_down_url = ['https://github.com/chcbaram/baram-fw-tools/releases/download/tools/mingw32.zip',
                        'https://github.com/chcbaram/baram-fw-tools/releases/download/tools/mingw32.zip']
  if os.path.exists(mingw_gcc_file_name) == False:
    wget.download(mingw_gcc_down_url[OS_BITS], out=mingw_gcc_file_name)

  print('\nDownload - OpenOCD') 
  openocd_down_url = ['https://github.com/openocd-org/openocd/releases/download/v0.12.0/openocd-v0.12.0-i686-w64-mingw32.tar.gz',
                      'https://github.com/openocd-org/openocd/releases/download/v0.12.0/openocd-v0.12.0-i686-w64-mingw32.tar.gz']
  if os.path.exists(openocd_file_name) == False:
    wget.download(openocd_down_url[OS_BITS], out=openocd_file_name)



def install_ARM_TOOL_CHAIN():
  print(" ")
  if os.path.exists(cmake_file_name) == True:
    print('Unzip - CMAKE')
    with zipfile.ZipFile(cmake_file_name, 'r') as zip_ref:
      zip_ref.extractall(arm_tool_path + "\\" + "cmake")

  if os.path.exists(make_file_name) == True:
    print('Unzip - MAKE')
    with zipfile.ZipFile(make_file_name, 'r') as zip_ref:
      zip_ref.extractall(arm_tool_path + "\\" + "make")  

  if os.path.exists(arm_gcc_file_name) == True:
    print('Unzip - ARM_GCC')
    with zipfile.ZipFile(arm_gcc_file_name, 'r') as zip_ref:
      zip_ref.extractall(arm_tool_path + "\\" + "arm_gcc")    

  if os.path.exists(mingw_gcc_file_name) == True:
    print('Unzip - MINGW_GCC')
    with zipfile.ZipFile(mingw_gcc_file_name, 'r') as zip_ref:
      zip_ref.extractall(arm_tool_path + "\\" + "mingw_gcc")      

  if os.path.exists(openocd_file_name) == True:
    print('Unzip - OpenOCD')
    with tarfile.open(openocd_file_name, 'r') as tar_ref:
      tar_ref.extractall(arm_tool_path + "\\" + "openocd")   

  arm_gcc_path   = arm_tool_path + "\\arm_gcc\\" + os.listdir(arm_tool_path + "\\arm_gcc")[0] + "\\bin"
  cmake_path     = arm_tool_path + "\\cmake\\" + os.listdir(arm_tool_path + "\\cmake")[0] + "\\bin"
  make_path      = arm_tool_path + "\\make\\" + os.listdir(arm_tool_path + "\\make")[0] + "\\bin"
  mingw_gcc_path = arm_tool_path + "\\mingw_gcc" + "\\bin"
  openocd_path   = arm_tool_path + "\\openocd" 


  PATH_STR = py_setenv.get_variable("PATH", user=True)


  print("Path - HOME_TOOLCHAIN_DIR")
  py_setenv.setenv("HOME_TOOLCHAIN_DIR", value=cur_path, user=True, suppress_echo=True)
  print("       " + cur_path)
  
  print("Path - ARM_GCC")
  py_setenv.setenv("ARM_TOOLCHAIN_DIR", value=arm_gcc_path, user=True, suppress_echo=True)
  print("       " + arm_gcc_path)

  print("Path - MINGW_GCC")
  py_setenv.setenv("GCC_TOOLCHAIN_DIR", value=arm_gcc_path, user=True, suppress_echo=True)
  print("       " + arm_gcc_path)


  print("Path - CMAKE")
  if PATH_STR.find(cmake_path) < 0:
    py_setenv.setenv("PATH", value=cmake_path, append=True, user=True, suppress_echo=True)
    print("     N " + cmake_path)
  else:
    print("       " + cmake_path)

  print("Path - MAKE")
  if PATH_STR.find(make_path) < 0:
    py_setenv.setenv("PATH", value=make_path, append=True, user=True, suppress_echo=True)
    print("     N " + make_path)
  else:
    print("       " + make_path)

  print("Path - MINGW_GCC")
  if PATH_STR.find(mingw_gcc_path) < 0:
    py_setenv.setenv("PATH", value=mingw_gcc_path, append=True, user=True, suppress_echo=True)
    print("     N " + mingw_gcc_path)
  else:
    print("       " + mingw_gcc_path)


  print("Path - OpenOCD")
  py_setenv.setenv("OPENOCD_DIR", value=openocd_path, user=True, suppress_echo=True)
  print("       " + openocd_path)



def install_ESP_IDF(json_obj):
  for obj in json_obj:  
    print(obj)
  
    for item in json_obj[obj]: 
      print("    %-10s"%item + " : " + json_obj[obj][item])

    esp_idf_path = cur_path + "\\esp\\esp-idf-" + json_obj[obj]['branch']
    esp_idf_git = "https://github.com/espressif/esp-idf.git"
    esp_idf_ver = json_obj[obj]['branch']

    if json_obj[obj]['install'] != "True":
      print("Not Install..")
      continue
    else:
      print("Install..")

    if os.path.exists(esp_idf_path) == True:
      # shutil.rmtree(repo_path, onerror=make_dir_writable)
      print("Already Exist..")
      return

    git.Repo.clone_from(esp_idf_git,
                        esp_idf_path,
                        progress= CloneProgress(),
                        branch=esp_idf_ver, recursive=True,                     
                        )
    print(esp_idf_path)
    os.chdir(esp_idf_path)

    p = subprocess.Popen(["powershell", "Set-ExecutionPolicy RemoteSigned -Scope CurrentUser"], stdout=sys.stdout)
    p.communicate()

    try:
      os.environ["IDF_PATH"] = cur_path + "\\esp\\esp-idf-" + esp_idf_ver
      os.environ["IDF_TOOLS_PATH"] = cur_path + "\\esp\\esp-tools-" + esp_idf_ver

      p = subprocess.Popen(["powershell", ".\\install.ps1"], stdout=sys.stdout)
      p.communicate()

      print("Path - " + json_obj[obj]['idf_env'])
      py_setenv.setenv(json_obj[obj]['idf_env'], value=os.environ["IDF_PATH"], user=True, suppress_echo=True)
      print("       " + os.environ["IDF_PATH"])

      print("Path - " + json_obj[obj]['tool_env'])
      py_setenv.setenv(json_obj[obj]['tool_env'], value=os.environ["IDF_TOOLS_PATH"], user=True, suppress_echo=True)
      print("       " + os.environ["IDF_TOOLS_PATH"])

    except:
      print("Error\n")
    

def install_PICO_SDK(json_obj):
  repo_path = cur_path + "\\rp2040\\pico-sdk-" + json_obj['branch']
  repo_git = "https://github.com/raspberrypi/pico-sdk.git"
  repo_ver = json_obj['branch']
  
  if os.path.exists(repo_path) == True:
    # shutil.rmtree(repo_path, onerror=make_dir_writable)
    print("Already Exist..")
  else:
    git.Repo.clone_from(repo_git,
                        repo_path,
                        progress= CloneProgress(),
                        branch=repo_ver, recursive=True,                     
                        )
    print("    " + repo_path)      
  
  os.environ["PICO_SDK_PATH"] = repo_path
  os.environ["PICO_TOOLCHAIN_PATH"] = os.environ["ARM_TOOLCHAIN_DIR"]

  py_setenv.setenv("PICO_SDK_PATH", value=os.environ["PICO_SDK_PATH"], user=True, suppress_echo=True)
  print("    PICO_SDK_PATH : " + os.environ["PICO_SDK_PATH"])

  py_setenv.setenv("PICO_TOOLCHAIN_PATH", value=os.environ["PICO_TOOLCHAIN_PATH"], user=True, suppress_echo=True)
  print("    PICO_TOOLCHAIN_PATH : " + os.environ["PICO_TOOLCHAIN_PATH"])
  
  print()      
  return


def install_PICO_EXTRAS(json_obj):
  repo_path = cur_path + "\\rp2040\\pico-extras-" + json_obj['branch']
  repo_git = "https://github.com/raspberrypi/pico-extras.git"
  repo_ver = json_obj['branch']
  
  if os.path.exists(repo_path) == True:
    # shutil.rmtree(repo_path, onerror=make_dir_writable)
    print("Already Exist..")
  else:
    git.Repo.clone_from(repo_git,
                        repo_path,
                        progress= CloneProgress(),
                        branch=repo_ver, recursive=True,                     
                        )
    print("    " + repo_path)      
  
  os.environ["PICO_EXTRAS_PATH"] = repo_path

  py_setenv.setenv("PICO_EXTRAS_PATH", value=os.environ["PICO_EXTRAS_PATH"], user=True, suppress_echo=True)
  print("    PICO_EXTRAS_PATH : " + os.environ["PICO_EXTRAS_PATH"])

  
  print()      
  return


def install_RP2040(json_obj):
  for obj in json_obj:  
    print(obj)

    for item in json_obj[obj]: 
      print("    %-10s"%item + " : " + json_obj[obj][item])
      
    if json_obj[obj]['install'] != "True":
      print("Not Install..")
      print()
      continue
    else:
      print("Install..")    
        
    if obj == "pico-sdk":
      install_PICO_SDK(json_obj[obj])
    if obj == "pico-extras"  :
      install_PICO_EXTRAS(json_obj[obj])
    


download_ARM_TOOL_CHAIN()
print()
install_ARM_TOOL_CHAIN()
print()


with open('setup.json') as f:
    json_obj = json.load(f)

for obj in json_obj:  
  if obj == "esp-idf":
    install_ESP_IDF(json_obj[obj])
    print()
    
  if obj == "rp2040":
    install_RP2040(json_obj[obj])
    print()
    