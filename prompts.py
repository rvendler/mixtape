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
    "The 'I'm Too Cool for This' Mix: Deliberately obscure bands and B-sides to show off your superior music taste at parties.",
    "Driving Home from Work at 5 PM: Traffic jam anthems and commuter blues. Songs about being stuck, going nowhere, and dreaming of escape.",
    "The Bedroom Producer: Lo-fi bedroom recordings, four-track experiments, and intentionally unpolished gems that sound like secrets.",
    "Neon Lights & Late Nights: Club kids and rave culture. Glow sticks optional, basslines mandatory.",
    "The 'My Older Sibling Made This' Tape: Cool music you discovered by raiding someone else's collection. Slightly too mature for your age.",
    "Suburban Rebellion: For kids who think mowing the lawn is oppression. Mild punk for the subdivisions.",
    "The Stoner's Philosophy Hour: Slow, heavy, and contemplative. Perfect for deep thoughts about nothing important.",
    "VHS Horror Movie Vibes: Industrial, dark ambient, and creepy synthwave. Soundtrack to your nightmares.",
    "The 'I Just Got My License' Mix: Freedom songs for your first solo drive. Windows down, volume up, parents worried.",
    "Fluorescent Grocery Store at 2 AM: Weird, lonely, late-night shopping music. Ambient and slightly unsettling.",
    "The Cheerleader's Secret Shame: Bubblegum pop on the outside, angry riot grrrl on the inside.",
    "Fake ID Energy: Songs that make you feel older and cooler than you actually are.",
    "The Art Kid's Soundtrack: Pretentious, experimental, and probably recorded in someone's garage.",
    "Pizza Party Chaos: High-energy, goofy songs for sleepovers and birthday parties gone wild.",
    "The 'I'm Moving to New York' Fantasy: Songs about big city dreams and small town escape plans.",
    "Waiting for the Phone to Ring: Anxious love songs for hoping your crush will call you back.",
    "The Grungy Coffee Shop: Acoustic guitars, flannel shirts, and existential lyrics scribbled in margins.",
    "Skipping Class to Sit in Your Car: Parking lot philosophy and first-period rebellion.",
    "The 'My Parents Are Fighting Again' Tape: Loud music to drown out the chaos downstairs.",
    "Basement Show Energy: DIY punk recorded on a boombox in someone's finished basement.",
    "The Exchange Student's Discovery: American music that sounds exotic to foreign ears.",
    "Roller Rink Romance: Cheesy love songs and disco beats for couples skate night.",
    "The Night Shift Worker's Dawn: Driving home as the sun rises, exhausted but somehow peaceful.",
    "Fake Sick Day Adventures: Songs for playing hooky and wandering around town alone.",
    "The 'I Think I'm in Love' Realization: That moment when friendship turns into something more.",
    "Garage Band Dreams: Songs that make you want to start a band with your friends immediately.",
    "The Babysitter's After-Hours: What you listen to once the kids are asleep and the house is yours.",
    "Comic Book Store Vibes: Nerd culture anthems and songs about feeling like an outsider hero.",
    "The 'Summer Job Sucks' Playlist: Music to make minimum wage more bearable.",
    "Waiting Room Anxiety: Nervous energy and fidgety songs for doctor's appointments and job interviews.",
    "The 'I'm Too Old for This' Mix: When you're 19 and feel ancient watching younger kids have fun.",
    "Blacklight Poster Atmosphere: Trippy, psychedelic songs for rooms lit only by lava lamps.",
    "The Debate Team's Victory Lap: Smart-kid music for academic overachievers who think they're punk.",
    "Parking Lot Makeout Session: Steamy slow jams for cramped car romance.",
    "The 'I Just Read Catcher in the Rye' Phase: Angsty songs about phonies and authenticity.",
    "Laundromat Meditation: Hypnotic, repetitive songs for watching clothes spin in circles.",
    "The Rich Kid's Rebellion: Expensive angst and trust fund punk rock.",
    "Thrift Store Treasure Hunt: Vintage vibes and songs about finding hidden gems in dusty bins.",
    "The 'My Friend's Older Brother is So Cool' Mix: Music that seems impossibly sophisticated.",
    "Dentist Office Nightmare: Songs that somehow make dental work even more uncomfortable.",
    "The 'I'm Definitely Going to Be Famous' Tape: Confidence-boosting anthems for future rock stars.",
    "Bus Stop Blues: Songs for waiting in the rain with no umbrella and questionable life choices.",
    "The Honors Student's Dark Side: Perfect grades, imperfect thoughts, and music parents wouldn't approve of.",
    "Stolen Cable TV Soundtrack: Songs that feel slightly illegal and definitely exciting.",
    "The 'Everyone Else is Fake' Mix: Superiority complex anthems for teenagers who think they're the only real ones.",
    "Hot Topic Employee Handbook: Mall goth essentials and eyeliner application music.",
    "The 'I Want to Disappear' Collection: Songs for feeling invisible and kind of liking it.",
    "Detention Hall Daydreams: Music for staring out windows and planning your escape from authority.",
    "The 'My Diary is Full' Emergency: Emotional overflow songs when writing isn't enough.",
    "Fake Vintage Cool: Songs that make you feel like you were born in the wrong decade.",
    "The Theater Kid's Emotional Range: Dramatic songs that require jazz hands and tears.",
    "Late-Night VHS Rewind: A hazy, dreamlike mix of ambient, lo-fi rock, and analog synths. For falling asleep to the TV glow and tape hiss.",
    "Mixtape from the Cool Older Cousin: Stuff that feels just a little too mature for your age. College radio gems, proto-indie rock, and shoegaze with mysterious band names.",
    "Mom's Car Stereo: A weirdly comforting blend of adult contemporary, soft rock, and 90s country-pop. Heavy on reverb and sentimentality.",
    "Basement Show Energy: Raw recordings, DIY vibes, and punk energy with half-broken instruments and passion louder than talent.",
    "When AIM Goes Silent: For the moment your crush logs off. Soft synth pop, indie ballads, and a hint of teen despair.",
    "Cafeteria Daydreams: Instrumentals and gentle pop you imagined your life to while zoning out in 4th period lunch.",
    "Backyard Bonfire Kisses: Acoustic guitars, warm harmonies, and a slow build toward that one unforgettable summer night.",
    "Beepers & Payphones: Tracks that live between the dial tone and the voicemail beep. Gritty urban textures mixed with slow jam vibes.",
    "Tragic Prom Night: Starts upbeat with glittering dance-pop, ends in mascara-streaked ballads and longing from the bathroom stall.",
    "After-School Special: The emotional arc of a teen drama. One mix to cry, reflect, rebel, and reconcile to.",
    "Corduroy & Patchouli: Earthy, jammy tracks from the tie-dye fringe of the alternative scene. Long solos, weird percussion, and deep thoughts.",
    "The Mixtape You Never Gave Them: The most personal one. Every track chosen for them, labeled in secret, tucked away forever.",
    "Locker Slams & Slurpee Breakups: Pop-rock angst and juvenile heartbreak. Cheap candy, cheaper love.",
    "TV Static Romance: Songs that sound like distorted VHS love letters. Warbly, swoony, a little bit haunted.",
    "Garage Band Dreams: Music that feels like your best friends trying to be famous in your neighbor's garage after school.",
    "CD-R Burnout: Late 90s burned CD culture. Overcompressed hits, awkward track transitions, and songs you only kind of liked.",
    "Bus Window Weather: For long rides where you pretended to be in a music video. Rain, reflections, and headphones pressed tight.",
    "Left on Read (in 1998): A soulful, low-key sad mix imagining what ghosting would've felt like on a pager.",
    "The Green Room Tape: Sounds to listen to before you go onstage, even if 'onstage' is just your bedroom mirror.",
    "The Mixtape That Got You Grounded: Explicit lyrics, anarchist themes, and that one track your mom overheard and freaked out about.",
    "Cable Access at 2AM: Oddball spoken word, weird synths, outsider music, and the sound of someone testing a theremin.",
    "Slumber Party Secrets: A sugar rush of bubblegum pop and tearjerker ballads whispered under blankets.",
    "The Science Fair Went Bad: Weirdly futuristic, electronic, experimental. You can almost smell the solder.",
    "Zines & Xeroxed Feelings: Lo-fi punk and spoken word tracks that sound like they came with hand-stapled lyrics and a political manifesto.",
    "First Kiss Behind the Gym: Nervous energy, slow beats, and dreamy awkwardness wrapped in fuzzy nostalgia.",
    "House Party at Someone's Older Brother's Place: Dubious beer, loud rap, nu-metal, and something someone says is 'jungle.'",
    "Disassociation Station: When you're physically there but mentally far, far away. Droning beats, distant vocals, and time stretched thin.",
    "The Skatepark at Dusk: When everyone's too tired to land another trick. Mellow beats, bruised knees, and cracked decks.",
    "Mixtape for My Future Self: Hopeful, confused, curious—like a sonic time capsule. One part journal, one part letter.",
    "Under the Bleachers: Secretive, rebellious, and just a little bit dangerous. The mix you sneak into your Walkman in detention.",
    "Backyard Sprinkler Summer: Goofy, joyous, over-the-top songs that make you feel 9 again. Pop punk meets bubblegum.",
    "Crush on a Cashier: The kind of infatuation that lasts three weeks but feels like a lifetime. Soft beats, warm vocals, dumb grins.",
    "Leftover Halloween Candy: Spooky, sticky, strange. Indie goth-pop and eerie novelty songs you kind of love.",
    "The Long Walk Home: When the party ends badly and you have time to think. Sparse arrangements, soft beats, and late-night thoughts.",
    "Your Older Sibling's Broken Heart: Second-hand sadness, heavy ballads, and weirdly wise songs that made you grow up faster.",
    "The Night Got Weird: A chaotic, unpredictable mix for when the hangout spirals from casual to cosmic. Jump cuts from trip-hop to ska to spoken word.",
    "I Can't Sleep and It's Probably My Fault: A guilt-ridden midnight tape that swings from acoustic sorrow to overly dramatic industrial beats.",
    "Songs That Shouldn't Work Together But Do: An intentional genre crash—jazz into nu-metal, folk into breakbeats. The glue is pure chaos and heart.",
    "The Whole Movie in One Tape: Each song is a scene—opening credits, montage, car chase, romantic fallout, triumphant ending. No actual film required.",
    "Too Happy to Be Sad, Too Sad to Be Happy: A perfectly conflicted rollercoaster that won't let you settle into one emotion. It's beautifully confusing.",
    "Everything I Couldn't Say Out Loud: A confession in the form of random songs. Some are subtle hints, others are screamingly obvious.",
    "That Mix You Put On and Suddenly You're Cleaning Your Room: Starts lazy and slow, gets weirdly motivating in the middle, ends on a cathartic scream.",
    "Sunday Morning Existential Dread: You're drinking juice, staring out the window, and wondering what any of it means. The music doesn't help. In a good way.",
    "The Soundtrack to a Friendship Ending: Not romantic heartbreak—just the weird, quiet pain of growing apart. A bittersweet blend of warm and cold tracks.",
    "It's Raining Inside Me: Every song feels like water running down a windowpane. Some are dramatic, others just... drip quietly.",
    "Songs You Pretend Not to Like but Know Every Word To: Cringe-core classics, cheesy ballads, bubblegum trash. And you love every second of it.",
    "The 'This Isn't a Date' Date Mix: A carefully curated tape to play it cool. Casual at first, accidentally romantic by track 7.",
    "Music for Lying on the Floor and Spinning: Whether you're drunk, heartbroken, or just overstimulated—this mix doesn't judge.",
    "Songs I Think You'd Like If You Gave Them a Chance: A love letter disguised as a mixtape. Genre irrelevant—it's about showing someone how you see them.",
    "Music for Imaginary Conversations: The soundtrack to every fake argument or apology you rehearse in the shower.",
    "The Bathroom Mirror Monologue Mix: For practicing comebacks, pep talks, or existential breakdowns while brushing your teeth.",
    "I Had a Dream Like This Once: A surreal, out-of-body blend of eerie, euphoric, and oddly nostalgic songs. Feels like déjà vu and static electricity.",
    "Everything Reminds Me of Them: Even when the lyrics don't match—something in the melody or vibe hits just right. Every track is them.",
    "The Mixtape You Find in a Glovebox and Don't Know Who Made: A mysterious, haunting mix with no clear theme. Feels like someone else's memory.",
    "Midnight at the 24-Hour Diner: Fluorescent lights, coffee refills, and tired souls. Genres melt together like syrup on Formica.",
    "No One's Home and the Music Is Too Loud: You're alone and a little reckless. This mix jumps from guilty pleasures to primal screams.",
    "Deleted Scenes from the 90s: A soundtrack for the lost footage, the quiet moments that never made it to the VHS. Loops, demos, and emotional leftovers.",
    "My Mood Board Is Just Vibes: A highly aesthetic, zero-cohesion mixtape meant to be felt, not understood. Genre: Mood.",
    "Music to Play While Driving Nowhere: Doesn't matter where you're going—it's the motion, the engine hum, and the dramatic thoughts.",
    "Tape Made by Your Future Self: A strange and comforting time capsule. Sounds half-familiar, half-impossible. Feels like advice in a dream.",
]

mixtape_prompt = """Come up with 10 fictitious bands and songs for a 1990s cassette mixtape with the theme: "{theme}"

For the mixtape, provide the following information:
- Mixtape backstory (e.g. "This was a romantic tape made by Neil to Laura, a girl he liked", or "This was a collecting of local underground punk bands", always in third person)
- Mixtape title (e.g. "From Neil to Laura", or "Underground Buzz")
- Mixtape homemade cover illustration prompt, including the title to go on the cover, examples:
"Mixtape cassette cover, pencil drawing on top of photograph of a man in a suit, drawn across him. Writing: "Lamehouse", written with old uneven typewriter, ink blotches. DIY aesthetic. 1990s feel."
"Mixtape cassette cover, colored pencil drawing of a lighthouse, handdrawn, amateur. Writing: "To Jane", shaky lettering. DIY aesthetic. 1990s romantic feel."
"Mixtape cassette cover, pen scribbles, all hand drawn, chaotic, dirty and unbalanced. Writing: "NEW HARDCORE" in black felt tip, bad uneven lettering. DIY aesthetic. 1990s punk feel."
"Mixtape cassette cover, magazine collage + hand drawn details. Writing: "NIGHT OUT" in black felt tip, uneven handwriting. DIY aesthetic. 1990s feel."
"Crudely Hand drawn cover for a homemade mixtape, from Charlie to Lily. Drawn with colored pencils. Viewed straight on."
You can use paper clippings, collages, photos, drawings, etc -- all kinds of handmade things
The illustation prompt must specify that things are handmade, uneven, and so on, so we get that natural look and feel.

For each song, provide the following information:
- Band name (e.g. "The Funky Monkeys")
- Song name (e.g. "The Cage After Dark")
- Lyrics description ("Silly lyrics about animals having fun at the zoo after closing hours.")
- Music genre (e.g. "90s alternative rock, loud quiet loud style" - must always start with 90s, as that is the appropriate era, and you should use genres that existed at this time)
- Vocals style (e.g. "female")
- Is it an ensemble (e.g. a boy band or a girl group with multiple singers)

For band names, make sure you apply a variety of different naming schemes - single word, The "something", the singer's name, two words, a question, or other variations. Make sure you vary names and number of words in the names.
For song names, make sure they are varied and don't just restate the theme of the mixtape, but are about many different things — some cryptic, some abstract, some straightforward. Use a wide range of naming styles, such as: Single-word titles, Phrases or sentences, Cryptic or symbolic names, Questions, Character names, Verb-driven or action-based titles, Found objects or nostalgic ephemera, Strange or playful names, Contradictions or juxtapositions, Places and time-based titles
Avoid naming every song after the mixtape's title or theme. Let the songs tell their own stories, even if they're only loosely connected by vibe.

Guidelines and direction for naming each band and song:
{band_and_song_naming_guidelines}

Guidelines for the illustration:
{cover_image_guidelines}

Output in the following JSON format:

{{
	"backstory": "<mixtape backstory, always written in third person perspective>",
	"title": "<mixtape title>",
	"illustration": "<mixtape illustration prompt for image generation>",
	"songs_thiking": "<write your thougts about songs for the mixtape, ideas for different band names and song names that go in different directions and formats>",
	"songs":
	[
		{{
			"band_name": "<band name>",
			"song_name": "<song name>",
			"lyrics_description": "<lyrics description>",
			"music_genre": "<90s music genre, do NOT mention any band names here, that will cause rejection, start with the general genre, and then more specifics after that>",
			"vocals_style": "<male or female, no other options>",
            "is_ensemble": <frue if a boy band/girl group with multiple singers, otherwise false>
		}},
		...
	]
}}

Respond ONLY with the JSON."""

lyrics_prethink_prompt = """Your task is to think about lyrics for a ficitious song to go on a mixtape with the theme: "{theme}"

The song is called: {song_name}
The music genre is: {music_genre}
The vocals style is: {vocals_style}

Guidance for the lyrics: {lyrics_description}

Remember, your goal is not state the theme or guidance directly in the lyrics, but let it inspire you.

You should NOT yet write the lyrics, instead consider the following:

1. What is the song about? Remember, the song's theme doesn't have to be the same as the mixtape's theme - it just needs to fit on a mixtape with that theme.
2. What is the viewpoint of the song?
3. What are some specifics you want to lean into in the lyrics? How do you avoid it being too on the nose? Make sure you show, don't tell.
4. Some songs are very personal and mention people and places by names. Is this such a song? If so, who and what does it mention?
5. What should the tone and attitude be?
6. What sets it apart from other songs and makes it interesting or unique?
7. Consider what kind of lyrics and writing style is usually applied in this musical genre
8. What kind of language should you use? Direct, romantic, with or without metaphors, etc. Is it complex or simplistic?

Write down your thoughts these points. They don't have to come together to one coherent whole yet."""

lyrics_prompt = """Now write lyrics for the song based on the spec and your considerations above.

Remember, good lyrics evoke something in the listener. They don't preach or school the listener outright, they communicate by pulling the listener into their world and showing them, not telling them. Embrace these techniques.

Prefix each section in the lyrics with one of [intro], [verse], [pre-chorus], [chorus], [bridge], [solo], [outro].

Your song should have the following structure:
{structure}

Please follow these points of guidance for lyrics for the different sections:
{lyrics_guidance}

Do NOT give any other guidance in addition to the lyrics. Only the tags above and the lyrics to be sung.
The lyrics MUST be real lyrics, not indications of sound effect or other things, only sung lyrics, not using any parentheses.

Remember that the setting is the 1990s, so don't make reference to mobile phones, laptops, social media, or other more modern things that didn't exist in that time period.

Output only the lyrics, nothing else."""

lyrics_guides = {
    "verse": [
        "Make verses personal and descriptive, take us through a specific event and scene",
        "Start each verse at a different time of day to show progression",
        "Write like you're confiding a secret to your best friend",
        "Focus on one specific memory that represents the bigger picture",
        "Use 'I remember when...'' as your jumping off point",
        "Write about the moment everything changed, not the change itself",
        "Capture the feeling right before you knew what the feeling was",
        "Use weather as a metaphor for your internal state",
        "Start with a confession that makes the listener lean in",
        "Write about what you didn't say rather than what you said",
        "Focus on the small gesture that revealed everything",
        "Describe the physical sensations of the emotion",
        "Make each verse progressively more intense or vulnerable",
        "Use the same sentence structure but change the details",
        "Start each line with a different sense (e.g. I saw, I heard, I felt, I tasted)",
        "Open with a seemingly ordinary object and let it reveal the story",
        "Write the verse as a answering phone message you never left",
        "Contrast what you saw with what you wished you'd seen",
        "Speak to your past self in the second person",
        "Build the verse around a ticking countdown (count down from {num_lines} to 1)",
        "Narrate the moment as if time just slowed to half-speed",
        "Use street names and landmarks to ground the listener in place",
        "Flip between memory and wishful thinking each alternate line",
        "Show the aftermath first, then rewind to how it happened",
        "Write the verse as a list of things left behind",
        "Ask yourself 'why?'' at the end of every verse",
    ],

    "pre-chorus": [
        "Make each line a question",
        "Ask the questions your listener is thinking but afraid to voice",
        "Use e.g. 'What if' to explore possibilities and fears",
        "Frame each line as a different type of question (e.g. who, what, when, where, why, how",
        "Ask questions that have no easy answers",
        "Use rhetorical questions that build tension toward the chorus resolution",
        "Create a musical and lyrical climb that makes the chorus feel inevitable",
        "Use punchy lines to build urgency",
        "Repeat the same phrase with slight variations to create momentum",
        "List what's at stake before the chorus pays it off",
        "Use e.g. 'Maybe' statements that express doubt before the chorus brings certainty",
        "Transition from the verse's story to the chorus's universal truth",
        "Express the internal conflict that the chorus will resolve",
        "Use the pre-chorus to voice the fear that the chorus will conquer",
        "Build from whisper-quiet vulnerability to explosive emotion",
        "Show the moment of realization before the chorus declares it",
        "Pose impossible 'either/or' scenarios that raise the stakes",
        "Use escalating metaphors that threaten to spill over",
        "Repeat the first three words of each line like a heartbeat",
        "Frame each question as if you already know the painful answer",
        "Stack conditional phrases (e.g. 'If I ..., then will you ...'') to create suspense",
        "Let doubts tumble out in run-on sentences",
        "Contrast whispered admissions with blunt, one-word punches",
        "Insert a single word of denial ('no') at the end of every line",
        "Cascade from concrete detail to abstract feeling line by line",
        "Start each line with e.g. 'Maybe I'm ...' to expose hidden insecurities",
        "Voice the fear you've avoided naming in the verses",
        "End every line with the same rhyme to build pressure",
    ],

    "chorus": [
        "Make every line start with the same keyword",
        "Repeat the most important word or phrase like a mantra",
        "Start every line with the same powerful word (e.g. Tonight, Maybe, Never, Always)",
        "Create a call-and-response between different parts of the melody",
        "Use the song title as an anchor that everything else revolves around",
        "Make it simple enough to sing drunk at 2 AM but meaningful enough to tattoo",
        "Express what everyone feels but no one says",
        "Turn your specific story into everyone's anthem",
        "Use 'we' instead of 'I' to make it communal",
        "State the lesson learned or the truth discovered",
        "Make it the line people will quote as their favorite caption",
        "Let this be where all the verse's tension explodes",
        "Use bigger, broader strokes than the detailed verses",
        "Make it the moment of triumph, surrender, or breakthrough",
        "Give the listener permission to feel everything fully",
        "Create the line they'll scream-sing in their car",
        "Use the same melody but change one key word in each repetition",
        "Start with a statement, end with a question (or vice versa)",
        "Make each chorus repeat identical except for one crucial word change",
        "Use parallel structure: e.g. 'I will..., I will..., I will...'",
        "Boil the whole story into one vivid image and repeat it",
        "Answer the pre-chorus question with a single declarative sentence",
        "Use mirror-image phrases (e.g. 'You said / I said') for impact",
        "Start each line with e.g. 'This is...' to brand the core emotion",
        "Write the chorus as a promise you can't keep—but want to",
        "Flip a common cliché on its head and own the twist",
        "Let each line broaden the camera angle—from room, to street, to sky",
        "Use a contradiction (e.g. 'I'm breaking while I'm whole') as the hook",
        "Make every line end on the same vowel sound for chant-like unity",
        "Turn the chorus into a rallying cry using collective 'we' imagery",
        "State the consequence if the feeling is ignored",
        "Echo the first line at the end but with one crucial word altered",
        "Offer a single irresistible invitation in different ways each line",
        "Declare the universal truth the verses only hinted at",
        "End with a cliffhanger word that drops straight into the next section",
    ],

    "bridge": [
        "This is a counter section. If the verse is specific, this should be generic. If the verse is generic, then this should be specific",
        "If verses are personal, make the bridge universal (or vice versa)",
        "Change the pace completely",
        "Shift tense - e.g. from past tense to present tense or future tense",
        "Move from internal thoughts to external actions",
        "Switch from first person to second person ('you' instead of 'I')",
        "Reveal the twist that reframes everything we've heard",
        "Show the other side of the story",
        "Jump forward in time to show the aftermath",
        "Introduce a new character's voice or perspective",
        "Present the counterargument to your chorus's main point",
        "Plant the seed that will bloom in the final chorus",
        "Show the moment of decision that changes everything",
        "Create the 'aha' moment that makes the final chorus hit different",
        "Set up the final emotional payoff with new context or revelation",
        "Shift from narrative to raw confession—no images, just truth",
        "Write the bridge as a single-sentence stream of consciousness",
        "Introduce a stark 'what if' scenario that never happens",
        "Answer the chorus with its opposite emotion",
        "Put the whole song in jeopardy with one shocking admission",
        "Strip away rhyme to spotlight plainspoken honesty",
        "Bring in a line of dialogue that reframes the story",
        "Expose the secret motivation you've been hiding from the listener",
        "Turn the conflict inward: address your own reflection",
        "Reveal the cost of the triumph sung in the chorus",
        "Pose a hard moral question the song can't answer",
        "Offer a fleeting glimpse of redemption, then pull back",
    ]
}

band_name_guides = [
    "A single word",
    "A single word followed by a question mark",
    "Two words squeezed together into one word",
    "A question",
    "Two words",
    "Two words that are opposites",
    "Two words divided by a / symbol",
    "<something/someone> the <something>",
    "<name> and the <something>",
    "first name only",
    "full name (first+last) of singer",
    "The <something>",
    "<verb> the <something>",
    "<A location> band",
    "The <color> <somethings>",
    "<an object>",
    "<something> <group of people>",
    "Three words",
    "<name> and <name>",
    "<something> <boys or girls>",
    "The <men/women/etc.> in <something>",
    "The <house/place/office/place> of <something>",
    "A single word ending with an exclamation point",
    "Two words that rhyme",
    "Two words where the first is an adjective, the second a plural noun",
    "Two words linked by a hyphen",
    "Two words where one is a color, the other an animal",
    "Two words, both starting with the same letter (alliteration)",
    "Two words, one in English, one in another language",
    "Three words forming a complete sentence",
    "Three words that create an oxymoron",
    "Three words, the middle word is 'and'",
    "Three words, all nouns",
    "A short phrase that's a verb in the imperative mood",
    "A short phrase that ends with a question mark",
    "A number followed by a noun",
    "An airport code",
    "A star constellation name",
    "A mythological figure + a number",
    "A food + a tool",
    "A color + an abstract noun",
    "An adjective + 'Collective'",
    "An adjective + 'Orchestra'",
    "'The' + a single syllable noun",
    "'The New' + <something>",
    "'The' + <last name> + 'Experience'",
    "'<Last name> & Sons/Daughters'",
    "'The' + <place> + 'Project'",
    "'<Verb>-ing the' + <plural noun>",
    "'<Noun> vs. <Noun>'",
    "'<Noun>, <Noun> & <Noun>'",
    "'<Name>'s <plural noun>'",
    "'<Animal> on <Object>'",
    "'<Emotion> in <Season>'",
    "'<Direction> of <Noun>'"
]

song_name_guides_simple = [
    "A single word",
    "A single word in ALL CAPS",
    "Two words",
    "Two words that rhyme",
    "Three words",
    "Three words forming a mini-sentence",
    "Three words: verb + your + noun",
]

song_name_guides = [
    # — one-worders
    "A single word ending with an exclamation point",
    "A single word followed by a question mark",

    # — two-word frames
    "Two words, both nouns",
    "Two words: adjective + noun",
    "Two words joined by a hyphen",
    "Two words beginning with the same letter (alliteration)",
    "Two words that are opposites",
    "Two words, the second in parentheses",

    # — three-word frames
    "Three words, each longer than the last",
    "Three words, the middle word is 'and'",

    # — question & statement hooks
    "A yes/no question",
    "A 'Why' question",
    "A rhetorical question ending '...right?'",
    "A declarative sentence starting with 'I Am'",
    "A statement followed by a question in parentheses",

    # — time & place
    "A specific time (e.g. '2:17 AM')",
    "A month and year (e.g. 'July 1999')",
    "A street address",
    "A coordinate pair (e.g. '40°42′N 74°00′W')",
    "A city + comma + state/country",
    "'Midnight in <Place>'",
    "'<Season> in <Place>'",

    # — action verbs
    "Imperative verb command (e.g. 'Hold On')",
    "Verb + preposition + noun (e.g. 'Fall Into You')",

    # — emotional palette
    "A single emotion",
    "Emotion + number (e.g. 'Happiness 101')",
    "Color + emotion (e.g. 'Blue Regret')",

    # — metaphor & imagery
    "Animal + mechanical object (e.g. 'Wolves and Wires')",

    # — numeric & symbol play
    "A fraction (e.g. '50% Heart')",

    # — quotes & parentheticals
    "Quote from dialogue (e.g. 'She Said, \"Stay\"')",
]

cover_image_guide = [
    "pencil drawing on top of photograph",
    "pencil drawing",
    "chaotic pen scribbles",
    "photo collage",
    "photo collage with bits replaced",
    "newspaper clippings",
    "pencil drawing",
    "crude photocopied image",
    "glossy magazine image",
    "a negative photo (reversed colors)",
    "torn-notebook-paper collage",
    "scanned sticky-note mosaic",
    "polaroid photo taped at the corners",
    "paint-splatters over a photocopy",
    "marker doodles on lined paper",
    "imprecise screen-print layers",
    "risograph two-color print look",
    "hand-stamped rubber-ink patterns",
    "spray-paint stencil over snapshot",
    "sticker-bombed backdrop",
    "ink-wash bleed edges",
    "old ticket-stub collage",
    "photo fragments taped back together",
    "hand-cut silhouette montage",
    "contact-sheet film strips",
    "glitchy xerox repeats",
    "school photo with drawn-on accessories",
    "TV screen photograph with static lines",
    "double-exposed film experiment",
    "carbon paper transfer image",
    "thermal fax paper print",
    "mimeograph purple-ink dupe",
    "iron-on transfer peeling off",
    "layered tissue paper cutouts",
    "magazine page with holes cut out",
    "hand-colored black & white photocopy",
    "contact paper stencil design",
    "overhead projector transparency stack",
    "cassette tape unspooled into design",
    "35mm film negative strips",
    "instant camera multiple exposures",
    "photomat booth strip cut up",
    "VHS pause-screen capture print",
]

cover_image_color_guide = [
    "black and white",
    "monochrome",
    "black, white and one strong color",
    "full color",
    "faded colors",
    "bright, strong colors",
    "a few colors",
    "pastel chalk tones",
    "neon highlighter palette",
    "sepia-washed vintage",
    "risograph pink & electric blue",
    "fluorescent pops on black",
    "photocopy-blue haze",
    "split-complementary pops",
    "rainbow-gradient marker strokes",
    "muted colored-pencil set",
    "rust-red and cream",
    "cyan-magenta negative inversion",
    "black ground with metallic gold accents",
    "newsprint off-white + black",
    "Day-Glo orange and hot pink",
    "purple mimeograph ink fade",
    "thermal paper brown-orange",
    "highlighter yellow bleeding",
    "red-eye photo flash accidents",
    "color-shifting holographic foil",
    "newspaper color comics palette",
    "office highlighter trio",
    "purple carbon copy smudge",
    "orange safety-vest bright",
    "green computer paper tractor-feed",
    "magenta and cyan printer test",
    "yellow legal pad background",
    "blue ballpoint pen only",
    "red Sharpie marker dominant",
    "silver metallic crayon accents",
    "brown paper bag natural",
    "white-out correction fluid pops",
    "construction paper primary brights",
]

cover_image_details = [
    "sunglasses painted on faces",
    "moustaches painted on faces",
    "faces scratched out",
    "lots of scribbles",
    "little stars addes",
    "cartoon-style words added",
    "elegant flowy lines",
    "masking-tape Xs in the corners",
    "visible thread-stitch lines",
    "yellowing sellotape strips",
    "hand-drawn arrows everywhere",
    "doodle hearts & lightning bolts",
    "random ink blots",
    "grid-paper texture peeking through",
    "wrinkled fold lines",
    "pressed leaf taped down",
    "receipt scraps layered",
    "smiley-face sticker",
    "thumb-tack pin-holes",
    "phone numbers written in margins",
    "doodle flames around edges",
    "peace signs and anarchy symbols",
    "hearts with initials inside",
    "geometric patterns in corners",
    "spiral notebook ring holes",
    "hole punch confetti scattered",
    "correction tape white streaks",
    "highlighter marker bleeding",
    "ink fingerprint stamps",
    "ruler measurement marks",
    "compass-drawn perfect circles",
    "eraser smudge marks",
    "pencil shavings glued down",
    "white-out painted designs",
]

cover_image_lettering = [
    "letters cut from magazines",
    "old typewriter letters",
    "uneven hand-written pencil letters",
    "neatly hand-drawn letters",
    "shaky handwriting",
    "angry, uneven handwriting",
    "block letters in thick marker",
    "bubble letters filled with patterns",
    "chalkboard-smudge script",
    "cereal-box cut-out letters",
    "duct-tape lettering",
    "white correction-fluid scrawl",
    "glitter gel-pen letters",
    "needle-point stitched letters",
    "spray-paint stencil glyphs",
    "rubber-stamp ink ghosts",
    "ballpoint-pen scratch letters",
    "chunky crayon capitals",
    "3-D drop-shadow hand-drawn letters",
    "fax-machine photocopy blur text",
    "peeling vinyl-sticker letters",
    "lino-print serif blocks",
    "groove-pattern record letters",
    "dot-matrix printer font",
    "label-maker plastic tape strips",
    "carbon paper transfer text",
    "embossed label maker raised letters",
    "photocopied handwriting repeated",
    "stencil letters with spray overspray",
    "calculator display number font",
    "computer dot-matrix all caps",
    "transfer letter sheets partially used",
    "magic marker bleeding letters",
    "pencil letters traced over multiple times",
    "finger-painted sloppy letters",
    "torn paper letter shapes",
    "scratched-in letters with pen",
    "white-out letters on dark background",
]

cover_image_damage = [
    "one corner torn off",
    "dirt smear across image",
    "burnt corner",
    "scratches and folds",
    "faded in the sun",
    "paint drops",
    "coffee-ring stain",
    "water-warped ripples",
    "thumb-tack pinholes",
    "yellowed tape residue",
    "dog-eared corners",
    "cigarette burn mark",
    "ink blot bleed-through",
    "sticker outline ghost",
    "centerfold crease line",
    "ripped then taped back together",
    "sun-bleached stripe",
    "mud splatter dots",
    "mildew speckling",
    "fingerprint smudges",
    "random staple holes",
    "pen scribble crossing out part",
    "peeling corner curl",
    "glue drips hardened",
    "scuffed surface haze",
    "ring binder hole tears",
    "backpack zipper scrape marks",
    "locker door slam creases",
    "soda can ring stains",
    "chewed corner from boredom",
    "highlighter bleed-through stains",
    "three-hole punch partial tears",
    "rubber band indent marks",
    "book bag compression wrinkles",
    "humid weather warp bubbles",
    "pencil case zipper snags",
    "folder brad fastener rust spots",
    "white-out flaking off patches",
    "paper clip rust impression",
    "sticky note residue rectangles",
    "library pocket glue remnants",
]
