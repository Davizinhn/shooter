import cx_Freeze

# base = "Win32GUI" allows your application to open without a console window
executables = [cx_Freeze.Executable('main.py', base = "Win32GUI")]

cx_Freeze.setup(
    name = "Generic Space Shooter",
    options = {"build_exe" : 
        {"packages" : ["pygame"], "include_files" : ['assets/']}},
    executables = executables
)

## python setup.py build