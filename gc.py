import os
import re
import sty
import json
import math
import time
import emoji
import locale
import random
import string
import datetime
import warnings
import mimetypes
import subprocess
from colour import Color
from pathlib import Path
from shutil import rmtree
from textwrap import wrap
from unidecode import unidecode
from mutagen import File as mFile
from emoji import emojize, demojize
from urllib.parse import quote_plus
from requests import Session, exceptions
from argparse import ArgumentParser, SUPPRESS
from PIL import Image, ImageDraw, ImageColor, ImageFont, ImageChops, ImageOps, UnidentifiedImageError

__title__   = "gif-captions"
__author__  = "kubinka0505"
__credits__ = __author__
__version__ = "1.0"
__date__    = "54th March 2024"

#-=-=-=-#

__START_TIME = time.time()
is_windows = os.sys.platform.lower().startswith("win")
__BaseDir = os.path.abspath(os.path.dirname(__file__))

if not is_windows:
	import distro

#-=-=-=-#

def open_(path: str) -> string:
	"""
	File opening handler.

	Args:
		path: Path of existing file to be opened, relative to the `__file__` location directory.

	Returns:
		string: Opened `path` content.
	"""
	path = os.path.join(__BaseDir, "Data", "Scripts", path)
	return open(path, encoding = "UTF-8").read()

files = [
	"Utils/language.py",
	"Utils/command.py",
	"Utils/main.py",
	"Utils/variable.py",
	"Utils/package.py",
	"Utils/optimize.py",
	"ArgParse/main.py",
	"Utils/internet.py",
	"Utils/update_notification.py",
	"Utils/audio.py",
	"Utils/image.py",
	"Utils/video.py",
	"ArgParse/settings.py",
	"process.py",
	"ending.py"
]

for file in files:
	exec(open_(file))