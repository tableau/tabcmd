# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

localized_strings = [
    ('tabcmd/locales/en/LC_MESSAGES/tabcmd.mo', 'tabcmd/locales/en/LC_MESSAGES'),
    ('tabcmd/locales/de/LC_MESSAGES/tabcmd.mo', 'tabcmd/locales/de/LC_MESSAGES'),
    ('tabcmd/locales/es/LC_MESSAGES/tabcmd.mo', 'tabcmd/locales/es/LC_MESSAGES'),
    ('tabcmd/locales/fr/LC_MESSAGES/tabcmd.mo', 'tabcmd/locales/fr/LC_MESSAGES'),
    ('tabcmd/locales/ga/LC_MESSAGES/tabcmd.mo', 'tabcmd/locales/ga/LC_MESSAGES'),
    ('tabcmd/locales/it/LC_MESSAGES/tabcmd.mo', 'tabcmd/locales/it/LC_MESSAGES'),
    ('tabcmd/locales/ja/LC_MESSAGES/tabcmd.mo', 'tabcmd/locales/ja/LC_MESSAGES'),
    ('tabcmd/locales/ko/LC_MESSAGES/tabcmd.mo', 'tabcmd/locales/ko/LC_MESSAGES'),
    ('tabcmd/locales/pt/LC_MESSAGES/tabcmd.mo', 'tabcmd/locales/pt/LC_MESSAGES'),
    ('tabcmd/locales/sv/LC_MESSAGES/tabcmd.mo', 'tabcmd/locales/sv/LC_MESSAGES'),
    ('tabcmd/locales/zh/LC_MESSAGES/tabcmd.mo', 'tabcmd/locales/zh/LC_MESSAGES'),
    ]

a = Analysis(
    ['tabcmd\\tabcmd.py'],
    pathex=[],
    binaries=[],
    datas=localized_strings,
    hiddenimports=['tableauserverclient', 'requests.packages.urllib3', 'pkg_resources'],
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
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
