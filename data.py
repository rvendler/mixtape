song_presets_light = [
    "presets/cassette_clean_tape.fxp",
    "presets/cassette_insight_bayside.fxp",
    "presets/cassette_insight_its_moving.fxp",
    "presets/cassette_insight_lets_go.fxp",
    "presets/cassette_insight_radio_tape.fxp",
    "presets/cassette_insight_warm_keys.fxp",
    "presets/cassette_little.fxp",
    "presets/cassette_tascam.fxp",
    "presets/cassette_torley_chonky_drums.fxp",
    "presets/cassette_torley_comforting_anachronism.fxp",
    "presets/cassette_torley_crispy_focus.fxp",
    "presets/cassette_torley_extra_touch.fxp",
    "presets/cassette_torley_home_flavor.fxp",
    "presets/cassette_torley_intriguing_sheen.fxp",
    "presets/cassette_torley_left_in_the_sun.fxp",
    "presets/cassette_torley_rolloff_highs.fxp",
    "presets/cassette_torley_stable_boost.fxp",
    "presets/cassette_torley_warming_nuance.fxp",
]

song_presets_medium = [
    "presets/cassette_1978.fxp",
    "presets/cassette_clean_tape.fxp",
    "presets/cassette_insight_bayside.fxp",
    "presets/cassette_insight_drifter.fxp",
    "presets/cassette_insight_its_moving.fxp",
    "presets/cassette_insight_lets_go.fxp",
    "presets/cassette_insight_radio_tape.fxp",
    "presets/cassette_insight_warm_keys.fxp",
    "presets/cassette_little.fxp",
    "presets/cassette_movement.fxp",
    "presets/cassette_old_synth.fxp",
    "presets/cassette_tascam.fxp",
    "presets/cassette_torley_chonky_drums.fxp",
    "presets/cassette_torley_comforting_anachronism.fxp",
    "presets/cassette_torley_crispy_focus.fxp",
    "presets/cassette_torley_extra_touch.fxp",
    "presets/cassette_torley_fragile_memories.fxp",
    "presets/cassette_torley_home_flavor.fxp",
    "presets/cassette_torley_intriguing_sheen.fxp",
    "presets/cassette_torley_left_in_the_sun.fxp",
    "presets/cassette_torley_lofi_way.fxp",
    "presets/cassette_torley_mellow_my_harsh.fxp",
    "presets/cassette_torley_rolloff_highs.fxp",
    "presets/cassette_torley_stable_boost.fxp",
    "presets/cassette_torley_unstable_shadows.fxp",
    "presets/cassette_torley_warming_nuance.fxp",
]

song_presets_heavy = [
    "presets/cassette_1978.fxp",
    "presets/cassette_clean_tape.fxp",
    "presets/cassette_insight_bayside.fxp",
    "presets/cassette_insight_drifter.fxp",
    "presets/cassette_insight_its_moving.fxp",
    "presets/cassette_insight_lets_go.fxp",
    "presets/cassette_insight_radio_tape.fxp",
    "presets/cassette_insight_warm_keys.fxp",
    "presets/cassette_little.fxp",
    "presets/cassette_movement.fxp",
    "presets/cassette_old_synth.fxp",
    "presets/cassette_raw_insight_old_timer.fxp",
    "presets/cassette_raw_reporter.fxp",
    "presets/cassette_raw_torley_badley_chewed.fxp",
    "presets/cassette_raw_torley_bass_fuzzer.fxp",
    "presets/cassette_raw_torley_cymbalism.fxp",
    "presets/cassette_raw_torley_disturbed_flanger.fxp",
    "presets/cassette_raw_torley_giorgio_corroder.fxp",
    "presets/cassette_raw_torley_industrial_crush.fxp",
    "presets/cassette_raw_torley_it_follows.fxp",
    "presets/cassette_raw_torley_purity_destroyer.fxp",
    "presets/cassette_raw_torley_rich_phase.fxp",
    "presets/cassette_raw_torley_snappening.fxp",
    "presets/cassette_raw_torley_so_baked.fxp",
    "presets/cassette_raw_torley_trapped_delicacy.fxp",
    "presets/cassette_raw_torley_warble_of_interest.fxp",
    "presets/cassette_tascam.fxp",
    "presets/cassette_torley_chonky_drums.fxp",
    "presets/cassette_torley_comforting_anachronism.fxp",
    "presets/cassette_torley_crispy_focus.fxp",
    "presets/cassette_torley_extra_touch.fxp",
    "presets/cassette_torley_fragile_memories.fxp",
    "presets/cassette_torley_home_flavor.fxp",
    "presets/cassette_torley_intriguing_sheen.fxp",
    "presets/cassette_torley_left_in_the_sun.fxp",
    "presets/cassette_torley_lofi_way.fxp",
    "presets/cassette_torley_mellow_my_harsh.fxp",
    "presets/cassette_torley_rolloff_highs.fxp",
    "presets/cassette_torley_stable_boost.fxp",
    "presets/cassette_torley_unstable_shadows.fxp",
    "presets/cassette_torley_warming_nuance.fxp",
]

page_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mixtape - {mixtape_name}</title>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;700&display=swap" rel="stylesheet">
    <style>
        body {{
            font-family: 'Montserrat', sans-serif;
            margin: 0;
            padding: 15px;
            background-color: #f5f5f5;
            font-size: 14px;
        }}
        
        .container {{
            max-width: 950px;
            margin: 0 auto;
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 3px 5px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }}
        
        .top-section {{
            display: flex;
            padding: 20px;
            gap: 20px;
        }}
        
        .image-section {{
            flex: 0 0 320px;
        }}
        
        .image-section img {{
            width: 320px;
            height: 470px;
            object-fit: cover;
            border-radius: 6px;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
        }}
        
        .music-section {{
            flex: 1;
            padding-left: 15px;
        }}
        
        .music-section h2 {{
            margin-top: 0;
            color: #333;
            font-size: 20px;
            margin-bottom: 15px;
            font-weight: 700;
        }}
        
        .playlist {{
            background-color: #f9f9f9;
            border-radius: 6px;
            padding: 15px;
            margin-bottom: 15px;
        }}
        
        .track {{
            display: flex;
            align-items: center;
            padding: 8px;
            margin-bottom: 8px;
            background-color: white;
            border-radius: 4px;
            cursor: pointer;
            transition: background-color 0.3s;
            font-size: 13px;
        }}
        
        .track:hover {{
            background-color: #e8f4f8;
        }}
        
        .track.active {{
            background-color: #d4edda;
            border-left: 3px solid #28a745;
        }}
        
        .track-number {{
            margin-right: 12px;
            font-weight: 700;
            color: #666;
            min-width: 18px;
            font-size: 12px;
        }}
        
        .track-title {{
            flex: 1;
            color: #333;
        }}
        
        .audio-controls {{
            background-color: #f8f9fa;
            padding: 12px;
            border-radius: 6px;
            margin-top: 15px;
            border: 1px solid #e9ecef;
        }}
        
        audio {{
            width: 100%;
            outline: none;
        }}
        
        .current-track {{
            color: #333;
            margin-bottom: 8px;
            font-weight: 400;
            font-size: 13px;
        }}
        
        .quote-section {{
            padding: 20px;
            background-color: #f8f9fa;
            border-top: 1px solid #e9ecef;
        }}
        
        .quote {{
            font-style: italic;
            font-size: 15px;
            line-height: 1.5;
            color: #555;
            text-align: center;
            max-width: 650px;
            margin: 0 auto;
            font-weight: 300;
        }}
        
        .lyrics-section {{
            padding: 20px;
            background-color: #fafafa;
            border-top: 1px solid #e9ecef;
            min-height: 200px;
        }}
        
        .lyrics-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }}
        
        .lyrics-title {{
            font-size: 16px;
            font-weight: 700;
            color: #333;
            margin: 0;
        }}
        
        .lyrics-toggle {{
            background: #28a745;
            color: white;
            border: none;
            padding: 6px 12px;
            border-radius: 4px;
            font-size: 12px;
            cursor: pointer;
            transition: background-color 0.3s;
        }}
        
        .lyrics-toggle:hover {{
            background: #218838;
        }}
        
        .lyrics-content {{
            background-color: white;
            border-radius: 6px;
            padding: 20px;
            border: 1px solid #e9ecef;
            max-height: 400px;
            overflow-y: auto;
            transition: opacity 0.3s ease;
        }}
        
        .lyrics-content.collapsed {{
            max-height: 0;
            padding: 0 20px;
            opacity: 0;
            overflow: hidden;
        }}
        
        .lyrics-text {{
            font-size: 14px;
            line-height: 1.6;
            color: #444;
            white-space: pre-line;
            font-family: 'Montserrat', sans-serif;
        }}
        
        .lyrics-placeholder {{
            color: #888;
            font-style: italic;
            text-align: center;
            padding: 40px 20px;
        }}
        
        .current-song-info {{
            font-size: 13px;
            color: #666;
            margin-bottom: 10px;
            font-style: italic;
        }}
        
        @media (max-width: 768px) {{
            .top-section {{
                flex-direction: column;
                padding: 15px;
            }}
            
            .image-section {{
                flex: none;
                align-self: center;
            }}
            
            .image-section img {{
                width: 100%;
                height: auto;
                max-width: 320px;
            }}
            
            .music-section {{
                padding-left: 0;
                padding-top: 15px;
            }}
            
            .container {{
                margin: 10px;
            }}
            
            body {{
                padding: 10px;
            }}
            
            .lyrics-header {{
                flex-direction: column;
                align-items: flex-start;
                gap: 10px;
            }}
        }}
    </style>
</head>
<body>
    <br>
    <div class="container">
        <div class="top-section">
            <div class="image-section">
                <img src="{cover_url}" alt="{mixtape_name}">
            </div>
            
            <div class="music-section">
                <h2>{mixtape_name}</h2>
                <div class="playlist">
                    {playlist}
                </div>
                
                <div class="audio-controls">
                    <div class="current-track">Now Playing: {song_1_name}</div>
                    <audio controls id="audioPlayer">
                        <source src="{song_1_url}" type="audio/mpeg">
                        Your browser does not support the audio element.
                    </audio>
                </div>
            </div>
        </div>
        
        <div class="quote-section">
            <div class="quote">
                {quote}
            </div>
        </div>
        
        <div class="lyrics-section">
            <div class="lyrics-header">
                <h3 class="lyrics-title">Lyrics</h3>
                <button class="lyrics-toggle" onclick="toggleLyrics()">Show/Hide</button>
            </div>
            
            <div class="lyrics-content collapsed" id="lyricsContent">
                <div class="current-song-info" id="currentSongInfo">
                    {song_1_name}
                </div>
                <div class="lyrics-text" id="lyricsText">
                    <div class="lyrics-placeholder">
                        Lyrics will appear here when available.<br>
                        Click on different tracks to see their lyrics.
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        const tracks = document.querySelectorAll('.track');
        const audioPlayer = document.getElementById('audioPlayer');
        const currentTrackDisplay = document.querySelector('.current-track');
        const lyricsText = document.getElementById('lyricsText');
        const currentSongInfo = document.getElementById('currentSongInfo');
        
        // Lyrics database - populated from Python
        const lyricsDatabase = {lyrics};

        function updateLyrics(trackTitle) {{
            currentSongInfo.textContent = `${{trackTitle}}`;
            
            if (lyricsDatabase[trackTitle]) {{
                lyricsText.innerHTML = lyricsDatabase[trackTitle];
            }} else {{
                lyricsText.innerHTML = `<div class="lyrics-placeholder">Lyrics not available for this track.<br>Check back later for updates!</div>`;
            }}
        }}

        function toggleLyrics() {{
            const lyricsContent = document.getElementById('lyricsContent');
            lyricsContent.classList.toggle('collapsed');
        }}

        tracks.forEach(track => {{
            track.addEventListener('click', function() {{
                // Remove active class from all tracks
                tracks.forEach(t => t.classList.remove('active'));
                
                // Add active class to clicked track
                this.classList.add('active');
                
                // Get the audio source and title
                const audioSrc = this.getAttribute('data-src');
                const trackTitle = this.querySelector('.track-title').textContent;
                
                // Update audio player
                audioPlayer.src = audioSrc;
                currentTrackDisplay.textContent = `Now Playing: ${{trackTitle}}`;
                
                // Update lyrics
                updateLyrics(trackTitle);
                
                // Play the audio
                audioPlayer.play();
            }});
        }});

        // Auto-play next track when current ends
        audioPlayer.addEventListener('ended', function() {{
            const activeTrack = document.querySelector('.track.active');
            const nextTrack = activeTrack.nextElementSibling;
            
            if (nextTrack && nextTrack.classList.contains('track')) {{
                nextTrack.click();
            }}
        }});

        // Initialize lyrics for the first track
        const firstTrack = document.querySelector('.track.active .track-title');
        if (firstTrack) {{
            updateLyrics(firstTrack.textContent);
        }}
    </script>
</body>
</html>"""