# Verbosity

FFmpeg_verbosity = "-8"
SoX_verbosity = "1"
PNGQuant_verbosity = ""
Gifsicle_verbosity = "-w"

if args.verbosity == 0:
	FFmpeg_verbosity = "8"
if args.verbosity == 1:
	FFmpeg_verbosity = "24"
	SoX_verbosity = "2"
	PNGQuant_verbosity = "-v"
	Gifsicle_verbosity = "-i -cinfo -xinfo -sinfo -V"

#-=-=-=-#
# Limits

args.audio_bitrate = clamp(args.audio_bitrate, *LIMIT_AUDIO_BITRATE)
args.lossy = clamp(args.lossy, *LIMIT_AUDIO_BITRATE)

#-=-=-=-#
# Fonts
font_data = os.path.join(__BaseDir, "Data", "Assets", "Fonts", os.path.basename(args.font))
if os.path.exists(font_data):
	args.font = font_data

#-=-=-=-#
# Inputs

if not INTERNET_CONNECTION:
	if emojize(args.text) != demojize(args.text):
		logger(
			lang["argparse/settings"]["no_connection"],
			"warning"
		)

		logger(
			lang["argparse/settings"]["emoji.no_connection"],
			"error"
		)

if not os.path.exists(args.visual):
	if INTERNET_CONNECTION:
		if is_URL(args.visual):
			logger(
				lang["argparse/settings"]["url.ok"],
				"debug"
			)
			logger(
				lang["argparse/settings"]["visual.parse_from_url"],
				"info"
			)

			args.visual = get_service(args.visual)

			logger(
				lang["argparse/settings"]["visual.download.run"],
				"info"
			)

			logger(
				"URL: " + args.visual,
				"debug"
			)

			args.visual = download_file(args.visual, session_directory)
		else:
			logger(
				lang["argparse/settings"]["url.invalid"],
				"warning"
			)
	else:
		logger(
			lang["argparse/settings"]["no_connection"],
			"warning"
		)

		logger(
			lang["argparse/settings"]["visual.download.no_connection"],
			"warning.error"
		)

if args.audio is not None:
	if not os.path.exists(args.audio):
		if INTERNET_CONNECTION:
			if is_URL(args.audio):
				logger(
					lang["argparse/settings"]["url.ok"],
					"debug"
				)

				logger(
					lang["argparse/settings"]["audio.download.run"],
					"info"
				)

				logger(
					"URL: " + args.audio,
					"debug"
				)

				args.audio = download_file(args.audio, session_directory)
			else:
				logger(
					lang["argparse/settings"]["url.invalid"] + " - " + \
					lang["argparse/settings"]["audio.download.no_connection"][0].lower() + \
					lang["argparse/settings"]["audio.download.no_connection"][1:],
					"warning"
				)
		else:
			logger(
				lang["argparse/settings"]["no_connection"],
				"warning"
			)

			logger(
				lang["argparse/settings"]["audio.download.no_connection"],
				"warning.error"
			)

args.visual = os.path.abspath(args.visual)

if args.audio:
	args.audio = os.path.abspath(args.audio)
else:
	if audio.is_silent(args.visual, FFmpeg):
		logger(
			lang["argparse/settings"]["audio.empty_no_sound"],
			"warning"
		)
		args.audio = ""
	else:
		args.audio = args.visual

args.output_directory = os.path.abspath(args.output_directory)
args.font = os.path.abspath(args.font)

args.text_color = hex2rgb(args.text_color)
args.background_color = hex2rgb(args.background_color)

#-=-=-=-#
# Handling

# Validate visual input
if os.path.exists(args.visual):
	if os.path.isdir(args.visual):
		logger(
			lang["argparse/settings"]["visual.wrong_type"],
			"error"
		)
else:
	logger(
		lang["argparse/settings"]["visual.not_exists"],
		"error"
	)

# Validate audio input
_aud_err = 0
if args.audio:
	if os.path.exists(args.audio):
		if os.path.isdir(args.audio):
			logger(
				lang["argparse/settings"]["audio.wrong_type"],
				"error"
			)
			_aud_err = 1
	else:
		logger(
			lang["argparse/settings"]["audio.not_exists"],
			"warning"
		)
		_aud_err = 1

	if _aud_err:
		logger(
			lang["argparse/settings"]["output_without_sound"],
			"warning"
		)
		args.audio = ""

# Validate directory
if os.path.exists(args.output_directory):
	if os.path.isfile(args.output_directory):
		logger(
			lang["argparse/settings"]["output_directory.wrong_type"],
			"error"
		)
else:
	os.makedirs(args.output_directory, exist_ok = True)

# Validate font
if os.path.exists(args.font):
	if os.path.isdir(args.font):
		logger(
			lang["argparse/settings"]["font.wrong_type"],
			"error"
		)
else:
	logger(
		lang["argparse/settings"]["font.not_exists"],
		"error"
	)

#-=-=-=-#
# Output locations

logger("", "debug")

_showcase = {
	lang["argparse/settings"]["show.visual"]: args.visual,
	lang["argparse/settings"]["show.audio"]: args.audio,
	lang["argparse/settings"]["show.font"]: args.font,
	lang["argparse/settings"]["show.output_directory"]: args.output_directory,
	lang["argparse/settings"]["show.session_directory"]: session_directory
}
_showcase_longest_length = len(sorted(_showcase.keys(), key = len)[-1])

for k, v in _showcase.items():
	if v:
		logger(
			(k + ":").ljust(_showcase_longest_length + 2, " ") + f'"{v}"',
			"info.location"
		)

logger("", "info")