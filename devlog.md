# devlog

- 2023-10-18
  - How can I convert text strips into audio strips?  
    Use the Blender Python API to iterate throught text strips: [Sequence Editor](https://docs.blender.org/api/current/bpy.types.SequenceEditor.html) and [Sequence](https://docs.blender.org/api/current/bpy.types.Sequence.html). Call the [VOICEVOX ENGINE](https://github.com/VOICEVOX/voicevox_engine) local server API to generate `.wav` files, then insert them with the `SequenceEditor` API.

  - Is it OK to put audio files in `/tmp` and call `new_sound`?  
    No, then they can't be loaded after deletion.

- 2023-10-22
  - I tried making a competitive programming video using Blender VSE, Whisper and VOICEVOX ENGINE: [here is the article (link)](https://toyboot4e.github.io/2023-10-22-blender-vse.html). [tin2tin/Subtitle_Editor](https://github.com/tin2tin/Subtitle_Editor) helped me A LOT. Huge thanks!

