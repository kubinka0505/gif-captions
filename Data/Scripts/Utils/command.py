class commands:
	class optimizers:
		"""
		Commands used for files optimization.
		"""
		static = '{package} {colors_limit} --ext .png -f -s 1 --skip-if-larger --nofs "{input_image_file_path}" {package_verbosity}'
		dynamic = '{package} --careful --no-comments -b -d {delay_count} -O8 {factor} "{input_image_file_path}" -l{loop_count} {package_verbosity}'

	class video:
		"""
		Commands used for video files manipulation.
		"""
		frame_rate = '{package} -i "{input_file}" -hide_banner -stats'

		# Extract frames
		extract_frames = '{package} -i "{input_visual_file}" -vsync vfr "{frames_directory}/Frame_%05d.png" -y -hide_banner -loglevel {package_verbosity} -stats'

		# GIF creation
		generate_palette = '{package} -i "{frames_directory}/Frame_%05d.png" -vf "palettegen=reserve_transparent={transparent}" -fflags +bitexact -flags:v +bitexact -flags:a +bitexact "{output_visual_file}" -y -hide_banner -loglevel {package_verbosity} -stats'
		create_transparent_gif = '{package} -thread_queue_size 1024 -i "{frames_directory}/Frame_%05d.png" -i "{input_palette_image_file}" -lavfi "select=not(mod(n\,-1)),paletteuse=alpha_threshold=128" -gifflags -offsetting -fflags +bitexact -flags:v +bitexact -flags:a +bitexact "{output_visual_file}" -y -hide_banner -loglevel {package_verbosity} -stats'

		# Combine frames
		combine_frames_video = '{package} -loop 1 -r {output_visual_file_frame_rate} -thread_queue_size 1024 -i "{frames_directory}/Frame_%05d.png" {audio_arguments} -movflags faststart -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" -vsync vfr {output_video_codec} -pix_fmt yuv420p -fflags +bitexact -flags:v +bitexact -flags:a +bitexact "{output_visual_file_path}" -y -hide_banner -loglevel {package_verbosity} -stats'
		combine_frames_video_audio = '-i "{input_audio_file}" -t {input_audio_duration} -ab {input_audio_bitrate}k -af "aresample={input_audio_samplerate}:cutoff=1"'

	class audio:
		"""
		Commands used for audio files manipulation.
		"""
		get_channels = '{package} -i "{input_file_path}" -lavfi "[0:a]channelsplit=channel_layout=stereo[left][right]" -map "[left]" -f md5 - -map "[right]" -f md5 -'
		convert = '{package} -i "{input_audio_file_path}" -fflags +bitexact -flags:v +bitexact -flags:a +bitexact "{output_audio_file_path}" -y -hide_banner -loglevel {package_verbosity} -stats'
		normalize = '{package} "{input_audio_file_path}" -D -L -c {input_audio_channels} -b 16 --norm={normalization_level} --comment "" -G "{output_audio_file_path}" -V{package_verbosity}'
		is_silent = '{package} -i "{input_file_path}" -af astats -f null -hide_banner -'

	# No space for Windows explorer "/select," flag compensation
	open_in_explorer = '{executable}"{file}" {null_device}'