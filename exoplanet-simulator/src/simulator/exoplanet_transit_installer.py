import PyInstaller.__main__
import os
import shutil
import sys

if os.path.exists('dist'):
    shutil.rmtree('dist')
if os.path.exists('build'):
    shutil.rmtree('build')

pyinstaller_args = [
    'exoplanet_transit_simulator.py',
    '--name=ExoplanetTransitSimulator',
    '--onefile',
    '--windowed',
    '--icon=icon.ico',
    '--add-data=README.md:.',
    '--hidden-import=numpy',
    '--hidden-import=matplotlib',
    '--hidden-import=matplotlib.backends.backend_tkagg',
    '--clean',
    '--noconfirm',
]

PyInstaller.__main__.run(pyinstaller_args)

print("PyInstaller build completed!")

if not os.path.exists('icon.ico'):
    try:
        import matplotlib.pyplot as plt
        import numpy as np
        from matplotlib.patches import Circle
        
        fig, ax = plt.subplots(figsize=(5, 5))
        ax.set_aspect('equal')
        ax.set_xlim(-1.2, 1.2)
        ax.set_ylim(-1.2, 1.2)
        ax.axis('off')
        
        star = Circle((0, 0), 0.5, color='orange')
        ax.add_patch(star)
        
        planet = Circle((0.8, 0), 0.2, color='blue')
        ax.add_patch(planet)
        
        plt.savefig('icon.png', dpi=100, bbox_inches='tight', transparent=True)
        plt.close()
        
        from PIL import Image
        img = Image.open('icon.png')
        img.save('icon.ico')
        os.remove('icon.png')
        print("Created icon.ico")
    except Exception as e:
        print(f"Could not create icon: {e}")
        with open('icon.ico', 'wb') as f:
            f.write(b'')

if sys.platform.startswith('win'):
    inno_script = """
[Setup]
AppName=Exoplanet Transit Simulator
AppVersion=1.0
DefaultDirName={autopf}\\ExoplanetTransitSimulator
DefaultGroupName=Exoplanet Transit Simulator
UninstallDisplayIcon={app}\\ExoplanetTransitSimulator.exe
Compression=lzma2
SolidCompression=yes
OutputDir=.
OutputBaseFilename=ExoplanetTransitSimulator_Setup

[Files]
Source: "dist\\ExoplanetTransitSimulator.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\\Exoplanet Transit Simulator"; Filename: "{app}\\ExoplanetTransitSimulator.exe"
Name: "{commondesktop}\\Exoplanet Transit Simulator"; Filename: "{app}\\ExoplanetTransitSimulator.exe"
    """
    
    with open('installer_script.iss', 'w') as f:
        f.write(inno_script)
    
    print("Created Inno Setup script (installer_script.iss)")
    print("To create the installer, run Inno Setup Compiler with this script")

print("\nBuild process completed!")
print("The executable can be found in the 'dist' folder")
if sys.platform.startswith('win'):
    print("To create a Windows installer, run Inno Setup Compiler with 'installer_script.iss'")
