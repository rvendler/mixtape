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
        if has_pre_chorus:
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
            lyrics = llm.query(prompts.lyrics_prompt.format(
                theme = project.state["mixtape_type"],
                song_name = song["song_name"],
                music_style = song["music_style"],
                vocals_style = song["vocals_style"],
                lyrics_description = song["lyrics_description"],
                structure = structure
                ))
            print(lyrics)
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
        jprint(headers)
        jprint(payload)
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

        jprint(data)        

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
            style = f"{song['music_style']}, {song['vocals_style']} vocals"
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


def step_apply_tape_vst(project):
    for song in project.state["mixtape"]["songs"]:
        if not "vst_processed" in song:
            for song_id in song["song_ids"]:
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
    step_create_audio_simple_poll(project)
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
    
    print(submit_suno_job("Test for marsZ", "Happy pop punk", lyrics="[verse]\nThis is a test\n\n[chorus]Test, test, test"))

    if ArgManager.get_arg("project") == None:
        print("project not specified")
        exit(1)
        
    main()
