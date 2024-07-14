# Ensure colored output
subprocess.call("", shell = True)

#-=-=-=-#

def search_package(query: str, variable: str) -> str:
	"""
	Searches for installed system package.

	Args:
		query: Package name to be searched.
		variable: Mandatory in Windows. System environment variable containing executable file that file name contains `query`.

	Raises:
		OSError: If package was not found.

	Returns:
		string: Package system name or executable path.
	"""
	if is_windows:
		query += ".exe"
		for entry in os.environ[variable].split(os.pathsep):
			if query.lower() in entry.lower():
				if os.path.isfile(entry):
					return entry

		raise OSError(lang["main"]["pkg_not_found.exe"].format(
				package_name = query,
				variable_name = variable,
			)
		)
	else:
		try:
			subprocess.check_output(["which", query])
			return query
		except subprocess.CalledProcessError:
			raise OSError(lang["main"]["pkg_not_installed"].format(
					package_name = query
				)
			)

def get_console_output(command: str) -> tuple:
	"""
	Returns content from the given executed command.

	Args:
		command: Command which console output should be retrieved.

	Returns:
		tuple: Called `communicate` bound method of `Popen` function.
	"""
	process = subprocess.Popen(
		command,
		stdout = subprocess.PIPE,
		stderr = subprocess.PIPE,
		shell = True
	)

	retval = process.communicate()
	retval = [line.decode("UTF-8") for line in retval]

	return retval

def open_in_explorer(file: str, select: bool = True) -> str:
	"""
	Opens `file` location inside the operating system's file explorer.

	Args:
		file: Absolute path of existing file, which location fill be opened.
		select: Windows only. Determines whether the `file` should be selected inside the operating system's file explorer.

	Returns:
		string: Command used to open the `file` location.
	"""
	file = os.path.abspath(file)

	if is_windows:
		executable = r"start /max C:\Windows\explorer.exe"

		if select:
			executable += " /select,"
	elif os.sys.platform.startswith("linux"):
		distro_name = distro.id()

		if distro_name == "ubuntu":
			executable = "nautilus"
		elif distro_name == "debian":
			executable = "nemo"
		elif distro_name == "rhel":
			executable = "gnome-open"
		else:
			command = "xdg-open"
	else:
		executable = "open"

	if not is_windows:
		executable += " "

	null_device = "" if is_windows else "> /dev/null 2>&1"

	#-=-=-=-#
	
	command = commands.open_in_explorer
	command = command.format(
		executable = executable,
		file = final_file,
		null_device = null_device
	)

	logger(
		lang["main"]["open_in_explorer"],
		"debug"
	)
	logger(command, "debug.command")
	subprocess.call(command, shell = True)

	return command

def file_size(path: str) -> str:
	"""
	Returns human-readable file size

	Args:
		path: Existing file.

	Returns:
		string: Size and its unit.
	"""
	size = os.path.getsize(path)

	for unit in ["B", "KB", "MB", "GB", "TB"]:
		if size < 1024:
			break
		size /= 1024

	size = str(round(size, 2))
	size_s = size.split(".")
	if len(size_s[1]) < 2:
		size += "0"

	return "{0} {1}".format(size, unit)

def hex2rgb(color: str) -> tuple:
	"""
	Converts HEX color to RGB tuple.

	Args:
		color: HEX color starting with "#" and divisible by 3.

	Returns:
		tuple: R, G, and B conversion of HEX `color`.
	"""
	color = color.lstrip("#")

	if len(color) == 3:
		color = "".join(c * 2 for c in color)

	return tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))

def random_string(length: int = 8) -> str:
	"""
	Generates random string.

	Args:
		length: Target length of generated string.

	Returns:
		string: Randomly generated string.
	"""
	chars = string.ascii_letters + string.digits
	return "".join(random.choice(chars) for _ in range(length))

def output_name(string: str, limit: int) -> str:
	"""
	Normalizes output file name non-ASCII characters and removes interpunction.

	Args:
		string: String to be normalized.
		limit: Maximum output `string` length.

	Returns:
		string: Normalized `string` truncated to `limit`.
	"""
	string = unidecode(string)
	string = re.sub(r"[^\w\s]", "", string)

	string = string.split(" ")
	string = [element for element in string if element]
	string = "_".join(string)

	return string[:limit]

def stripext(path: str, uppercase: bool) -> str:
	"""
	Strips an path from its extension. 

	Args:
		path: Path containing extension.
		uppercase: Determines whether stripped extension should be uppercase.

	Returns:
		string: `path` stripped of extension if `path` is file, otherwise `path`.
	"""
	if os.path.isdir(path):
		retval = path

	extension = os.path.splitext(path)
	if extension[-1]:
		index = -1
	else:
		index = 0
	extension = extension[index]
	

	retval = extension.strip(".")
	if uppercase:
		retval = retval.upper()
	else:
		retval = retval.lower()

	return retval

def all_in(iterable: iter, obj: iter) -> bool:
	"""
	Tests whether all values in iterable are in object.

	Args:
		iterable: Collection of objects that are to be located in `obj`.
		obj: Iterable on which check will be done.

	Returns:
		boolean: True if all of elements of `iterable` are located in `obj`.
	"""
	return all(element in iterable for element in iterable)

def clamp(number: float, minimum: float, maximum: float) -> float:
	"""
	Limits number to given range.

	Args:
		number (float): Number to limit.
		minimum (float): Minimum `number` limit.
		maximum (float): Maximum `number` limit.

	Returns:
		float: Limited number.
	"""
	return min(max(minimum, number), maximum)

def logger(value: str, log_type: str = "info") -> tuple:
	"""
	Logging utility.

	Args:
		value (string): Logging message.
		log_type (string): String log type with two elements separated by dot. (subtype)

	Returns:
		tuple: `log_type`, log subtype and `value`.
	"""
	value_original = value

	log_type = log_type.lower().split(".")[:2]
	log_subtype = log_type[0]
	if len(log_type) > 1:
		log_subtype = log_type[1]
	log_type = log_type[0]

	_colors = {
		"type": {
			"info": colors.info,
			"debug": colors.flaw,
			"warn": colors.warning,
			"error": colors.error
		},
		"subtype": {
			"update": colors.warning,
			"audio": colors.meta_info_2,
			"video": colors.meta_info_2,
			"optim": colors.ok,
			"location": colors.ok,
		}
	}
	_colors["subtype"].update(_colors["type"])

	for k, v in _colors["type"].items():
		if log_type.startswith(k):
			color = v

	for k, v in _colors["subtype"].items():
		if log_subtype.startswith(k):
			color = v

	# Values
	if value:
		value_raw = "[{0}] {1}".format(log_subtype.upper(), value)
		value = color + "[" + log_subtype.upper() + "]" + colors.reset + " " + value

	# Output
	if args.verbosity != -1:
		if args.verbosity == 1:
			if log_type.startswith(("error", "info", "warning", "debug")):
				print(value)
		if args.verbosity == 0:
			if log_type.startswith(("error", "info", "warning")):
				print(value)

	# Saving to file
	with open(logs_file, "a") as logs:
		if value:
			logs.write(value_raw)
			logs.write("\n")

	if log_type == "error":
		raise SystemExit()

	return (log_type, log_subtype, value_original)

#-=-=-=-#

class colors:
	"""
	Colors variables used for console outputs.
	"""
	error = "#C10"
	ok = "#0C0"
	flaw = "#F36"
	info = "#4AF"
	warning = "#FC0"
	meta_info = "#999"
	meta_info_2 = "#90F"

_cls = colors
for var in list(vars(_cls))[2:-2]:
	setattr(
		_cls,
		var,
		sty.fg(
			*ImageColor.getrgb(
				Color(getattr(_cls, var)).hex_l
			)
		)
	)

_cls.reset = sty.fg.rs