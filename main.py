import os
from PIL import Image
from image_canvas import ImageCanvas
from saves_manager import SavesManager
import argparse
from argmanager import ArgManager
import config
from llm import LLM
import random
import prompts
import json
import requests
import time
import re
import random
from typing import List, Dict, Any
import data
from mt import MT
from replicateimage import ReplicateImage
from collections import deque
import html

# cut edges on inlay (overlay)
# better covers
# avoid dust motes etc.
# better music genres
# lyrics guidance per section - direct, question, repeat, etc.

def build_song_structure() -> List[Dict[str, Any]]:
    """
    Generates a random song structure as a list of sections.

    This function creates a song structure by randomly selecting the number
    of verses, the presence of optional sections like an intro, bridge, or
    solo, and the properties of each section. It ensures that repeated
    sections (verse, chorus, pre-chorus) are consistent in their line count.

    Returns:
        list: A list of dictionaries, where each dictionary represents a
              song section and contains its name, number of lines, and
              the determined line length ('short', 'medium', or 'long').
    """
    # --- 1. Define Section Possibilities ---
    SECTION_DEFS = {
        'intro': [0, 1, 2],
        'verse': [4, 6, 8],
        'pre-chorus': [2, 4],
        'chorus': [4, 8],
        'bridge': [2, 4, 8],
        'solo': [0],
        'interlude': [0],
        'outro': [2, 4]
    }
    LINE_LENGTHS = ['short', 'medium', 'long']
    song_structure = []

    # --- 2. Decide Core Song Parameters ---

    # Determine consistent line counts for repeated sections
    verse_lines = random.choice(SECTION_DEFS['verse'])
    chorus_lines = random.choice(SECTION_DEFS['chorus'])
    bridge_lines = random.choice(SECTION_DEFS['bridge']) # Determined early now
    pre_chorus_lines = random.choice(SECTION_DEFS['pre-chorus'])

    # Now, apply constraints using the simpler min() logic.
    if verse_lines == 8:
        chorus_lines = min(chorus_lines, 4)
        bridge_lines = min(bridge_lines, 4)
    elif chorus_lines == 8:
        bridge_lines = min(bridge_lines, 4)

    # First, decide which section type, if any, will have long lines.
    # We add multiple 'None' values to decrease the probability of a long section.
    sections_for_long_choice = list(SECTION_DEFS.keys()) + [None] * 6
    long_line_section = random.choice(sections_for_long_choice)

    # Now, assign lengths to all section types.
    section_line_lengths = {}
    for section_type in SECTION_DEFS:
        if section_type == long_line_section:
            section_line_lengths[section_type] = 'long'
        else:
            # All other sections can only be short or medium.
            section_line_lengths[section_type] = random.choice(['short', 'medium'])

    # Decide which optional sections to include and how many verses
    num_verses = random.randint(2, 3)
    if num_verses == 3:
        part1_verses = 2
        part2_verses = 1
    else:
        part1_verses = random.choice([ 2, 1 ])
        part2_verses = 2 - part1_verses

    has_intro = random.choice([True, False, False])
    has_pre_chorus = random.choice([True, False])
    has_bridge = random.choice([True, False, False, False])
    has_solo = random.choice([True, False, False, False, False, False])
    has_outro = random.choice([True, False, False])
    has_intro_chorus = False
    has_interlude = random.choice([True, False, False])

    if num_verses == 3:
        has_solo = False
        has_intro = False
        has_outro = False
        SECTION_DEFS['verse'] = 4
        SECTION_DEFS['pre-chorus'] = 2

    if part1_verses == 1 and part2_verses == 1:
        has_bridge = random.choice([True, True, False])
        has_interlude = random.choice([True, True, False])
        if has_bridge == False and has_interlude == False:
            has_bridge = True

    if num_verses == 2:
        has_intro_chorus = random.choice([True,False])
        if has_intro_chorus:
            has_intro = random.choice([True, False, False, False, False])

    # --- 3. Build the Song Structure Chronologically ---

    # Add Intro
    if has_intro:
        intro_lines = random.choice(SECTION_DEFS['intro'])
        if intro_lines > 0:
            song_structure.append({
                'section': 'intro',
                'lines': intro_lines,
                'line_length': section_line_lengths['intro']
            })

    # Intro chorus
    if has_intro_chorus:
        song_structure.append({
            'section': 'chorus', 'lines': chorus_lines,
            'line_length': section_line_lengths['chorus']
        })

    # Add Verse/Chorus Block 1
    song_structure.append({
        'section': 'verse', 'lines': verse_lines,
        'line_length': section_line_lengths['verse']
    })
    if has_pre_chorus:
        song_structure.append({
            'section': 'pre-chorus', 'lines': pre_chorus_lines,
            'line_length': section_line_lengths['pre-chorus']
        })
    song_structure.append({
        'section': 'chorus', 'lines': chorus_lines,
        'line_length': section_line_lengths['chorus']
    })

    # Add Verse/Chorus Block 2 (if applicable)
    if part1_verses >= 2:
        song_structure.append({
            'section': 'verse', 'lines': verse_lines,
            'line_length': section_line_lengths['verse']
        })
        if has_pre_chorus:
            song_structure.append({
                'section': 'pre-chorus', 'lines': pre_chorus_lines,
                'line_length': section_line_lengths['pre-chorus']
            })
        song_structure.append({
            'section': 'chorus', 'lines': chorus_lines,
            'line_length': section_line_lengths['chorus']
        })

    # Add Bridge and Solo (middle section)
    if has_bridge:
        song_structure.append({
            'section': 'bridge', 'lines': bridge_lines,
            'line_length': section_line_lengths['bridge']
        })
    if has_solo:
        song_structure.append({
            'section': 'solo', 'lines': 0,
            'line_length': section_line_lengths['solo']
        })

    if has_interlude:
        song_structure.append({
            'section': random.choice(["interlude", "break", "movement", "riff", "hook", "drop"]), 'lines': 0,
            'line_length': section_line_lengths['interlude']
        })        

    # Add Verse/Chorus Block 3 (if applicable)
    if part2_verses == 1:
        song_structure.append({
            'section': 'verse', 'lines': verse_lines,
            'line_length': section_line_lengths['verse']
        })
        if part1_verses == 1 and has_pre_chorus:
            song_structure.append({
                'section': 'pre-chorus', 'lines': pre_chorus_lines,
                'line_length': section_line_lengths['pre-chorus']
            })
        song_structure.append({
            'section': 'chorus', 'lines': chorus_lines,
            'line_length': section_line_lengths['chorus']
        })

    # Add Outro
    if has_outro:
        outro_lines = random.choice(SECTION_DEFS['outro'])
        if outro_lines > 0:
            song_structure.append({
                'section': 'outro', 'lines': outro_lines,
                'line_length': section_line_lengths['outro']
            })

    return song_structure

def jprint(j):
    print(json.dumps(j, indent=4))

def initialize_llm():
    llm_instance = LLM(default_model=config.DEFAULT_MODEL)
    llm_instance.init_openrouter(api_key=config.OPENROUTER_API_KEY)
    llm_instance.init_openai(organization=config.OPENAI_ORG, api_key=config.OPENAI_API_KEY)
    llm_instance.init_anthropic(api_key=config.ANTHROPIC_API_KEY)
    llm_instance.init_llamaai(api_key=config.LLAMAAI_API_KEY)
    
    return llm_instance

def truncate_by_word(input_string, max_length):
  """
  Removes words from the end of a string until its length is
  less than or equal to max_length.
  """
  if len(input_string) <= max_length:
    return input_string

  # Split the string into a list of words
  words = input_string.split()

  # Keep removing the last word as long as the string is too long
  while len(' '.join(words)) > max_length:
    words.pop() # .pop() removes the last item from a list

  # Join the remaining words back into a string
  return ' '.join(words)

def step_create_mixtape(force_regeneration, project, llm):
    if (not force_regeneration) and ("mixtape" in project.state):
        return True

    mixtape_type = ArgManager.get_arg("theme")
    if mixtape_type == None:
        mixtape_type = random.choice(prompts.mixtape_types)

    band_and_song_naming_guidelines = ""

    for i in range(1,11):
        band_and_song_naming_guidelines += f"Band #{i} name guideline: {random.choice(prompts.band_name_guides)}\n"
        band_and_song_naming_guidelines += f"Song #{i} name guideline: {random.choice(random.choice([prompts.song_name_guides_simple, prompts.song_name_guides]))}\n"

    q = prompts.mixtape_prompt.format(
            theme = mixtape_type,
            band_and_song_naming_guidelines = band_and_song_naming_guidelines)

    mixtape = llm.jquery(
        q,
        max_tokens = 8192, temperature = 1.0, model = config.DEFAULT_MODEL)

    print(mixtape_type)
    jprint(mixtape)

    mixtape["band_and_song_naming_guidelines"] = band_and_song_naming_guidelines

    # make sure genres are max 180 characters
    for song in mixtape["songs"]:
        if len(song["music_genre"]) > 180:
            print(f"""Truncating music genre for {song["song_name"]}""")
            song["music_genre"] = truncate_by_word(song["music_genre"], 180)

    project.state["mixtape_type"] = mixtape_type
    project.state["mixtape"] = mixtape
    project.save()

    return True

def step_create_song_structures(force_regeneration, project):
    for song in project.state["mixtape"]["songs"]:
        if force_regeneration or (not "structure" in song):
            print(f"""Creating song structure for {song["song_name"]}""")
            structure = build_song_structure()
#            jprint(structure)
            song["structure"] = structure
            project.save()

def truncate_by_line(input_string, max_length):
  """
  Removes lines from the end of a string until its total length
  is less than or equal to max_length.
  """
  if len(input_string) <= max_length:
    return input_string

  # Split the string into a list of lines
  lines = input_string.splitlines()

  # Keep removing the last line as long as the joined string is too long
  # We use '\n'.join() to correctly calculate the length with newlines
  while len('\n'.join(lines)) > max_length:
    lines.pop() # Removes the last item (line) from the list

  # Join the remaining lines back into a single string with newlines
  return '\n'.join(lines)

def step_create_lyrics(force_regeneration, project, llm):
    for song in project.state["mixtape"]["songs"]:
        if force_regeneration or (not "lyrics" in song):
            print(f"""Creating lyrics for {song["song_name"]}""")
            structure = ""
            lyrics_sections_guidance = {}
            for section in song["structure"]:
                section_type = section["section"]
                structure += f"""[{section_type}]\n"""
                structure += f"""- {section["lines"]} lines of {section["line_length"]} length.\n"""

                if section_type not in lyrics_sections_guidance:
#                    print("section_type: " + section_type)
                    if section_type in prompts.lyrics_guides:
#                        print("found in guidance")
                        lyrics_sections_guidance[section_type] = random.choice(prompts.lyrics_guides[section_type]).format(
                            num_lines = section["lines"])

            lyrics_guidance = ""
            for section_type, guidance in lyrics_sections_guidance.items():
                lyrics_guidance += f"{section_type}: {guidance}\n"

            song["lyrics_guidance"] = lyrics_guidance

            messages = []

            messages.append({"role": "user", "content": prompts.lyrics_prethink_prompt.format(
                theme = project.state["mixtape_type"],
                song_name = song["song_name"],
                music_genre = song["music_genre"],
                vocals_style = song["vocals_style"] + (" ensemble" if song.get("is_ensemble", False) else ""),
                lyrics_description = song["lyrics_description"],
                lyrics_guidance = song["lyrics_guidance"],
                structure = structure
                )})

            lyrics_prethink = llm.query_messages(messages, max_tokens = 8192, temperature = 1.0, model = config.DEFAULT_MODEL)

            messages.append({"role":"assistant", "content": lyrics_prethink})

            messages.append({"role": "user", "content": prompts.lyrics_prompt.format(
                theme = project.state["mixtape_type"],
                song_name = song["song_name"],
                music_genre = song["music_genre"],
                vocals_style = song["vocals_style"] + (" ensemble" if song.get("is_ensemble", False) else ""),
                lyrics_description = song["lyrics_description"],
                lyrics_guidance = song["lyrics_guidance"],
                structure = structure
                )})

            lyrics = llm.query_messages(messages, max_tokens = 8192, temperature = 1.0, model = config.DEFAULT_MODEL)

            messages.append({"role":"assistant", "content": lyrics})

#            jprint(messages)

#            lyrics = llm.query(prompts.lyrics_prompt.format(
#                theme = project.state["mixtape_type"],
#                song_name = song["song_name"],
#                music_genre = song["music_genre"],
#                vocals_style = song["vocals_style"],
#                lyrics_description = song["lyrics_description"],
#                structure = structure
#                ))
#            print(lyrics)

            if len(lyrics) > 3000:
                print(f"""Truncating lyrics for {song["song_name"]}""")
                song["non_truncated_lyrics"] = lyrics
                lyrics = truncate_by_line(lyrics)

            song["lyrics"] = lyrics
            project.save()

BASE_URL = "https://api.sunoapi.com/api/v1/suno"

def submit_suno_job(title, style, lyrics=""):
    url = f"{BASE_URL}/create"
    headers = {
        'Authorization': f'Bearer {config.SUNO_API_KEY}',
        'Content-Type': 'application/json'
    }
    payload = {
        "custom_mode": True,
        "prompt": lyrics,
        "tags": style,
        "title": title,
        "mv": "chirp-v4-5-plus" # Using the latest model as per API docs
    }

    try:
        print(f"Submitting job for '{title}'...")
#        jprint(headers)
#        jprint(payload)
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=30)
        response.raise_for_status()
        result = response.json()
        print(f"-> Job submission successful. Task ID: {result.get('task_id')}")
        return result.get('task_id')
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"Status Code: {http_err.response.status_code}")
        print("Response Body:", http_err.response.text)
        if http_err.response.status_code == 401:
            print("\nACTION REQUIRED: Your 'SUNO_API_KEY' is invalid or has expired.")
        return None
    except Exception as err:
        print(f"An other error occurred during job submission: {err}")
        return None

def poll_suno_job_status(task_id):
    url = f"{BASE_URL}/task/{task_id}"
    headers = {'Authorization': f'Bearer {config.SUNO_API_KEY}'}

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()

#        jprint(data)        

        message = "succeeded"

        for song in data["data"]:
            state = song.get("state", "pending")
            if state != "succeeded":
                message = state

        if len(data["data"]) < 1:
            message = "pending"

        if message == 'succeeded':
            return data.get('data', {}) # Contains the 'clips' array
        elif message in [ "pending", "running" ]:
            return 'processing'
        else:
            print(f"Job failed with status: {data['status']}. Reason: {data.get('error_message', 'Unknown')}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while polling job {task_id}: {e}")
        return None

def download_suno_clip(clip_data, folder, title_prefix):
    """
    Downloads a single clip using the audio_url from the API response.
    Returns the clip_id on success, None on failure.
    """
    clip_id = clip_data.get('clip_id')
    download_url = clip_data.get('audio_url')

    if not download_url:
        print(f"No audio URL found for clip ID {clip_id}.")
        return None

    try:
        response = requests.get(download_url, stream=True, timeout=60)
        response.raise_for_status()

        # Create a unique, safe filename
        filename = f"saves/{folder}/{clip_id}.mp3"
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"✅ Downloaded '{title_prefix}' (Clip ID: {clip_id})")
        return clip_id
    except requests.exceptions.RequestException as e:
        print(f"Error downloading clip {clip_id}: {e}")
        return None

def step_create_audio_simple_poll(force_regeneration, project, max_in_flight=10, poll_interval=30):
    songs_to_create = deque([
        s for s in project.state["mixtape"]["songs"] if (force_regeneration or (not s.get("song_ids")))
    ])
    # Tracks jobs submitted to the API but not yet complete.
    # Format: { 'task_id': {'title': 'Song Title', 'song_ref': song} }
    in_flight_jobs = {}

    if not songs_to_create:
        return

    print(f"Starting API-based polling process for '{project.name}'.")
    print(f" Max in-flight jobs: {max_in_flight} | Poll Interval: {poll_interval}s")

    while songs_to_create or in_flight_jobs:
        # A temporary list to hold songs that fail to submit in this pass
        submissions_to_retry = []

        # 1. Queue new jobs up to the concurrent limit
        while len(in_flight_jobs) < max_in_flight and songs_to_create:
            song = songs_to_create.popleft()
            title = song["song_name"]
            ensemble = " ensemble" if song.get("is_ensemble", False) else ""
            style = f"{song['music_genre']}, {song['vocals_style']}{ensemble} vocals"
            lyrics = song["lyrics"]

            task_id = submit_suno_job(title, style, lyrics)
            if task_id:
                in_flight_jobs[task_id] = {'title': title, 'song_ref': song}
            else:
                print(f"Failed to submit '{title}'. It will be retried in the next cycle.")
                # Add to the temporary retry list instead of the main queue
                submissions_to_retry.append(song)

        # After attempting to fill the queue, add the failed songs back for the next outer loop iteration
        if submissions_to_retry:
            songs_to_create.extend(submissions_to_retry)

        if not in_flight_jobs:
            if not songs_to_create: break
            time.sleep(poll_interval)
            continue

        # 2. Poll all in-flight jobs
        print(f"\n---\nPolling {len(in_flight_jobs)} in-flight job(s)...")
        completed_tasks = []
        for task_id, job_data in in_flight_jobs.items():
            title = job_data['title']
            print(f"Checking status for: '{title}' (Task ID: {task_id})")
            poll_result = poll_suno_job_status(task_id)

            if poll_result == 'processing':
                print(f"-> Status: Still processing.")
                continue

            if poll_result:  # Success: poll_result contains the final object with clips
                print(f"-> Status: Success! Job for '{title}' is complete. Downloading clips...")
                clips = poll_result
                downloaded_clip_ids = []

                for clip in clips:
                    # Pass clip data, project folder, and title for logging
                    downloaded_id = download_suno_clip(clip, project.name, title)
                    if downloaded_id:
                        downloaded_clip_ids.append(downloaded_id)

                song_to_update = job_data['song_ref']
                song_to_update['song_ids'] = downloaded_clip_ids
                project.save()
                print(f"-> Progress for '{title}' saved.")
                completed_tasks.append(task_id)

            else:  # Failure: poll_result is None
                print(f"-> Status: Failed. Job for '{title}' (Task ID: {task_id}) could not be completed.")
                completed_tasks.append(task_id)

        # 3. Clean up completed/failed jobs from the in_flight list
        for task_id in completed_tasks:
            if task_id in in_flight_jobs:
                del in_flight_jobs[task_id]

        # 4. Wait before the next cycle
        if songs_to_create or in_flight_jobs:
            print(f"\n...Cycle complete. Waiting {poll_interval} seconds...\n")
            time.sleep(poll_interval)

    print(f"\nAll songs for project '{project.name}' have been processed.")

def rune_make_suno_request(title, style, lyrics=""):
  url = "https://studio-api.prod.suno.com/api/generate/v2-web/"

  headers = {
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.9,da;q=0.8',
    'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsImNhdCI6ImNsX0I3ZDRQRDExMUFBQSIsImtpZCI6Imluc18yT1o2eU1EZzhscWRKRWloMXJvemY4T3ptZG4iLCJ0eXAiOiJKV1QifQ.eyJhdWQiOiJzdW5vLWFwaSIsImF6cCI6Imh0dHBzOi8vc3Vuby5jb20iLCJleHAiOjE3NTQwNjg5NDksImZ2YSI6Wzk5OTk5LC0xXSwiaHR0cHM6Ly9zdW5vLmFpL2NsYWltcy9jbGVya19pZCI6InVzZXJfMllkN0xLVm9wNWQ4V1JJYWJISVU3aHI1M2RSIiwiaHR0cHM6Ly9zdW5vLmFpL2NsYWltcy9lbWFpbCI6InJ2ZW5kbGVyQGdtYWlsLmNvbSIsImh0dHBzOi8vc3Vuby5haS9jbGFpbXMvcGhvbmUiOm51bGwsImlhdCI6MTc1NDA2NTM0OSwiaXNzIjoiaHR0cHM6Ly9jbGVyay5zdW5vLmNvbSIsImp0aSI6IjhiOGQyZDVkMTA4YzE2ZGJmM2U2IiwibmJmIjoxNzU0MDY1MzM5LCJzaWQiOiJzZXNzXzJ1WE5tc0ZNOHZ1dXUzM0NrRm9uSVpGVm5sTiIsInN1YiI6InVzZXJfMllkN0xLVm9wNWQ4V1JJYWJISVU3aHI1M2RSIn0.B7btZhnPr6K4fJ326y5k50qvhm9BOBqjyn0XO7CR4mNPKjLEL7gr2l7ws-gkMV3uTRO5LsGBoyJZeJMOtgo2TmSSYXPmS8od7oXkJkCOINjA_UqhM6kvdYDgjZ8lVf2CPUrEEmXF2tcuuVoG4uNBYeruz4Q-umFEJeBWDXbitYQmAJLHcNPvCT9Ifdi1jkfT159l9RNAvshiVKyKkAXgyml8to0v7Utz536KJ4mPNCT2p5PYeHHbFVTGgzm5jQj-IrcKUmGw4iIWd9RR-7cJk5Zcnauu014Yg-cvfxv1Uviw6zkPvQ1xRRGtOsFKa_rXPfnExHvXPgbDOsYObeNQ8Q',
    'Content-Type': 'text/plain;charset=UTF-8',
    'Origin': 'https://suno.com',
    'Referer': 'https://suno.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'
  }

  # The full payload from your request, including the long token
  payload = {
    "token": "P1_eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.haJwZACjZXhwzmiM6j6ncGFzc2tlecUErThSwgitgIVVzCR6KAA9xQ-btL5jESYw80GJ3aDN3ByzWdwoAriB-x218Pu4GQ1SCCBQ05jv5i29tqv1QgCWtIvWBLx6moP0yk4c6KpRQR-2kHAF_sofdMvUhS9W1VdYTiWojic6u_zSK8FtvxW7z33bevS0DH0EzF7CxKY4e6872n8QyOnH0xjmsyksWs0qlYzNHEArcsae10KeLQeQfr5wlTnSZ_ncWGxZu6Qde7l_sCrbwlNaG7ISDY5p6BCKflzDxsDnWiiriLNKxrXAamWPlEQ5EknkoLVRwtMj68I-aKxgEKq5uOgRF5mnw6ApL9ug7yqCydLd-PE8llcUVAi6Up6TntLmW568i-a1RKswfa3anALKFQNggpNQTq_0A0b6ybA2vpJ-mRKEYGWnY8AlszmixxTdVTDrnU8M1Ck3VcW_gG1qEYfFP76QWsb-DXmBLLs_Y6fBQijg6KGKvYxIJ43-GEw8nyaSXeUFkrU1mzg_PINSlTZs5-AxQRilv08bGSvmcm60xD7pfzTJM8q9HIPrk9DkgtrWPhERrq8SkGR63moV8LWdG5stfY4oeWwRU3ceckCT82gksS10P4fhNf3RdCqFrVGuPUBQPkA1ez-a2zhc4TJEXUz-j1dJtrvyNAjAMWUvGZrlq0bSv9yA2E3Y81ec93cssFenTLQmQ4pgQQcS_3JsZUpROTzwW0KLBxRfZl5-F7WQWRTcsNEdquVD24spNgUoFfFAjthh3hbZxTdZo82xyiAP6ka_AbdAnQAUq8-tvjYuzaMsscinBPCp6fsXeGBfq9nW8sD6rqbQVUcCUwl6Fr8NDTInWrmuccx7vOKnRbhpkm23g47mwz3909dtVbLuqgytHqQt9oTPM_TYy-OsnXmpyUfswcj1e9TWtCNHxr8Pz8p31PFJ18zC92d-B9UjcM7Nl5JhF5p-V_r0ESYcVsL7Q3JnfTLvQ0dE3h3DyWXthY2fK1EuDPTCjRQuzd3u7TPpul12-XrRe4ENKLyVxc1U5RTKkcAqCI5tK6M4iDUK6-4Fv1M9mtLdjYpeJxo5Rz_lwRNKlrHWt5d_Pduh4lK3IGyvdLe_OVLCNFqzXzfVlXsr1GTFp6foxZ9GT0Jm6Ee9E12vzksrYUO2EHe_d3ab5W6V2-d2PqIJ_oNASdrxxpaagDvBKb20-Ep3r1g7AYRVNI4XYxhnknRsPdfh9P3pB390l-Kn7jnyyqK3NMuGJxUDmEJtkDrpR4RkfqC3YqGEKb5A5zAGYQx8Xfzw28dhku3Rq0E-M4729Ekz9ijnYCdp5gQ3voKsmY45WuP_yhx5S6FwdXJCAwypcY-5fZjHAQ0FQ_cd63OQmMisMrmdjQf7qDIX3UDG4pCv-bAqIhyVDX2rX3cX4pczmVAtP1z1sFQ2S-ezrTFvzRS_wkdmDG11wJLelEckz9tBeMilo-MipSz03Iq14I5iQOe2XKCwIVMxdLV8KKJtBurYN7F35j1edE2BY665cfBZz5G-OrRpgy1cz0GzVicyyqKaWyFaEX05x8yBl4wFmEi2Ij7H1_9GZRGAgertGUCKSseaT_Ecgh_K6or8mTe5x8EvE2com6Jrcqc1Nzk3Y2RmqHNoYXJkX2lkzhQ8hB8.rSqTeaKfOoRAJ76oNE_zoDQ36mkthYwB-SyFXewzd1E",
    "prompt": lyrics,
    "generation_type": "TEXT",
    "tags": style,
    "negative_tags": "",
    "mv": "chirp-bluejay",
    "title": title,
    "continue_clip_id": None,
    "continue_at": 0,
    "continued_aligned_prompt": None,
    "infill_start_s": None,
    "infill_end_s": None,
    "task": None,
    "override_fields": ["prompt", "tags"],
    "persona_id": None,
    "playlist_clip_ids": [],
    "underpainting_start_s": None,
    "underpainting_end_s": None,
    "overpainting_start_s": None,
    "overpainting_end_s": None,
    "artist_clip_id": None,
    "artist_start_s": None,
    "artist_end_s": None,
    "cover_clip_id": None,
    "metadata": {
      "create_mode": "custom",
      "user_tier": "3eaebef3-ef46-446a-931c-3d50cd1514f1",
      "lyrics_model": "remi-v1",
      "create_session_token": "336ee657-8fa6-46b5-96d9-bc66acfd05e9",
      "can_control_sliders": ["weirdness_constraint", "style_weight"]
    }
  }

  try:
    print("STEP 1: Sending generation request to Suno API...")
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()
    print(f"Request successful with Status Code: {response.status_code}")
#    jprint(response.json())
    return response.json()
  except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
    print(f"Status Code: {http_err.response.status_code}")
    print("Response Body:", http_err.response.text)
    print("\nACTION REQUIRED: Your 'Authorization' token is likely expired. Please follow the instructions in the script to update it.")
    return None
  except Exception as err:
    print(f"❌ An other error occurred: {err}")
    return None

def rune_download_clips(clips_data, folder):
  print("\nSTEP 2: Starting download process for generated clips...")
  clips_to_download = list(clips_data)
 
  while clips_to_download:
    wait_time = 30
    print(f"\n---\nWaiting {wait_time} seconds before trying {len(clips_to_download)} remaining clip(s)...\n---")
    time.sleep(wait_time)

    # Create a copy to iterate over, allowing us to safely remove items from the original list
    for clip in list(clips_to_download):
      clip_id = clip.get('id')
      clip_title = clip.get('title', 'untitled')
      download_url = f"https://cdn1.suno.ai/{clip_id}.mp3"
     
      print(f"\nAttempting to download: '{clip_title}' (ID: {clip_id})")
     
      try:
        response = requests.get(download_url, stream=True)
        if response.status_code == 200:
          # Sanitize the title to create a valid filename
          # Removes illegal characters and strips trailing spaces/underscores
          safe_title = re.sub(r'[\\/*?:"<>|]', "", clip_title).strip()
          filename = f"saves/{folder}/{clip_id}.mp3"
         
          with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
              f.write(chunk)
         
          print(f"Successfully downloaded and saved as '{filename}'")
          clips_to_download.remove(clip) # Remove from list after success
        elif response.status_code == 404:
          print(f"Clip not ready yet (Status: 404 Not Found). Will retry.")
        else:
          print(f" Download failed with status {response.status_code}. Will retry.")
      except requests.exceptions.RequestException as e:
        print(f"An error occurred during download attempt: {e}. Will retry.")

def rune_step_create_audio(force_regeneration, project):
  for song in project.state["mixtape"]["songs"]:
    if force_regeneration or (not "song_ids" in song):
      clips_data = rune_make_suno_request(song["song_name"], song["music_genre"] + ", " + song["vocals_style"] + (" ensemble" if song.get("is_ensemble", False) else "") + " vocals", song["lyrics"])

      if clips_data and 'clips' in clips_data:
        clips = clips_data.get('clips', [])
        if not clips:
          print("Request was successful, but no clips were returned in the response.")
        else:
          rune_download_clips(clips, project.name)
          song["song_ids"] = []
          for clip in clips:
            song["song_ids"].append(clip.get('id'))
          project.save()

def rune_attempt_download_clip(clip_id, title, folder):
  """Attempts to download a single clip and returns True on success."""
  download_url = f"https://cdn1.suno.ai/{clip_id}.mp3"
  try:
    response = requests.get(download_url, stream=True, timeout=30)
    if response.status_code == 200:
      filename = f"saves/{folder}/{clip_id}.mp3"
      os.makedirs(os.path.dirname(filename), exist_ok=True)
      with open(filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
          f.write(chunk)
      print(f"✅ Downloaded '{title}'")
      return True
    return False
  except requests.exceptions.RequestException:
    return False

def rune_step_create_audio_simple_poll(force_regeneration, project, max_in_flight=5, poll_interval=60):
  songs_to_create = deque([
    s for s in project.state["mixtape"]["songs"] if (force_regeneration or (not s.get("song_ids")))
  ])
  # Tracks songs submitted to the API but not yet fully downloaded.
  # Format: { 'song_name': {'clip_ids': {'id1', 'id2'}, 'song_ref': song} }
  in_flight_jobs = {}

  if not songs_to_create:
    return

  print(f"Starting simple polling process for '{project.name}'.")
  print(f" Max in-flight jobs: {max_in_flight} | Poll Interval: {poll_interval}s")

  while songs_to_create or in_flight_jobs:
   
    # 1. Queue new requests until the flight limit is reached
    while len(in_flight_jobs) < max_in_flight and songs_to_create:
      song = songs_to_create.popleft()
      title = song["song_name"]
     
      print(f"\n Submitting request for: '{title}'")
      ensemble = " ensemble" if song.get("is_ensemble", False) else ""
      response_data = rune_make_suno_request(title, f"{song['music_genre']}, {song['vocals_style']}{ensemble} vocals", song["lyrics"])

      if response_data and response_data.get('clips'):
        print(f" Request for '{title}' is in flight.")
        clips = response_data.get('clips', [])
        in_flight_jobs[title] = {
          'pending_clips': {c['id'] for c in clips},
          'all_clip_ids': {c['id'] for c in clips}, # Keep original set for saving
          'song_ref': song
        }
      else:
        print(f"Failed to submit '{title}'. Placing at the end of the queue.")
        songs_to_create.append(song)
        time.sleep(3) # Small delay after a failure

    # 2. Poll all clips for all in-flight jobs
    if not in_flight_jobs:
      if not songs_to_create: break # All done
      print("No jobs in flight. Looping to check queue.")
      continue
     
    print(f"\nPolling {len(in_flight_jobs)} in-flight job(s)...")
    downloaded_this_cycle = []
    for job_name, job_data in in_flight_jobs.items():
      # Use a copy for safe iteration while removing items
      for clip_id in list(job_data['pending_clips']):
        if rune_attempt_download_clip(clip_id, job_name, project.name):
          downloaded_this_cycle.append((job_name, clip_id))
          job_data['pending_clips'].remove(clip_id)
   
    # 3. Finalize any jobs where all clips have been downloaded
    completed_jobs = []
    for job_name, job_data in in_flight_jobs.items():
      if not job_data['pending_clips']: # Set is empty, job is done
        print(f"Job Complete: '{job_name}'")
        song_to_update = job_data['song_ref']
        song_to_update['song_ids'] = list(job_data['all_clip_ids'])
        project.save()
        print(f" Progress for '{job_name}' saved.")
        completed_jobs.append(job_name)

    # Clean up the in_flight list
    for job_name in completed_jobs:
      del in_flight_jobs[job_name]

    # 4. Sleep before the next cycle
    if songs_to_create or in_flight_jobs:
      print(f"\n...Cycle complete. Waiting {poll_interval} seconds...")
      time.sleep(poll_interval)
     
  print(f"\nAll songs for project '{project.name}' have been processed.")

def step_apply_tape_vst(force_regeneration, project):
    for song in project.state["mixtape"]["songs"]:
        if force_regeneration or (not "vst_processed" in song):
            vst_preset = random.choice(data.daw_presets)
            print(f"""Applying tape effects ({vst_preset}) for {song["song_name"]}""")
            song_id = song["song_ids"][0]
            mt_song = MT.from_file(f"saves/{project.name}/{song_id}.mp3")
            mt_song.apply_vst("DAWCassette", vst_preset)
            mt_song.save(f"saves/{project.name}/{song_id}-tape.mp3", "mp3")
            song["vst_processed"] = True
            song["vst_preset"] = vst_preset
            project.save()

def step_create_cover_image(force_regeneration, project, replicate_client):
    if force_regeneration or (not "cover_created" in project.state["mixtape"]):
        print(f"""Creating cover image""")
        replicate_client.generate_image(
            output_path=f"saves/{project.name}/cover.png",
            prompt=project.state["mixtape"]["illustration"],
            aspect="2:3",
            prompt_upsampling=False,
            model="google/imagen-4",
            seed=None)
        project.state["mixtape"]["cover_created"] = True
        project.save()

def step_process_cover_image(force_regeneration, project):
    if force_regeneration or (not "cover_processed" in project.state["mixtape"]):
        print(f"""Processing cover image""")
        cover_input_filename = f"saves/{project.name}/cover.png"
        cover_output_filename = f"saves/{project.name}/cover-processed.png"
        composite_output_filename = f"saves/{project.name}/cover-composited.png"

        canvas = ImageCanvas.from_file(cover_input_filename)
        if not canvas:
            print(f"Fatal: Could not load base image from {cover_input_filename}. Aborting.")
            return

        target_size = canvas.size

        layers = []

        if random.random() < 0.85:
            texture = random.choice([
                "assets/scratches_1.png",
                "assets/scratches_2.png",
                "assets/scratches_3.png",
                "assets/scratches_4.png",
                "assets/scratches_5.png",
                "assets/scratches_6.png",
                ])
            layers.append( { "file": texture, "mode": "lighten" })

        if random.random() < 0.65:
            texture = random.choice([
                "assets/dirt_1.png",
                "assets/dirt_2.png",
                "assets/dirt_3.png",
                "assets/dirt_4.png",
                ])
            layers.append( { "file": texture, "mode": "alpha" })

        if random.random() < 0.35:
            texture = random.choice([
                "assets/grime_1.png",
                "assets/grime_2.png",
                "assets/grime_3.png",
                "assets/grime_4.png",
                "assets/grime_5.png",
                ])
            layers.append( { "file": texture, "mode": "darken" })

        for layer_info in layers:
            layer_path = layer_info["file"]
            layer_mode = layer_info["mode"]
            
            layer_canvas = ImageCanvas.from_file(layer_path)
            if layer_canvas:
                canvas.blit(layer_canvas, pos=(0, 0), new_size=target_size, mode=layer_mode)
            else:
                print(f"Warning: Could not load layer image {layer_path}. Skipping.")

        canvas.save(cover_output_filename)

        scaled_canvas = canvas.rescale((391,590))
        composite_canvas_below = ImageCanvas.from_file("assets/cassette_below.png")
        composite_canvas_above = ImageCanvas.from_file("assets/cassette_above.png")
        composite_canvas_below.blit(scaled_canvas, pos=(33,40), mode="opaque")
        composite_canvas_below.blit(composite_canvas_above, pos=(0,0), mode="lighten")
        composite_canvas_below.save(composite_output_filename)

        project.state["mixtape"]["cover_processed"] = True
        project.save()

def clean_lyrics(lyrics_text):
    """
    Cleans a string of lyrics by trimming whitespace, removing metadata lines,
    and collapsing multiple empty lines into a single empty line.
    """
    # 1) Trim whitespace from the start and end of the entire string
    trimmed_text = lyrics_text.strip()
    lines = trimmed_text.split('\n')
    cleaned_lines = []

    for line in lines:
        # Also trim each individual line
        stripped_line = line.strip()

        # Skip lines that start with [ or ( (e.g., [Chorus])
        if stripped_line.startswith('['): # or stripped_line.startswith('('):
            continue

        # 2) Reduce contiguous empty lines to a single empty line
        if not stripped_line:
            # Only add an empty line if the last line wasn't also empty
            if cleaned_lines and cleaned_lines[-1] == "":
                continue
            else:
                cleaned_lines.append("")
        else:
            # It's a content line, so add the stripped version
            cleaned_lines.append(stripped_line)

    return '\n'.join(cleaned_lines)

def step_create_webpage(force_regeneration, project):
    if force_regeneration or (not "webpage_created" in project.state["mixtape"]):
        print(f"""Creating webpage""")
        playlist = ""
        song_1_name = None
        song_1_url = None
        song_index = 1

        lyrics = {}

        for song in project.state["mixtape"]["songs"]:
            song_name = song["band_name"] + " - " + song["song_name"]
            song_url = song["song_ids"][0]+"-tape.mp3"
            song_lyrics = song["lyrics"]
            if not song_1_name:
                song_1_name = song_name
                song_1_url = song_url
            playlist += f"""<div class="track active" data-src="{song_url}">
                        <span class="track-number">{song_index}.</span>
                        <span class="track-title">{html.escape(song_name)}</span>
                    </div>"""
            lyrics[song_name] = clean_lyrics(song_lyrics)
            song_index += 1

        page = data.page_template.format(
            cover_url = "cover-composited.png",
            mixtape_name = html.escape(project.state["mixtape"]["title"]),
            playlist = playlist,
            song_1_name = html.escape(song_1_name),
            song_1_url = song_1_url,
            quote = html.escape(project.state["mixtape"]["backstory"]),
            lyrics = json.dumps(lyrics)
            )
        with open(f"saves/{project.name}/page.html", "w", encoding="utf-8") as text_file:
            text_file.write(page)
        project.state["mixtape"]["webpage_created"] = True
        project.save()

def main(force_regeneration):
    """
    Loads a base image and applies several layers with different
    blending modes, then saves the result.
    """
    llm = initialize_llm()
    replicate_client = ReplicateImage(config.REPLICATE_API_TOKEN)

    project = SavesManager(ArgManager.get_arg("project"), False)

    step_1 = (ArgManager.get_arg("step1") == True)
    step_2 = (ArgManager.get_arg("step2") == True)
    step_3 = (ArgManager.get_arg("step3") == True)
    step_4 = (ArgManager.get_arg("step4") == True)
    step_5 = (ArgManager.get_arg("step5") == True)
    step_6 = (ArgManager.get_arg("step6") == True)
    step_7 = (ArgManager.get_arg("step7") == True)
    step_8 = (ArgManager.get_arg("step8") == True)

    step_all = (ArgManager.get_arg("stepall") == True)

    if step_4:
         # if new audio, we must run audio processing and webpage (new guids)
        step_5 = True
        step_8 = True

    if step_6:
         # if new image, we must run image processing
        step_7 = True

    # do it
    if step_1 or step_all:
        step_create_mixtape(force_regeneration, project, llm)

    if step_2 or step_all:
        step_create_song_structures(force_regeneration, project)

    if step_3 or step_all:
        step_create_lyrics(force_regeneration, project, llm)

    if step_4 or step_all:
        step_create_audio_simple_poll(force_regeneration, project)
#        rune_step_create_audio_simple_poll(force_regeneration, project)

    if step_5 or step_all:
        step_apply_tape_vst(force_regeneration, project)

    if step_6 or step_all:
        step_create_cover_image(force_regeneration, project, replicate_client)

    if step_7 or step_all:
        step_process_cover_image(force_regeneration, project)

    if step_8 or step_all:
        step_create_webpage(force_regeneration, project)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mixtapes")
    parser.add_argument("-p", "--project",type=str,help="Project name")
    parser.add_argument("-t", "--theme",type=str,help="Mixtape theme")
    parser.add_argument("-f", "--force",   action="store_true",help="Force regeneration")
    parser.add_argument("-s1", "--step1",  action="store_true", help="Perform step 1 (concept)")
    parser.add_argument("-s2", "--step2",  action="store_true", help="Perform step 2 (song structures)")
    parser.add_argument("-s3", "--step3",  action="store_true", help="Perform step 3 (lyrics)")
    parser.add_argument("-s4", "--step4",  action="store_true", help="Perform step 4 (audio generation)")
    parser.add_argument("-s5", "--step5",  action="store_true", help="Perform step 5 (audio processing)")
    parser.add_argument("-s6", "--step6",  action="store_true", help="Perform step 6 (image generation)")
    parser.add_argument("-s7", "--step7",  action="store_true", help="Perform step 7 (image processing)")
    parser.add_argument("-s8", "--step8",  action="store_true", help="Perform step 8 (webpage generation)")
    parser.add_argument("-sa", "--stepall",action="store_true", help="Perform all steps")
    args = parser.parse_args()
    
    try:
        ArgManager.init(args)
    except (RuntimeError, TypeError) as e:
        print(f"Failed to initialize ArgManager: {e}")
        sys.exit(1) # Exit if initialization fails
    
#    print(submit_suno_job("Test for marsZ", "Happy pop punk", lyrics="[verse]\nThis is a test\n\n[chorus]Test, test, test"))

    if ArgManager.get_arg("project") == None:
        print("project not specified")
        exit(1)
    
    force_regeneration = (ArgManager.get_arg("force") == True)

    main(force_regeneration)
