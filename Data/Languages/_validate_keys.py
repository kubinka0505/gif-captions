import os
import json
from pathlib import Path

def extract_subkeys(dictionary) -> list:
	keys = []

	for key, value in dictionary.items():
		if isinstance(value, dict):
			subkeys = extract_subkeys(value)
			keys.extend(subkeys)
		else:
			keys.append(key)

	return keys

#-=-=-=-#

lang = open("English.json")
lang = json.load(lang)

not_found = []

for value in extract_subkeys(lang):
	found = False

	for file in Path("../Scripts").rglob("*.py"):
		content = open(file, "r", encoding = "UTF-8").read()
		if content.find(f'"{value}') > -1:
			found = True
			break

	if not found:
		not_found.append(value)

if not_found:
	for element in not_found:
		print(element)