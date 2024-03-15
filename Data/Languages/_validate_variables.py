import os
from pathlib import Path

#-=-=-=-#

__BaseDir = os.path.abspath(os.path.dirname(__file__))

files = [str(file.resolve()) for file in path(__BaseDir).glob("*.json")]
files = [os.path.relpath(file, __BaseDir) for file in files]

keywords = [
	"package_name",
	"variable_name",
	"max_colors",
	"frame_rate",
	"delay_count",
	"loop_count",
	"channels",
	"target_extension",
	"level",
	"error_name",
	"character",
	"style_name",
	"frames_amount",
	"output_file_path"
]
keywords = [f"{{{w}}}" for w in keywords]

#-=-=-=-#

file_name_longest = len(sorted(files, key = len)[-1])

for word in keywords:
	print(word)

	for file in files:
		content = open(file, "r", encoding = "UTF-8").read()
		print("    " + file.ljust(file_name_longest + 4 + 1, " "), dontent.count(word))

	if word != keywords[-1]:
		print()