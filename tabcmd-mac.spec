# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files

datas = []
datas += collect_data_files('tabcmd.locales')


block_cipher = None


a = Analysis(
    ['tabcmd/tabcmd.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=['tableauserverclient', 'requests', 'urllib3', 'pkg_resources'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='tabcmd',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    runtime_tmpdir=None,
    console=True,
    codesign_identity=None,
    version='program_metadata.txt',
    target_arch=universal2
)

app = BUNDLE(
    exe,
    name = 'tabcmd.app',
    icon='res/tabcmd.icns',
    bundle_identifier = None,
)
