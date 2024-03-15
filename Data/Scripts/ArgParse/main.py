parser = ArgumentParser(
	description = lang["argparse/main"]["description"],
	add_help = False,
	allow_abbrev = False
)

required = parser.add_argument_group(lang["argparse/main"]["group.required"])
optional = parser.add_argument_group(lang["argparse/main"]["group.optional"])
style = parser.add_argument_group(lang["argparse/main"]["group.style"])
optimization = parser.add_argument_group(lang["argparse/main"]["group.optimization"])
switch = parser.add_argument_group(lang["argparse/main"]["group.switch"])

#-=-=-=-#
# Required

required.add_argument(
	"-i", "--visual", type = str,
	required = True,
	metavar = '"path"',
	help = lang["argparse/main"]["required.visual"]
)

required.add_argument(
	"-t", "--text", type = str,
	required = True,
	metavar = '"str"',
	help = lang["argparse/main"]["required.text"]
)

#-=-=-=-#
# Optional

optional.add_argument(
	"-a", "--audio", type = str,
	default = None,
	nargs = "?",
	metavar = '"path"',
	help = lang["argparse/main"]["optional.audio"]
)

optional.add_argument(
	"-w", "--text-wrap", type = int,
	default = 18,
	metavar = "int >= 1",
	help = lang["argparse/main"]["optional.text_wrap"]
)

optional.add_argument(
	"-od", "--output-directory", type = str,
	default = outputs_directory,
	metavar = '"path"',
	help = lang["argparse/main"]["optional.output_directory"]
)

optional.add_argument(
	"-v", "--verbosity", type = int,
	choices = range(-1, 1 + 1),
	default = 0,
	metavar = "-1 <= int <= 1",
	help = lang["argparse/main"]["optional.verbosity"]
)

#-=-=-=-#
# Style

style.add_argument(
	"-f", "--font", type = str,
	default = "Futura.otf",
	metavar = '"Font.<o/t>tf"',
	help = lang["argparse/main"]["style.font"]
)

style.add_argument(
	"-fg-col", "--text-color", type = str,
	default = "#000",
	metavar = "#123456",
	help = lang["argparse/main"]["style.text_color"]
)

style.add_argument(
	"-bg-col", "--background-color", type = str,
	default = "#FFF",
	metavar = "#123456",
	help = lang["argparse/main"]["style.background_color"]
)

style.add_argument(
	"-s", "--emoji-style", type = str,
	default = "Twitter",
	metavar = '"str"',
	help = lang["argparse/main"]["style.emoji_style"]
)

style.add_argument(
	"-sw", "--width", type = int,
	default = 0,
	metavar = "int > 0",
	help = lang["argparse/main"]["style.width"]
)

#-=-=-=-#
# Optimization

optimization.add_argument(
	"-ab", "--audio-bitrate", type = int,
	choices = range(LIMIT_AUDIO_BITRATE[0] + LIMIT_AUDIO_BITRATE[1] + 1, 16),
	default = 224,
	metavar = "{0} <= int <= {1}".format(*LIMIT_AUDIO_BITRATE),
	help = lang["argparse/main"]["optimization.audio_bitrate"]
)

optimization.add_argument(
	"-d", "--delay-count", type = int,
	default = 0,
	metavar = "int >= 0",
	help = lang["argparse/main"]["optimization.delay_count"]
)

optimization.add_argument(
	"-l", "--loop-count", type = int,
	default = 0,
	metavar = "int >= 0",
	help = lang["argparse/main"]["optimization.loop_count"]
)

optimization.add_argument(
	"-lsy", "--lossy", type = int,
	metavar = "{0} <= int <= {1}".format(*LIMIT_LOSSY),
	default = LIMIT_LOSSY[1],
	help = lang["argparse/main"]["optimization.lossy"]
)

#-=-=-=-#
# Switch

switch.add_argument(
	"-togif", "--force-gif",
	action = "store_true",
	help = lang["argparse/main"]["switch.force_gif"]
)

switch.add_argument(
	"-webm", "--webm-encode",
	action = "store_true",
	help = lang["argparse/main"]["switch.webm_encode"]
)

switch.add_argument(
	"-kc", "--keep-session-directory",
	action = "store_true",
	help = lang["argparse/main"]["switch.keep_session_directory"]
)

switch.add_argument(
	"-nod", "--no-open-directory",
	action = "store_true",
	help = lang["argparse/main"]["switch.no_open_directory"]
)

switch.add_argument(
	"-nox", "--no-optimization",
	action = "store_true",
	help = lang["argparse/main"]["switch.no_optimization"]
)

switch.add_argument(
	*fpl_flags,
	action = "store_true",
	help = lang["argparse/main"]["switch.force_primary_language"]
)

switch.add_argument(
	"-h", "--help",
	action = "help",
	help = lang["argparse/main"]["main.help"]
)

args = parser.parse_args()