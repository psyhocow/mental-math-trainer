"""PyInstaller build definition shared by Windows, macOS, and Linux."""

from pathlib import Path
import sys

from PyInstaller.utils.hooks import collect_all


root = Path(SPECPATH)
pygame_datas, pygame_binaries, pygame_hiddenimports = collect_all("pygame")
datas = pygame_datas + [(str(root / "assets" / "ambient.wav"), "assets")]
icon = None
if sys.platform == "win32":
    icon = str(root / "assets" / "icon.ico")
elif sys.platform == "darwin":
    icon = str(root / "assets" / "icon.icns")

a = Analysis(
    [str(root / "run.py")],
    pathex=[str(root)],
    binaries=pygame_binaries,
    datas=datas,
    hiddenimports=pygame_hiddenimports,
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
    [],
    exclude_binaries=True,
    name="MentalMathTrainer",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="MentalMathTrainer",
)

if sys.platform == "darwin":
    app = BUNDLE(
        coll,
        name="MentalMathTrainer.app",
        icon=str(root / "assets" / "icon.icns"),
        bundle_identifier="com.psyhocow.mentalmathtrainer",
        info_plist={"NSHighResolutionCapable": "True"},
    )
