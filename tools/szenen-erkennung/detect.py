import sys, json, time
from scenedetect import open_video, SceneManager, ContentDetector, AdaptiveDetector
path, start, end, out = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
v = open_video(path)
sm = SceneManager()
sm.add_detector(ContentDetector(threshold=27.0, min_scene_len=int(float(v.frame_rate)*0.5)))
sm.downscale = max(1, v.frame_size[0] // 320)
t=time.time()
v.seek(start)
sm.detect_scenes(v, end_time=end, show_progress=False)
cuts=[(float(a.seconds), float(b.seconds)) for a,b in sm.get_scene_list(start_in_scene=True)]
json.dump({"path":path,"start":start,"end":end,"fps":float(v.frame_rate),"scenes":cuts,"sec":time.time()-t}, open(out,"w"))
print(len(cuts), "scenes", round(time.time()-t,1), "s")
