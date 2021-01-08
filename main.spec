# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

SETUP_DIR = 'C:\\Users\\Shrimpwr\\Desktop\\Study\\softwaredev_course_design\\source\\'

a = Analysis(['main.py', 
            'books_manage.py', 
            'download.py',
            'C:\\Users\\Shrimpwr\\Desktop\\Study\\softwaredev_course_design\\source\\UI\\init.py',
            'C:\\Users\\Shrimpwr\\Desktop\\Study\\softwaredev_course_design\\source\\UI\\Ui_book_page.py',
            'C:\\Users\\Shrimpwr\\Desktop\\Study\\softwaredev_course_design\\source\\UI\\Ui_main.py',
            'C:\\Users\\Shrimpwr\\Desktop\\Study\\softwaredev_course_design\\source\\UI\\Ui_result_page.py',
            'C:\\Users\\Shrimpwr\\Desktop\\Study\\softwaredev_course_design\\source\\UI\\Ui_search_page.py',
            'C:\\Users\\Shrimpwr\\Desktop\\Study\\softwaredev_course_design\\source\\UI\\Ui_search_page.py',
            ],
             pathex=['C:\\Users\\Shrimpwr\\Desktop\\Study\\softwaredev_course_design\\source'],
             binaries=[],
             datas=[
                 (SETUP_DIR + "UI", "UI"), 
                 (SETUP_DIR + "data", "data")
                ],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='main')
