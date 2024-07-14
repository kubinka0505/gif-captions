logger(
	lang["ending"]["output.saving"].format(
		output_file_path = final_file
	),
	"info"
)

runtime = datetime.timedelta(seconds = time.time() - __START_TIME)

#-=-=-=-#
# Output information

_outinfo = {
	lang["ending"]["info.runtime"]:   str(runtime)[2:-3],
	lang["ending"]["info.file.size"]: file_size(final_file),
	lang["ending"]["info.file.type"]: stripext(final_file, True)
}
_outinfo_longest_length = len(sorted(_outinfo.keys(), key = len)[-1])

if args.verbosity != -1:
	if not args.no_open_directory:
		open_in_explorer(final_file)

	logger("", "info")
	for k, v in _outinfo.items():
		if v:
			logger(
				(k + ":").ljust(_outinfo_longest_length + 2, " ") + v,
				"info"
			)
			
	logger("", "debug")

#-=-=-=-#
# Remove session directory

if not args.keep_session_directory:
	rmtree(session_directory, ignore_errors = True)