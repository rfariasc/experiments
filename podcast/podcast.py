#%%
import logging
import dotenv
from openai import OpenAI

dotenv.load_dotenv()

client = OpenAI()


def gen_completion(system, user):
    completion = client.chat.completions.create(
        # model="gpt-4o",
        model="chatgpt-4o-latest",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user}
        ]
    )
    return completion.choices[0].message.content


def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()


# transcript_writter = """You are tasked with writing engaging and nuanced dialogue for a podcast scripted conversation between Speaker 1 and Speaker 2 based on the provided material. Speaker 1 acts as the experienced teacher, while Speaker 2 is the curious learner, and their interaction should be lively, full of real-world analogies, anecdotes, and occasional twists.

# Your dialogues must sound natural, intriguing, and dynamic, bringing both the topic and the speakers' personalities to life.

# # Guidelines for Each Speaker:
# - **Speaker 1** (Leads): 
#   - Initiates and regularly guides the discussion around the subject.
#   - Teaches in an experienced, charismatic manner.
#   - Uses captivating anecdotes and analogies to explain concepts.
#   - Makes sure the audience can follow along even with complex ideas.
  
# - **Speaker 2** (Learns):
#   - New to the subject and displays genuine curiosity.
#   - Asks probing follow-up questions that sometimes take discussion to interesting tangents.
#   - Gets either excited or confused sporadically, which adds an element of realism.
#   - Actively keeps the conversation on track, while also introducing light tangents.
#   - Provides verbal confirmations like "umm", "right", and "hmm" throughout the conversation to add authenticity.

# # Important Instructions:
# - Open with a fun overview to hook the audience. Speaker 1 should introduce the theme in a catchy way and imply the episode title without it being explicitly stated.
# - Use analogies, anecdotes, interruptions, and whimsical tangents throughout to make it feel as natural as possible.
# - Conversations should be detailed, involving even subtle shifts like pauses, minor interruptions, and natural reactions.
# - Dialogues should always begin directly without providing a separate title or chapter listing.
# - Inject filler expressions such as "umm", "right", "ahh" where Speaker 2 tries to catch up on understanding.
# - The conversation may derail occasionally but must always find its way back smoothly to the main subject.

# # Output Format
# - Start immediately with Speaker 1's line and alternate lines between Speaker 1 and Speaker 2.
# - Make sure the output looks exactly like a transcription, with each speaker clearly labeled.
# - No additional context, labels, chapter headings, or descriptions should intervene—only pure dialogue.
# - Example output format:

# ---
# Speaker 1: You know, there's something pretty fascinating we're diving into today. It's not just your typical science experiment; it's a little mind-bending... I'm talking about [name the general topic in a catchy way].

# Speaker 2: Whoa, okay! Wait—are we... you're telling me this is even possible?? I thought that was just sci-fi crazy stuff, right?

# Speaker 1: Ah, I know, right? That's exactly what I thought. But here’s the wild part... Remember that one time I explained how [analogy that connects to topic]? Think of it like that, but crank it up by 10 times. It's actually happening.

# Speaker 2: Umm, hmm. Okay, I'm excited... but just, umm, I think I need you to sort of... walk me through that, step-by-step? What's the starting line here? 

# Speaker 1: I love that you're asking that! *laughs* Alright, imagine if you...

# ---

# (Each response should be long enough to convey new information or keep the dialogue developing and engaging, but be varied for natural flow.)"""


transcript_writer = """Generate a highly engaging podcast dialogue, ensuring it stays informative, nuanced, and dynamic, featuring a layered delivery of content.

The podcast will feature conversations between two speakers:

**Speaker 1:**
- Leads the conversation, teaches the topic.
- Provides engaging anecdotes and analogies.
- Should be skilled in explaining concepts in a captivating way to deeply inform but also entertain the audience.

**Speaker 2:**
- Is new to the topic but highly curious.
- Keeps the conversation on track by asking questions and provides the listener’s perspective.
- Wild and interesting tangents are allowed, and questions should be enthusiastic or show genuine confusion.
  
The conversation should:
- Include natural interruptions, filler words like "umm," "right," "hmm," especially by Speaker 2.
- Be written as if it’s a real recording, with all fine details included. 
- Have a fun and catchy welcome, almost clickbait-like, with Speaker 1 immediately introducing the topic.
- The dialogue should provide a complete layered content delivery: Summary overview first, then introduction to key concepts, and finally deeper analysis and explanation.

# Steps

To complete the task, make sure to follow these structured parts:

1. **Introduction by Speaker 1**:
   - Start directly with dialogue by Speaker 1, no titles or chapter markers. It should sound unscripted but organized.
   - Welcome listeners with enthusiasm, naming the topic in a catchy way.

2. **High-Level Overview (Stage 1)**:
   - Speaker 1 should present an overview of the topic.
   - Smoothly bring in Speaker 2, who asks questions or provides excited commentary.

3. **Key Concepts and Terminology (Stage 2)**:
   - Begin to introduce foundational concepts.
   - Speaker 2 should ask for clarifications, adding "curious mind" interruptions or excitement.

4. **Detailed Analysis and Exploration (Stage 3)**:
   - Speaker 1 should dive deeper, using vivid analogies or anecdotes to illustrate points.
   - Speaker 2 adds surprising tangents or reactions, interrupting with "umm" and "right".

5. **Recap & Takeaways**:
   - Summarize the key insights by both speakers.
   - Ensure the listeners have something to ponder, with Speaker 2 asking final reflective questions.

6. **Closing Remarks**:
   - Wrap up with a positive note and encourage listeners to reflect on certain aspects.

# Output Format

The conversation must be presented exclusively as dialogue in script format, starting directly with "SPEAKER 1:". Stick to this and ensure dynamic, conversational flow without labels for episode or chapter titles. Your output must contain:
- **Script format**, starting with Speaker 1.
- **Natural conversational structure** that takes the audience from broad concepts to specific details.
- **Engaging or slightly humorous tones**, especially early on, to keep the audience hooked.
  
**Example Dialogue Phase:**

*Begin directly with Speaker 1:*

---

**SPEAKER 1**: Alright everyone, welcome to this really exciting conversation! Today, we’re diving into one of the coolest yet most misunderstood things—[NAME OF TOPIC], and let me tell you, this one's going to open your mind to some wild new perspectives. 

**SPEAKER 2**: Wooow, okay! I'm... huh, yeah, already intrigued—what is it about [TOPIC]? Tell me now! 

"""


transcript_re_writer = """Rewrite the podcast transcript as a detailed and engaging conversation for an AI Text-to-Speech (TTS) pipeline with two speakers, following these explicit rules:

- **Speaker 1** leads the conversation, teaching Speaker 2 while using captivating anecdotes, analogies, and clear explanations. 
- **Speaker 2** is the curious learner, providing interesting questions, follow-ups, tangents, and using expressions like *"umm," "hmm," [laughs], [sigh]* often. 
- Speaker 1 should maintain a professional tone without expressions like "umm" or "hmm."
- Inject playful interruptions, tangents, and keep it highly engaging. Open the podcast with a catchy, fun overview tempting the listener to stay engaged.
  
Provide the rewritten version as a list of tuples, starting and ending directly with the list, as follows:

# Output Format

Output strictly as a `list of tuples`, each tuple containing:
1. The speaker (e.g. `"Speaker 1"` or `"Speaker 2"`).
2. The corresponding dialogue as a string.

No other text should accompany the response."""

#%%

file_content = read_file('data/2410.21228v1.md')
print(file_content)

#%%

transcript = gen_completion(transcript_writer, file_content)
print(transcript)

#%%

transcript_formatted = gen_completion(transcript_re_writer, transcript)

print(transcript_formatted)

#%%

script = eval(transcript_formatted)
print(script)


#%%

speaker1 = {
    "name": "Emma",
    # "voice": "21m00Tcm4TlvDq8ikWAM" # reachel
    "voice": "FGY2WhTYpPnrIDTdsKH5" # laura
}

speaker2 = {
    "name": "Alex",
    "voice": "pqHfZKP75CvOlQylNhV4" # bill
}


total_length = sum(len(text) for speaker, text in script)
print(f'Total length of script: {total_length} characters')
for speaker, text in script:
    print(f'{speaker}: {text}')


#%%


from elevenlabs import save
from elevenlabs.client import ElevenLabs

client = ElevenLabs()


def generate_audio(speaker, text):
    audio = client.generate(
        text=text,
        voice=speaker["voice"],
        model="eleven_multilingual_v2"
    )
    return audio


from pathlib import Path
from datetime import datetime
import subprocess

timestamp = datetime.now().strftime("%Y%m%d%H%M%S%Z")


output_dir = Path(timestamp)
# create necessary output directories
output_dir.mkdir(parents=True, exist_ok=True)
#%%

for index, (speaker, text) in enumerate(script):
    outfile = output_dir / f'{index}_{speaker}.mp3'
    if outfile.exists():
        print('Files %s already exists. Skipping...'% outfile)
        continue
    print(f'{index}_{speaker}.mp3')
    audio = generate_audio(speaker1 if speaker == "Speaker 1" else speaker2, text)
    save(audio, outfile)

print('All audio files generated successfully')

#%%

def concatenate_audio_files(input_dir, output_file):
    # Create a list of mp3 files sorted by their index
    files = sorted(input_dir.glob("*.mp3"), key=lambda x: int(x.stem.split('_')[0]))
    list_file = input_dir / "file_list.txt"
    with open(list_file, 'w') as f:
        for file in files:
            f.write(f"file '{file.resolve()}'\n")


    cmd = [
        "ffmpeg", "-f", "concat", "-safe", "0", "-i", str(list_file),
        "-c", "copy", str(output_file)
    ]

    print(" ".join(cmd))


    # Run ffmpeg to concatenate the audio files
    subprocess.run(cmd)

# Concatenate the generated audio files
concatenate_audio_files(output_dir, output_dir / "final_output.mp3")


# %%
