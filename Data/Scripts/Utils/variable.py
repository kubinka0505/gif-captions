# Data

IMAGE_PNG_MAX_COLORS = 256
IMAGE_CAPTION_MAX_X = 5000
IMAGE_CAPTION_MAX_Y = 7500
VISUAL_FRAME_RATE_UNSET = 25
AUDIO_NORM_LEVEL = 0

FORMATS_STATIC = ["PNG"]
FORMATS_DYNAMIC = ["GIF"]

EMOJI_API_URL = "https://emojicdn.elk.sh/{emoji_unicode}?style={emoji_style}"
EMOJI_UNICODE_ENGLISH = {key: emoji.EMOJI_DATA[key]["en"] for key in emoji.EMOJI_DATA}

STRING_TIME_NOW = datetime.datetime.now().strftime("%d-%m-%Y %H-%M-%S")
STRING_RANDOM_GLOBAL = random_string()

OUTPUT_NAME_LIMIT = 18

LIMIT_AUDIO_BITRATE = 96, 512
LIMIT_LOSSY = 1, 200

REPOSITORY = "/".join((__author__, __title__))

#-=-=-=-#
# Files

temporary_files_directory = os.path.expanduser(r"~\AppData\Local\Temp") if is_windows else (os.sep + "tmp")
outputs_directory = os.path.join(__BaseDir, "Outputs")

session_directory = os.path.join(
	temporary_files_directory,
	__title__,
	"Sessions",
	"_".join((
		*STRING_TIME_NOW.split(" "),
		STRING_RANDOM_GLOBAL
	))
)

extracted_frames_directory = os.path.join(session_directory, "Frames")
caption_field_image = os.path.join(session_directory, "caption.png")
logs_file = os.path.join(session_directory, "logs.txt")

#-=-=-=-#
# Setup

FORMATS_STATIC = tuple([extension.lower() for extension in FORMATS_STATIC])
FORMATS_DYNAMIC = tuple([extension.lower() for extension in FORMATS_DYNAMIC])

FORMATS_OPTIMIZE = [FORMATS_STATIC, FORMATS_DYNAMIC]
FORMATS_OPTIMIZE = [item for sublist in FORMATS_OPTIMIZE for item in sublist]

# Create directories
os.makedirs(extracted_frames_directory, exist_ok = True)
os.makedirs(outputs_directory, exist_ok = True)