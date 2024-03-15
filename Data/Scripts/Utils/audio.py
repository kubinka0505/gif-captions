class audio:
	def get_channels(input_file: str, package: str) -> int:
		"""
		Retrieves audio channels.

		Args:
			input_file (string): File to get channels from.
			package (string): Package used to file conversion.

		Returns:
			integer: Amount of channels in `input_file`.
		"""
		command = commands.audio.get_channels
		command = command.format(
			input_file_path = input_file,
			package = package
		)

		logger(
			lang["audio"]["get_channels.run"], 
			"debug"
		)
		logger(command, "debug.command")
		output = get_console_output(command)
		output = output[0].split("\n")
		output = [element.split("MD5=")[1] for element in output if element]

		retval = len(set(output))
		if not retval:
			try:
				retval = mFile(path).info.channels
			except Exception:
				retval = 2

		logger(
			lang["audio"]["get_channels.result"].format(
				channels = retval
			),
			"info.audio"
		)
		return retval

	def convert(input_file: str, extension: str, directory: str, package: str, verbosity) -> str:
		"""
		Converts audio file.

		Args:
			input_file (string): File to convert.
			extension (string): Target output file extension.
			directory (string): Target output file directory.
			package (string): Package used to file conversion.
			verbosity (string): `package` verbosity.

		Returns:
			string: Absolute path of converted file.
		"""
		extension_display = stripext(extension, True)
		extension = "." + extension_display.lower()

		output_file = os.path.splitext(os.path.basename(input_file))[0] + "_converted" + extension
		output_file = os.path.join(directory, output_file)

		command = commands.audio.convert
		command = command.format(
			input_audio_file_path = input_file,
			output_audio_file_path = output_file,
			package = package,
			package_verbosity = verbosity
		)

		logger(
			lang["audio"]["convert.extension"].format(
				target_extension = extension_display
			),
			"info.audio"
		)
		logger(command, "debug.command")
		subprocess.call(command, shell = True)

		return output_file

	def normalize(input_file: str, directory: str, level: float, package: str, verbosity) -> str:
		"""
		Normalizes audio file to given dBFS peak.

		Args:
			input_file (string): File to normalize.
			directory (string): Target output file directory.
			level (float): Target audio peak normalization gain.
			package (string): Package used to file normalization.
			verbosity: `package` verbosity.

		Returns:
			string: Absolute path of normalized audio file.
		"""
		input_file = audio.convert(
			input_file, "WAV",
			session_directory,
			FFmpeg,
			FFmpeg_verbosity
		)

		input_channels = audio.get_channels(input_file, FFmpeg)

		output_file = os.path.splitext(input_file)[0] + "_normalized.wav"
		output_file = os.path.join(directory, output_file)

		command = commands.audio.normalize
		command = command.format(
			input_audio_file_path = input_file,
			input_audio_channels = input_channels,
			normalization_level = level,
			output_audio_file_path = output_file,
			package = package,
			package_verbosity = verbosity
		)

		logger(
			lang["audio"]["normalize.run"].format(
				level = level
			),
			"info.audio"
		)
		logger(command, "debug.command")
		subprocess.call(command, shell = True)

		return output_file

	def is_silent(input_file: str, package: str) -> bool:
		"""
		Checks if file has no sound.

		Args:
			input_file (string): File on which silence detection operation will be performed.
			package (string): Package used to check silence.

		Returns:
			boolean: True if `input_file` is silent, otherwise False.
		"""
		retval = False

		command = commands.audio.is_silent
		command = command.format(
			input_file_path = input_file,
			package = package
		)

		logger(
			lang["audio"]["no_silent.run"],
			"debug"
		)
		logger(command, "debug.command")

		output = get_console_output(command)

		try:		
			output = [line for line in output if "[parsed_astats" in line.lower()]
			output = [line for line in output if "rms level db:" in line.lower()]
			output = [element.split(":")[-1].strip() for element in output]

			if len(set(output)) < 2:
				if output[-1].lower() == "-inf":
					return True
		except IndexError:
			retval = True

		return retval