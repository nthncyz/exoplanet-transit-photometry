import PyInstaller.__main__
import os
import shutil
import sys

# Clean any previous build artifacts
if os.path.exists('dist'):
    shutil.rmtree('dist')
if os.path.exists('build'):
    shutil.rmtree('build')

# Define the PyInstaller command
pyinstaller_args = [
    '../src/simulator/exoplanet_transit_simulator.py',  # Main script (updated path for your structure)
    '--name=ExoplanetTransitSimulator',  # Name of the output
    '--onefile',  # Create a single executable file
    '--windowed',  # Don't show console window (for Windows)
    '--icon=icon.ico',  # Application icon
    '--add-data=../README.md:.',  # Include README
    '--hidden-import=numpy',  # Ensure NumPy is included
    '--hidden-import=matplotlib',  # Ensure Matplotlib is included
    '--hidden-import=matplotlib.backends.backend_tkagg',  # Required for Matplotlib GUI
    '--clean',  # Clean PyInstaller cache
    '--noconfirm',  # Don't ask for confirmation
]

# Run PyInstaller
PyInstaller.__main__.run(pyinstaller_args)

print("PyInstaller build completed!")

# Create icon file if it doesn't exist (simple placeholder)
if not os.path.exists('icon.ico'):
    try:
        import matplotlib.pyplot as plt
        import numpy as np
        from matplotlib.patches import Circle
        
        # Create a simple icon
        fig, ax = plt.subplots(figsize=(5, 5))
        ax.set_aspect('equal')
        ax.set_xlim(-1.2, 1.2)
        ax.set_ylim(-1.2, 1.2)
        ax.axis('off')
        
        # Draw star
        star = Circle((0, 0), 0.5, color='orange')
        ax.add_patch(star)
        
        # Draw planet
        planet = Circle((0.8, 0), 0.2, color='blue')
        ax.add_patch(planet)
        
        # Save as PNG first
        plt.savefig('icon.png', dpi=100, bbox_inches='tight', transparent=True)
        plt.close()
        
        # Convert PNG to ICO using PIL
        from PIL import Image
        img = Image.open('icon.png')
        img.save('icon.ico')
        os.remove('icon.png')
        print("Created icon.ico")
    except Exception as e:
        print(f"Could not create icon: {e}")
        # Create an empty file as placeholder
        with open('icon.ico', 'wb') as f:
            f.write(b'')

# For Windows, create an Inno Setup script
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
