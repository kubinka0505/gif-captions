class image:
	def make_caption(
		text: str,
		text_wrap: int,
		font: str,
		fg_color: str,
		bg_color: str,
		line_height: float,
		emoji_style: str
	) -> Image.open:
		"""
		Generates a caption field with text.

		Args:
			text: Caption text.
			text_wrap: Amount of characters which after remaining text will be moved to new line.
			font: Text font path.
			fg_color: RGB caption text color.
			bg_color: RGB caption background color.
			line_height: Lines separation height.
			style: Emoji target style.

		Raises:
			SystemExit: If one of the emoji characters is not supported on the `style`.

		Returns:
			Image.open: Image object.
		"""
		base = Image.new("RGBA", (IMAGE_CAPTION_MAX_X, IMAGE_CAPTION_MAX_Y), (0, 0, 0, 0))

		text = wrap(emojize(text), text_wrap)
		font = ImageFont.truetype(font, 100)

		img_list = []
		img_list_expanded = []

		#-=-=-=-#

		max_X = image.getsize(font, "W")[0]
		max_Y = image.getsize(font, "|")[1]

		spacing_Y = 0

		for line in text:
			line_img = base.copy()
			line_img_draw = ImageDraw.Draw(line_img)
			spacing_X = 0

			for character in line:
				if character in EMOJI_UNICODE_ENGLISH:
					try:
						emoji_img = image.get_emoji_image(demojize(character), emoji_style)
					except UnidentifiedImageError as error:
						raise SystemExit(
							lang["image"]["caption.create.unsupported_emoji"].format(
								error_name = error.__class__.__name__,
								character = demojize(character),
								style_name = emoji_style.title()
							)
						)

					emoji_img = emoji_img.resize(
						(max_Y,) * 2,
						Image.LANCZOS
					)

					line_img.paste(
						emoji_img,
						(spacing_X, 0),
						emoji_img
					)
					spacing_X += emoji_img.size[0]
					character = character.replace(character, "")

				line_img_draw.text(
					xy	= (spacing_X, 0),
					text = character,
					font = font,
					fill = fg_color
				)

				spacing_X += image.getsize(font, character)[0]

			spacing_Y += image.getsize(font, line)[1]
			line_img = line_img.crop(line_img.getbbox())
			img_list.append(line_img)

		for img in img_list:
			text_image = Image.new(
				"RGBA",
				(
					img.size[0],
					img.size[1] + max_Y,
				),
				(0, 0, 0, 0)
			)
			text_image.paste(img, (0, max_Y), img)
			img_list_expanded.append(text_image)

		spacing_Y = 0
		for img in img_list_expanded:
			base.paste(
				img,
				(
					(base.size[0] - img.size[0]) // 2,
					int(spacing_Y)
				),
				img
			)
			spacing_Y += img.size[1] / line_height

		#-=-=-=-#

		base = base.crop(base.getbbox())

		background = Image.new(
			"RGBA",
			(
				int(base.size[0] + (2 * max_X)),
				#int(base.size[1] + max_Y)
				max_Y + (max_Y * len(text))
			),
			bg_color
		)
		background.paste(
			base,
			(
				(background.size[0] - base.size[0]) // 2,
				(background.size[1] - base.size[1]) // 2,
			),
			base
		)

		return background

	def get_emoji_image(character: str, style: str) -> Image.open:
		"""
		Retrieves emoji image from API.

		Args:
			character (string): Unicode character to retrieve as image.
			style (string): Emoji target style.

		Raises:
			AttributeError: If `style` is not supported.
			LookupError: If emoji image could not be fetched.

		Returns:
			Image.open: Retrieved emoji image object.
		"""
		styles = [
			"Apple", "Google", "Microsoft",
			"Samsung", "WhatsApp", "Twitter",
			"Facebook", "JoyPixels", "OpenMoji",
			"EmojiDex", "LG", "HTC", "Mozilla"
		]
		styles = [elem.lower() for elem in styles]
		style = style.lower().strip()

		if style not in styles:
			raise AttributeError(
				lang["image"]["get_emoji_image.unsupported"].format(
					style_name = style.title()
				)
			)

		url = EMOJI_API_URL.format(
			emoji_unicode = quote_plus(emojize(character)),
			emoji_style = style
		)

		err = 0
		try:
			url = InternetSession.get(url, stream = True).raw
		except Exception:
			err = 1

		if err:
			raise LookupError(
				lang["image"]["get_emoji_image.error_fetch"]
			)

		retval = Image.open(url)
		retval = retval.convert("RGBA")

		return retval

	def getsize(font: ImageFont, text: str) -> tuple:
		"""
		Legacy `PIL.ImageFont.getsize` function.

		Args:
			font (PIL.ImageFont): Font object.
			text (string): Text to measure.

		Returns:
			Width and height (in pixels) of `text` using `font`.
		"""
		left, top, right, bottom = font.getbbox(text)
		return right - left, bottom - top

	def is_grayscale(path: str) -> bool:
		"""
		Checks if image is grayscale.

		Args:
			path (string): Absolute path of existing image.

		Returns:
			bool: True if `path` `PIL.Image` object is in grayscale, otherwise False.
		"""
		image = Image.open(path).convert("RGB")

		retval = True

		RGB = image.split()
		for color in range(1, 2 + 1):
			if ImageChops.difference(RGB[0], RGB[color]).getextrema()[1] != 0:
				retval = False
				break

		return retval

	def is_transparent(path: str) -> bool:
		"""
		Checks if image has transparency.

		Args:
			path(string): Absolute path of existing image.

		Returns:
			bool: True if `path` `PIL.Image` object contains transparency, otherwise False.
		"""
		image = Image.open(path)

		retval = False

		if image.info.get("transparency", None) is not None:
			retval = True
		if image.mode == "P":
			transparent = image.info.get("transparency", -1)
			for _, index in image.getcolors():
				if index == transparent:
					retval = True
		elif image.mode == "RGBA":
			extrema = image.getextrema()
			if extrema[3][0] < 255:
				retval = True

		return retval