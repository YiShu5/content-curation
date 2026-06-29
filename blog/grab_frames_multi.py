"""从一个视频里一次性抠多帧:下载低清整片一次 → 语义定位 N 个时间戳 → ffmpeg 各抽一帧。
专给单源稿配同源截图用(录屏类视频抠的是真实幻灯/演示,无标识)。
跑法:cd blog && .venv/bin/python grab_frames_multi.py
"""
import os, subprocess, tempfile, sys
from pathlib import Path
import numpy as np
import embeddings
import today_signal as T

ROOT = Path(__file__).resolve().parent.parent
YT = str(ROOT / ".venv" / "bin" / "yt-dlp")
DIR = ROOT / "archive" / "20250205-Deep-Dive-into-LLMs-like-ChatGPT-c3b687a0"
URL = "https://www.youtube.com/watch?v=7xTGNNLPyMI"
OUT = ROOT / "docs" / "images"
OUT.mkdir(parents=True, exist_ok=True)

# (slug, 用于语义定位的中文描述, 微调秒数)
FRAMES = [
    ("k-compress", "预训练本质上是对互联网的有损压缩，我们得到的是互联网的幽灵", 0),
    ("k-token", "文本被切分成token，使用字节对编码BPE，GPT-4大约有十万个不同的token", 0),
    ("k-overview", "训练分三个阶段：预训练读教科书、监督微调看例题、强化学习做练习题", 0),
    ("k-nine11", "模型分不清9.11和9.9哪个大，瑞士奶酪，在简单问题上出错", 0),
    ("k-step", "每个token只能做有限计算，复杂推理要分散到多个token，让模型一步步推理", 0),
]


def hhmmss(s):
    s = int(s)
    return f"{s//3600:02d}:{s%3600//60:02d}:{s%60:02d}"


locs = {}
for slug, phrase, shift in FRAMES:
    vec = np.asarray(embeddings.embed_query(phrase), dtype=np.float32)
    loc = T._locate_timestamp(DIR, vec)
    if loc:
        sec, snip, score = loc
        locs[slug] = sec + shift
        print(f"定位 {slug}: {hhmmss(sec)} score={score:.3f} :: {snip[:42]}")
    else:
        print(f"定位 {slug}: 失败")

with tempfile.TemporaryDirectory() as td:
    tmpl = os.path.join(td, "v.%(ext)s")
    print("下载低清整片(只下这一次)...")
    r = subprocess.run(
        [YT, "-f", "bv*[height<=720]/b[height<=720]/wv*/w",
         "--extractor-args", "youtube:player_client=android",
         "--no-part", "-o", tmpl, URL], capture_output=True, text=True)
    vids = [os.path.join(td, f) for f in os.listdir(td)
            if f.rsplit(".", 1)[-1] in ("mp4", "mkv", "webm")]
    if not vids:
        print("下载失败:", (r.stderr or "")[-600:]); sys.exit(1)
    vid = vids[0]
    print("整片到手,开始抽帧...")
    for slug, sec in locs.items():
        out = OUT / f"{slug}.png"
        subprocess.run(["ffmpeg", "-y", "-ss", hhmmss(sec), "-i", vid,
                        "-frames:v", "1", "-q:v", "2", str(out)],
                       capture_output=True, text=True)
        print(("OK   " if out.exists() else "失败 ") + slug, "->", out.name)
print("done")
