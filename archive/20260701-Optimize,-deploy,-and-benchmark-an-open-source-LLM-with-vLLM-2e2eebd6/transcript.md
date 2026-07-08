---
source_url: "https://www.youtube.com/watch?v=a9T9kWwpaNg"
platform: youtube
uploader: "未知"
title: "Optimize, deploy, and benchmark an open-source LLM with vLLM"
upload_date: "None"
duration: 132
fetched_at: "2026-07-01T02:07:53.259542Z"
transcript_source: youtube-transcript-api
---

[00:00:00] I'm thrilled to introduce this course on
[00:00:01] fast and efficient LLM inference, built
[00:00:04] in partnership with Red Hat, and taught
[00:00:06] by Sergey Kliger. Deploying open source
[00:00:09] LLMs efficiently, so they can serve many
[00:00:11] users at once with low latency and
[00:00:13] reasonable cost, is challenging.
[00:00:16] In this course, you'll learn how to take
[00:00:18] a large language model and serve it
[00:00:20] efficiently using vLLM, a widely adopted
[00:00:23] and very popular open source serving
[00:00:26] system.
[00:00:27] A 70 billion parameter LLM might take
[00:00:30] about 140 gigs of memory just for the
[00:00:33] weights.
[00:00:34] Additionally, the KV cache values, which
[00:00:36] store token information, also take up
[00:00:39] significant memory.
[00:00:40] So, a model like that might require
[00:00:42] multiple GPUs to serve a single request.
[00:00:46] In this course, you'll learn techniques
[00:00:47] that help you manage that critical
[00:00:49] memory [music] efficiently. For example,
[00:00:52] you apply quantization to shrink the
[00:00:54] memory footprint of the model, [music]
[00:00:56] which also speeds up how the data moves
[00:00:58] through memory.
[00:00:59] You also see how vLLM's paged attention
[00:01:03] manages the model's memory, especially
[00:01:05] the KV cache at runtime, so your model
[00:01:08] can handle many concurrent requests.
[00:01:11] Building on that, you'll learn how
[00:01:12] prefix caching vLLM uses previously
[00:01:15] computed values when requests share the
[00:01:18] same system prompt, so the model doesn't
[00:01:20] redo work that's already done.
[00:01:22] >> To put all of this into practice, you'll
[00:01:23] run the optimized deploy benchmark
[00:01:25] workflow on your own model. We'll start
[00:01:27] with quantization, where you'll learn
[00:01:29] how to compress the model without
[00:01:30] sacrificing accuracy. And you'll learn
[00:01:33] exactly what a KV cache is and why it's
[00:01:35] important, and how to serve it with vLLM
[00:01:37] and watch paged attention and prefix
[00:01:39] caching in action. And finally, you'll
[00:01:41] benchmark your deployment by simulating
[00:01:43] real-world traffic and measuring how
[00:01:45] well your model performs with metrics
[00:01:47] like latency and throughput. Along the
[00:01:49] way, you'll learn how to navigate the
[00:01:50] tradeoffs between speed, cost, and
[00:01:52] accuracy that come with every deployment
[00:01:54] decision.
[00:01:55] >> The techniques you learn in this course
[00:01:56] are what power efficient LM serving in
[00:01:58] production today. And you also learn
[00:02:00] about VLMs, which is an important piece
[00:02:03] of AI infrastructure today. So, I hope
[00:02:06] you enjoy the course.