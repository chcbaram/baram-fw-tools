import os
import wget
import platform
import zipfile
import py_setenv


print("---------------")
print("BARAM F/W TOOLS")
print("2023. 7. 31.")
print("---------------\n")

OS_64BIT = 0
OS_32BIT = 1


cmake_file_name = 'tool_cmake.zip'
arm_gcc_file_name = 'tool_arm_gcc.zip'
mingw_gcc_file_name = 'tool_mingw_gcc.zip'
make_file_name = 'tool_make.zip'


os_arch = platform.architecture()

if os_arch[0] == '64bit':
  print("Windows 64Bit")
  OS_BITS = OS_64BIT
else:
  print("Windows 32Bit")
  OS_BITS = OS_32BIT


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


print(" ")
print('Unzip - CMAKE')
with zipfile.ZipFile(cmake_file_name, 'r') as zip_ref:
  zip_ref.extractall("cmake")

print('Unzip - MAKE')
with zipfile.ZipFile(make_file_name, 'r') as zip_ref:
  zip_ref.extractall("make")  

print('Unzip - ARM_GCC')
with zipfile.ZipFile(arm_gcc_file_name, 'r') as zip_ref:
  zip_ref.extractall("arm_gcc")    

print('Unzip - MINGW_GCC')
with zipfile.ZipFile(mingw_gcc_file_name, 'r') as zip_ref:
  zip_ref.extractall("mingw_gcc")      



cur_path = os.getcwd()

arm_gcc_path = cur_path + "\\arm_gcc\\" + os.listdir(cur_path + "\\arm_gcc")[0] + "\\bin"
cmake_path = cur_path + "\\cmake\\" + os.listdir(cur_path + "\\cmake")[0] + "\\bin"
make_path = cur_path + "\\make\\" + os.listdir(cur_path + "\\make")[0] + "\\bin"
mingw_gcc_path = cur_path + "\\mingw_gcc" + "\\bin"



PATH_STR = py_setenv.get_variable("PATH", user=True)


print("Path - ARM_GCC")
py_setenv.setenv("ARM_TOOLCHAIN_DIR", value=arm_gcc_path, user=True, suppress_echo=True)
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

