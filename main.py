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
        'outro': [2, 4]
    }
    LINE_LENGTHS = ['short', 'medium', 'long']
    song_structure = []

    # --- 2. Decide Core Song Parameters ---

    # Determine consistent line counts for repeated sections
    verse_lines = random.choice(SECTION_DEFS['verse'])
    chorus_lines = random.choice(SECTION_DEFS['chorus'])
    pre_chorus_lines = random.choice(SECTION_DEFS['pre-chorus'])

    # Determine a line length for each type of section
    section_line_lengths = {
        section: random.choice(LINE_LENGTHS) for section in SECTION_DEFS
    }

    # Decide which optional sections to include and how many verses
    num_verses = random.randint(2, 3)
    has_intro = random.choice([True, False, False])
    has_pre_chorus = random.choice([True, False])
    has_bridge = random.choice([True, False, False, False])
    has_solo = random.choice([True, False, False, False, False, False])
    has_outro = random.choice([True, False, False])

    if num_verses == 3:
        has_solo = False
        has_intro = False
        has_outro = False
        SECTION_DEFS['verse'] = 4
        SECTION_DEFS['pre-chorus'] = 2

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
    if num_verses >= 2:
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
        bridge_lines = random.choice(SECTION_DEFS['bridge'])
        song_structure.append({
            'section': 'bridge', 'lines': bridge_lines,
            'line_length': section_line_lengths['bridge']
        })
    if has_solo:
        song_structure.append({
            'section': 'solo', 'lines': 0,
            'line_length': section_line_lengths['solo']
        })

    # Add Verse/Chorus Block 3 (if applicable)
    if num_verses == 3:
        song_structure.append({
            'section': 'verse', 'lines': verse_lines,
            'line_length': section_line_lengths['verse']
        })
#        if has_pre_chorus:
#            song_structure.append({
#                'section': 'pre-chorus', 'lines': pre_chorus_lines,
#                'line_length': section_line_lengths['pre-chorus']
#            })
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

def step_create_mixtape(project, llm):
    if "mixtape" in project.state:
        return True

    mixtape_type = ArgManager.get_arg("theme")
    if mixtape_type == None:
        mixtape_type = random.choice(prompts.mixtape_types)

    mixtape = llm.jquery(prompts.mixtape_prompt.format(theme = mixtape_type), max_tokens = 8192, temperature = 1.0, model = config.DEFAULT_MODEL)

    print(mixtape_type)
    jprint(mixtape)

    project.state["mixtape_type"] = mixtape_type
    project.state["mixtape"] = mixtape
    project.save()

    return True

def step_create_song_structures(project):
    for song in project.state["mixtape"]["songs"]:
        if not "structure" in song:
            structure = build_song_structure()
            jprint(structure)
            song["structure"] = structure
            project.save()

def step_create_lyrics(project, llm):
    for song in project.state["mixtape"]["songs"]:
        if not "lyrics" in song:
            structure = ""
            for section in song["structure"]:
                structure += f"""[{section["section"]}]\n"""
                structure += f"""- {section["lines"]} lines of {section["line_length"]} length.\n"""

            messages = []

            messages.append({"role": "user", "content": prompts.lyrics_prethink_prompt.format(
                theme = project.state["mixtape_type"],
                song_name = song["song_name"],
                music_genre = song["music_genre"],
                vocals_style = song["vocals_style"],
                lyrics_description = song["lyrics_description"],
                structure = structure
                )})

            lyrics_prethink = llm.query_messages(messages, max_tokens = 8192, temperature = 1.0, model = config.DEFAULT_MODEL)

            messages.append({"role":"assistant", "content": lyrics_prethink})

            messages.append({"role": "user", "content": prompts.lyrics_prompt.format(
                theme = project.state["mixtape_type"],
                song_name = song["song_name"],
                music_genre = song["music_genre"],
                vocals_style = song["vocals_style"],
                lyrics_description = song["lyrics_description"],
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

def step_create_audio_simple_poll(project, max_in_flight=2, poll_interval=30):
    songs_to_create = deque([
        s for s in project.state["mixtape"]["songs"] if not s.get("song_ids")
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
            style = f"{song['music_genre']}, {song['vocals_style']} vocals"
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
    'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsImNhdCI6ImNsX0I3ZDRQRDExMUFBQSIsImtpZCI6Imluc18yT1o2eU1EZzhscWRKRWloMXJvemY4T3ptZG4iLCJ0eXAiOiJKV1QifQ.eyJhdWQiOiJzdW5vLWFwaSIsImF6cCI6Imh0dHBzOi8vc3Vuby5jb20iLCJleHAiOjE3NTQwMDMwNjIsImZ2YSI6Wzk5OTk5LC0xXSwiaHR0cHM6Ly9zdW5vLmFpL2NsYWltcy9jbGVya19pZCI6InVzZXJfMllkN0xLVm9wNWQ4V1JJYWJISVU3aHI1M2RSIiwiaHR0cHM6Ly9zdW5vLmFpL2NsYWltcy9lbWFpbCI6InJ2ZW5kbGVyQGdtYWlsLmNvbSIsImh0dHBzOi8vc3Vuby5haS9jbGFpbXMvcGhvbmUiOm51bGwsImlhdCI6MTc1Mzk5OTQ2MiwiaXNzIjoiaHR0cHM6Ly9jbGVyay5zdW5vLmNvbSIsImp0aSI6IjA0MDIxOWNmNzcyNTBiMDQ0YzMzIiwibmJmIjoxNzUzOTk5NDUyLCJzaWQiOiJzZXNzXzJ1WE5tc0ZNOHZ1dXUzM0NrRm9uSVpGVm5sTiIsInN1YiI6InVzZXJfMllkN0xLVm9wNWQ4V1JJYWJISVU3aHI1M2RSIn0.N1EBASP8YRVxmGxnp1opU_C58nQJNFozg0ELsl7torGI-4Os-iclnu0MFZDafkiFUanyXcYIGXLqSLaEb4kCqC9qa5pskpcwEcDJRwEBC8cywKfgFj34ERQDvGaeV5oisITYx7_h4LW-pPSHLMC3iIpQqWyJI-3tdhZEqDPU9yIgAQqya2jrIWMg1iv--YYLhkRQbqI178smz79qMKUupcwy9qFVmfCB3X5tCOGi6X4ybRJ1YGn_saKRXlDfl7d07MFkYdECS3ixfQNh1ewlqSevGsfhh0s5RTMZh280XHvpTPmKfjQhv5tzqmChoTwucxGqB1zSWDwtDPODU_Wt0Q',
    'Content-Type': 'text/plain;charset=UTF-8',
    'Origin': 'https://suno.com',
    'Referer': 'https://suno.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'
  }

  # The full payload from your request, including the long token
  payload = {
    "token": "P1_eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.haJwZACjZXhwzmiL6OCncGFzc2tlecUEmvEXM6qHdF-HkL7eKQJ575FODgu2RSAze1hJQuXEFnR6986-c2MHpXqZGAAXRSOSd3jOJ7lfeJMABftgZx_Ibc-xVaXkkSUInFgqESFmyd5rWK6CFlxUuqcrzEMQTntzhbykZ5nzHKwUREDzrI6gWjUCF5fKBwWc5y2TwtyIVHc-7JWLOUvWSOaioahD3T2g3nxqS8rbMlFTxWTWVVL1JcH-B1OnH4tVkaawLIm6UDMTYwrWGMUon79Dq1UF05RKOLi6QS2lJwFlNgfzt4QfNPPJSI1nEQ0MVekbaWDro1EuvyiIVkD1dQJ7zhM4U7JIOYG5e2oqIqtMEGiPX2FWZs2Hw7oj8UiNIJlQxfbDbyO4KyB7z1rI9yKXKr3ZQVGbwXlo6C-AoQYCdrAFDqY85Tv-erSAG4rt1eNhIz58Wf1AQWNUcEt1AvLv_pCh2d8AMjjHB5NRrQ3Sm_T9Lea-CUQObEHxL-MDdtSw8f6XIIYxFaJf-Yoax3seh8NTwv7kzrmVHTdOpxk5cj2ttiA3dYH7w_egBHadCfYh0qyE9oWJz5wODfOdepcIhYMKFvV-ro4lJwPFIiy290yoR9Xfc-3v0q61Ul121_gohtDWN_l69Acc67ESosVR5FsWGivxUlXahPAyuC-rfuvMrXoXBg3GEqDhpxZq6-0zse0Bjk6mmLfG9Ul8ACeTZBYjNM1Zl_HTT9-Ljr9gqwiozEJWSmWc4VtZfi7Pde7JjdoSqTRwgPHzVAmj707lujAF5-0zThGMV_ZodifeDjcfcsLj8AxX0d7BD0jFTuYbDrzERSoRwwbbiP1Xzoy0oSjn4pr7L6RZ7iVltEKFS9oduD_adFFcLAVVKEHHZljfIdcigaqd6aL11h62rLi_PDx5Eq2MNtO2O3kaECoHvI6uNWbjtTK-5Mpr2GZjSHL_KniL-UrT3V24FP1Z6o1Rn1xkx9YjYdJl2FtzvEUd3aAdpIWsmGZcnzqTW4Ejd1VCB5fE9kwt7lbc1jFpBIkBXIPZQjUprwVwhRyAh5x8L27dNjXk_J_PuU2NmJLoCHSUUEaVqbMfnvM7hu7dEybUTXvigpzaiO4RP8aWwvAFgYBehYIiD2w9Fx30wZlNWILvZ5ZlDV7MrETpQ7iFAeQJo3fja_F86QSLv3nCl6bGM7gJSwig4pqcXFJcoxmzaLEUdWR00B42a6JQreFB61hDIxAjTBUrA40Xf2GFP_DieWlO3E7-q5XDnFmkBmzDNt778vXvPXfXNaQBR8HHAFQK2MjkDcByVPbq0uuqWs5fxxi43Naq20dy3MDU4uO7DORylpMTYoXaFMg09VqQJU7yPHXH54KdOLusyEQDk3AUqmThFtEcChE3Cx2wlfhfFyt3xVjMvsikv7OB2L0Kgl3xlk19Ihf9mp4aQhV5_1h70CpvgZaTCPK1Y0pPgvcPCjbWKT9N70GZPJzrctyNmdhFpcqYAhmWBL5G6b4z85gluqWr_OUt-uf2-oXdQ6GRy9tHK8pHo3ioe9NaPEsBG9y-XQ8rTSbcm7BsLCrlbMRAKP9V5xbUzL8Q3LsTyM634lPOomtyqDI1MWZmMmE1qHNoYXJkX2lkzhQ8hB8.WUWaP_zn8RnvskhaV3EAFvojVINBbZVakXXMIAwhVW8",
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
    jprint(response.json())
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

def rune_step_create_audio(project):
  for song in project.state["mixtape"]["songs"]:
    if not "song_ids" in song:
      clips_data = rune_make_suno_request(song["song_name"], song["music_style"] + ", " + song["vocals_style"] + " vocals", song["lyrics"])

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

def rune_step_create_audio_simple_poll(project, max_in_flight=5, poll_interval=60):
  songs_to_create = deque([
    s for s in project.state["mixtape"]["songs"] if not s.get("song_ids")
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
      response_data = rune_make_suno_request(title, f"{song['music_style']}, {song['vocals_style']} vocals", song["lyrics"])

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

def step_apply_tape_vst(project):
    for song in project.state["mixtape"]["songs"]:
        if not "vst_processed" in song:
            song_id = song["song_ids"][0]
#            for song_id in song["song_ids"]:
            vst_preset = random.choice(data.song_presets_light)
            mt_song = MT.from_file(f"saves/{project.name}/{song_id}.mp3")
            mt_song.apply_vst("Cassette", vst_preset)
            mt_song.save(f"saves/{project.name}/{song_id}-tape.mp3", "mp3")
            song["vst_processed"] = True
            project.save()

def step_create_cover_image(project, replicate_client):
    if not "cover_created" in project.state["mixtape"]:
        replicate_client.generate_image(
            output_path=f"saves/{project.name}/cover.png",
            prompt=project.state["mixtape"]["illustration"],
            aspect="2:3",
            prompt_upsampling=False,
            model="google/imagen-4",
            seed=None)
        project.state["mixtape"]["cover_created"] = True
        project.save()

def step_process_cover_image(project):
    if True or not "cover_processed" in project.state["mixtape"]:
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

def step_create_webpage(project):
    if True or not "webpage_created" in project.state["mixtape"]:
        playlist = ""
        song_1_name = None
        song_1_url = None
        song_index = 1

        for song in project.state["mixtape"]["songs"]:
            song_name = song["band_name"] + " - " + song["song_name"]
            song_url = song["song_ids"][0]+"-tape.mp3"
            if not song_1_name:
                song_1_name = song_name
                song_1_url = song_url
            playlist += f"""<div class="track active" data-src="{song_url}">
                        <span class="track-number">{song_index}.</span>
                        <span class="track-title">{song_name}</span>
                    </div>"""
            song_index += 1

        page = data.page_template.format(
            cover_url = "cover-composited.png",
            mixtape_name = project.state["mixtape"]["title"],
            playlist = playlist,
            song_1_name = song_1_name,
            song_1_url = song_1_url,
            quote = project.state["mixtape"]["backstory"]
            )
        with open(f"saves/{project.name}/page.html", "w") as text_file:
            text_file.write(page)
        project.state["mixtape"]["webpage_created"] = True
        project.save()

def main():
    """
    Loads a base image and applies several layers with different
    blending modes, then saves the result.
    """
    llm = initialize_llm()
    replicate_client = ReplicateImage(config.REPLICATE_API_TOKEN)

    project = SavesManager(ArgManager.get_arg("project"), False)

    step_create_mixtape(project, llm)
    step_create_song_structures(project)
    step_create_lyrics(project, llm)
#    step_create_audio_simple_poll(project)
    rune_step_create_audio_simple_poll(project)
    step_apply_tape_vst(project)
    step_create_cover_image(project, replicate_client)
    step_process_cover_image(project)
    step_create_webpage(project)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mixtapes")
    parser.add_argument("-p", "--project",type=str,help="Project name")
    parser.add_argument("-t", "--theme",type=str,help="Mixtape theme")
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
        
    main()
