mixtape_types = [
	"Alternative Nation: A collection of grunge, post-grunge, and alternative rock anthems. Think Nirvana, Pearl Jam, Smashing Pumpkins, and Soundgarden.",
	"Britpop Invasion: For when you're feeling a bit cheeky. All the best from Oasis, Blur, Pulp, and The Verve.",
	"Riot Grrrl Power: A raw, feminist punk mix with bands like Bikini Kill, Sleater-Kinney, and L7.",
	"Skate Punk & Pop Punk: High-energy, fast-paced anthems from Green Day, The Offspring, Blink-182, and NOFX.",
	"Electronica & Big Beat: Sounds from the rave and club scene. The Chemical Brothers, The Prodigy, Fatboy Slim, and Daft Punk.",
	"Lilith Fair Vibes: A showcase of the decade's powerful female singer-songwriters, such as Alanis Morissette, Sarah McLachlan, Jewel, and Fiona Apple.",
	"Industrial Strength: Dark, heavy, and electronic. A mix for when you're feeling angsty, featuring Nine Inch Nails, Ministry, and KMFDM.",
	"Teen Angst: For staring at the ceiling and feeling misunderstood. Must-haves include Radiohead's Creep and The Cranberries' Zombie.",
	"Summer Sunshine: The ultimate feel-good mix for a sunny day with the windows down. Think Len's Steal My Sunshine, and Smash Mouth's All Star.",
	"Heartbreak Hotel: Your go-to breakup tape. Side A is for anger (Alanis Morissette), Side B is for crying (Sinéad O'Connor, Boyz II Men).",
	"Chillout Zone: Low-key, atmospheric tracks for studying, relaxing, or a late-night drive. Massive Attack, Portishead, and Air are essential.",
	"Rainy Day Feelings: Melancholy and introspective songs for a quiet, gray day. Featuring Jeff Buckley, Mazzy Star, and Elliott Smith.",
	"Pure Rage: When you just need to scream. A mix of Rage Against the Machine, Korn, and early Limp Bizkit.",
	"Road Trip Anthems: Songs that were made for the open highway. Gin Blossoms' Hey Jealousy, Red Hot Chili Peppers' Under the Bridge, and Tom Cochrane's Life Is a Highway.",
	"The 'For My Crush' Tape: A classic. Side A is full of hopeful, romantic songs. Side B is what you listen to if they don't feel the same way.",
	"The 'Whatever' Mix: For when you're feeling apathetic and kind of slacker-ish. Pavement, Beck, and early Weezer.",
	"One-Hit Wonders: A celebration of those artists who had their glorious 15 minutes of fame. Featuring Macarena, Mambo No. 5, and I'm Too Sexy.",
	"Girl Power!: An explosive mix celebrating female artists and groups that defined the decade, from the Spice Girls to No Doubt and TLC.",
	"Songs from the Back of the School Bus: A chaotic, bass-heavy mix heard from a shared Walkman. Mostly hip hop and rock that would annoy the bus driver.",
	"Learning to Skateboard (and Falling A Lot): A raw, high-energy soundtrack of skate punk and hip hop for practicing ollies in an empty parking lot.",
	"The Mall Food Court: A bright, loud, and messy mix of everything playing in every store at once. Mainstream pop, R&B, and rock.",
	"Awkward High School Party: The music playing in the background while everyone stands around the walls, too nervous to talk. Usually Weezer's Blue Album, Oasis, or Pavement.",
	"One Last Night in Your Hometown: For the night before leaving for college. A mix of nostalgia, sadness, and excitement for the future. Starts with Semisonic's 'Closing Time,' ends with Vitamin C's 'Graduation.'",
	"The Goth's Lament: Music for writing bad poetry by candlelight. The Cure, Type O Negative, Nine Inch Nails' The Downward Spiral, and Tori Amos.",
	"The Film Student's Coffee Shop Mix: Obscure indie rock, brooding trip-hop, and anything from a Tarantino soundtrack.",
	"The Jock's Locker Room Hype Mix: Aggressive rock, nu-metal, and party hip hop to get pumped up before the big game.",
	"Fluorescent Lights & Hairspray: The sound of getting ready for a school dance. Upbeat pop, dance hits from La Bouche and Ace of Base, and diva ballads.",
	"The Color Orange: A mix of songs that just feel bright, energetic, and a little weird. 'Semi-Charmed Life,' 'Steal My Sunshine,' and 'Flagpole Sitta.'",
	"Static on the TV After Midnight: Eerie, quiet, and slightly unsettling tracks for 3 AM insomnia. Portishead, Tricky, and the B-sides from Radiohead's OK Computer.",
	"Sun-Bleached & Salty: The feeling of a long beach day fading into a cool evening bonfire. Sublime, Sugar Ray, 311, and Everclear.",
]

mixtape_prompt = """Come up with 10 fictitious bands and songs for a 1990s cassette mixtape with the theme: "{theme}"

For the mixtape, provide the following information:
- Mixtape backstory (e.g. "This was a romantic tape made by Neil to Laura, a girl he liked", or "This was a collecting of local underground punk bands")
- Mixtape title (e.g. "From Neil to Laura", or "Underground Buzz")
- Mixtape homemade cover illustration, including the title to go on the cover (e.g. "Mixtape cassette cover, pencil drawing on top of photograph of a man in a suit, drawn across him. Writing: "Lamehouse", written with old uneven typewriter, ink blotches. DIY aesthetic. 1990s feel.", or "Mixtape cassette cover, colored pencil drawing of a lighthouse, handdrawn, amateur. Writing: "To Jane", shaky lettering. DIY aesthetic. 1990s romantic feel.", or "Mixtape cassette cover, pen scribbles, all hand drawn, chaotic, dirty and unbalanced. Writing: "NEW HARDCORE" in black felt tip, bad uneven lettering. DIY aesthetic. 1990s punk feel.", or "Mixtape cassette cover, magazine collage + hand drawn details. Writing: "NIGHT OUT" in black felt tip, uneven handwriting. DIY aesthetic. 1990s feel.", or "Crudely Hand drawn cover for a homemade mixtape, from Charlie to Lily. Drawn with colored pencils. Viewed straight on.")

For each song, provide the following information:
- Band name (e.g. "The Funky Monkeys")
- Song name (e.g. "The Cage After Dark")
- Lyrics description ("Silly lyrics about animals having fun at the zoo after closing hours.")
- Music style (e.g. "90s alternative rock, loud quiet loud style")
- Vocals style (e.g. "female")

Output in the following JSON format:

{{
	"backstory": "<mixtape backstory>",
	"title": "<mixtape title>",
	"illustration": "<mixtape illustration prompt for image generation>",
	"songs":
	[
		{{
			"band_name": "<band name>",
			"song_name": "<song name>",
			"lyrics_description": "<lyrics description>",
			"music_style": "<music style, do NOT mention any band names here, that will cause rejection>",
			"vocals_style": "<male or female>"
		}},
		...
	]
}}

Respond ONLY with the JSON."""

lyrics_prompt = """Write lyrics for a ficitious song to go on a mixtape with the theme: "{theme}"

The song is called: {song_name}
The music style is: {music_style}
The vocals style is: {vocals_style}

Guidance for the lyrics: {lyrics_description}

Prefix each section in the lyrics with one of [intro], [verse], [pre-chorus], [chorus], [bridge], [solo], [outro].

Your song should have the following structure:
{structure}

Do NOT give any other guidance in addition to the lyrics. Only the tags above and the lyrics to be sung.
The lyrics MUST be real lyrics, not indications of sound effect or other things, only sung lyrics, not using any parentheses.

Output only the lyrics, nothing else."""

