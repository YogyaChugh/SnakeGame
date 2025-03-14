# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('background.jpeg','.'),('body_bottomleft.png','.'),('body_bottomright.png','.'),('body_horizontal.png','.'),('body_topleft.png','.'),('body_topright.png','.'),('body_vertical.png','.'),('fruit.png','.'),('head_down.png','.'),('head_left.png','.'),('head_right.png','.'),('head_up.png','.'),('Logo.png','.'),('saved_fruits.json','.'),('saved_maps.json','.'),('saved_snakes.json','.'),('tail_down.png','.'),('tail_left.png','.'),('tail_left.png','.'),('tail_right.png','.'),('tail_up.png','.'),('wooden_block.png','.'),('wooden_dark_block.png','.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['Logo.png'],
)
