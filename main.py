import bpy
import subprocess
import tempfile
from pathlib import Path


# fps = bpy.context.scene.render.fps

# base_tmp_dir = Path("/tmp/blender-voicevox-speech")
# base_tmp_dir.mkdir(exist_ok=True)

# REMARK: The `base_url` must not have whitespaces, or it is `split` on command execution.
base_url = "localhost:50021"


# sequence editor
se = bpy.context.scene.sequence_editor

# text -> json file path
def query_json(speaker, text):
  # create temporary text file (to not consider URL encoding by ourselves)
  text_file = tempfile.NamedTemporaryFile('w', delete=False, suffix=".txt")
  text_file.write(text)
  text_file.close()

  # query JSON file content
  url = f"{base_url}/audio_query?speaker={speaker}"
  cmd = ["curl", "-s", "-X", "POST", url, "--get", "--data-urlencode", f"text@{text_file.name}"]

  # run
  res = subprocess.run(cmd, capture_output=True)
  json_file = tempfile.NamedTemporaryFile('w', delete=False, suffix=".json")
  json_file.write(res.stdout.decode())
  json_file.close()

  return json_file.name


# json file path -> audio file path
def query_audio(speaker, json_path):
  header = "Content-Type: application/json"
  url = f"{base_url}/synthesis?speaker={speaker}"
  cmd = ["curl", "-s", "-H", header, "-X", "POST", "-d", f"@{json_path}", url]

  # run
  res = subprocess.run(cmd, capture_output=True)
  if res.returncode != 0:
    print("error on VOICEVOX JSON query:", res.returncode, ":", cmd)
    return ""

  audio_file = tempfile.NamedTemporaryFile('wb', delete=False, suffix=".wav")
  audio_file.write(res.stdout)
  audio_file.close()

  return audio_file.name


# `frame_start`: int
def query_at_once(name, speaker, text, channel, frame_start):
  json_path = query_json(speaker, text)
  # TODO: proper null check
  if json_path == "":
    return

  audio_path = query_audio(speaker, json_path)

  # sound sequence
  ss = se.sequences.new_sound(name, audio_path, channel, frame_start)


def main():
  # text sequences:
  for s in filter(lambda s: s.select and s.type == 'TEXT', se.sequences_all):
    print(s.text, s.frame_start, s.frame_duration)
    query_at_once("test-audio.wav", 0, s.text, 3, int(s.frame_start))


main()


# TODO: Is it OK to place the audio files in the temporary directory?

