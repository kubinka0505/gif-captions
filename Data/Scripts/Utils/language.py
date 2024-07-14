# Setup

def load_language(filename: str, directory: str) -> dict:
	"""
	Loads language.

	Args:
		file (string): Language locale file name.
		directory (string): Directory containing `file`.

	Raises:
		TypeError: If language file is a directory.
		FileNotFoundError: If language file was not found.

	Returns:
		dictionary: Language dictionary object.
	"""
	retval = {}

	language = os.path.join(directory, filename)
	if os.path.exists(language):
		if os.path.isdir(language):
			raise TypeError(f'"{language}" is a directory!')
	else:
		raise FileNotFoundError(f'"{language}"')

	retval = open(language, encoding = "UTF-8")
	retval = json.load(retval)

	return retval

def capitalize_dict_values(dictionary: dict) -> dict:
	"""
	Capitalizes values of dicionary subkeys.

	Args:
		dictionary: Dictionary which values will be capitalized.

	Returns:
		dictionary: Collection containing capitalized values.
	"""
	retval = {}

	for key, value in dictionary.items():
		if isinstance(value, dict):
			retval[key] = capitalize_dict_values(value)
		elif isinstance(value, str):
			retval[key] = value[0].upper() + value[1:]
		else:
			retval[key] = value

	return retval

#---#

language_display = locale.getlocale()[0].split("_")[0].title()
language_directory = os.path.join(__BaseDir, "Data", "Languages")

language_default = "English"
language_format = ".json"

language_file = language_display + language_format
language_primary = language_default + language_format

#-=-=-=-#
# Validate languages

err = 0
try:
	lang = load_language(language_file, language_directory)
except Exception:
	warnings.warn(
		f"{language_display} language file could not be loaded, English will be used.\n",
		UserWarning
	)
	err = 1

fpl_flags = ["-fpl", "--force-primary-language"]
force_primary_language = any(x.lower() in fpl_flags for x in os.sys.argv)

if any((err, force_primary_language)):
	try:
		lang = load_language(language_primary, language_directory)
	except FileNotFoundError:
		raise SystemExit("Primary language file was not found, exiting.")

#-=-=-=-#
# Process values

lang = capitalize_dict_values(lang)

if force_primary_language:
	lang["argparse/main"]["switch.force_primary_language"] = SUPPRESS

lang["process"]["wait"] = lang["process"]["wait"].lower()