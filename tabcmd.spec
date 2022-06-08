# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# https://stackoverflow.com/questions/61718298/compiling-gettext-locales-with-pyinstaller-in-python-3-x
def get_locales_data():
    locales_data = []
    for locale in os.listdir(os.path.join('tabcmd', 'locales')):
        locales_data.append((
            os.path.join('tabcmd', 'locales', locale, 'LC_MESSAGES', 'tabcmd.mo'),
            os.path.join('tabcmd', 'locales', locale, 'LC_MESSAGES')
        ))
    print("bundling localization data")
    print(locales_data)
    return locales_data

a = Analysis(['tabcmd\\tabcmd.py'],
             pathex=[],
             binaries=[],
             datas=get_locales_data(),
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
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
          a.binaries,
          a.zipfiles,
          a.datas,  
          [],
          name='tabcmd',
          debug=False, #'imports',
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None , uac_admin=True,
          icon= 'res\\tabcmd.ico'
          )
