# Install/Usage
```
Files:
    /pics               // Pictures/Logos to replace
    /se_nauman_yubico   // Yubikey support
    /se_nauman_program  // Additional program 
    /utils              // Test files. Only works in X11
    dependencies.sh     // Get all dependencies for the makefile
    Makefile            // Install / Create package
    README.md           // This file
  
Commands:
    # Create package(.img-file)
    make package DESTDIR=`mktemp -d`
        
    # Add to a webserver
    python -m SimpleHTTPServer
    
    # Include into a netinstall
    inst.updates=http://1.2.3.4:8000/anaconda_addon.img
  
```

# Development
## Fedora 
```
# DNF-installable packages
dnf install anaconda python3-yubico python3-crypto

# Pyinstaller, dependency for Gtk, Pango
## Altgraph
tar -zvxf altgraph-0.14.tar.gz
cd altgraph-0.14
python3.7 setup.py install

## Macholib
tar -zvxf macholib-1.8.tar.gz
cd macholib-1.8
python3.7 setup.py install

## PEFile
sudo dnf install python3-pefile

## Pyinstaller
unzip pyinstaller-develop.zip
cd pyinstaller-develop
python3.7 setup.py install
```