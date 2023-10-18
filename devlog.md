# devlog

- 2023-10-18
  - How can I convert text strips into audio strips?  
    Use the Blender Python API: [Sequence Editor](https://docs.blender.org/api/current/bpy.types.SequenceEditor.html), [Sequence](https://docs.blender.org/api/current/bpy.types.Sequence.html).

  - Is it OK to put audio files in `/tmp` and call `new_sound`?  
    No, then they can't be loaded after deletion.

