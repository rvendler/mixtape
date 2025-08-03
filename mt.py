import subprocess
import os
import tempfile
from pydub import AudioSegment

class MT:
	def __init__(self, audiosegment=None):
		# Initialize with either a provided AudioSegment or silence
		if audiosegment:
			self.audiosegment = audiosegment
		else:
			self.audiosegment = AudioSegment.silent(duration=0)

	@classmethod
	def from_file(cls, filename: str):
		"""
		Alternative constructor that loads an audio file during initialization.

		:param filename: The path to the audio file to be loaded.
		:return: An instance of MTTrack initialized with the loaded audio.
		"""
		audiosegment = AudioSegment.from_file(filename)
		return cls(audiosegment)

	def load(self, filename):
		self.audiosegment = AudioSegment.from_file(filename)

	def save(self, filename, format="mp3"):
		self.audiosegment.export(filename, format=format)

	def insert(self, b, offset_ms: int):
		# If the offset is beyond the length of 'a', pad 'a' with silence until the offset
		if offset_ms > len(self.audiosegment):
			padding = AudioSegment.silent(duration=offset_ms - len(self.audiosegment))
			self.audiosegment = self.audiosegment + padding		
		# Get the part of 'a' before and after the offset
		before = self.audiosegment[:offset_ms]
		after = self.audiosegment[offset_ms + len(b.audiosegment):] if offset_ms + len(b.audiosegment) < len(self.audiosegment) else AudioSegment.silent(0)

		# Concatenate the segments: before, b, and after
		self.audiosegment = before + b.audiosegment + after

	def get_length_ms(self) -> int:
		return len(self.audiosegment)

	def clamp_length(self, max_length_ms: int):
		if len(self.audiosegment) > max_length_ms:
			self.audiosegment = self.audiosegment[:max_length_ms]

	def append_silence(self, duration_ms: int):
		silence = AudioSegment.silent(duration=duration_ms)
		self.audiosegment += silence

	def fade_in(self, duration: int):
		self.audiosegment = self.audiosegment.fade_in(duration)

	def fade_out(self, duration: int):
		self.audiosegment = self.audiosegment.fade_out(duration)

	def append(self, other_track):
		self.audiosegment += other_track.audiosegment

	def overlay(self, other_track, offset_ms: int):
		# Handle padding if the offset is greater than the current length
		if offset_ms > len(self.audiosegment):
			padding = AudioSegment.silent(duration=offset_ms - len(self.audiosegment))
			self.audiosegment += padding

		# Extend the track if necessary to fit the overlay
		overlay_end_time = offset_ms + len(other_track.audiosegment)
		if overlay_end_time > len(self.audiosegment):
			extension = AudioSegment.silent(duration=overlay_end_time - len(self.audiosegment))
			self.audiosegment += extension

		# Overlay the other track at the specified offset
		self.audiosegment = self.audiosegment.overlay(other_track.audiosegment, position=offset_ms)

	def apply_gain(self, gain_db: float):
		"""
		Adjusts the volume of the track by a specified number of decibels (dB).
		Positive values increase the volume, and negative values decrease the volume.

		:param gain_db: The gain adjustment in decibels (dB). Positive for increase, negative for decrease.
		"""
		if gain_db == 0.0:
			return
		self.audiosegment = self.audiosegment.apply_gain(gain_db)

	def apply_highpass(self, cutoff_freq: float):
		"""
		Applies a highpass filter to the audio track.

		:param cutoff_freq: The cutoff frequency for the highpass filter in Hz.
		"""
		self.audiosegment = self.audiosegment.high_pass_filter(cutoff_freq)

	def apply_lowpass(self, cutoff_freq: float):
		"""
		Applies a lowpass filter to the audio track.

		:param cutoff_freq: The cutoff frequency for the lowpass filter in Hz.
		"""
		self.audiosegment = self.audiosegment.low_pass_filter(cutoff_freq)

	def apply_compressor(self, threshold: float = -20.0, ratio: float = 4.0, attack: float = 5.0, release: float = 50.0):
		"""
		Applies a compressor effect to the audio track.

		:param threshold: The threshold in dB where compression starts.
		:param ratio: The compression ratio.
		:param attack: The attack time in milliseconds (how quickly the compressor starts).
		:param release: The release time in milliseconds (how quickly the compressor stops).
		"""
		self.audiosegment = self.audiosegment.compress_dynamic_range(
			threshold=threshold, ratio=ratio, attack=attack, release=release
		)

	def trim_silence(self, silence_threshold=-50.0, chunk_size=10, start_silence=50, middle_silence=450, end_silence=250):
		"""
		Trims long periods of silence from the audio, allowing for customizable silence thresholds
		and limits on how much silence to preserve at the start, middle, and end of the audio.

		:param silence_threshold: The dBFS threshold below which audio is considered silence.
		:param chunk_size: The size of the chunks (in milliseconds) used to scan for silence.
		:param start_silence: Max amount of silence to preserve at the beginning.
		:param middle_silence: Max amount of silence to preserve in the middle.
		:param end_silence: Max amount of silence to preserve at the end.
		:return: None. Modifies the `audiosegment` in place.
		"""
		sound = self.audiosegment
		parts = []
		num_parts = 0
		pos_ms = 0
		remaining_ms = len(sound) - pos_ms

		while remaining_ms > 0:
			use_chunk_size = min(chunk_size, remaining_ms)
			is_silence = sound[pos_ms:pos_ms+use_chunk_size].dBFS < silence_threshold

			if pos_ms == 0:  # First
				p = {
					"silence": is_silence,
					"start": pos_ms,
					"length": use_chunk_size,
					"pos": "first"
				}
				parts.append(p)
			else:
				if parts[num_parts]["silence"] == is_silence:
					parts[num_parts]["length"] += use_chunk_size
				else:
					p = {
						"silence": is_silence,
						"start": pos_ms,
						"length": use_chunk_size,
						"pos": "middle",
					}
					parts.append(p)
					num_parts += 1
			pos_ms += use_chunk_size
			remaining_ms = len(sound) - pos_ms

		parts[num_parts]["pos"] = "end"

		# Create a new trimmed audiosegment
		ts = None

		for part in parts:
			is_silence = part["silence"]
			start = part["start"]
			length = part["length"]
			pos = part["pos"]

			use_length = length

			if is_silence:
				if pos == "first" and length > start_silence:
					use_length = start_silence
				elif pos == "middle" and length > middle_silence:
					use_length = middle_silence
				elif pos == "end" and length > end_silence:
					use_length = end_silence

				if use_length > length:
					use_length = length

			if ts is None:
				ts = sound[start:start + use_length]
			else:
				ts += sound[start:start + use_length]

		# Update the audiosegment with the trimmed version
		self.audiosegment = ts

	def apply_vst(self, vst_name: str, preset_name: str):
		"""
		Applies a VST plugin using MrsWatson.exe on the current audio track.

		:param vst_name: The name of the VST plugin to apply.
		:param preset_name: The preset name within the VST plugin to use.
		"""
		# Create temporary files for input and output WAVs
		input_file = tempfile.mktemp(suffix=".wav")
		output_file = tempfile.mktemp(suffix=".wav")
		
		try:
			# Export the current audiosegment to a temporary WAV file
			self.audiosegment.export(input_file, format="wav")

			# Construct the command to execute MrsWatson with the appropriate options
			command = [
				"tools/mrswatson/MrsWatson64.exe", 
				"--input", input_file, 
				"--output", output_file, 
				"--plugin", f"{vst_name},{preset_name}"
			]
			
			# Execute the command and wait for it to complete
			subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
			#subprocess.run(command, check=True)

			# Load the processed output WAV back into the audiosegment
			processed_audio = AudioSegment.from_file(output_file, format="wav")

			# Replace the current audiosegment with the processed version
			self.audiosegment = processed_audio

		finally:
			# Clean up temporary files
			if os.path.exists(input_file):
				os.remove(input_file)
			if os.path.exists(output_file):
				os.remove(output_file)

	def apply_mastering(self):
		input_file = tempfile.mktemp(suffix=".wav")
		output_file = tempfile.mktemp(suffix=".wav")
		
		try:
			self.audiosegment.export(input_file, format="wav")

			command = [
				"tools/phase_limiter/phase_limiter.exe", 
				"--input", input_file, 
				"--output", output_file 
			]
			
			# Execute the command and wait for it to complete
			subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
			#subprocess.run(command, check=True)

			# Load the processed output WAV back into the audiosegment
			processed_audio = AudioSegment.from_file(output_file, format="wav")

			# Replace the current audiosegment with the processed version
			self.audiosegment = processed_audio

		finally:
			# Clean up temporary files
			if os.path.exists(input_file):
				os.remove(input_file)
			if os.path.exists(output_file):
				os.remove(output_file)

class MTMixer:
	def __init__(self):
		# Internal list to store MTTracks and their respective gains
		self.tracks_with_gain = []

	def add_track(self, track: MT, gain: float):
		"""
		Adds an MTTrack to the mixer with a specified gain value.

		:param track: An instance of MTTrack.
		:param gain: The gain in dB to be applied to the track when mixed.
		"""
		self.tracks_with_gain.append((track, gain))

	def generate_mix(self) -> MT:
		"""
		Generates a mix of all added MTTracks, applying the specified gain to each.

		:return: A new MTTrack that is the combined mix of all tracks.
		"""
		if not self.tracks_with_gain:
			raise ValueError("No tracks have been added to the mixer.")

		# Start with the first track in the list
		base_track, base_gain = self.tracks_with_gain[0]
		mixed_audiosegment = base_track.audiosegment.apply_gain(base_gain)

		# Overlay each subsequent track on top of the base track
		for track, gain in self.tracks_with_gain[1:]:
			# Apply gain to the current track and overlay it
			track_with_gain = track.audiosegment.apply_gain(gain) if gain != 0.0 else track.audiosegment
			mixed_audiosegment = mixed_audiosegment.overlay(track_with_gain)

		# Return the combined mix as a new MTTrack
		return MT(mixed_audiosegment)

class MultiTrack:
	def __init__(self):
		"""
		Initializes a MultiTrack instance with an empty dictionary of channels.
		Each channel is identified by a unique string or integer.
		"""
		self.channels = {}  # key: channel identifier, value: MT instance
		self.gains = {}	 # key: channel identifier, value: gain in dB
		self.master_gain = 0.0  # Master gain in dB

	def _get_channel(self, channel_id):
		"""
		Retrieves the MT instance for the given channel. If it doesn't exist, creates it.

		:param channel_id: The identifier for the channel (string or integer).
		:return: The MT instance associated with the channel.
		"""
		if channel_id not in self.channels:
			self.channels[channel_id] = MT()
			self.gains[channel_id] = 0.0  # Default gain
		return self.channels[channel_id]

	# Channel Management Methods

	def add_track(self, channel_id, track: MT, gain: float = 0.0):
		"""
		Adds or replaces a track in the specified channel with an optional gain.

		:param channel_id: The identifier for the channel (string or integer).
		:param track: An instance of MT to be added to the channel.
		:param gain: The gain in dB to be applied to the track when mixed.
		"""
		self.channels[channel_id] = track
		self.gains[channel_id] = gain

	def remove_track(self, channel_id):
		"""
		Removes the track associated with the specified channel.

		:param channel_id: The identifier for the channel (string or integer).
		"""
		if channel_id in self.channels:
			del self.channels[channel_id]
			del self.gains[channel_id]

	def set_gain(self, channel_id, gain_db: float):
		"""
		Sets the gain for the specified channel.

		:param channel_id: The identifier for the channel (string or integer).
		:param gain_db: The gain in decibels (dB).
		"""
		channel = self._get_channel(channel_id)
		# To prevent cumulative gain adjustments on the AudioSegment,
		# reset the channel's AudioSegment by removing previous gain and applying new gain.
		# However, pydub does not support removing gain, so it's best to manage gain separately.
		# Here, we assume that 'set_gain' sets the desired gain without modifying the AudioSegment.
		self.gains[channel_id] = gain_db

	def get_gain(self, channel_id):
		"""
		Retrieves the gain for the specified channel.

		:param channel_id: The identifier for the channel (string or integer).
		:return: Gain in dB.
		"""
		return self.gains.get(channel_id, 0.0)

	# Master Gain Methods

	def set_master_gain(self, gain_db: float):
		"""
		Sets the master gain for the entire mix.

		:param gain_db: The master gain in decibels (dB). Positive to increase volume, negative to decrease.
		"""
		self.master_gain = gain_db

	def get_master_gain(self) -> float:
		"""
		Retrieves the current master gain.

		:return: Master gain in dB.
		"""
		return self.master_gain

	# Loading and Saving

	def from_file(self, channel_id, filename: str, gain: float = 0.0):
		"""
		Loads an audio file into the specified channel.

		:param channel_id: The identifier for the channel (string or integer).
		:param filename: The path to the audio file to be loaded.
		:param gain: The gain in dB to be applied to the track when mixed.
		"""
		track = MT.from_file(filename)
		self.add_track(channel_id, track, gain)

	def save_mix(self, filename, format="mp3"):
		"""
		Saves the mixed audio from all channels into a single file, applying the master gain.

		:param filename: The path where the mixed audio will be saved.
		:param format: The format of the output file (default: "mp3").
		"""
		mixed = self.generate_mix()
		mixed.save(filename, format=format)

	def save_channel(self, channel_id, filename, format="mp3"):
		"""
		Saves the specified channel's audio to a file.

		:param channel_id: The identifier for the channel (string or integer).
		:param filename: The path where the audio will be saved.
		:param format: The format of the output file (default: "mp3").
		"""
		channel = self._get_channel(channel_id)
		channel.save(filename, format=format)

	# Audio Manipulation Methods

	def load(self, channel_id, filename):
		"""
		Loads an audio file into the specified channel, replacing any existing track.

		:param channel_id: The identifier for the channel (string or integer).
		:param filename: The path to the audio file to be loaded.
		"""
		self.from_file(channel_id, filename)

	def insert(self, channel_id, other_track: MT, offset_ms: int):
		"""
		Inserts another track into the specified channel at the given offset.

		:param channel_id: The identifier for the channel (string or integer).
		:param other_track: The MT instance to be inserted.
		:param offset_ms: The offset in milliseconds where the insertion should occur.
		"""
		channel = self._get_channel(channel_id)
		channel.insert(other_track, offset_ms)

	def append(self, channel_id, other_track: MT):
		"""
		Appends another track to the specified channel.

		:param channel_id: The identifier for the channel (string or integer).
		:param other_track: The MT instance to be appended.
		"""
		channel = self._get_channel(channel_id)
		channel.append(other_track)

	def overlay(self, channel_id, other_track: MT, offset_ms: int):
		"""
		Overlays another track onto the specified channel at the given offset.

		:param channel_id: The identifier for the channel (string or integer).
		:param other_track: The MT instance to overlay.
		:param offset_ms: The offset in milliseconds where the overlay should occur.
		"""
		channel = self._get_channel(channel_id)
		channel.overlay(other_track, offset_ms)

	def apply_gain(self, channel_id, gain_db: float):
		"""
		Applies gain to a specific channel.

		:param channel_id: The identifier for the channel (string or integer).
		:param gain_db: The gain in decibels (dB) to apply.
		"""
		# Update the stored gain
		current_gain = self.gains.get(channel_id, 0.0)
		new_gain = current_gain + gain_db
		self.gains[channel_id] = new_gain

	def apply_highpass(self, channel_id, cutoff_freq: float):
		"""
		Applies a highpass filter to a specific channel.

		:param channel_id: The identifier for the channel (string or integer).
		:param cutoff_freq: The cutoff frequency for the highpass filter in Hz.
		"""
		channel = self._get_channel(channel_id)
		channel.apply_highpass(cutoff_freq)

	def apply_lowpass(self, channel_id, cutoff_freq: float):
		"""
		Applies a lowpass filter to a specific channel.

		:param channel_id: The identifier for the channel (string or integer).
		:param cutoff_freq: The cutoff frequency for the lowpass filter in Hz.
		"""
		channel = self._get_channel(channel_id)
		channel.apply_lowpass(cutoff_freq)

	def apply_compressor(self, channel_id, threshold: float = -20.0, ratio: float = 4.0, attack: float = 5.0, release: float = 50.0):
		"""
		Applies a compressor effect to a specific channel.

		:param channel_id: The identifier for the channel (string or integer).
		:param threshold: The threshold in dB where compression starts.
		:param ratio: The compression ratio.
		:param attack: The attack time in milliseconds (how quickly the compressor starts).
		:param release: The release time in milliseconds (how quickly the compressor stops).
		"""
		channel = self._get_channel(channel_id)
		channel.apply_compressor(threshold, ratio, attack, release)

	def trim_silence(self, channel_id, silence_threshold=-50.0, chunk_size=10, start_silence=50, middle_silence=450, end_silence=250):
		"""
		Trims silence in a specific channel with customizable parameters.

		:param channel_id: The identifier for the channel (string or integer).
		:param silence_threshold: The dBFS threshold below which audio is considered silence.
		:param chunk_size: The size of the chunks (in milliseconds) used to scan for silence.
		:param start_silence: Max amount of silence to preserve at the beginning.
		:param middle_silence: Max amount of silence to preserve in the middle.
		:param end_silence: Max amount of silence to preserve at the end.
		"""
		channel = self._get_channel(channel_id)
		channel.trim_silence(silence_threshold, chunk_size, start_silence, middle_silence, end_silence)

	def apply_vst(self, channel_id, vst_name: str, preset_name: str):
		"""
		Applies a VST plugin to a specific channel.

		:param channel_id: The identifier for the channel (string or integer).
		:param vst_name: The name of the VST plugin to apply.
		:param preset_name: The preset name within the VST plugin to use.
		"""
		channel = self._get_channel(channel_id)
		channel.apply_vst(vst_name, preset_name)

	# Mixer Functionality

	def generate_mix(self) -> MT:
		"""
		Generates a mixed track from all channels, applying individual gains and the master gain.

		:return: An MT instance representing the mixed audio.
		"""
		if not self.channels:
			raise ValueError("No channels have been added to the MultiTrack.")

		mixer = MTMixer()

		for channel_id, track in self.channels.items():
			channel_gain = self.gains.get(channel_id, 0.0)
			effective_gain = channel_gain + self.master_gain  # Apply master gain to channel gain
			mixer.add_track(track, effective_gain)

		mixed = mixer.generate_mix()

		return mixed

	# Utility Methods

	def list_channels(self):
		"""
		Lists all active channel identifiers.

		:return: A list of channel identifiers.
		"""
		return list(self.channels.keys())

	def get_channel_length(self, channel_id) -> int:
		"""
		Retrieves the length of the specified channel in milliseconds.

		:param channel_id: The identifier for the channel (string or integer).
		:return: Length in milliseconds.
		"""
		channel = self._get_channel(channel_id)
		return channel.get_length_ms()

	def clamp_length(self, channel_id, max_length_ms: int):
		"""
		Clamps the length of the specified channel to a maximum duration.

		:param channel_id: The identifier for the channel (string or integer).
		:param max_length_ms: The maximum length in milliseconds.
		"""
		channel = self._get_channel(channel_id)
		channel.clamp_length(max_length_ms)

	def add_silence(self, channel_id, duration_ms: int):
		"""
		Adds silence to the end of the specified channel.

		:param channel_id: The identifier for the channel (string or integer).
		:param duration_ms: Duration of silence to add in milliseconds.
		"""
		channel = self._get_channel(channel_id)
		channel.add_silence(duration_ms)

	def fade_in(self, channel_id, duration: int):
		"""
		Applies a fade-in effect to the specified channel.

		:param channel_id: The identifier for the channel (string or integer).
		:param duration: Duration of the fade-in in milliseconds.
		"""
		channel = self._get_channel(channel_id)
		channel.fade_in(duration)

	def fade_out(self, channel_id, duration: int):
		"""
		Applies a fade-out effect to the specified channel.

		:param channel_id: The identifier for the channel (string or integer).
		:param duration: Duration of the fade-out in milliseconds.
		"""
		channel = self._get_channel(channel_id)
		channel.fade_out(duration)