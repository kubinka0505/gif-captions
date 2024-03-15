if INTERNET_CONNECTION:
	try:
		# Update notice
		with InternetSession.get(f"https://api.github.com/repos/{REPOSITORY}/releases") as Site:
			if Site.ok:
				if len(Site.json()) > 0:
					__version_latest__ = Site.json()[0]["tag_name"]

					if float(__version_latest__) > float(__version__):
						logger(
							lang["update_notification"]["notification"],
							"info.update"
						)
						logger("", "info")
	except exceptions.ConnectionError:
		pass