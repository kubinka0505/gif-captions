<h1 align=center>
	<i>gif-captions</i>
</h1>

<p align=center>
	<a href="https://colab.research.google.com/github/kubinka0505/gif-captions/blob/master/Documents/gif-captions.ipynb"><img src="https://shields.io/badge/Colab-Open-F9AB00?&logoColor=F9AB00&style=for-the-badge&logo=Google-Colab"></a>　<a href="License.txt"><img src="https://custom-icon-badges.demolab.com/github/license/kubinka0505/gif-captions?logo=law&color=red&style=for-the-badge"></a>
</p>

<p align=center>
	<img src="https://custom-icon-badges.demolab.com/github/languages/code-size/kubinka0505/gif-captions?logo=database&style=for-the-badge">　<a href="https://codeclimate.com/github/kubinka0505/gif-captions"><img src="https://shields.io/codeclimate/maintainability/kubinka0505/gif-captions?logo=Code-Climate&style=for-the-badge"></a>　<a href="https://app.codacy.com/gh/kubinka0505/gif-captions"><img src="https://shields.io/codacy/grade/e543ef61f70249488127c3634c5c8d20?logo=Codacy&style=for-the-badge"></a>
</p>

## Description 📝
Pack of scripts providing widely customizable [GIF captions](https://knowyourmeme.com/memes/gif-captions) generation.

A complete rewrite of my [`iFunny-Captions`](https://github.com/kubinka0505/iFunny-Captions) project, providing <u>**better code quality and maintainability**</u>, at the expense of possible speed and number of features.

**Supports:**
- 🎴 Static images captions
- 🖼️ Dynamic images captions
- ▶️ **Videos captions**
- 🔊 **Audio support** + [**peak normalization**](https://wikipedia.org/wiki/Audio_normalization)
- 📉 Output files optimization
- 🔠 **Custom fonts**
- 🔗 URL media inputs
- 🙂 Emojis in text<sup>*</sup>
- 🎌 [**12** Languages](Data/Languages)
   - 🇨🇿 🇳🇱 🇬🇧 🇫🇷 🇩🇪 🇮🇹 🇯🇵 🇵🇱 🇵🇹 🇷🇺 🇪🇸 🇹🇷
- 🖥️ Graphical User Interface<sup>*</sup> [<img src="Documents/Pictures/Main/Google_Colab.svg" width=25>](https://colab.research.google.com/github/kubinka0505/gif-captions/blob/master/Documents/gif-captions.ipynb)

<sup>*</sup> - Internet connection required

## Requirements 📥

Programs:
- [**`Python >= 3.7`**](http://www.python.org/downloads) 🐍

Modules:
- [`sty`](https://github.com/feluxe/sty) - Colored prints 🎨
- [`unidecode >= 1.3.8`](https://github.com/avian2/unidecode) - [Text normalization](http://wikipedia.org/wiki/Text_normalization#Techniques) ⚙️
- [`colour`](https://github.com/vaab/colour) - Colored text values handling 🎨
- [`requests >= 2.13`](https://github.com/psf/requests) - URL fetching 🔗
- [`distro >= 1.9`](https://github.com/python-distro/distro)<sup>*</sup> - Unix directory opening handler 📂
- [`mutagen >= 1.45.1`](https://github.com/quodlibet/mutagen) - Audio state checker & video length handler ⏳
- [`Pillow >= 9`](https://github.com/python-pillow/Pillow) - Images creation 🖼️
- [`emoji >= 2`](https://github.com/carpedm20/emoji) - Emoji support ✨

Packages (bold links are **Windows** static executable binaries):
- [**`FFmpeg >= 4.4`**](https://videohelp.com/software/ffmpeg/old-versions)
- [**`SoX >= 14.4.2`**](https://videohelp.com/software/sox/old-versions)
- [**`Gifsicle >= 1.92-2`**](https://eternallybored.org/misc/gifsicle/releases) - **Check after 64-bit if possible!**
- [**`PNGQuant >= 2.14`**](https://pngquant.org/#download) *(optional)*
- [`Python3-PIP`](https://packages.debian.org/sid/python3-pip)</a><sup>*</sup>
- [`Python3-TK`](https://packages.debian.org/sid/python3-tk)</a><sup>*</sup>

<sup>*</sup> - Required on non-Windows operating systems

---
## Installation 📝

**When on Linux**, install packages using this one-liner:
```bash
sudo apt-get install git python3-pip ffmpeg sox pngquant gifsicle
```
1. Clone the repository and move to its directory.
	```bash
	git clone http://github.com/kubinka0505/gif-captions
	cd gif-captions
	```
2. Install required modules by `python3 -m pip install -r requirements.txt`
3. 
	- If on Windows:
		- Allocate [the required packages executable files](#requirements-) to `PATH` system environment variable
	- Otherwise:
		- Install [required packages](#requirements-).
4. Run `gc.py -h` for arguments.
5. Locate output image in the outputs directory (`Outputs` by default).

---

### Example usage ⚙️

> [!CAUTION]
> Due to the audio desynchronizing problems, **program does not drop frames**.
> 
> It means that in example videos with `24` frames per second framerate with duration of `10` seconds and width of `1000` pixels are going to have enormous size.
> 
> ---
> <sup>ℹ️ See the `--width` flag.</sup>

1. Generate video caption with video and its original sound, or (if silent) GIF.
	- `gc.py -i "video_with_audio.mp4" -t "Lorem ipsum"`
2. Generate WebM video caption with dynamic image and audio file, which content will be looped until audio end duration.
	- `gc.py -i "https://example.org/image.gif" -t "Lorem ipsum" -a "audio.mp3" -webm`
3. Generate static image caption with modified colors and emoji style.
	- `gc.py -i "../picture.jpg" -t "Text with emojis :snake:" -fg-col #FF0000 -bg-col #333 -s apple`
4. Generate dynamic image caption with max dimension `500` and saved to other directory.
	- `gc.py -i "video_without_sound.mp4" -t "Lorem ipsum" -sw 500 -d "~/Pictures/captions`

---

### Supported GIF services 🗃️

> [!IMPORTANT]
> In case if service is not working - please copy its **direct non-static image URL**.

<table>
  <thead>
	<tr>
		<th>Tenor</th>
		<th>Giphy</th>
		<th>Pinterest</th>
	</tr>
  </thead>
  <tbody>
	<tr align=center>
		<td><a href="https://tenor.com" target="_blank"><img src="Documents/Pictures/Image_Services_Logos/Tenor.svg" alt=Tenor width=65></a></td>
		<td><a href="https://giphy.com" target="_blank"><img src="Documents/Pictures/Image_Services_Logos/Giphy.svg" alt=Giphy width=65></a></td>
		<td><a href="https://pinterest.com" target="_blank"><img src="Documents/Pictures/Image_Services_Logos/Pinterest.svg" alt=Pinterest width=65></a></td>
	</tr>
  </tbody>
</table>

---

## Meta Info ℹ️
All versions of this project have been tested on:

| OS | Distribution | OS Version | Python Version | System Architecture (`bits`) |
|:-:|:-:|:-:|:-:|:-:|
| Windows | ― | 10 | 3.10.11 | 64 |
| Linux | Ubuntu | 20.04 | 3.8.10 | 64 |