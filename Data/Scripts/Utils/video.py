class video:
	def frame_rate(input_file: str, package: str, verbosity) -> int:
		"""
		Retrieve frames per second rate from visual media.

		Args:
			input_file (string): File to retrieve frame rate from.
			package (string): Package used to retrieve the frame rate.
			verbosity (string): `package` verbosity.

		Returns:
			integer: Frame rate of `input_file`.
		"""
		retval = VISUAL_FRAME_RATE_UNSET

		_frame_rate_id = " tbr,"

		command = commands.video.frame_rate
		command = command.format(
			package = package,
			input_file = input_file
		)

		logger(
			lang["video"]["frame_rate.run"],
			"debug"
		)
		logger(command, "debug.command")
		output = get_console_output(command)
		try:
			index = 6
			if stripext(input_file, False) in FORMATS_DYNAMIC:
				index = 2

			output = output[1].split("\n")[index]
			output = output.split("tbr")[-2]
			output = output.split(",")[-1]
			output = output.strip()
		except IndexError:
			logger(
				lang["video"]["frame_rate.error"] + "(" + str(retval) + ")",
				"debug"
			)

		if output.isdigit():
			retval = int(output)

		return retval

	def extract_frames(input_file: str, frames_directory: str, package: str, verbosity) -> list:
		"""
		Extract frames from visual media.

		Args:
			input_file (string): File to extract frames from.
			frames_directory (string): Absolute existing directory path to extract frames to.
			package (string): Package used for frames extraction.
			verbosity: `package` verbosity.

		Returns:
			list: Absolute paths of extracted frames.
		"""
		command = commands.video.extract_frames
		command = command.format(
			package = package,
			input_visual_file = input_file,
			frames_directory = frames_directory,
			package_verbosity = verbosity
		)

		logger(
			lang["video"]["frames.extract.run"] + " (" + lang["process"]["wait"] + ")",
			"debug.video"
		)
		logger(command, "debug.command")
		subprocess.call(command, shell = True)

		frames = [str(file.resolve()) for file in Path(frames_directory).glob("*.*")]

		# Convert to RGBA in order to fix loss color on `PIL.Image.paste`
		for frame in frames:
			frame_obj = Image.open(frame)
			frame_obj = frame_obj.convert("RGBA")
			frame_obj.save(frame)

		return frames

	def generate_palette(frames_directory: str, output_directory: str, package: str, verbosity) -> str:
		"""
		Generates unified color palette from frames.

		Args:
			frames_directory (string): Absolute existing directory path containing frames.
			output_directory (string): Absolute existing directory path to save palette to.
			package (string): Package used to palette generation.
			verbosity: `package` verbosity.

		Returns:
			string: Absolute path of generated palette.
		"""
		output_file = os.path.join(output_directory, "Palette.png")

		command = commands.video.generate_palette
		command = command.format(
			frames_directory = frames_directory,
			output_visual_file = output_file,
			transparent = int(image.is_transparent(frames[0])),
			package = package,
			package_verbosity = verbosity
		)

		logger(
			lang["video"]["create.palette.run"], 
			"debug.video"
		)
		logger(command, "debug.command")
		subprocess.call(command, shell = True)

		return output_file

	def create_gif(output_file: str, frames_directory: str, package: str, verbosity) -> str:
		"""
		Creates GIF from frames.

		Args:
			output_file (string): Target output file location.
			frames_directory (string): Absolute existing directory path containing frames.
			package (string): Package used to palette generation.
			verbosity: `package` verbosity.

		Returns:
			string: Absolute path of generated GIF.
		"""
		palette_file = video.generate_palette(
			frames_directory,
			os.path.dirname(frames_directory),
			package,
			verbosity
		)

		command = commands.video.create_transparent_gif
		command = command.format(
			package = package,
			frames_directory = frames_directory,
			input_palette_image_file = palette_file,
			output_visual_file = output_file,
			package_verbosity = verbosity
		)

		logger(
			lang["video"]["create.dynamic.run"],
			"debug.video"
		)
		logger(command, "debug.command")
		subprocess.call(command, shell = True)

		return output_file

	def combine_frames(
		sound: str,
		output_directory: str,
		extension: str,
		sound_bitrate: int,
		package: str,
		verbosity
	) -> str:
		"""
		Creates video from frames.

		Args:
			sound (string): Optional. Absolute existing audio file path.
			output_directory (string): Absolute existing directory path to save output file to.
			extension (string): Target output file extension.
			sound_bitrate (integer): Audio bitrate in kb/s.
			package (string): Package used to create video.
			verbosity: `package` verbosity.

		Returns:
			string: Absolute path of created video.
		"""
		extension = stripext(extension, False)
		output_file = os.path.join(
			output_directory,
			"{0}_{1}.{2}".format(
				output_name(args.text, OUTPUT_NAME_LIMIT),
				STRING_RANDOM_GLOBAL,
				extension
			)
		)

		is_image_static = extension.endswith(FORMATS_STATIC)
		is_image_dynamic = extension.endswith(FORMATS_DYNAMIC)

		if is_image_static:
			if args.force_gif:
				logger(
					lang["video"]["save.static_as_dynamic"],
					"info.video"
				)
				is_image_dynamic = True
			elif not sound:
				Image.open(frames[0]).save(output_file)

		if is_image_dynamic:
			if not sound:
				logger(
					lang["video"]["create.dynamic.no_sound.is_dynamic"],
					"debug.video"
				)
				output_file = video.create_gif(
					output_file,
					extracted_frames_directory,
					package,
					verbosity
				)

		if sound:
			audio_norm = audio.normalize(
				sound,
				session_directory,
				AUDIO_NORM_LEVEL,
				SoX,
				SoX_verbosity
			)
			audio_object = mFile(audio_norm)
			audio_duration = str(audio_object.info.length)
			audio_samplerate = audio_object.info.sample_rate

			audio_arguments = commands.video.combine_frames_video_audio
			audio_arguments = audio_arguments.format(
				input_audio_file = audio_norm,
				input_audio_duration = audio_duration,
				input_audio_bitrate = sound_bitrate,
				input_audio_samplerate = audio_samplerate,
			)

			video_codec = ""
			if extension.endswith("webm"):
				video_codec = "libvpx-vp9"
			if extension.endswith("mp4"):
				video_codec = "libx264"

			if video_codec:
				video_codec = "-c:v " + video_codec

			frame_rate = video.frame_rate(args.visual, FFmpeg, FFmpeg_verbosity)

			command = commands.video.combine_frames_video
			command = command.format(
				package = package,
				frames_directory = extracted_frames_directory,
				audio_arguments = audio_arguments,
				output_video_codec = video_codec,
				output_visual_file_frame_rate = frame_rate,
				output_visual_file_path = output_file,
				package_verbosity = verbosity
			)

			logger(
				lang["video"]["frames.combine.run"],
				"debug.video"
			)
			logger(command, "debug.command")
			subprocess.call(command, shell = True)

		return output_file