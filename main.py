import bpy
import subprocess
import tempfile
from pathlib import Path


# Change this directory to save VOICEVOX audio files
tmp_dir = "/tmp"

# VOICEVOX local server URL
base_url = "localhost:50021"

# sequence editor
se = bpy.context.scene.sequence_editor


# text -> json file path
def voicevox_query_json(speaker, text):
  # create temporary text file (to not consider URL encoding by ourselves)
  text_file = tempfile.NamedTemporaryFile('w', delete=False, dir=tmp_dir, suffix=".txt")
  text_file.write(text)
  text_file.close()

  # query JSON file content
  url = f"{base_url}/audio_query?speaker={speaker}"
  cmd = ["curl", "-s", "-X", "POST", url, "--get", "--data-urlencode", f"text@{text_file.name}"]

  # run
  res = subprocess.run(cmd, capture_output=True)
  json_file = tempfile.NamedTemporaryFile('w', delete=False, dir=tmp_dir, suffix=".json")
  json_file.write(res.stdout.decode())
  json_file.close()

  return json_file.name


# json file path -> audio file path
def voicevox_query_audio(speaker, json_path):
  header = "Content-Type: application/json"
  url = f"{base_url}/synthesis?speaker={speaker}"
  cmd = ["curl", "-s", "-H", header, "-X", "POST", "-d", f"@{json_path}", url]

  # run
  res = subprocess.run(cmd, capture_output=True)
  if res.returncode != 0:
    print("error on VOICEVOX JSON query:", res.returncode, ":", cmd)
    return ""

  audio_file = tempfile.NamedTemporaryFile('wb', delete=False, dir=tmp_dir, suffix=".wav")
  audio_file.write(res.stdout)
  audio_file.close()

  return audio_file.name


# `frame_start`: int
def insert_voice_audio(name, speaker, text, channel, frame_start):
  json_path = voicevox_query_json(speaker, text)
  # TODO: proper null check
  if json_path == "":
    return

  audio_path = voicevox_query_audio(speaker, json_path)

  # sound sequence
  ss = se.sequences.new_sound(name, audio_path, channel, frame_start)


def main():
  # 玄野武宏
  # See also: http://127.0.0.1:50021/docs/speakers
  speaker = 11

  # target audio output channel
  channel = 4

  # iterate through selected text sequences:
  for s in filter(lambda s: s.select and s.type == 'TEXT', se.sequences_all):
    print(s.text, s.frame_start, s.frame_duration)
    # insert VOICEVOX audio
    insert_voice_audio("test-audio.wav", speaker, s.text, channel, int(s.frame_start))

  print("--> done voicevox conversion")

main()


