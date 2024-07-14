class optimizers:
	def main(input_file: str) -> str:
		"""
		Automated file optimizer utility.

		Args:
			input_file (string): Absolute path of existing file to optimize.

		Returns:
			string: Absolute path of optimized file or, if error occured, `input_file`.
		"""
		extension = stripext(input_file, False)

		if extension in FORMATS_OPTIMIZE:
			logger(
				lang["process"]["output.optimize"] + " (" + lang["process"]["wait"] + ")",
				"info.optimize"
			)

		if extension in FORMATS_STATIC:
			return optimizers.static(
				input_file,
				IMAGE_PNG_MAX_COLORS
			)
		if extension in FORMATS_DYNAMIC:
			return optimizers.dynamic(
				input_file,
				args.delay_count,
				args.loop_count
			)

		return input_file

	def static(input_file: str, colors_limit: int) -> str:
		"""
		Static image files optimizer.

		Args:
			input_file (string): Absolute path of existing static image file to optimize.
			colors_limit (integer): Amount of colors which image palette will be reduced to.

		Returns:
			string: Absolute path of optimized input file.
		"""
		input_file_image = Image.open(input_file)

		if image.is_grayscale(input_file):
			input_file_image = input_file_image.convert("L")
			logger(lang["optim"]["static.grayscale"], "info.optimize")

		input_file_image.save(input_file, optimize = True)

		command = commands.optimizers.static
		command = command.format(
			input_image_file_path = input_file,
			colors_limit = colors_limit,
			package = PNGQuant,
			package_verbosity = PNGQuant_verbosity
		)

		logger(
			lang["optim"]["static.run"].format(
				max_colors = colors_limit
			),
			"debug.optimize"
		)
		logger(command, "debug.command")
		subprocess.call(command, shell = True)

		return input_file

	def dynamic(input_file: str, delay_count: int, loop_count: int) -> str:
		"""
		Dynamic image files optimizer.

		Args:
			input_file (string): Absolute path of existing dynamic image file to optimize.
			delay_count (integer): Target output file delay count per frame.
			loop_count (integer): Target output file loop count.

		Returns:
			string: Absolute path of optimized input file.
		"""
		if not delay_count:
			logger(
				lang["optim"]["dynamic.delay_count"],
				"debug.optimize"
			)

			frame_rate_detected = video.frame_rate(
				input_file,
				FFmpeg,
				FFmpeg_verbosity
			)

			if frame_rate_detected:
				delay_count = frame_rate_detected
				delay_count = math.ceil(delay_count / 10)
				delay_count += 2

		logger(
			lang["optim"]["dynamic.delay_count.set"].format(
				delay_count = delay_count
			),
			"debug.optimize"
		)

		command = commands.optimizers.dynamic
		command = command.format(
			input_image_file_path = input_file,
			delay_count = delay_count,
			loop_count = loop_count,
			factor = "" if args.no_optimization else f"--lossy={args.lossy}",
			package = Gifsicle,
			package_verbosity = Gifsicle_verbosity
		)

		logger(
			lang["optim"]["dynamic.run"].format(
				delay_count = delay_count,
				loop_count = loop_count
			), "debug.optimize"
		)
		logger(command, "debug.command")
		subprocess.call(command, shell = True)

		return input_file