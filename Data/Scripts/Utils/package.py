packages = "FFmpeg", "SoX", "PNGQuant", "Gifsicle"

#-=-=-=-#

for Package in packages:
	err = 0

	try:
		pkg = search_package(Package.lower(), "PATH")

		if is_windows:
			pkg = f'"{pkg}"'

		locals()[Package] = pkg
	except Exception as error:
		print(
			colors.error + \
			lang["pkg"]["not_found"].format(
				package_name = Package
			) + \
			colors.reset
		)

		raise SystemExit()