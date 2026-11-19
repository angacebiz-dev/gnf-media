# Toon v3 (Ricks Clips-style test, Jonah, Nov 19 2026)
- scene3.py = first 351 lines of pipeline v2 scene.py + scene3_tail.py (Blender 5.3 bpy sets: ship, storm, fish belly, beach, Nineveh)
- toon3.py = 2D toon characters; shots3.py = timeline + 48 shots; comp3.py = compositor (camera moves, effects, captions)
- voice3.py = Kokoro am_michael narration; mix3.py = music + effects, voice kept 13+ dB over the bed
Order: voice3.py -> scene3.py (bgs) -> scene3.py --anchors -> comp3.py 0 N -> mix3.py -> ffmpeg
