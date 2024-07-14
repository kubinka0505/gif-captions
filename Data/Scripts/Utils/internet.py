# Session
InternetSession = Session()
InternetSession.headers.update(
	{
		"User-Agent":
		"Mozilla/5.0 (Windows NT 10.0; Win32; x32) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
	}
)

#-=-=-=-#

def check_connection(timeout: float = 0.5) -> bool:
	"""
	Checks if there's internet connection available.

	Args:
		timeout: Float value being the max connection waiting time.

	Returns:
		bool: True if connection available, otherwise False.
	"""
	try:
		InternetSession.head("https://google.com", timeout = timeout)
		retval = True
	except Exception:
		retval = False

	return retval

def is_URL(url: str) -> bool:
	"""
	Verifies whether `url` is URL.

	Args:
		url: String URL address.

	Returns:
		bool: True if `url` is URL, otherwise False.
	"""
	for delimiter in ["https://", "http://"]:
		url = url.split(delimiter)[-1]
	url = "http://" + url

	try:
		retval = InternetSession.head(url).ok
	except Exception:
		retval = False

	return retval

def download_file(url: str, directory: str) -> str:
	"""
	Downloads file to a given directory.

	Args:
		url: String URL address.
		directory: Target file directory.

	Returns:
		string: Absolute path of downloaded file.
	"""
	res = InternetSession.get(url, allow_redirects = True, stream = True)

	for delimiter in ("#", "&", "?"):
		filename = url.split(delimiter)[0]
		
	filename = os.path.basename(filename)
	outfile = os.path.join(directory, filename)

	with open(outfile, "wb") as f:
		for chunk in res.iter_content(chunk_size = 1024):
			if chunk:
				f.write(chunk)

	return outfile

def get_service(url: str) -> str:
	"""
	Scraping main Image URL from various pages.

	Args:
		url (string): String URL address.

	Warning:
		Commented statements are deprecated, but may work.
		Enable on your own responsibility.

	Returns:
		string: Modified or original `URL`
	"""
	get = InternetSession.get
	res = get(url)

	try:
		# Tenor
		if all_in(("tenor.com/", "/view/"), url):
			try:
				url = res.text.split('"og:video"')[1].split("content")[1].split('"')[1]
			except IndexError:
				url = res.text.split("contentUrl")[1].replace("\\u002F", "/").split('"')[2]

		# Giphy
		if "giphy.com/gifs/" in url:
			try:
				url = res.text.split('"og:video"')[1].split("content")[1].split('"')[1]
			except IndexError:
				url = "https://media" + str(res.text).split("https://media")[2].split('"')[0]

		# Pinterest
		if "pinterest.com/pin/" in url:
			try:
				url = res.text.split('"video-snippet"')[1].split("contentUrl")[1].split('"')[2]
			except IndexError:
				url = res.text.split("pin-image-preload")[1].split("href")[1].split('"')[1]

		# Gifer
		#if "gifer.com/" in url:
		#	url = "https://i.gifer.com/{0}.gif".format(url.split("/")[-1])

	except Exception:
		pass

	return url

#-=-=-=-#

INTERNET_CONNECTION = check_connection()