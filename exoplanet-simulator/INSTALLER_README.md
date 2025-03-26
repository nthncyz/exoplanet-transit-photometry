# **Exoplanetary Transit Simulation Installer**  

This repository contains everything needed to package and distribute the **Exoplanet Transit Simulator** as a standalone installer.  

---

## **Getting Started**  

### **Windows**  
1. Run `build_installer.bat`  
2. If you have Inno Setup installed, open `installer_script.iss` in the Inno Setup Compiler and compile  
3. Share the generated `ExoplanetTransitSimulator_Setup.exe`  

### **macOS/Linux**  
1. Make the script executable:  
   ```sh
   chmod +x build_installer.sh
   ```  
2. Run the build script:  
   ```sh
   ./build_installer.sh
   ```  
3. The packaged executable will be available in the `dist` folder  

---

## **Manual Installation**  

1. Install dependencies:  
   ```sh
   pip install -r requirements.txt
   ```  
2. Run the installer script:  
   ```sh
   python exoplanet_transit_installer.py
   ```  
3. *(Windows only:)* Compile the Inno Setup script if needed  

---

## **What's Included**  

- **`exoplanet_transit_simulator.py`** – The main application  
- **`exoplanet_transit_installer.py`** – Script to create an executable  
- **`requirements.txt`** – List of required Python packages  
- **`build_installer.bat` / `build_installer.sh`** – Scripts to automate packaging  
- **`installer_script.iss`** – Inno Setup script for generating a Windows installer  

---

## **Requirements**  

- **Python 3.7 or newer**  
- *(For Windows installers:)* [Inno Setup](https://jrsoftware.org/isinfo.php) *(optional)*  

---

## **Distribution**  

Standalone installer that sets up the **Exoplanet Transit Simulator** without requiring users to install Python or any additional dependencies.  
