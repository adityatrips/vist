import requests
from os import system
from subprocess import call
from sys import version_info
from urllib.request import urlretrieve


def run_commands(command_list, message):
    while True:
        try:
            for command in command_list:
                c = command.split()
                call(c)
        except:
            print("There was an error. Please try again.")
            continue
        else:
            print(message)
            break


def install_modules():
    # Import modules
    from os.path import isfile, join
    from sys import prefix
    from pkgutil import iter_modules
    import importlib

    # Check if pip is installed
    pip_path = join(prefix, 'bin', 'pip3')
    if not isfile(pip_path):
        # install pip if it isn't installed
        print("Installing PIP. PIP is necessary to install important modules for python.")
        run_commands('sudo apt install python3-pip gstreamer-1.0',
                     'PIP installed successfully!')
        # Check again
        if not isfile(pip_path):
            # Raise error if couln't install pip
            print(
                "Failed to find or install pip! Please add it to PATH or install manually!")
            quit()

    # install other modules not available in pip
    run_commands(['sudo apt install -y python3-pyaudio'],
                 'Installed pyaudio successfully!')

    modules = ['SpeechRecognition', 'gTTS',
               'requests', 'geocoder', 'func-timeout', 'playsound']
    try:
        for lib in modules:
            globals()[lib] = importlib.import_module(lib)
    except ImportError:
        print("Installing pip modules...")
        for module in modules:
            print(f"Installing {module}...")
            try:
                call(['pip3', 'install', module])
                call(['pip', 'install', module])
            except:
                pass
            system('clear')
            print(f"Installed {module} successfully!")
    else:
        print("All dependencies are installed!")


def download_mp3_files():
    print("Downloading important mp3 files...")
    urlretrieve(
        'https://drive.google.com/uc?export=download&id=1f1UHs2yZ-LZP7yq5RdqvPGnHjjP0WG9O',
        'beep.mp3')
    urlretrieve(
        'https://drive.google.com/uc?export=download&id=1g6wM9N05Zem1rwSbJnG9N0PC1MNR487A',
        'couldYouSayThatAgain.mp3'
    )
    print("Everything is ready! You can run VIST.py without any issues now!")


install_modules()
download_mp3_files()
quit()
