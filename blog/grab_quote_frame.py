"""从视频里抓「大佬说某句金句」的那一帧。
用法（在 blog/ 下，用 blog/.venv 跑，因为要 import embeddings/today_signal）：
  blog/.venv/bin/python grab_quote_frame.py --dir ../archive/xxx --url <yt> \
      --quote "<用于语义定位的句子，英文转录就传英文>" --out ../docs/images/x.png
定位用向量匹配转录块（复用 today_signal._locate_timestamp），再 yt-dlp 下该时段 + ffmpeg 抽帧。
"""
import argparse, os, subprocess, tempfile, sys
from pathlib import Path
import numpy as np
import embeddings
import today_signal as T

YT = str(Path(__file__).resolve().parent.parent / ".venv" / "bin" / "yt-dlp")


def hhmmss(s):
    s = int(s)
    return f"{s//3600:02d}:{s%3600//60:02d}:{s%60:02d}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--url", required=True)
    ap.add_argument("--quote", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--win", type=float, default=3.0)   # 定位点前留几秒
    ap.add_argument("--shift", type=float, default=2.0)  # 在窗口内再往后挪几秒抽帧
    a = ap.parse_args()

    vec = np.asarray(embeddings.embed_query(a.quote), dtype=np.float32)
    loc = T._locate_timestamp(Path(a.dir), vec)
    if not loc:
        print("NO_TIMESTAMP（该转录无时间戳，无法定位）"); sys.exit(2)
    sec, snippet, score = loc
    print(f"定位: {hhmmss(sec)} (score={score:.3f}) 片段≈{snippet!r}")
    at = sec + a.shift

    # android client 取低清整片（yt-dlp 原生下载器扛得住限速），再 ffmpeg 本地抽帧
    with tempfile.TemporaryDirectory() as td:
        out_tmpl = os.path.join(td, "v.%(ext)s")
        cmd = [YT, "-f", "bv*[height<=720]/b[height<=720]/bv*/b/wv*/w",
               "--extractor-args", "youtube:player_client=android",
               "--no-part", "-o", out_tmpl, a.url]
        r = subprocess.run(cmd, capture_output=True, text=True)
        vids = [os.path.join(td, f) for f in os.listdir(td)
                if f.rsplit(".", 1)[-1] in ("mp4", "mkv", "webm")]
        if not vids:
            print("DL_FAIL:", (r.stderr or "")[-700:]); sys.exit(3)
        rr = subprocess.run(["ffmpeg", "-y", "-ss", hhmmss(at), "-i", vids[0],
                             "-frames:v", "1", "-q:v", "2", a.out],
                            capture_output=True, text=True)
        if not os.path.exists(a.out):
            print("FRAME_FAIL:", (rr.stderr or "")[-700:]); sys.exit(4)
    print("OK ->", a.out, f"@ {hhmmss(at)}")


if __name__ == "__main__":
    main()
