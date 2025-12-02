import sys
import os
import subprocess as sps
from shutil import which
from typing import List, Optional
from eel.types import OptionsDictT

# Every browser specific module must define run(), find_path() and name like this

name: str = 'Google Chrome/Chromium'

def run(path: str, options: OptionsDictT, start_urls: List[str]) -> None:
    if not isinstance(options['cmdline_args'], list):
        raise TypeError("'cmdline_args' option must be of type List[str]")
    if options['app_mode']:
        for url in start_urls:
            sps.Popen([path, '--app=%s' % url] +
                       options['cmdline_args']),
                       stdout=sps.PIPE, stderr=sps.PIPE, stdin=sps.PIPE)
    else:
        args: List[str] = options['cmdline_args'] + start_urls
        sps.Popen([path, '--new-window'] + args,
                   stdout=sps.PIPE, stderr=sys.stderr, stdin=sps.PIPE)


def find_path() -> Optional[str]:
    # Priority 1: Check PATH using which
    common_names = ['google-chrome', 'chromium', 'chromium-browser', 'chrome', 'google-chrome-stable']
    for name in common_names:
        path = which(name)
        if path:
            return path

    # Priority 2: Platform-specific logic
    if sys.platform in ['win32', 'win64']:
        return _find_chrome_win()
    elif sys.platform == 'darwin':
        return _find_chrome_mac() or _find_chromium_mac()
    elif sys.platform.startswith('linux'):
        return _find_chrome_linux()
    else:
        return None


def _find_chrome_mac() -> Optional[str]:
    default_dirs = [
        r'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
        r'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
    ]
    for path in default_dirs:
        if os.path.exists(path):
            return path
            
    # use mdfind ci to locate Chrome in alternate locations and return the first one
    name = 'Google Chrome.app'
    try:
        out = sps.check_output(["mdfind", name]).decode().split('\n')
        alternate_dirs = [x for x in out if x.endswith(name)]
        if len(alternate_dirs):
            return alternate_dirs[0] + '/Contents/MacOS/Google Chrome'
    except (sps.CalledProcessError, FileNotFoundError):
        pass
        
    return None


def _find_chromium_mac() -> Optional[str]:
    default_dir = r'/Applications/Chromium.app/Contents/MacOS/Chromium'
    if os.path.exists(default_dir):
        return default_dir
    # use mdfind ci to locate Chromium in alternate locations and return the first one
    name = 'Chromium.app'
    try:
        out = sps.check_output(["mdfind", name]).decode().split('\n')
        alternate_dirs = [x for x in out if x.endswith(name)]
        if len(alternate_dirs):
            return alternate_dirs[0] + '/Contents/MacOS/Chromium'
    except (sps.CalledProcessError, FileNotFoundError):
        pass
        
    return None


def _find_chrome_linux() -> Optional[str]:
    # Fallback to standard locations if not found in PATH
    standard_paths = [
        '/usr/bin/google-chrome',
        '/usr/bin/chromium',
        '/usr/bin/chromium-browser',
        '/usr/local/bin/google-chrome',
        '/snap/bin/chromium',
        '/var/lib/flatpak/exports/bin/com.google.Chrome',
        '/opt/google/chrome/google-chrome',
    ]

    for path in standard_paths:
        if os.path.exists(path) and os.access(path, os.X_OK):
            return path
            
    return None


def _find_chrome_win() -> Optional[str]:
    import winreg as reg
    reg_path = r'SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe'
    chrome_path: Optional[str] = None

    for install_type in reg.HKEY_CURRENT_USER, reg.HKEY_LOCAL_MACHINE:
        try:
            reg_key = reg.OpenKey(install_type, reg_path, 0, reg.KEY_READ)
            chrome_path = reg.QueryValue(reg_key, None)
            reg_key.Close()
            if not os.path.isfile(chrome_path):
                continue
        except WindowsError:
            chrome_path = None
        else:
            break

    return chrome_path