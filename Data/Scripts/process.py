logger(
	lang["process"]["frames.extract"],
	"info"
)

frames = video.extract_frames(
	args.visual,
	extracted_frames_directory,
	FFmpeg,
	FFmpeg_verbosity
)

logger(
	lang["process"]["caption.create"],
	"info"
)
caption = image.make_caption(
	text = args.text,
	text_wrap = args.text_wrap,
	font = args.font,
	fg_color = args.text_color,
	bg_color = args.background_color,
	line_height = 1.5,
	emoji_style = args.emoji_style
)
caption.save(caption_field_image)

logger(
	lang["process"]["caption.apply"].format(
		frames_amount = len(frames)
	) + " (" + lang["process"]["wait"] + ")",
	"info"
)

for frame in frames:
	frame_obj = Image.open(frame)

	if args.width:
		frame_obj = ImageOps.contain(frame_obj, (args.width, args.width), Image.LANCZOS)

	caption = ImageOps.contain(caption, frame_obj.size, Image.LANCZOS)

	frame_obj = ImageOps.pad(
		frame_obj,
		(
			frame_obj.size[0],
			frame_obj.size[1] + caption.size[1]
		),
		color = args.background_color,
		centering = (0, 1)
	)
	frame_obj.paste(
		caption,
		(
			(frame_obj.size[0] - caption.size[0]) // 2,
			0
		),
		caption
	)
	frame_obj.save(frame)

	index = str(frames.index(frame))
	if args.verbosity > -1:
		print(
			"[{0}/{1}]".format(
				index.rjust(len(str(len(frames))), "0"),
				len(frames)
			),
			end = "\r"
		)

#-=-=-=-#

if len(frames) == 1:
	msg = lang["process"]["frames.save_01"]
else:
	msg = lang["process"]["frames.combine"].format(
		frames_amount = len(frames)
	)

logger(
	msg + " (" + lang["process"]["wait"] + ")",
	"info"
)

output_format = "png"
if len(frames) > 1:
	output_format = "gif"

if args.audio:
	output_format = "mp4"
	if args.webm_encode:
		output_format = "webm"

if args.force_gif:
	output_format = "gif"

logger(
	lang["process"]["output.create"],
	"info"
)
final_file = video.combine_frames(
	args.audio,
	args.output_directory,
	output_format,
	args.audio_bitrate,
	FFmpeg,
	FFmpeg_verbosity
)

if not os.path.exists(final_file):
	logger(
		lang["process"]["output.error"],
		"error"
	)

if not args.no_optimization:
	final_file = optimizers.main(final_file)