---
source_url: "https://www.youtube.com/watch?v=nepKKz-MzFM"
platform: youtube
uploader: "未知"
title: "FFmpeg: The Incredible Technology Behind Video on the Internet | Lex Fridman Podcast #496"
upload_date: "None"
duration: 15502
fetched_at: "2026-06-30T00:00:50.124101Z"
transcript_source: youtube-transcript-api
---

[00:00:00] - The important is, is your
code good? We care about
[00:00:03] excellent code. We don't care who you
are. Like maybe you're a dog. I don't
[00:00:07] care, right? I don't care where you
come from. I need to look at your code.
[00:00:11] Oh, yeah, but I'm an engineer
at this very large company in
[00:00:15] Italy, in Germany, in the US. We
don't care. We care about the
[00:00:19] quality of your code because this
is what defines our community
[00:00:23] and which means that we have a lot of people
who contribute who are some very different
[00:00:27] backgrounds and very introverted.
Sure. But that's okay, right?
[00:00:31] - FFmpeg is probably one of the biggest CPU
users in the world. Everything we've just
[00:00:35] said in the past couple of minutes,
every sentence is someone's
[00:00:39] lifetime's work. There are books about
every sentence. So the level of complexity
[00:00:44] in many cases is inordinate.
[00:00:45] - FFmpeg has one hundred thousand lines
of assembly for all the codecs.
[00:00:50] - For all codecs. Mm-hmm.
[00:00:50] - And just this one has two hundred
and forty thousand. Every cycle
[00:00:55] matters. We are talking
about probably three billion
[00:00:58] devices which are going to decode
video nonstop because, for
[00:01:02] example, thirty percent of the
video from Netflix is now in AV1,
[00:01:06] fifty percent of YouTube.
[00:01:07] - This is what peak video
codecs should look like.
[00:01:11] Seventy-nine point nine percent
assembly, nineteen point six percent C,
[00:01:15] and zero point five percent other.
[00:01:18] - And what's incredible is with those tweets,
which is factual, people get crazy.
[00:01:25] - For the last two years, they go crazy.
No, intrinsics is fine. The compiler-
[00:01:28] - You can optimize your compiler.
Auto-vectorization, it's your fault. You don't
[00:01:32] understand. And we've
tried that forever, right?
[00:01:35] - For two years, and two years later,
showing hundreds of examples
[00:01:40] of handwritten assembly. No, no, no, you're
doing it wrong. The compiler can do this.
[00:01:43] The intelligence agencies tried to, like,
say, "Can you put a backdoor in VLC?"
[00:01:48] - Yes. Two of them.
[00:01:50] - Well, what did you say?
[00:01:51] - No. Well, I was a lot less polite.
[00:01:54] - Basically saying, "Hell no."
[00:01:56] - Like, if we had to compromise our software,
we would shut it down. This is clear.
[00:02:00] - Any tweets Kieran, you regret?
[00:02:04] - Tweets I regret?
[00:02:05] - Or is it like that, how does the
French song go? Regret nothing.
[00:02:08] - Don't regret anything. No, it's because
regrets are attacks on your mind.
[00:02:17] - The following is a conversation
all about FFmpeg and VLC
[00:02:21] with Jean-Baptiste Kempf
and Kieran Kunhya.
[00:02:25] FFmpeg is an open source
software system that is
[00:02:30] the invisible backbone behind
YouTube, Netflix, Chrome,
[00:02:33] VLC, Discord, and basically
every platform that
[00:02:37] touches video or audio on the internet.
[00:02:41] It can decode, encode,
transcode, stream, and
[00:02:45] play almost any video or audio format ever
[00:02:49] created. To me, it is one of
the most incredible software
[00:02:53] systems ever developed, and
it's all done by volunteers.
[00:02:59] VLC is also a legendary
piece of software. It is an
[00:03:03] open source media player that plays
basically anything you throw at
[00:03:07] it, any format, any platform,
no ads, no tracking.
[00:03:11] It has been downloaded over
six billion times, and
[00:03:15] again, for me, it has been
one of my favorite pieces of
[00:03:18] software ever, with the most
legendary logo, which I,
[00:03:22] of course, had to honor in this
conversation by wearing the
[00:03:27] VLC traffic cone hat the whole time.
[00:03:31] So again, above all else, thank
you to the incredible volunteer
[00:03:35] engineers who put their heart and
soul into this code that has been
[00:03:39] used and loved by billions
of people. Thank you.
[00:03:43] And about the two great engineers and human
beings I'm talking to in this episode,
[00:03:50] Jean-Baptiste is the
president of VideoLAN and
[00:03:54] is a key figure behind VLC and FFmpeg.
Kieran is a longtime codec engineer, FFmpeg
[00:04:01] contributor, and the man
behind the now infamous
[00:04:05] FFmpeg account on
Twitter/X that I recommend
[00:04:09] everybody follow for the memes and for the
[00:04:13] unapologetic celebration of open source
and great low-level software engineering.
[00:04:20] Let me also say that it's
inspiring and humbling that
[00:04:24] so much of modern civilization
rests on software built by
[00:04:28] people who are not chasing
fame or money, but are
[00:04:31] obsessed with the craft of engineering.
[00:04:34] We live in a world where billions of
people consume video every day without
[00:04:38] ever thinking about the invisible
machinery underneath it. But that
[00:04:42] machinery matters. Open source
infrastructure matters.
[00:04:46] It is one of the great examples of
human beings quietly collaborating
[00:04:50] across borders to build something useful,
durable, and elegant for the rest of us.
[00:04:57] And so this conversation is
not just about codecs and
[00:05:01] media pipelines. It is also
about the deeper spirit of
[00:05:05] engineering and generosity that
makes projects like FFmpeg possible.
[00:05:11] Again, I can never say
it enough. Thank you.
[00:05:16] This is the Lex Fridman Podcast. To
support it, please check out our
[00:05:20] sponsors in the description,
where you can also find links
[00:05:23] to contact me, ask questions,
give feedback, and so on.
[00:05:28] And now, dear friends, here's
Jean-Baptiste Kempf and Kieran Kunhya.
[00:05:35] So the legend goes VLC can
open everything. What's the
[00:05:39] weirdest thing that you
know that it can open?
[00:05:43] - You know, there is a ton of people
who are using VLC to record VHS
[00:05:46] videos, right? Like, it's just like you
plug it with a capture card and you
[00:05:50] can basically record VHS video.
[00:05:52] - Well, how does that work?
[00:05:53] - Basically, it's, you know, those type of
capture card where you can put a Peritel
[00:05:57] in or- ... or RCA, and you put that, and
actually VLC can play those type of cards,
[00:06:02] and there is a module which allows
to control directly some of those
[00:06:06] VCR camcorders. We support DVD
audios lately, right? We spent
[00:06:10] the summer working on
DVD-Audio support, and
[00:06:14] like there is no, no one's making any
DVD audio support. There is a custom
[00:06:17] encryption schemes.
[00:06:19] - What about Lucasfilm?
[00:06:20] - Oh, yeah, and there is of course all the
weird codecs support, game codecs supported
[00:06:23] by FFmpeg.
[00:06:25] - The one Star Wars video game, the first ten-
second opening sequence, someone has gone and
[00:06:29] implemented that and made sure that's
bit exact on one disc that existed at
[00:06:33] one time of one little
sequence in the game.
[00:06:36] - And then funnily, there was a... At
one VideoLAN conference, we made a
[00:06:40] competition to make the weirdest
and most horrible file ever
[00:06:44] ... and see if VLC could play it.
[00:06:46] - What did it end up being? What's the file?
[00:06:48] - It was an MKV file made by Derek-
[00:06:52] ... which each of the frame was
changing resolution, aspect
[00:06:56] ratio- ... rotation and it was like-
[00:06:59] - Did it work?
[00:07:00] - Yes. And there was another one where
[00:07:03] the whole video was actually animated
subtitles, right? SSA, right? So-
[00:07:08] - Yeah. I remember that, yeah
[00:07:08] - ... each, this one was-
[00:07:10] And so each frame was a black frame,
but on top of that there was a,
[00:07:14] a subtitle that was
animated for each frame.
[00:07:16] - There was a file that's a valid ZIP and a valid
MP3 at the same time or something like that,
[00:07:20] so.
[00:07:20] - So yeah, we'd made a
competition of stupid files.
[00:07:23] - And it worked. It opened
all of the stupid files.
[00:07:27] - Yes.
[00:07:27] - By the way,
[00:07:28] For people who are not familiar, I am
wearing a hat. Would it be fair to say this
[00:07:32] is the best worst logo
of all time, the cone?
[00:07:36] - Yeah, by far, right? The logo
of VLC is so iconic, right?
[00:07:40] Like we are a team with a small
number of people and the icon
[00:07:44] is known everywhere. I go to
middle of nowhere in India or in
[00:07:47] China, people know the
cone, right? And 25% of
[00:07:51] the website traffic that
comes to our main website is
[00:07:55] cone player, right? So, so many people don't
know VLC, right? They know the cone player.
[00:07:59] - That's the thing they
Google for is cone player.
[00:08:01] - Yeah. They go on Google and they put cone
player and they download VLC, right?
[00:08:05] So that's iconic. And once we tried to
change it as a joke, right? We said
[00:08:09] it was going to be a type of uh,
[00:08:12] caterpillar construction and
we said that during April 1st-
[00:08:18] ... and we had around 10,000 emails saying,
"No, don't change the logo," and so on, right?
[00:08:21] So it's so iconic, right? It's so
distinctive, right? If you want to do a
[00:08:25] video player, you're going to put a play
button on a TV, right? And that's a YouTube,
[00:08:29] YouTube logo, right? It's unoriginal.
This one is orange, right?
[00:08:33] - Yeah.
[00:08:33] - It's very bright and it's weird.
[00:08:37] - And it's ridiculous and it's absurd and it's
hilarious. It becomes meme and meme becomes
[00:08:41] culture. Yeah.
[00:08:41] - And you keep it and you know about it
and you know that in 20 years, like you
[00:08:45] still have, going to have the cones and
remember, oh yeah, that was a video player.
[00:08:49] - Yeah. And we'll talk about, you
know, the mission of FFmpeg being
[00:08:53] a kinda the archival aspect of it. So
you can think about 1,000 years from
[00:08:57] now we'll have all these videos
that only VLC can open. Humans,
[00:09:01] human civilization has already
destroyed itself multiple times and the
[00:09:05] only thing that will remain is this
like, you know, the cockroaches will be
[00:09:09] crawling around and it'll be the VLC
logo- ... with some of the archival
[00:09:13] footage that VLC can open. And the
aliens will show up and they'll press
[00:09:17] play and they'll get to see it all 'cause-
[00:09:18] - Well, really, really hope so, right? But there is also so
many memes where people say, "Well, I'm sure I can put
[00:09:22] a pancake inside my DVD drive
and VLC will play it." Like-
[00:09:25] - Can they?
[00:09:26] - No, we tried. It doesn't. Um-
[00:09:27] - Doesn't.
[00:09:28] - ... but we actually have a video
of us trying that. Didn't work.
[00:09:31] - A codec for physical reality, I don't
know what that would even look like.
[00:09:34] - There was a guy who did that, right?
He printed a small cone, right?
[00:09:38] Like the ones we distribute as
goodies and inside he put an
[00:09:41] RFID chip which was his way of
playing a movie, right? And so he-
[00:09:46] ... put this on a RFID player and when
he put that it was playing like The
[00:09:50] Last Star Wars and so on. So instead
of having like DVD boxes, he had like
[00:09:54] VLC cones all around and he plugged that
and that was like physical objects.
[00:09:59] - So the thing that we're talking
about is everything around video
[00:10:03] codecs, video encoding, video
decoding, video streaming, video
[00:10:07] player client that I'm wearing
on my head, the entire
[00:10:10] ecosystem enabling free media.
We'll talk about FFmpeg, we'll talk
[00:10:14] about VideoLAN, VLC and all
the other incredible video
[00:10:18] technology that is used probably
by billions of people. So JB,
[00:10:25] you're the lead developer behind
the legendary VLC player.
[00:10:29] Kieran, amongst many other things, you're
lead developer behind the legendary
[00:10:33] FFmpeg handle on Twitter. And both of
you have spicy opinions I would say.
[00:10:40] So today we wanna talk
about FFmpeg and VLC.
[00:10:45] For context for people who
are not aware and I'm sure
[00:10:49] basically everybody listening
to this have used these two
[00:10:53] technologies probably
regularly without knowing it.
[00:10:57] So FFmpeg underlies basically
most video on the internet
[00:11:01] including YouTube, Netflix,
Chrome, Firefox, of course
[00:11:05] VLC and countless other
video platforms. It
[00:11:08] is estimated that over 90% of video
processing workflows online and
[00:11:12] offline involve FFmpeg. VLC has been
downloaded at least 6.5 billion times. But
[00:11:22] likely that number, 'cause it's
impossible to really count the number
[00:11:26] is much higher than that.
Virtually any operating system
[00:11:30] supports virtually any media format.
[00:11:35] The limitation being it
can't open pancakes. So,
[00:11:39] Can we just lay out some of
the basics to help people
[00:11:43] understand what's involved in
all of this? So when we press
[00:11:47] play on a video player like
VLC, what happens? What--
[00:11:52] How does it go from the
file or the stream to the
[00:11:56] pixels on the screen and the sound
on the speaker? What are the big
[00:11:59] stages to be aware of?
[00:12:01] - So there are several stages, right?
The first stage is to get from
[00:12:05] an address, right, which
is the type of URL, to
[00:12:09] give you a byte of streams, right?
So this would be, for example, HTTP,
[00:12:14] file, DVD, right? You give the
path to the media, and it gives
[00:12:17] you a stream of data.
[00:12:19] - The stream needs to be cut up by what's
known as the container, the demultiplexer or
[00:12:23] demux. We'll try and keep the jargon
light throughout this, but it
[00:12:27] needs to go and start demarcating video and
audio frames. So it just gets data from the
[00:12:31] operating system blocks at a time and
needs to start cutting these frames up
[00:12:35] into compressed data. It then
needs to start doing simple
[00:12:39] parsing of the video frames- ... mainly
to figure out whether that codec is GPU
[00:12:44] decodable or needs to fall back
to software. We're very sort
[00:12:48] of used to assuming the GPU will play all
of these things. There'll be hardware
[00:12:52] acceleration. I think it's up to forty-
five percent of files are not GPU
[00:12:55] decodable. So these need to be probed.
They need to be detected. There can
[00:12:59] be variants of a given codec, some
of which are decodable on the
[00:13:03] GPU. Different vendors of GPU
might have different capabilities,
[00:13:07] so those need to be detected. So if
it's GPU capable, you pass it through
[00:13:11] to the GPU black box. So now if
there's a software fallback,
[00:13:15] that means in the beginning
is to first do deentropy
[00:13:19] coding, so removing the mathematical
coding of the bit stream. So this
[00:13:22] uses capabilities such as
Huffman coding or arithmetic
[00:13:25] coding to actually decompress the
mathematical layer of the bit stream.
[00:13:30] We then need to start reading the syntax
elements for intra prediction. So intra
[00:13:34] prediction are like still images
of the video, so your I-frames.
[00:13:40] So this works and operates in the spatial domain.
So you do your intra prediction in spatial
[00:13:44] domain. You have a residual because
your prediction isn't quite
[00:13:47] matching that of reality. So you've made a
prediction, but then there's a little bit
[00:13:51] left, and that's what's known as the
residual. This is stored in the frequency
[00:13:55] domain, and these are quantized
to decompact their space.
[00:13:59] We then need to do the inverse
transform to bring them back to the
[00:14:03] spatial domain and apply these residuals.
[00:14:05] - So a lot of the process of the
decoding is this thing is compressed.
[00:14:10] And you have to predict the
highest quality thing that's
[00:14:14] supposed to go there. I-frame- ... is the
best representation you have spatially.
[00:14:19] And then there's a lot of temporal
compression that can happen
[00:14:23] depending on the codec, and then you're
predicting. You're predicting what
[00:14:26] the reality that was captured
in this rawest form.
[00:14:29] - Yeah, because what people don't
realize is that the compression on
[00:14:33] video and audio is
[00:14:36] one hundred times, right? Like, people
don't realize how compressed we, we
[00:14:40] do, right? For audio, you move,
you compress by, when you go from
[00:14:44] normal audio to MP3, you compress
by ten times, right? When, when you
[00:14:48] move to video, you need one hundred times,
two hundred times, right? So you need
[00:14:51] to remove all the details,
but that you don't care about
[00:14:56] because all the compressions that we do, and
that's very important, people forget about
[00:14:59] that, is to be viewed by humans, right?
[00:15:02] So all the codecs, either for
audio, mimic basically how your
[00:15:06] ear works, right? And a lot
of things about, like, the
[00:15:09] response on the ear and same for
your eyes, right? And so, for
[00:15:14] example, on video, we don't work
on RGB, right? Everyone expects
[00:15:18] to work in RGB. We don't,
right? We move to YUV, which is
[00:15:22] basically one is luminance,
brightness, and the other are colors.
[00:15:26] And this matches your eyes, where inside your
eyes you have the cones and the buttons, right?
[00:15:30] With some of them look on brightness and
more on, on the other on colors, right? So
[00:15:34] we need to compress a lot, and so
we need to degrade. But in order to
[00:15:38] degrade, we need to match the human
perception, and this is why it's so
[00:15:42] difficult. And then we need
to use the maximum power,
[00:15:46] mathematical power, very complex
technologies. We move to the
[00:15:49] frequency domain, as Kieran
said. We do a ton of
[00:15:53] dequantizing, in order to get the best
compression, but it still looks good.
[00:15:58] - You're trying to compress in
order to maximize the highest
[00:16:02] quality thing for human perception.
[00:16:04] - That is correct. And this is very
important, right? Compression is not like
[00:16:08] a ZIP, right? A ZIP, you have
data in, you get data out,
[00:16:12] right? And you try with all the
ZIP compression to arrive with
[00:16:17] the limit. Here we are degrading
the signal, right? And so we
[00:16:20] need to degrade both the audio and
the video signal in the best way
[00:16:24] possible. And we can do that,
but it involves, first,
[00:16:28] a lot of theoretical knowledge
about how the eye works, but
[00:16:32] it, a lot of mathematical change,
a lot of mathematical tricks,
[00:16:36] right? For example, when you
move to RGB and you do go to
[00:16:40] YUV, for example, what
we do very often is that
[00:16:44] we scale down the resolution of the
color compared to the brightness.
[00:16:48] And most of the time, just
this without compression, it
[00:16:51] divides the size by two, but
most people don't see it,
[00:16:55] right? And so on and so
on, right? And then you go
[00:16:59] to very complex mathematical
change. So of course
[00:17:04] Fourier transforms, which de facto are
not Fourier transforms, they are like
[00:17:07] discrete cosine transform, but that's
the same idea. So frequency domain
[00:17:11] we split the video by blocks,
right? So that's why when it's
[00:17:15] wrongly decoded, you see those blocks
and badly encoded, you see those blocks,
[00:17:19] and so on, to arrive to
compression states that are
[00:17:23] insanely high, right? And each generation
of the codec is like thirty percent less-
[00:17:29] ... for the same quality, right?
And this requires amount of
[00:17:32] power of computational power that is huge.
[00:17:35] - No, no, but you should elaborate. It's
thirty percent better, but an order of
[00:17:39] magnitude, perhaps, perhaps even
two orders of magnitude more
[00:17:42] compression power. That's
the big difference.
[00:17:45] - What do you mean by compression power?
[00:17:47] - Sorry, CPU power to achieve
that level of compression.
[00:17:49] - Oh, yeah. So you have to be able to
leverage the CPU and sometimes GPU, like
[00:17:53] you mentioned. And then we should
mention that a lot of this
[00:17:56] programming is done at
the lowest possible-
[00:18:01] ... stack, whether it's C and
of course, as the legendary—
[00:18:05] ... Twitter handle re-emphasizes
over and over, a lot of assembly.
[00:18:10] - So what happens globally is that you
have an address, right? Which gives you
[00:18:14] with the operating system, a stream of bytes, a
stream of data, right? And this is the first step.
[00:18:18] And the second step arises with demuxing,
where you're going to separate audio,
[00:18:22] video, subtitle in type of different
tracks. And then on each of those
[00:18:26] tracks, you're going to decompress
them, decode them, either audio with an
[00:18:30] audio codec, video to video codec,
and subtitle to subtitle codec.
[00:18:34] And once you've decompressed those
type of things, you have raw images,
[00:18:38] raw, and then you're going to talk with
your graphics card and your screen and
[00:18:42] display that. And same for the audio, you're
going to talk to your audio card, which
[00:18:46] then is going to go in analog
to your audio speakers.
[00:18:50] - And everything we've just said
in the past couple of minutes,
[00:18:53] every sentence is someone's lifetime's
work. There are books about-
[00:18:56] ... every sentence. So
the level of complexity
[00:18:59] in many cases is inordinate. You
know, it's, it's... Every sentence
[00:19:03] has thousands of people working on this-
[00:19:06] ... in industry as a
whole, books written about
[00:19:10] it. So there's a lot of detail,
there's a lot of subtleties, there's a
[00:19:14] lot of both academic and practical
realities, both of which matter.
[00:19:20] - Uh, we mentioned codecs, but I don't
think you mentioned containers.
[00:19:24] So what, what are the actual containers
[00:19:28] for some of the stuff we're talking
about? So people are familiar with MP4,
[00:19:33] uh, MOV, MKV. So anyway, what are containers
versus the thing that goes inside?
[00:19:41] - So the container is what we call also the
muxer, right? When I say demuxing, it
[00:19:45] means decontainerizing, right?
So actually, if you look,
[00:19:49] mux means multiplexer and
demultiplexer, right?
[00:19:53] Mux and demux are those. And same, a
codec is actually coder, decoder, right?
[00:19:58] Um, and so containers are this collection
[00:20:02] of multiple tracks, right? So it's
a, what normal people call the file
[00:20:06] format, but it's a bit
more, um, subtle than that.
[00:20:10] But the most known one, of course,
is MP4, but when I started,
[00:20:14] it was AVI, right? AVI was
the, the video format from-
[00:20:17] ... from Microsoft, and
MOV, M-O-V, which became
[00:20:21] MP4, was a format from Apple.
In the open source community
[00:20:25] one of the person that is still active on
VideoLAN is called Steve Lhomme and started,
[00:20:29] This Matroska format, which is,
like, a bit more complex and
[00:20:33] more future-proof. And
there are so many others.
[00:20:38] - So, I mean, there's a, it's a pretty common
thing, and maybe it'll even happen in
[00:20:42] this conversation, that
people confuse container
[00:20:45] and the codec, right? So
confuse MP4 and H.264, for
[00:20:49] example. Is that a horrible violation?
[00:20:51] - No, it's not, because technically the
name of H.264 is MPEG-4 Part 10. Because
[00:20:59] MPEG-4 is actually a meta
specification which has
[00:21:03] several things in it,
right? There is the Part 2.
[00:21:07] so there is, like, audio codecs,
right? AAC de facto is MP4 audio-
[00:21:11] ... something. There are actually
several video codecs, right, inside the
[00:21:15] MPEG-4 specification. One
of them is MPEG-4 Part 10,
[00:21:19] called also AVC, called
also H.264. Right? So
[00:21:24] it's completely the fault of the
industry to make things difficult
[00:21:28] to understand. So that's very
difficult so that people
[00:21:31] then don't understand why sometimes
you talk about MPEG-4 Part 10,
[00:21:35] where you mean H.264,
and why it's not MP4.
[00:21:38] - So you can technically shove in all
kinds of different codecs inside
[00:21:42] containers and horribly so.
[00:21:44] - But broadly speaking, though,
MP4 is understood to generally
[00:21:48] be H.264 plus AAC audio. 99% of
the time that's that, and that,
[00:21:55] the rest are de minimis, the small effects, you
know, edge effects really compared to that.
[00:21:58] So it's not the end of the
world. There, there are people
[00:22:02] who do get annoyed by that. But also in
reality, something like VLC, just to point out,
[00:22:06] the file may say .MP4, but it may be
something completely different, and that's
[00:22:10] one of the challenges both FFmpeg
and VLC have is the real world is a
[00:22:14] completely different place to
a three- letter file format.
[00:22:17] - And this is very important to say, right?
Like, for example, in VLC and in FFmpeg,
[00:22:21] we discard the file format, right? We look
[00:22:25] into the file to understand
what's in it because so many
[00:22:28] people, like, they say, "Oh, it's a video,
it should must be MP4," but technically it's
[00:22:32] an MOV or maybe it's a MKV, right? So we
[00:22:36] analyze in real time everything that we
have, and we don't trust- ... the format.
[00:22:42] - So what information does the
fact that it's .MP4 give you?
[00:22:45] - It helps, right? It gives you a
hint, right? Just like, oh, it's
[00:22:49] finished by .MP4. I will
start first by opening,
[00:22:54] probing it with the MP4 container demuxer
[00:22:58] to see, well, it should be that. But I don't
trust it, and if I'm lost, I say, "Okay,
[00:23:02] maybe I'm going to try it." So it
bumps the priority of the module.
[00:23:06] - So how do you get to... just to
take a bit of a tangent there.
[00:23:11] You know, the dumb thing
is if you try the MP4,
[00:23:15] but it turns out it's a different
codec than you would have expected,
[00:23:19] Most players just break there.
[00:23:21] - Yes.
[00:23:22] - Yes.
[00:23:22] - And so how do you not break? There's
just philosophically, I'm sure
[00:23:26] there's a bunch of stumbling
blocks along the way where it's
[00:23:30] easy to just break and stop, freak
out. That's it. How does VLC not?
[00:23:34] - This is why VLC is popular.
But the reason is because
[00:23:38] actually VLC was, is just
a client of a streaming
[00:23:42] solution called VideoLAN
from a very long time
[00:23:46] ago, from the late '90s. And
when you're playing video
[00:23:50] which are on UDP, right, in network,
they might be damaged, right?
[00:23:54] So you don't trust your inputs, and this is
very important into the security is that you
[00:23:58] don't trust your inputs. So everything in
VLC is prepared to work with broken files.
[00:24:06] And it's a philosophical idea from
the beginning, and everything
[00:24:10] is engineered into that. And
it's a culture, right? And so,
[00:24:14] for example... And VLC became very popular
on that because a long time ago when people
[00:24:18] were pirating content which
they do a lot less today-
[00:24:23] - And none of us ever have-
[00:24:24] - No, of course not. Um— ... the metadata
to play some files like AVI is at,
[00:24:30] at the end of the file, right? And when you're
downloading, you don't have that, right?
[00:24:34] So VLC was just like, "Hey, this file is
broken, but I'm still going to try to
[00:24:38] interpret it," and this was very useful.
[00:24:41] - We hinted at the awesomeness of
the various different stages.
[00:24:45] We hinted at the awesomeness of codecs, the
depth and the richness and the complexity
[00:24:49] of everything involved there.
What— Let's try to define
[00:24:53] what is a video codec? What's
involved there? What does it mean to
[00:24:57] compress something? You
already started to hint at it—
[00:24:59] ... but can we elaborate
a little bit more?
[00:25:01] - So there's a huge amount of
redundancy in any video both
[00:25:05] spatial and temporal, and the point
of any video codec is to remove
[00:25:09] this redundant data, use mathematical
properties as part of this reduction
[00:25:13] process. So more often than not, using
several orders of magnitude more
[00:25:17] compute to compress because that's
more costly versus both costly
[00:25:21] both financially and in CPU resources—
[00:25:23] ... versus the decompression. So
it's asymmetric in that respect. Uh,
[00:25:27] often the case because compression is done
once, but there could be lots of viewers of
[00:25:31] another file. So to take that
information and compress it by
[00:25:36] 100x, 200x, removing
redundant information and
[00:25:40] using mathematical properties to make
that small, but also have properties
[00:25:44] such as error resilience.
So as, as JB suggested,
[00:25:48] VLC in the beginning was, was used
to play UDP network feeds, and UDP
[00:25:51] network feeds lose packets. And
so some of the design goals of a
[00:25:55] codec is also to be recoverable.
[00:25:58] You need to actually be able to join a stream.
It's not necessarily a file. You need to join,
[00:26:03] get on the decoding process,
and start decoding.
[00:26:06] - And, and to give a more image to people
[00:26:10] who are not familiar, right? Like, when
you're going to see any type of movie, right?
[00:26:14] You're going to see the camera is
going to pan, right, and travel. And
[00:26:18] you realize that, for example, all the
background is the same from, for, like,
[00:26:22] a minute, right? Or—
[00:26:23] ... thirty seconds, right? So you can
reuse the cloud that you see uh, on
[00:26:27] the background, you can reuse that
from a frame to another, right?
[00:26:31] And so it's, gets the more, the more
[00:26:35] memory you have, the more power, the more
comparisons you can make, right? And so
[00:26:39] the more compressed you can be.
And most of the modern codecs are
[00:26:43] basically doing that.
[00:26:44] - So just to make it even more explicit.
So what is video? Video is a
[00:26:50] bunch of pixels often RGB.
[00:26:54] You have three values, and you have
a grid of pixels, and you have,
[00:26:58] let's say, twenty-four or thirty or sixty,
[00:27:02] frames a second, and you
just have all these pixels
[00:27:05] repeating and showing different stuff-
[00:27:08] ... thirty times a second. And so
the question, the philosophical,
[00:27:12] the technical question is, how
can I compress all of that,
[00:27:17] store all of that at 100x?
[00:27:20] - Yep. Or 1,000x, right?
[00:27:22] - 1,000x.
[00:27:22] - The target is 1,000x, right?
[00:27:24] - And the goal is when you say redundancy,
what is redundant? Meaning stuff at best
[00:27:32] that humans wouldn't
notice if it was missing.
[00:27:35] - So for example, you have a picture
of a cloud, right? And from the
[00:27:39] next frame, they're still going to be the same cloud,
so it's redundant. You could just put it once and
[00:27:43] not do it, right? Or you have a
black background behind me, for
[00:27:47] example. The black is the same on the whole
picture, right? So you can say, "Well, you know, in
[00:27:51] this picture, take the pixels that
you have on the top left and the one
[00:27:55] on the top right. I'm not going to give the value.
I'm just going to tell you it's the same at the top
[00:27:58] left." And then you can
say for frame one reuse
[00:28:02] something from the previous frame or the
previous, previous frame, and so on and
[00:28:06] so on, right? So you
could... Basically, it's
[00:28:10] unlimited, but then it's limited
in terms of memory or in terms
[00:28:14] of compute power. Because, for
example, if you need to compare pixels
[00:28:17] on two hundred frames in the past on 4K
resolutions, it's a huge amount of compute.
[00:28:26] - And then when you're showing it, you have
to do the decompress of all of that.
[00:28:30] So is it the codec, the, has the
[00:28:33] encoding and the decoding is a coupled
process that you're developing?
[00:28:37] - Yes, exactly, right. And
those are two different
[00:28:41] trade-offs, right? Are you going to
compress more? But then it might be
[00:28:45] more difficult to decode. Are you going to
[00:28:49] comp- to make it a codec that is
more complex to encode and easier to
[00:28:53] decode? Are you going to make a codec that
is easier to encode because you need to be
[00:28:56] fast, but then the, the client side,
the, the player is going to spend more
[00:29:00] time? That's why you have so many
different type of codecs, is that it's not
[00:29:05] always easy. And to make it even
more complex, modern codecs
[00:29:09] like AV1, AV2, or VVC are
actually not codecs. They are
[00:29:12] a collection of tools, right?
There are multiple tools, multiple
[00:29:16] codecs in the same codec to, depending
on the image, get the more compression.
[00:29:21] - So just to elaborate, codecs like AV1, VVC
[00:29:26] have a much wider, have a wide
audience. It could be a screen share
[00:29:30] content, it could be video, it
could be animation. All of these
[00:29:34] require different coding tools. So
[00:29:38] what happens these days is a collection
of tools are put in and called
[00:29:42] AV1 and called AV2, called VVC
to allow for different use
[00:29:45] cases. So you may be on Zoom
and sharing your PowerPoint,
[00:29:49] and then you need to show the
audience a video. That codec needs to
[00:29:53] start changing its tool set depending on
the content to compress in a different way.
[00:29:59] - And like you said, there's a bunch of
incredible engineers behind each part of
[00:30:03] that, each part of the tools
that make up AV1, for example.
[00:30:06] Uh, so we've kind of danced
around it. We talked about VLC,
[00:30:10] the logo, the hat. Let's talk about
FFmpeg. What, what is FFmpeg exactly?
[00:30:17] - FFmpeg is basically the low-level
libraries for codecs, so compressions
[00:30:26] and decompression, muxers and
demuxers, and filters. It's—
[00:30:30] The core is this, and then you have
several tools which allow you to create a
[00:30:34] type of pipeline to process
any type of video files.
[00:30:38] And it's used as a
library absolutely inside
[00:30:41] everything from VLC to
Chrome to your smart TVs, to
[00:30:46] basically any video that you
see online you usually use
[00:30:49] FFmpeg. And FFmpeg in it has all those
[00:30:53] type of tools, and sometimes
depend on other libraries like
[00:30:57] x264, libvpx, and others, right? So it's
really now the de facto tool to process
[00:31:05] images.
[00:31:06] - From a philosophical level, I think
it's incredible that your home
[00:31:10] videos, your grandmother's home videos
and trillion-dollar corporations
[00:31:15] effectively are on a level playing
field using the same technology stack.
[00:31:21] It's— it wouldn't be a surprise, you
know, these big companies just have three
[00:31:24] thousand-line FFmpeg commands.
[00:31:27] There are some that use the API, but there
are some that just have long command lines.
[00:31:31] - So yeah, there's a bunch of tools,
like literally command line tool,
[00:31:35] FFmpeg, of course, FFprobe. There's libraries,
libavcodec, libavformat, libavfilter.
[00:31:43] But the FFmpeg on the command line—
[00:31:47] is, like, legendary because you
can cut— Like, there's so many
[00:31:51] parameters. You can customize
everything to hell.
[00:31:53] - It's a language. It's an actual language.
[00:31:55] - It's an actual— yeah, you could think
of it as a programming language.
[00:31:57] - Yeah, of course, I'm sure. Because— so most
of the people, they're going to take FFmpeg,
[00:32:02] file in, file out, and specify the
format, right? But you can-- We've seen
[00:32:07] thousands of characters, and we've
seen also, like, people, like, doing
[00:32:11] programming generation of command lines
[00:32:14] to make FFmpeg. There is a ton of
people who are using AI to generate
[00:32:18] command lines for FFmpeg because you have no
idea what it is. But you can do- specify so
[00:32:22] many filters right on the
command line, right? So
[00:32:26] FFmpeg is this collection of toolbox for
multimedia processing that everyone uses.
[00:32:34] And everyone that is watching your videos
is also using it, right? You're on
[00:32:38] YouTube. Well, it's FFmpeg on
the client side. Well, the your
[00:32:42] server side, on the server side. The client
side is probably Chrome. Well, you're using
[00:32:45] FFmpeg also.
[00:32:46] And you're using OBS to record. Well,
it's FFmpeg, right? You're using a ton
[00:32:50] of important, like, big box,
professional boxes. Well, it's very
[00:32:54] possible that inside some
part of FFmpeg is running.
[00:32:57] - I mean, there's like so many, just
to give people an idea, like I use
[00:33:01] FFmpeg a lot on, on everything.
Just trivial stuff like,
[00:33:06] Take a video, add an
intro video and an outro
[00:33:09] video, and fade one into
the other like what is it
[00:33:13] called? Dip to black, like
where it dips and then shows
[00:33:17] the next video and does the
same thing with audio. There's
[00:33:21] like a cross dissolve of the audio.
It's quiet, it quiets the audio and
[00:33:25] makes it loud again. And then
there's a bunch of stuff like
[00:33:29] showing the captions on
screen card, like baking the
[00:33:33] captions in. You can customize the font.
[00:33:36] You can do all kinds of layering
of audio and video. There's a
[00:33:40] million things and of
course, all of that works
[00:33:45] like magically with basically any codec.
[00:33:49] Like anything you can shove in on the
audio and the video side, it works.
[00:33:53] - But it's like if you look at, for example,
[00:33:56] you can do things that you would
do with Adobe After Effects-
[00:33:59] ... in command line on FFmpeg, right? It's,
and it's very interesting because, for
[00:34:03] example, for imaging,
there is not such tool.
[00:34:07] There is a few tools, but not
with the breadth of FFmpeg.
[00:34:10] - So ImageMagick has a similar kind of-
[00:34:13] - Yes, but you will not-
[00:34:14] - ... spirit, but it-
[00:34:14] - ... do some filters, complex filters. You
don't have the equivalent of Photoshop-
[00:34:18] in command line, right? But for video,
you have FFmpeg in command line.
[00:34:22] - Yeah. It's incredible. I mean, it's
like an example of a thing when a
[00:34:26] bunch of great people get together
and they get a vision, and they
[00:34:29] stick by that vision for many
years, which is incredible.
[00:34:33] - And the vision behind, and the
same for VLC and FFmpeg, is that
[00:34:38] we make everything that is very
complex easy to use for the normal
[00:34:44] people, for everyone.
[00:34:45] Right? Our goal is to make something
that is insanely complex technically
[00:34:49] and make it easy to use, right?
And people, they use VLC, they
[00:34:53] drop a file. They don't realize
how complex the file is, but they
[00:34:57] play it. Or, or people put any
type of thing inside FFmpeg with
[00:35:01] complex filters, and it just works
like magically, right? And people-
[00:35:05] And this is our mission, right?
Make very complex things.
[00:35:08] - We wouldn't be here and you
wouldn't be here if this
[00:35:11] required, you know, a traditional
television studio setup.
[00:35:16] It's tools like FFmpeg that
democratize this. The podcast and
[00:35:19] streaming revolution,
the YouTube revolution-
[00:35:22] was caused. You know, FFmpeg was
a big player in that because it
[00:35:26] democratized this technology that was once
in the nineties, for example, you needed
[00:35:32] equipment that cost hundreds of thousands of dollars
to do compression. It was the size of a car,
[00:35:37] and now everybody has that at almost
an exact level playing field, and
[00:35:41] that's something that's so remarkable.
[00:35:42] - It gave voice to a lot of people.
And just to clarify, we say you,
[00:35:46] you wouldn't be here, not
the human, but the podcast.
[00:35:49] - The podcast. Oh, sorry. You as a... Sorry.
[00:35:50] - I would still... VLC did not have
anything to do on a biological
[00:35:55] level- ... at creating me as a human.
[00:35:56] - But, but it's like you realize also
everything moved from text to images
[00:36:00] and images to video, right?
[00:36:02] Look at social networks. Video
is everywhere. It's the most
[00:36:05] powerful medium there is,
right? And when you see
[00:36:09] shorts and, and in Reels
and in TikTok, right? It's
[00:36:13] amazingly powerful to
give... Video is amazing for
[00:36:17] that, right? But the
complexity is important.
[00:36:20] - This is what people don't realize.
I mean, this is really it
[00:36:24] gave power to the individual all
across the world. That's real
[00:36:28] freedom. And I think, I can't believe
it, but we still haven't mentioned the
[00:36:32] actual obvious thing for people
who are not familiar, which
[00:36:35] it's open source, and
there's a open source
[00:36:39] community of users and
developers behind it. So
[00:36:43] it's really, it's a movement. So,
like, we'll talk a bunch in a
[00:36:47] bunch of different ways about the community
behind it. But can you speak to the open
[00:36:51] source element? So when we say what is
FFmpeg, it's an open source project.
[00:36:57] - Yeah. So FFmpeg, VLC,
x264, VideoLAN, everything
[00:37:01] we do is fully open source. And for the
people who don't understand how open
[00:37:05] source is, my usual analogy is about
a chocolate cheesecake, right? Um,
[00:37:09] usually for you, when you want to buy your
cheesecake, you go to a bakery, they give you the
[00:37:12] cheesecake. The other one way of
having a cheesecake is have your
[00:37:16] grandma give you a recipe of how to
make that. When we do open source,
[00:37:20] we give you the chocolate cake,
and we give you the recipe to
[00:37:24] actually remake the same cake,
but at the same time tell you how
[00:37:28] to build the oven and also
how you're allowed to modify
[00:37:32] the recipe and resell it to someone else.
[00:37:35] And this is because software is
just a very long recipe of small
[00:37:39] instruction. Computers are not
very clever. They go very, very
[00:37:43] fast. So a normal program has
tens of billions of instructions
[00:37:46] instead of the tens when you
have your chocolate recipe. So
[00:37:50] a lot of the software industry was
about selling software, like where you
[00:37:54] just have like the final
cheesecake. In open source, we
[00:37:58] give you everything, and
that managed to get a
[00:38:02] lot of people work together, right? Because
then you decide that you're going to
[00:38:06] make the best program, the best
recipe for video, and you create
[00:38:10] communities. In FFmpeg, since the
beginning of FFmpeg, probably
[00:38:15] two thousand to three thousand-
[00:38:17] - In the thousands, yeah
[00:38:17] - ... people have contributed from the beginning,
right? And then it's exactly like the
[00:38:21] Linux kernel, right? The Linux kernel
has probably ten thousand people
[00:38:24] contributing everywhere, and
they get together, well,
[00:38:28] mostly online, right? So they
virtually get together to create the
[00:38:32] best tool for something. And on
FFmpeg and VLC, it's just like,
[00:38:38] well, this codec doesn't work, so I'm
going to work on the codec, and I'm going
[00:38:42] to add the support for this file
inside FFmpeg, so it will be
[00:38:46] beneficial to everyone. Because again, we
work for the greater good. We work for
[00:38:51] everyone, and that is what open source is.
[00:38:54] - And we should mention,
depending on the licensing,
[00:38:57] You could probably build a billion-dollar,
maybe even a trillion-dollar company
[00:39:04] around basic... as a wrapper to...
[00:39:07] - Well, yes- ... people do.
[00:39:09] People do, right? There was a
lot of problems with mostly,
[00:39:13] Cloud providers who are basically
running some open source tools,
[00:39:17] In the cloud and just give you the API to
[00:39:21] access to that. And there was a lot of um,
[00:39:25] databases like Mongo or Elastic
who changed their license in order
[00:39:29] to avoid those type of scenarios.
[00:39:31] - This is a question we get a lot in
FFmpeg is, "Why don't you do that?"
[00:39:35] And you can't. We have, we have thousands of
contributors, some of whom aren't even alive anymore.
[00:39:40] It would need all of their agreement to
do that, and JB will go maybe a bit later
[00:39:44] and talk about how challenging that
process was in VLC to do the re-licensing.
[00:39:49] - The license is a social contract
in terms of Rousseau de
[00:39:53] facto of the community. The community does
[00:39:57] not agree on much beside
the license. People go
[00:40:01] around, discuss around because
of the license, and that
[00:40:05] also allow those license fork, right?
Sometimes the community splits, but
[00:40:09] it's possible because of the
license and to merge back.
[00:40:12] And we've seen that so many
times, right? GCC and GC,
[00:40:15] And EGCS in the past. We have
seen, for example, all the web
[00:40:19] browsers, right? They started as web,
like KHTML, which becomes WebKit and
[00:40:23] then which becomes Blink,
right? So open source
[00:40:26] license is like the core of the community
[00:40:30] and people are coming from all around the
world, very different type of religion,
[00:40:37] Political borders. They work
[00:40:41] in the same way on a project
to solve a specific problem,
[00:40:45] and the specific problem we're working on
is to make multimedia easy for everyone.
[00:40:50] - Uh, looking it up on Perplexity here, looking
at the different open source licenses.
[00:40:54] Most major open source licenses
fall into two buckets:
[00:40:58] permissive, very few conditions,
and copyleft, share-alike
[00:41:02] requirements for derivatives. Below
is a brief practical summary of the
[00:41:06] main ones you'll see in the wild. MIT
license, BSD, ISC, Apache, GNU GPL, GNU AGPL.
[00:41:20] Where's LGPL? Yeah, LGPL. Let's see.
[00:41:23] There's the Mozilla Public License.
There's Eclipse Public License. It
[00:41:27] goes on. There's a lot of variety.
I mean, I think the really popular
[00:41:31] ones is MIT, GPL, LGPL-
[00:41:34] - Yeah. And BSD. BSD
[00:41:36] - ... and BSD, Apache. Sometimes you'll see-
[00:41:38] - Apache as well
[00:41:38] - ... Apache. Unlicense, that's an option. Attempts to
dedicate code to the public domain with a fallback
[00:41:42] permissive license.
[00:41:43] - There are many licenses for many different
things. What people don't understand
[00:41:47] that public domain is something that
doesn't exist worldwide, right?
[00:41:51] So it's all the open source licensing
[00:41:55] use the copyright law, right, the
international copyright law, in order
[00:41:59] to give rights on how you
use the software or how you
[00:42:03] modify. It's de facto a copyright license
[00:42:06] contract that you give to the end
user or to the developer. And
[00:42:10] so you have like the first one, which
are basically very permissive, MIT, BSD.
[00:42:14] You give the code and basically
you do whatever you want, right?
[00:42:19] You take it, you want, you modify,
you do what you want. And this
[00:42:23] is popular for JavaScript and the
type of BSD operating system.
[00:42:29] - So some of them, one of the parameters
is whether they require attribution,
[00:42:33] meaning if you use the
code, you have to say-
[00:42:35] - Yes. So in those types of permissive
licenses, some you need to say if you
[00:42:39] use it, which is called attribution,
and some you don't. And then there is
[00:42:43] the other part of license
which are copyleft,
[00:42:46] where you need to give
back to the community your
[00:42:50] modifications and with
different strings attached.
[00:42:53] some weak copyleft license,
like the Mozilla Public
[00:42:57] License, to some which
are a bit stronger like a
[00:43:01] GPL, or even very strong
like AGPL. So all of
[00:43:05] those are different types of
licensing that depends on what
[00:43:09] your goals are and how you want to structure
your community, which is why I spoke about
[00:43:12] social contract, because this is
very important to understand.
[00:43:16] FFmpeg and VLC are mostly GPL or
LGPL. The Linux kernel is GPL
[00:43:24] but Android is Apache. A ton of JavaScript
frameworks that are using are mostly MIT.
[00:43:32] All the BSD kernels, OpenBSD, NetBSD
are of course BSD. And so it's
[00:43:39] philosophical change on how you want
people to contribute back- ... basically.
[00:43:44] - So I think you talked about that,
you've moved at one point from GPL to
[00:43:52] LGPL on certain parts of the project.
What... Can you describe the difference
[00:43:55] between the two, and what does it take to
move to, I guess, a more permissive...
[00:44:00] So that direction is more permissive.
LGPL is more permissive than GPL.
[00:44:04] - Yeah. So you have to realize
that you can always go from
[00:44:07] more permissive to less permissive,
right? Because of course,
[00:44:12] those licenses are basically
statements, and so if you restrict,
[00:44:16] you can always restrict more, right?
So in a GPL project, you can take
[00:44:20] MIT code, but you cannot do the
opposite, right? Because they are more
[00:44:24] constrained to match. Indeed,
in fact, I changed the core
[00:44:29] of libVLC, which is the engine
of VLC- ... from GPL to LGPL.
[00:44:37] And there were two reasons to do that.
The first one is that so people can
[00:44:41] use the VLC engine, libVLC, into
[00:44:45] third-party applications. So a lot of
applications which are playing video
[00:44:49] on your phone or on your tablet
are actually VLC engine in it-
[00:44:52] ... which is calling FFmpeg
in it. Um, so that was
[00:44:57] one of the ways to create one of the companies
I created, which is doing consulting
[00:45:01] and integration of those types of
applications where you integrate VLC
[00:45:05] into third-party solutions
like inside game engines or
[00:45:09] stuff like that. With GPL, you couldn't do that
because that means you needed to open source
[00:45:13] everything, and those are for a lot of,
like, commercial companies who don't want
[00:45:17] that.
[00:45:18] - So you can create a company with LGPL,
you can create a company around it.
[00:45:22] - Yes.
[00:45:22] - You can do a commercial thing.
You don't have to open source it.
[00:45:24] So that's a big, big leap.
[00:45:25] - So you could play video in your game.
[00:45:27] - Yes.
[00:45:27] - The problem is I'm a game developer,
and I want to play some videos-
[00:45:32] ... and I don't want to be forced to open source
the entire game just to play those videos.
[00:45:36] So that's where the consulting
business, the libVLC LGPL-
[00:45:40] ... allows you to do that. The LGPL,
the library GPL as it used to be known,
[00:45:43] allows you to do that.
[00:45:44] - And FFmpeg is exactly the
same. It force... LGPL
[00:45:48] forces you to give back what you
change on this component, this-
[00:45:52] ... library, which is
why it's library GPL.
[00:45:55] And so you can use FFmpeg
as LGPL into, like,
[00:45:59] any type of application, even non-open
source, but you need to give back the
[00:46:03] modification you did on
FFmpeg. Same on libVLC.
[00:46:06] - Is it limiting from an open
source perspective to go GPL?
[00:46:10] Because if you-- if your library, if
your code is GPL, it means you're not...
[00:46:17] You're basically discouraging
companies from building a business-
[00:46:22] - Yes
[00:46:22] - ... around it, right? Is
that, is that fair to say?
[00:46:23] - It depends on the company, but the
company whose business model requires
[00:46:27] the source, the application to be
closed source, yes, it's limited.
[00:46:32] So that's why, for example, I moved
to LGPL. The second reason is a,
[00:46:35] a bit more obscure, is that the
terms and conditions of the,
[00:46:39] App Store, the Apple App
Store for iOS makes it very
[00:46:43] complex to have GPL application
on it, while it's easier to have
[00:46:47] LGPL applications on it. So
VLC on Windows and on Mac,
[00:46:52] And on Linux is GPL. The core is LGPL.
[00:46:55] But on iOS the iPhone
version and the Apple TV
[00:46:59] version is a type of different
license called the MPL.
[00:47:03] And yes, I went and changed the
license and it was a long story.
[00:47:08] - Yeah. So I think basically to change
the license you have to contact all the
[00:47:12] contributors.
[00:47:12] - Yes. It's very important to
understand that open source
[00:47:16] projects are what we call
in the US copyright law
[00:47:20] joint work, or in civil law collective
[00:47:23] works or collaborative
works, is that you work all
[00:47:27] together in terms of the same goal, and then
you create one software, which is one release.
[00:47:32] But the copyright is kept
by all the individuals.
[00:47:36] Some open source projects don't do that. They force
copyright assignment, but this is not what we do.
[00:47:40] We're communities. So everyone
has basically copyright on what
[00:47:44] they changed. And this
copyright stays even
[00:47:48] if at the end your contribution
was deleted because the new
[00:47:51] contribution was based on your previous
one, right? So if you want to properly
[00:47:55] re-license, you need to find all the
contributors. And at that time, I
[00:47:59] had to contact more than three
hundred and fifty people. And
[00:48:03] sometimes, well, they're just an email, right?
So it's... you need to actually track down.
[00:48:07] I actually, like, travel to
some place to go someone that I
[00:48:10] was like, sorry, that I'd
found online to see a-- to
[00:48:14] go to their job and say, "Well, you
licensed that. Can you-- do you
[00:48:18] want to change from GPL to LGPL?" Most of the
times they don't even care. They wanted to
[00:48:22] help VLC. But also it brought
me to very complex situation. I
[00:48:26] arrived to the work of a person
who was a factory worker.
[00:48:30] Um, and I said, "Well, I
need to you to sign that,"
[00:48:35] because it was his son who died who
actually wrote the code, right?
[00:48:40] So I had to explain all those
type of open source meaning,
[00:48:43] and no, I was not a company trying
to rip out the two line or five
[00:48:47] line that that guy did-
[00:48:49] ... but was useful, and the whole
community agreed on that, and he had
[00:48:53] no idea I was a factory worker. This com--
And I was a lot younger, right? Like
[00:48:57] it was fourteen years
ago, and like, like I was
[00:49:01] almost in tears, right? It's very difficult,
right? We are talking about lives of people and
[00:49:05] he explaining, and we went talk
about the photo of this guy, right?
[00:49:09] So it's important to do it
right and to do it correctly.
[00:49:13] But yes, that means tracking down everything
because every contribution works.
[00:49:18] There are some project who don't respect
that, and we do re-licensing a bit, like,
[00:49:22] aggressively.
[00:49:23] But as I said, it destroyed the whole
heart of the community because it's-- we
[00:49:27] only agree on the, on the
license, so that's important.
[00:49:31] - I would emphasize the community is
such a wide-ranging group of people.
[00:49:35] There's people in the Syrian war zone
with electricity part-time. There's,
[00:49:41] there's all people from all walks of life-
[00:49:44] ... rich, poor, young, old. So
it's quite remarkable to get,
[00:49:50] you know, a group of people aligned
on something. And that's an
[00:49:54] achievement in itself.
[00:49:55] - Yeah. It's incredible. And a lot
of them are introverts, so you
[00:50:00] coming to find them and getting them and
getting them to answer an email might
[00:50:03] be quite difficult.
[00:50:05] - Most of us are introverts, right? You
need to be more precise. You have
[00:50:09] extremely introverts, extremely, extremely
introverts and introverts, right?
[00:50:12] It's just like a whole spectrum of
different people. It doesn't matter. The
[00:50:16] important is, is your code good?
[00:50:19] Is your code great? Is your technology
great? We care about excellent code.
[00:50:23] We don't care who you are. Sorry, it's
just like we have no idea to check.
[00:50:28] We cannot check, right? Like, maybe
you're a dog. I don't care, right?
[00:50:32] I don't care where you come from. I
need to look at your code. And this is
[00:50:35] important because people don't understand that,
and they come to the community and send them some
[00:50:39] patches, and they get rejected,
and they don't like that because,
[00:50:44] I mean, you're just like, "Sorry, it's not
up to our standards." "Oh, yeah, but I'm
[00:50:48] engineer at this very large
company in Italy, in Germany,
[00:50:52] in the US." We don't care. We care
about the quality of your code
[00:50:56] because this is what defines our
community, and which means that we have a
[00:51:00] lot of people who contribute who are
some very different backgrounds and,
[00:51:04] and very introverts, sure.
But that's okay, right?
[00:51:07] - So one of the legends of
the community is of course,
[00:51:11] Linus Torvalds, who created Linux and is
[00:51:15] a longtime maintainer of
the Linux kernel. As the
[00:51:19] legend goes, he can be pretty harsh
on this meritocratic process of
[00:51:23] reviewing the code and saying it's
not good enough. Can you just speak
[00:51:27] to the legend of Linus Torvalds?
[00:51:29] - Linus is one of a kind, right? And
[00:51:33] I would even go and say that what he did
on Git is more interesting than what he
[00:51:37] did on the Linux kernel.
[00:51:39] He's very harsh, but what people
don't see is usually when he's
[00:51:43] harsh to, it's people who are
maintainer of part of the
[00:51:47] kernel, right? So they know him,
right? So he's not very harsh like
[00:51:51] that to everyone. The thing is,
what he created in his room
[00:51:55] is basically powering every
server online, right? Even
[00:51:58] at Microsoft cloud called Azure,
I'm quite sure seventy, eighty
[00:52:02] percent of the servers are running Linux.
All your Android phones are running
[00:52:06] Linux. What he did with the
power of open source, sure,
[00:52:12] is amazing. And yes, the
quality of the Linux
[00:52:15] kernel is very high, and
yes, it's difficult, but
[00:52:20] we cannot compromise on that.
We cannot compromise on quality
[00:52:24] because in the end, and you have
to understand that, is the core
[00:52:28] community of VLC is five people. The core
community of FFmpeg is ten to fifteen,
[00:52:34] and we are the ones who are going
to maintain your code, right?
[00:52:38] Because one thousand contributors in
the timeline and just ten staying, it's
[00:52:42] one percent chance that someone
comes and stays. One percent.
[00:52:46] So you will have change of job, change
of wives, you have children, you
[00:52:50] have accident in life. You're going to
change jobs, whatever. You're not going to
[00:52:54] come back. It's most likely. So we are
the one going to maintain your code.
[00:53:00] It needs to be maintainable.
It needs to be excellent.
[00:53:05] And yes, sometimes that means that you need
to rework your work because it was good, but
[00:53:09] it's not excellent, and we need
excellence because we are very
[00:53:12] few to maintain something that
is critical for the whole.
[00:53:15] - But we should also mention that there is
some spiciness, some harshness to the
[00:53:19] language that's sometimes used when you're
keeping this high bar of excellence.
[00:53:25] Is there something to say to that?
[00:53:27] - It's, it's true, right? It's also the
fact that, for example, what we're doing
[00:53:31] is low level. It's extremely
technical. You get into this
[00:53:35] community. The tone gets very like
[00:53:39] a type of-- It's a subculture, right? So
people who arrive from the external are
[00:53:43] basically not known to the
subculture. Most of those people
[00:53:47] around FFmpeg and VLC, we do
VideoLAN DevDays, VDD every,
[00:53:51] every year. They are so fun in
real life, and they love it.
[00:53:54] But it's true that you're online
and sometimes, like, the tone, you
[00:53:58] don't realize how it is. But that's okay.
[00:54:01] - It's a culture. I mean, you get this in
the gaming culture. There's pretty harsh,
[00:54:04] intense, the way people
communicate, and it's-- everyone
[00:54:08] understands that the way you show love
and respect just looks different in
[00:54:11] different communities. Sometimes
people... It depends. If it's a
[00:54:15] book club, usually people are going to
be much sweeter. If it's an open source
[00:54:21] project that's very high stakes
and used by millions of people-
[00:54:24] - But it's very not often insults
that you see, for example,
[00:54:28] in the gaming, right? And so
Linus' tone is a bit unusual
[00:54:32] even for the open source community. It's
more like it's more harsh on the results,
[00:54:36] saying, "No, this is not good. This is crap."
Those type of things that you will see.
[00:54:40] - Try not to make it about the
person, make it about the code.
[00:54:42] - Yes.
[00:54:43] - It's very, very matter of fact, and I think
you've got to look at it in terms of, you know,
[00:54:47] the famous FFmpeg is developed almost entirely
by volunteers, and that's true, and you've got
[00:54:51] to imagine someone's done a hard day's
work at their day job. They come home.
[00:54:56] You know, terseness might be a thing, you
know, it... And that's not something to take
[00:54:59] personally.
[00:55:01] - You're tired, you're busy, but you still
care about this open source stuff.
[00:55:05] But you may not be able to explain and
handhold someone on every subtle detail.
[00:55:10] - And also you have to
[00:55:12] realize that most people don't
speak English as native language.
[00:55:16] And this is especially for
open source projects like
[00:55:20] FFmpeg and VLC, which are mostly
centered out of Europe. Sometimes like
[00:55:26] people who are from the US
or, or just like are very
[00:55:30] not happy about the tone, but most of the time
it's also like they don't know better, right?
[00:55:34] It's difficult. The language is-- English
is a difficult language. There is so many
[00:55:37] subtleties and tone and so on
that you don't have, right?
[00:55:40] So often it's also difficult in
those type of community about like
[00:55:44] different cultures and languages.
[00:55:46] - So as the legend goes, JB, you repeatedly
turned down millions of dollars to keep
[00:55:54] VLC open source free for
everyone without ads.
[00:56:00] So take me through the reasoning
behind that decision of
[00:56:03] leaving millions of dollars on the table.
[00:56:06] - Yeah, that's like almost a
meme, right, on Reddit or-
[00:56:09] - There literally is a meme on Reddit.
[00:56:11] - 9GAG and yeah, yeah. See, there's-
[00:56:14] - You looking like a wizard in the,
in the VLC hat on Reddit. This
[00:56:20] is JB, the creator of VLC
media player. He refused
[00:56:24] tens of millions of dollars in
order to keep VLC ads free.
[00:56:28] Thanks, Jean-Baptiste Kempf. You
can even summon him on Reddit.
[00:56:33] - Yeah. And usually if you see, right, it's
usually like people tag me, right? And,
[00:56:37] and then there is me, and then
like I say, "Good morning."
[00:56:40] I got twenty-four K upvotes, which is great,
right? My karma on Reddit is amazing,
[00:56:44] at least on that account.
So the question is,
[00:56:49] needs to be answered first, what is
the story about VLC, right? Because
[00:56:54] yes, this is true, I refuse
[00:56:57] dozens of millions of dollars, yes,
several times. Yes, I could be a
[00:57:00] multimillionaire and be
somewhere on the beach. Um,
[00:57:03] but I did not do it because
I thought it was not
[00:57:07] moral and it was not the right thing
to do. And this is very important for
[00:57:11] myself, is to be like,
I work for the greater
[00:57:14] good, I work for people, and I don't
want-- It's not just by myself.
[00:57:18] But the reason is also because
I did not feel that I'm
[00:57:22] completely legitimate to do that,
and let me explain you why. VLC
[00:57:26] story is a very weird story. In France,
[00:57:30] we have university and we
have a type of top colleges
[00:57:34] and those top of excellency
schools are engineering schools,
[00:57:38] business schools, and
basically lawyers and medical,
[00:57:42] right? But they're outside of
university, and in order to enter those,
[00:57:46] you spend two years working
like crazy math, physics to
[00:57:50] enter those best engineering schools.
[00:57:53] One of the schools is called the École Centrale
Paris. It has changed name since, but it was
[00:57:57] called the École Centrale Paris.
And because it was Centrale, they
[00:58:01] had to move it because it was too small
after the World War II and, and they moved
[00:58:05] it, they wanted to move it to the center of
France in a place called Clermont-Ferrand.
[00:58:09] And the alumni decided that
this was not okay, right? It is
[00:58:12] a, the school that Eiffel, right,
the, the one who did the Eiffel
[00:58:16] Tower, attended to, right? So they said, "No,
no, we are amazing, great school. We cannot
[00:58:20] do that." And so they bought a piece
of land south of Paris very near
[00:58:24] Paris. And it was a campus managed
by a nonprofit of the alumni, okay?
[00:58:32] Because of that, everything on the
campus was managed by students. The
[00:58:36] university did nothing, right? So radio,
TV, supermarket, library defining who was
[00:58:44] going into which rooms. Everything
was managed by the students.
[00:58:48] - That's amazing. That's an amazing
experiment, that it all, all
[00:58:52] didn't go to hell quickly.
It somehow flourished.
[00:58:55] - It worked great, and I
learned so much in my life
[00:58:59] doing those side activities, right? Because you're
twenty-two and you need to run your campus,
[00:59:03] else you don't have electricity, right?
[00:59:05] So you care about that, right?
But anyway, in the '80s they
[00:59:09] did a full experiment of deploying
a network mostly sponsored
[00:59:13] by IBM and 3Com, which
was a token ring network.
[00:59:17] So token ring is something
that probably almost no one
[00:59:21] knows about anymore. It's a
networking technology where
[00:59:25] you don't have routers, right?
[00:59:26] Everyone is linked. It's type, like
really a ring, and when you want to
[00:59:30] send a message, you talk to your neighbor who's
going to put the message to the next one,
[00:59:34] who's going to put the
things to the next one,
[00:59:37] in terms of ring. The issue with token
ring is, of course, is that it's
[00:59:41] very slow because every computer
on the network needs to
[00:59:45] open the message, see if it's okay.
Is it for me? No, it's not, and
[00:59:48] then send it back, like a token
which is traveling around the ring.
[00:59:53] In the '80s, you're doing some
Telnet and sending mails as
[00:59:57] university. That's okay,
right? But starts the '90s,
[01:00:01] and the '90s and start video
games, and when you have high
[01:00:05] latency in video games, basically you die,
right? So in nineteen ninety-four, nineteen
[01:00:09] ninety-five, around Doom and Duke Nukem
coming around, they want a faster
[01:00:12] network. So the students go and see
the university and say, "You know
[01:00:16] what? We want a faster network. We
need to work," which, and also play
[01:00:20] video games. And the university
tells them that basically,
[01:00:24] "Oh, I'm sorry, we cannot help
you because you understand the
[01:00:28] campus is not ours. You manage it, so
[01:00:31] do something. And you should see
some basically partners of this
[01:00:35] university and basically go
away." And they go, and they
[01:00:39] actually go and see the CIO of
[01:00:43] Bouygues, which is a large French
company and who's doing some
[01:00:46] TVs in France. And he says,
"Well, you know what? The future
[01:00:50] of video is satellite." Well, today
we know it's not, but at least it was
[01:00:54] a good idea. In nineteen ninety-five, the
first satellite dish, and he says that
[01:00:59] instead of having like one satellite
dish and a big decoder for
[01:01:03] each of the students, which are one
thousand and five hundred, what about
[01:01:07] you build, like you put
an enormous dish and
[01:01:11] only one decoder, and you send the
video directly on the network.
[01:01:15] And that required a very fast
network. Today, it's obvious, but at
[01:01:19] the time was, like, the first to do video
streaming. So they built this project,
[01:01:23] which was called Network 2000.
[01:01:26] Of course, right, we are in the '90s, right?
Everything is- ... futuristic is called 2000,
[01:01:30] like—
[01:01:30] - Yeah, 2000, yeah.
[01:01:32] - And so they do the Network 2000
project. It's completely hacked.
[01:01:36] It crashes after 45 seconds. That's
okay. The demo is 40 seconds.
[01:01:40] It leaks memory. That's okay. They put
64 megabytes of RAM instead of the
[01:01:44] 8 or 16 you have, and the demo should have
stopped there. And that was the Network
[01:01:48] 2000 project by the students.
[01:01:49] - What was the format of the video
that they had to work with?
[01:01:52] - MPEG-2 because satellite is
MPEG-2 TS for transport,
[01:01:55] MPEG-2 video, and MPEG-2
audio at that time.
[01:01:59] And the project should have stopped there.
Everyone was happy. They had, like,
[01:02:03] amazing ATM network at 155 megabits per
[01:02:07] second. They had probably one of the
best network in Europe at that time, and
[01:02:11] they stopped the project. Six months or a
year later, two students arrive and say,
[01:02:15] "Well, you know what? Maybe other
people care about video streamed on a
[01:02:19] local network," and they
create the VideoLAN project,
[01:02:23] VideoLAN. And one of them is called
Christophe Massiot, that is a good
[01:02:27] friend of both Kieran and me, and
they start the project. It's not
[01:02:30] even open source yet, and
they spend around three years
[01:02:34] to get the school to agree to
make it open source. Because the
[01:02:38] university wanted to get some--
because of the IP and copyright of
[01:02:42] the students, wanted to basically
monetize these MPEG-2 decoders.
[01:02:47] - Just to be clear, so what was the main
application, streaming on a local network?
[01:02:50] - It was streaming on a local network.
[01:02:52] - By the way, that's just, like, to state the
obvious. This is before YouTube. This is before-
[01:02:56] - Ten years before YouTube. You
have a Pentium 60 or 75, right?
[01:03:00] You, the main machine was
486DX at 33 megahertz, right?
[01:03:04] - Bear in mind, television was the main
form of video at the time. You could
[01:03:08] get new channels. In the '90s, having even
one new channel when you grew up with four
[01:03:12] channels, having a fifth or a
sixth was a big deal, and so
[01:03:15] having this satellite
service with, you know,
[01:03:19] dozens, even hundreds of
channels was so groundbreaking.
[01:03:22] - Especially because this is university where you
had a ton of different nationalities, right?
[01:03:26] So there was a ton of people who wanted...
So the-- in the end, they had, like,
[01:03:30] several dishes on different types of satellites,
right? Because, for example, a lot of people were
[01:03:33] coming from the Maghreb or the
Middle East and they, so they went
[01:03:37] to different types of satellites.
Anyway, the solution worked great,
[01:03:43] and they started the VideoLAN project.
The VideoLAN project has several
[01:03:47] and some are completely crazy
solutions, like one how to
[01:03:51] create multicast on a unicast
network, but let's not come
[01:03:55] to that. It's too, too complex. But
VideoLAN client part is what became VLC.
[01:04:03] Actually, they basically strong-armed the
university to force it to open source
[01:04:07] because university did not understand
that. And in 2001, it's still early.
[01:04:11] But basically, yes, the
university agreed early 2001
[01:04:15] to make it open source. I joined
the project in 2003 because that's
[01:04:18] when I joined the university.
So the first thing is
[01:04:22] I'm not the one who created VLC
because actually no one did, right?
[01:04:26] - Just kind of naturally emerged from the VideoLAN
project. And we should mention that, like,
[01:04:30] again, you said it just, but
to make it clear, VideoLAN,
[01:04:35] As what it became was at the
time was a set of technologies
[01:04:39] around video, and the VLC, what you
called the client, that's the thing
[01:04:43] that most normies, uh-
[01:04:47] - That is correct, and
[01:04:48] - ... think of, like, as the thing, which is,
like, the thing that pops up when you click on a
[01:04:52] video and you play it.
[01:04:53] - So I arrive in 2003, and
then I will create the
[01:04:57] open source nonprofit
organization called VideoLAN,
[01:05:01] and I took everything out of the
university to create a nonprofit
[01:05:05] project and something sustainable.
It's, yes, it's true that I spent
[01:05:09] more time than anyone on VLC
and VideoLAN. That is sure.
[01:05:13] but it's a continuity of a
previous project, VideoLAN, the
[01:05:17] student project, which is a continuity
of the Network 2000 project, which is a
[01:05:21] continuity of that and that.
[01:05:22] - I'm sure there's moments along the
way there you were thinking of, like,
[01:05:26] what is the future of this from an
open source perspective? 'Cause as,
[01:05:30] as the internet is blowing up,
and there is companies... I
[01:05:34] mean, for people who don't remember,
like, there's companies making
[01:05:37] huge amounts of money.
[01:05:39] - And I can tell you that in 2005,
the project should have died,
[01:05:44] And I made it to continue the
[01:05:48] project. At some point, we were
only two active developers.
[01:05:52] and I thought it was great
technology and was useful,
[01:05:56] and it will be useful and I
made that my life and my,
[01:06:00] my time. And I made that grow from a
[01:06:04] few hundreds of thousands of users,
millions of users to what we have
[01:06:08] now, which is probably billions
of version of VLC around the
[01:06:12] world and used everywhere. So
[01:06:15] that's a bit the story of VLC. There
is ton of very funny stories around
[01:06:19] that. Many people from
around the world working
[01:06:23] on it, like you said, in Syria or
middle of nowhere in India. But
[01:06:27] along the way, I got several
offers which were either to
[01:06:31] bundle toolbars, right? You
remember those horrible toolbars-
[01:06:35] ... which were basically
spyware, or changing your web
[01:06:39] browser or your search
engine or even, like,
[01:06:43] advertisement inside VLC.
And I didn't like that,
[01:06:47] right? I am-- and people don't
understand that. It's not-- I'm not
[01:06:51] against money, right? I'm very happy
to make money. I created several
[01:06:54] startups and one I hope that
is going to work very well.
[01:06:58] It's the fact that I believe
that you need to win money
[01:07:02] ethically. There is a right way
of doing that, and doing sneaky
[01:07:06] advertisement or stealing data
is not the correct way, right?
[01:07:10] For example, if Netflix arrived at some point
and say, "Well, we want to put Netflix inside
[01:07:14] VLC," probably the story would have been
different, right? But they didn't. The only
[01:07:18] people who came to us
were shady ads company.
[01:07:22] And if I do that, right, I would have a
ton of money, right? And then three years
[01:07:26] later, project is gone, right? Someone
forks it and something else happens.
[01:07:31] - So it's not even necessarily ads or any
of that, it's the shadiness of the-
[01:07:35] ... dishonesty of the-- So you
had a good radar, you had a good
[01:07:39] threshold of like, "No,
this compromises the
[01:07:43] spirit of what this is
supposed to represent."
[01:07:46] - But also it's for me, right?
I'm like very selfishly, I
[01:07:49] need to go to bed at night and be happy
about what I've done, right? Maybe it's
[01:07:53] my upbringing, maybe it's my parents'
fault or whatever, right? But
[01:07:57] I believe there is right and wrong, right?
[01:08:01] And this was the right
decision at the time.
[01:08:05] It still is. I want to be
proud of what I've been doing.
[01:08:08] And like, if I had sold out, I would have
[01:08:12] betrayed so many other
people who work here.
[01:08:14] - Yeah, well, I should say me
and most of the internet
[01:08:17] thank you for that decision.
It's inspiring for others,
[01:08:23] I think that are pushing the
open source movement forward,
[01:08:28] that it's okay to do these
kinds of huge sacrifices
[01:08:32] if you believe it's right. And I think in that
case it was right and it was the reason that VLC
[01:08:36] became as successful as it was, 'cause
it's an embodiment, it's a symbol of
[01:08:43] like, you know, freedom and what the
open source community can create.
[01:08:46] - Yeah, and be a service for so many people
around the world, and this is important.
[01:08:50] - We should emphasize in the 2000s it was
really normal to download a program and it
[01:08:54] secretly installs some spyware. It was
buried in very faint text or in the
[01:09:00] license text box that nobody
reads that at the bottom-
[01:09:03] ... "Oh, I will be
installing this toolbar-
[01:09:04] ... and changing all these things,"
and it was very common to have to, you
[01:09:08] know, you install a program to do
something at the time of any sort.
[01:09:11] - To put yourself in the mind of a
developer at that time, I think it's
[01:09:15] very easy, to everybody listening
to this, it's very easy at that
[01:09:19] time to convince yourself to
take a few thousand dollars-
[01:09:24] ... a few thousand dollars to do
it. To say no to much more money—
[01:09:30] ... takes guts and takes vision.
[01:09:34] - The last offer I had was obscene,
[01:09:37] and they say, "Yeah, but imagine
with all that money you could build
[01:09:41] something new, open source," right?
It was like the mind trick was,
[01:09:46] it was difficult.
[01:09:47] But for me it was just like, "No, this doesn't
work like that or this is not the right thing,
[01:09:51] so I don't do it."
[01:09:54] and again, right, it's not that I don't
like money or whatever. It's just like
[01:09:58] it wasn't right.
[01:10:01] - Well, once again, thank you from me
and from the rest of the internet.
[01:10:04] Let me talk a little bit more about
the open source movement, about the
[01:10:08] fact that, as you say over and
over and over and over, FFmpeg,
[01:10:13] is and many open source
projects are built by
[01:10:16] volunteers. So there's a
bit of drama recently,
[01:10:20] uh, Kieran, on the interwebs, on Twitter.
[01:10:25] You have a spicy style
on Twitter that I think
[01:10:28] articulates and celebrates all
the incredible developers and
[01:10:32] development and the code, especially
[01:10:36] assembly that's involved in building some
of these codecs and building some of this
[01:10:40] incredible technology. But that
brings us to the, a bit of a
[01:10:44] debacle that happened. Tell me the
full saga of what happened with
[01:10:48] the Google security engineers.
[01:10:50] - Just to be clear, Google are one of the
biggest supporters of open source out there.
[01:10:54] They have been for a long time.
It's just I think some things kind
[01:10:57] of went a bit overboard
this time. So FFmpeg
[01:11:01] itself, and this is not like a secret,
it's on the homepage, you know, the,
[01:11:05] it processes untrusted data. There
can be security issues when you parse
[01:11:09] untrusted data. That's very normal. But
recently what changed was Google started
[01:11:13] using AI to create security reports
on an open source project, FFmpeg.
[01:11:19] Volunteers had to deal with that.
They did, they provided very limited
[01:11:22] funding, and they even went to the media
first announcing how good their AI was
[01:11:27] before the issues could be fixed.
[01:11:29] - And this is in the public forum.
[01:11:31] - Yeah, this is all public.
[01:11:32] - So report, reporting an issue, using
AI to find an issue in the code,
[01:11:36] which is a security vulnerability, and then
reporting that publicly before you're able to fix
[01:11:40] it.
[01:11:40] - Yeah. It's announcing how good their
AI is, that they provided a standard
[01:11:45] 90-day industry deadline without
[01:11:48] without really understanding
the nature of volunteer-driven
[01:11:52] development. In addition, this vulnerability
was on an obscure 1990s game codec.
[01:12:00] the way-- And let's look at it from their
standpoint to begin with. Let's you know—
[01:12:04] - Yeah. Can you steer me in their case?
[01:12:06] - Yeah, sure. They have substantial resources
working on the security of open source
[01:12:10] projects
[01:12:11] that, you know, are ubiquitous, and they've
used, you know, a lot of compute to do
[01:12:15] that and very expensive and very
capable security researchers,
[01:12:19] to do that. And that's their
viewpoint is they are contributing by
[01:12:23] doing that. But I think
that's where opinions differ.
[01:12:30] it opened up a lot of interesting
fissures I would say.
[01:12:36] it does seem that there's a portion
of the security community that
[01:12:41] look at themselves a bit like building
architects that never have to go to site.
[01:12:44] You know, going to site is something that
is a little bit beneath them, the actual
[01:12:48] day-to-day construction. They're there to do
their security things and it's someone else's
[01:12:52] problem. The security
industry also kind of has
[01:12:57] a very aggressive tone towards things.
The, the language they use is extremely
[01:13:01] aggressive. They use very strong language
like, "You will get popped." So and to,
[01:13:05] Joe Public, get popped,
[01:13:07] you know, means something quite bad.
For them it means to get hacked.
[01:13:11] The way I would look at it personally is a
little bit like the padlock on your home.
[01:13:15] The padlock on your home or,
you know, the lock on your home
[01:13:21] is there to protect against the
capabilities of what it's there to protect.
[01:13:28] It's not there to protect nuclear secrets.
It's not there to protect Fort Knox. And
[01:13:33] it could be looked at that they're
using AI at a level of scale to go
[01:13:37] and pick those locks and
then say, "Hey, your
[01:13:41] lock's not secure. You need to deal with
this." Whereas actually they're the ones with
[01:13:44] resources to be able to
[01:13:48] fix this. But that seems to not be something
either they'll contribute to in terms of
[01:13:52] patches or in terms of financially. And
the scale of AI is kind of the issue.
[01:13:56] The bug reports are very
wordy. They're very,
[01:14:00] very-- It's almost a denial of
service by AI-generated bug
[01:14:04] reports on very niche codecs.
[01:14:08] and the other issue the security community
has is everything is marked high priority.
[01:14:12] You're going to, you know, "This is the most important
thing in the world, and you need to deal with this.
[01:14:15] High, high, high, vulnerable,
scary, scary, scary,"
[01:14:18] on a game codec used on one disk in 1993.
[01:14:24] And that's where the
dichotomy lies. Going around
[01:14:28] telling everyone that their padlock's not
safe, well, that's a hobby project of
[01:14:32] somebody. The safety of
that codec is consummate to
[01:14:36] what that person thinks. It's their hobby. It's
good that they're security analyzing it, but it
[01:14:40] doesn't need a big scary warning,
"This is a critical vulnerability."
[01:14:45] We also may recently also
see that there was another
[01:14:48] quote-unquote vulnerability. It
wasn't at Google in this case, but
[01:14:53] a filter could overflow and have an
integer overflow, and one of your
[01:14:57] pixels could be the wrong color. And this
was marked high, 7.5 severity in red.
[01:15:05] And at some point, the security industry
needs to realize you can't keep crying wolf
[01:15:09] like this because this just leads to people,
you know, the equivalent thereof of putting
[01:15:14] password stickers on their PC. You know,
you can't just keep crying wolf every day.
[01:15:17] And I appreciate, you know, that's their
modus operandi is to create as much
[01:15:23] scare and fear. But from the Google
standpoint, at the end of the day,
[01:15:29] they need to contribute either
financially or with patches. Google
[01:15:32] uses FFmpeg at a scale probably you
or I couldn't even contemplate,
[01:15:38] millions of CPU cores.
[01:15:40] And yes, they contribute in areas mostly
regarding their own products, so VP9, AV1.
[01:15:47] But in a wider sense,
[01:15:51] there's a disproportionate level of contribution.
Yes, they fund students. Yes, they fund Summer
[01:15:55] of Code. And I think so Alex Strange
is a former FFmpeg developer I think
[01:16:01] posting in a personal capacity.
[01:16:02] - So he posted about security engineers on
[01:16:07] Hacker News. His post reads,
"The problem with security
[01:16:10] reports in general is
security people are rampant
[01:16:13] self-promoters, in parentheses, Linus
[01:16:17] once called them something
worse. Imagine you're a humble
[01:16:21] volunteer open source developer. If a
security researcher finds a bug in your code,
[01:16:28] they're going to make up a cute name
for it, start a website with a logo.
[01:16:33] Google is going to give them a
million-dollar bounty. They're going to
[01:16:37] go to DEF CON and get a prize,
and I assume go to some
[01:16:41] kind of secret security people
orgy where everyone is dressed
[01:16:45] like they're in The Matrix.
Nobody is going to do any of
[01:16:49] this for you when you fix it." basically
commenting on the sort of the incentives
[01:16:58] for the different people
involved and misaligned.
[01:17:01] - The problem here is the
disproportion of means on discovery
[01:17:07] compared to patching it, right? And
this is the biggest issue, right?
[01:17:12] And after that debacle,
Google did some changes.
[01:17:14] - They are now starting to
send patches, which is-
[01:17:17] - And they also now have reward
tools for fixing issues. So
[01:17:21] it has changed a bit because of
that debacle. So it's good, right?
[01:17:25] But we've seen, and we talk about
Google, but we have seen like some
[01:17:29] other large companies saying, "Oh, you need
to fix this bug because it's critical in our
[01:17:33] product."
[01:17:33] - Can you explain the XZ fiasco?
The FFmpeg tweet reads,
[01:17:39] "The XZ fiasco has shown
how a dependence on
[01:17:43] unpaid volunteers can cause
major problems. Trillion-dollar
[01:17:47] corporations expect free
and urgent support from
[01:17:51] volunteers. Microsoft,
Microsoft Teams posted on a
[01:17:55] bug tracker full of volunteers
that their issue is high priority.
[01:18:02] After politely requesting a support
contract from Microsoft for long-term
[01:18:05] maintenance, they offered a one-time
payment of a few thousand dollars
[01:18:09] instead. This is unacceptable. We
didn't make it up. This is what
[01:18:13] Microsoft Teams actually
did." And then you give
[01:18:17] the image and the details and all that kind
of stuff, showing that these trillion-dollar
[01:18:21] companies are not giving much
money, not giving much support.
[01:18:24] - They think an open source project is a
traditional vendor that they have an
[01:18:28] SLA. They think a public
bug tracker is actually,
[01:18:32] you know, a third-party vendor's Jira
where you can do all of these things. It's
[01:18:36] not. It is there to report bugs.
[01:18:38] I think the thing that made
this particularly heinous was
[01:18:42] the name-dropping of Microsoft, the
name-dropping that this is a visible product.
[01:18:46] If this was just a general bug report,
I think that would have made it a lot
[01:18:50] better.
[01:18:51] - Yeah, so they literally said, like,
"This is a big deal because a lot of
[01:18:55] people are using it in
Microsoft." I wonder what
[01:18:59] happens psychologically. So I think what
happens in these companies, maybe you can
[01:19:03] correct me, is they— You're right. They
just think of FFmpeg as like a vendor that
[01:19:10] Microsoft surely is paying
a huge amount of money to.
[01:19:14] They kind of assume that
in their interaction, and
[01:19:18] nobody anywhere on the stack
is going like, "Wait a minute.
[01:19:22] Shouldn't we be giving like
millions of dollars to FFmpeg?"
[01:19:25] - And this is a very big problem in
large— Like we're talking about some
[01:19:29] companies, but it's the same
everywhere, right? A lot of those
[01:19:33] companies. Like the, when we
talk to that person, right,
[01:19:37] he was just like a manager on one
project in Microsoft Teams, right? He
[01:19:41] had never really discussed
with open source community. He
[01:19:45] had no idea, right? It
was like—but the problem
[01:19:49] is that usually there is what we call
OSPOs, right? Open source program
[01:19:53] offices in those type of companies, and
they are the ones who are supposed to
[01:19:57] discuss with open source vendors. Um,
or open source communities. But like
[01:20:03] they often don't explain that correctly
internally, right? And here it's just like
[01:20:08] we are not your supplier. If you want
me to be your supplier, I'm very
[01:20:12] happy, right? I will send you a
contract and SLAs. Like I created
[01:20:16] five companies who are doing that around
open source projects, so that's okay.
[01:20:19] - We should say that some of the
spicy tweets that Kieran, you're
[01:20:23] behind, and some of the
debacle produced results.
[01:20:28] - Yes.
[01:20:28] - Positive results.
[01:20:29] - Donations have increased substantially.
They're still not enough to
[01:20:33] cover even a single
full-time developer, but
[01:20:36] on both a, you know, awareness
level and a technical level,
[01:20:41] there's substantially more technical awareness
and sort of awareness of the importance
[01:20:45] of FFmpeg as a result, as
a result of X and what's
[01:20:48] happened. I can say, you know,
it solved its purpose. People
[01:20:52] realize the level of
importance FFmpeg has.
[01:20:55] - And on VideoLAN it's the same, right? Like
for example, a, a very simple example.
[01:21:01] For more than a year, we
couldn't update VLC on
[01:21:05] Android because of a bug on the
Play Store, on Android Play
[01:21:09] Store, right? The only way
we got someone to answer
[01:21:13] was to put a very spicy, as you say
[01:21:17] tweet saying that we are going
to stop distributing VLC
[01:21:21] for Android, right? And we have around 100
million people using that. And now then
[01:21:28] someone from Android actually came and
discussed to us, right? We had the
[01:21:32] same issue with Microsoft or,
or like saying that we were
[01:21:36] going to stop distributing
VLC on the Windows Store. And
[01:21:39] unfortunately, we are so small that the
[01:21:44] only very strong power we
have to solve those issues
[01:21:48] is blaming on social network
because it snowballs and
[01:21:52] now they listen to us. But so as
large companies often have difficulty
[01:21:57] talking to us. Like for example, VLC,
right, is probably one of the top
[01:22:01] 10 software used on Windows. I
am not part of Microsoft ISV
[01:22:08] programs, right? I don't have a point
of contact at Microsoft, right?
[01:22:12] While I'm sure any other
software, Adobe, Spotify, has a
[01:22:16] point of contact. I don't
have that, right? So
[01:22:20] raising awareness works. It's sometimes
very spicy, lot of drama. Well,
[01:22:26] X and Twitter are okay for
that, but it's efficient.
[01:22:30] - Uh, so everybody listening to this should
go follow FFmpeg on Twitter, on X, follow
[01:22:38] VideoLAN on Twitter, on X. Go
donate. Donate ... to FFmpeg.
[01:22:45] - And thank you, Lex. Over the years, several
years you've been a supporter of, you
[01:22:49] know, FFmpeg and VideoLAN on X. You know,
giving us shout-outs, appreciating,
[01:22:54] you know, what we do.
[01:22:55] - FFmpeg for life.
[01:22:57] - And for example, like Tim
Sweeney, Carmack, and a few
[01:23:00] others, like very high-level people
have raised also the awareness
[01:23:04] on our X accounts, and
that helped a lot also.
[01:23:09] - Karpathy as well.
[01:23:09] - Karpathy, yes.
[01:23:10] - Karpathy as well, yeah.
[01:23:12] - Yeah. I mean, also, you know, outside of
the fact that so many people use it, it's
[01:23:15] so impactful on the world, it's also a
great representation of a great open
[01:23:19] source project. Like the value of assembly
and C and making sure that like you take
[01:23:27] programming seriously
for real world systems.
[01:23:30] - It's not just that. We'll talk about assembly later I'm
sure, 'cause that's its whole topic in itself, but it's
[01:23:34] also celebrating people like Andreas
Rheinhardt who do maintenance. It is, I
[01:23:40] believe unpaid, as I believe as
a volunteer. He's doing massive
[01:23:43] refactorings. Uh, Andreas
Rheinhardt and Anton Khirnov
[01:23:47] rewriting ffmpeg.c with threading.
Celebrating those guys,
[01:23:51] celebrating the untold
labor that's gone into this
[01:23:55] that actually doesn't change anything from the
user standpoint. The files are exactly the
[01:23:59] same, but wow, the, the, the airplane
has been rebuilt whilst it's in the air.
[01:24:03] - Christian Garcia said, "As a teenager running
this account," referring to the FFmpeg
[01:24:07] ... account, and you responded,
"Teenagers have written more assembly
[01:24:11] in FFmpeg than Google engineers." But also
[01:24:15] just pointing out that there's a lot of
incredible contributors who are teenagers.
[01:24:19] - Like JB said, we don't care who you
are, where you're from, what you do.
[01:24:24] Teenagers have written
thousands of lines of assembly,
[01:24:28] Over the years. Give a shout-out
back in the days to Daniel Kang.
[01:24:33] So also highlighting the work of people like
Ruikai Peng. This is a 16-year-old, some of his
[01:24:37] first contributions to FFmpeg,
[01:24:40] actually doing and putting some of these quote
unquote security researchers to shame by
[01:24:44] by actually finding issues
and fixing them and being
[01:24:47] 16. There's no barriers. There's
no barriers to you have to
[01:24:51] study on, at college under this person
and understand these. It's you can
[01:24:55] learn C, and let's be honest, it's
from, it's from the K&R book. Learn C.
[01:25:00] You can learn assembly. We'll talk
about that maybe a bit later.
[01:25:03] You can contribute to
world-class technologies.
[01:25:06] - In VLC one of the oldest
contributors called
[01:25:10] Felix, he's the one doing everything
on Mac and iOS. He's starting
[01:25:14] working on VLC. He was
16. We had a guy called
[01:25:18] Edward Wong, who used to be a
Google Summer of Code student who
[01:25:22] stayed for three years
around VideoLAN. He was 14,
[01:25:26] right? And, and part of Google
Summer of Code and Google
[01:25:29] Code-in, which were programs where
basically we have students or high school,
[01:25:34] We wrote a ton of assembly
for x264 and for VLC
[01:25:38] and for FFmpeg, right? So
everyone can contribute.
[01:25:41] - And he also did a good job because
he didn't play the alarmist CVE
[01:25:45] heist, create a CVE, which is like, a
[01:25:49] public exposure of security
and do these big scary
[01:25:53] red 7.5 high priority. He
just fixed an issue in Git
[01:25:57] after three days and just fixed it.
He didn't need to go and play a big
[01:26:00] security drama about it. And I think
[01:26:03] I posted, you know, the kids are all
right. Whereas- there's, you know,
[01:26:07] there is a por- I'm not saying all security
people do this, but there is a portion of the
[01:26:10] security community, as Alex said,
that likes to hype themselves up by
[01:26:14] creating drama. They would have
happily raised, "This is a high
[01:26:18] priority CVE 8.0" or whatever on a
[01:26:22] issue that actually was in Git. It wasn't even
in a release, it was in development, and three
[01:26:26] days later was fixed.
[01:26:27] - Well, I just want to put a little bit
of love out there, even to the bigger
[01:26:34] much love and respect to Google
engineers. Like you said, they're
[01:26:39] Some of the, the best software engineers in
the world, and they do contribute a lot-
[01:26:43] ... even on the security front. And
also, you know, I'm a big fan of
[01:26:46] Theo. Much love to Theo.
He was part of this,
[01:26:50] Debacle and drama a little bit.
I think when you just zoom
[01:26:53] out on the grand arc of human history,
[01:26:57] the drama contributed positively to
everybody involved. Donations went up.
[01:27:02] It brought more attention
to the topic, allowed
[01:27:06] everybody to bicker in a way that
ultimately got them to figure out
[01:27:10] what FFmpeg is all about.
[01:27:11] - So the way we looked at this is like it's a
rap battle at the end of the day, you know?
[01:27:16] No, but it is. We say stuff, we say stuff-
[01:27:19] ... but we can, we can leave it on. X is a
perfect place for, you know, international rap
[01:27:23] battle. You say stuff. I say stuff about your
mama, but it doesn't mean, you know, I have
[01:27:27] an actual personal issue with her.
[01:27:29] Uh, and that's what it looks like. The Theo
situation, you know, JB can maybe expand, went a
[01:27:33] little bit too far and there was a little...
But, you know, it's just a bit of fun.
[01:27:37] It's just a bit of rap battle.
It's a bit, it's WWE. You know,
[01:27:40] everyone's having a bit of fun on X.
[01:27:42] It doesn't need to be taken seriously.
You know, the teenagers thing, you know,
[01:27:46] that... So that guy was a Google employee saying,
"Hey, you know, there are other ways to run
[01:27:50] an open source business." You know, go and there's
like, oh, man, just have a bit of fun, you know?
[01:27:54] That's what the point of this account is.
And, and furthermore, if you can teach people
[01:27:58] about the ways of open source projects,
assembly, et cetera, by doing
[01:28:02] that, I think there's a lot to be offered here.
It's not dunking on people for dunking's sake.
[01:28:06] It's showing actually the story that
I think X learnt is these are not big
[01:28:10] corporate open source projects. This
is not Kubernetes where there's,
[01:28:14] you know, hundreds, maybe
thousands of people-
[01:28:15] ... paid to develop this stuff. These are just
people in their basements in their spare time,
[01:28:20] and if you can address that topic
in a fun and entertaining way-
[01:28:23] ... I think that's the good thing and
that's, that's the value of X and
[01:28:27] then the reach we have.
[01:28:28] - And to be honest, right, like
even at Google, Google is
[01:28:34] one entity, but so many different
people, right? And there is a ton
[01:28:38] of Google engineers we work with
[01:28:42] all the time, and even like
Google from YouTube to Chrome to
[01:28:46] Chrome Media to the rest of Google, those
are very different types of entities. But
[01:28:50] what we do is efficient.
And, for example for,
[01:28:54] for Theo, right? It went a bit too far.
I had him... Like I calmed everyone
[01:28:58] down. I had him on the phone. We said,
"Okay, like this goes too far," and so on.
[01:29:02] But in the end yeah, it's a rap
battle, but it's positive for the
[01:29:06] project. It, like the awareness
we have on open source and,
[01:29:10] and I mean true open source
from communities right now is
[01:29:14] increased dramatically in the last
two years, and this is useful.
[01:29:19] - Uh, what do you think motivates all the
incredible contributors that we've been
[01:29:23] talking about? Like, what's the
engine? It's so interesting to see.
[01:29:26] - So-
[01:29:26] - Like you said, they're sitting in the basement.
What's the driver? What's the engine there?
[01:29:29] - There are many drivers,
but weirdly the main one
[01:29:33] is that what we do in multimedia
plays videos, and video is
[01:29:37] cool, right? And, and for
example, we have so many
[01:29:41] people in the community who arrive
because they loved watching
[01:29:45] anime, right? And this is like
the advice when people ask me,
[01:29:50] "What should I work on in open source? How do
I start?" And my answer is always the same:
[01:29:54] work on something you love.
[01:29:56] I am working on VLC because I
love movies, right? And I love
[01:30:00] watching the same movies over and over,
even if my wife hates me when I do
[01:30:04] that, right? But because it's interesting,
right? Because it's a topic that
[01:30:08] you like, right? The first, that's
the first thing where people come to
[01:30:12] usually to VLC and FFmpeg.
The second thing is that
[01:30:15] technically we, because we
search for excellence, this is
[01:30:19] the best school ever, right?
This is the best school
[01:30:23] ever of programming. If
you're good in C, in
[01:30:27] FFmpeg, if you know how to write
assembly, I assure you you're going to
[01:30:31] be one of the best programmers ever,
even if you're working on writing
[01:30:34] TypeScript, because this is
the most amazing thing to
[01:30:38] do. And you will, like, have
to get reviews by some of
[01:30:42] the most seasoned programmers
ever who are going to look at
[01:30:46] every part of your code and tell you why
it's not great. It's like we are the
[01:30:50] best teachers that you've ever
had in programming, right?
[01:30:52] - Andrew Kelley started Zig. He was an
FFmpeg developer and started Zig after
[01:30:56] his FFmpeg school. I mean,
[01:30:59] it's the place to learn so many
aspects of programming in the
[01:31:03] real world, in a thing used by billions
of people. You have nowhere to
[01:31:07] hide. You have to be open and honest
about your flaws and how you can learn
[01:31:11] and be better.
[01:31:12] - And what is also interesting
in multimedia is
[01:31:15] that you have 16 milliseconds to
display a frame. It's not like
[01:31:19] a game engine where you can basically
slow down and wait a frame.
[01:31:23] Like, so it's, you need to be good, right?
There is no choice, else you don't have your
[01:31:27] video. And because of how codecs,
if you miss a frame, you're going
[01:31:31] to destroy the look of the video,
right? So you need to be good.
[01:31:35] You need to be perfect to have
the right thing. But also
[01:31:39] is that it's not just pure programming
in the mathematical sense, right?
[01:31:43] A lot of people don't understand, but
[01:31:47] in order to program correctly on the
open source multimedia community,
[01:31:51] you need to understand how computers
work. And when you write assembly,
[01:31:55] you need to understand about CPU
pipelining, right? You need to
[01:31:59] understand how SIMD works, how
the ALU works, right? You need to
[01:32:03] understand what, how IO works,
right? And this is what I
[01:32:07] think that is missing to a lot of
engineers and software engineers today, is
[01:32:11] understanding what we call
computer architecture. And,
[01:32:15] like, seriously, like some of the debates is
like, should we use this assembly call or this
[01:32:19] one? And people say, "Well, no, it's
going to be like three cycles on this
[01:32:23] type of CPU and this one," and has
massive impact on the output, right?
[01:32:27] - We should expand. FFmpeg is probably one of
the biggest CPU users in the world. There's
[01:32:31] it's probably running— ... as we speak
[01:32:35] easily 100 mil- order of magnitude 100
million, maybe even a billion CPUs
[01:32:39] as we speak. So every instruction
matters. There's not...
[01:32:45] The impact, at least in terms of CPU,
is massive for everything that we do.
[01:32:51] - So first you come because it's an interesting
subject, then you stay because it's
[01:32:55] excellent, and in the end
you're very proud of it because
[01:32:59] it's in the hands of
everyone. Like so many
[01:33:02] people like, "Oh, I'm working for whatever
consulting company and I'm doing some
[01:33:10] portal to download invoices
for your PG&E." Wow,
[01:33:14] great. Like, so many jobs are
like that. You're not going to,
[01:33:18] to tell that to your grandma. But if you
go to see your grandma and say, "I do
[01:33:21] this so that you can play video on your
laptop," they understand. And this is very
[01:33:25] important, right? Because you're
working on VLC, FFmpeg, H.264. It's
[01:33:29] in the hands of hundreds of millions
of people and you have an impact.
[01:33:33] And so you can be proud of
yourself. And so I think that
[01:33:37] in addition to doing a great resume, all
those things are why people contribute.
[01:33:42] - Yeah, those are side effects. My favorite
quote on this topic is John Collison.
[01:33:45] He said, "The world is a museum of passion
projects." You know, everything out
[01:33:49] there is a passion project. And open
source multimedia and open source
[01:33:53] in general, you can just do that
so much faster. There's such a
[01:33:57] faster network effect, you know?
[01:33:59] I can open a cafe and that can be my passion project,
but I have to get building codes, I have to build a
[01:34:03] building, I have to find a location,
I have to do all the, you know, all
[01:34:07] sorts of things. Well, in the software
world, that passion project can be,
[01:34:11] can move quickly, it can be
amplified by the network effect,
[01:34:16] and that amplification can
be more than the sum of the
[01:34:19] parts. You know, you can
be, you can find people
[01:34:22] interested in extremely obscure things
[01:34:26] and have a network effect and make
something that is truly amazing.
[01:34:31] - And on that topic of passion projects
Tim Sweeney actually said in a reply
[01:34:37] to a tweet that was
complimenting JB. He said,
[01:34:41] quote, "Many things in the world
only happen because an awesome
[01:34:45] person decides to do it. This
is the case with VLC." And
[01:34:49] that speaks to something interesting to me,
that it does seem that a small number of
[01:34:53] people, sometimes one person, can create
[01:34:58] something incredible in the software world.
Like you said this over and over and
[01:35:01] over. I think JavaScript is an
incredible thing created by,
[01:35:05] Initially a single person. Some
of the programming languages like
[01:35:09] Python and C and Java, like
just one person has this
[01:35:13] vision, has this design, and brings
it sometimes over a weekend is the
[01:35:17] initial spark.
[01:35:18] - Yes, Linus built Git in two weeks. Wow.
[01:35:23] - It changed the world, Git. I mean,
it really changed the world.
[01:35:25] - Linus' passion project. "Hey, I'm uploading
this tarball to an FTP, like deal with it."
[01:35:29] - But for me, it's not just in
software, right? And I believe in,
[01:35:34] in individuals that are going to
change the world, right? And it's with
[01:35:38] a good, as you said, vision,
right? I want to do that. It
[01:35:42] is useful, it will be useful. And
whether it's going to like build
[01:35:45] train or cars or rockets or
something like, I believe
[01:35:49] people who believe in themself
and have a vision can have a huge
[01:35:53] impact for humanity.
[01:35:56] - Let's actually zoom out before
we zoom back in. We'll just keep
[01:35:59] going up and down the stack.
So you know, we've been
[01:36:03] talking back and forth VLC and
FFmpeg. Kieran, you said that
[01:36:07] FFmpeg and VideoLAN, VLC coexist,
[01:36:11] and there's no central point
of importance. It's a kind of
[01:36:15] what you call the binary star system.
[01:36:18] Uh, they succeed because of each other.
Can you explain the difference, how
[01:36:22] they interact? What is the-
... are they competitors?
[01:36:26] - I don't think they're competitors.
I think the simple answer is, the
[01:36:30] short answer before I go into detail is
VLC is to FFmpeg as Android is to Linux.
[01:36:36] So they depend on each other, but they
coexist because of each other. So they
[01:36:40] are a binary star system
is the analogy I used.
[01:36:43] - By the way, I feel horrible that I
just recently learned that Alpha
[01:36:46] Centauri, the closest star system
to us, is a triple star system.
[01:36:50] - And when you start doing the physics, it's
a nightmare, right? But, but, but like-
[01:36:55] - Hence the three body problem.
But anyway. So a lot of
[01:36:58] FFmpeg pipelines involve
the x264 project, which is
[01:37:02] a VideoLAN project. I would put
a finger in the air and say
[01:37:06] 80-plus percent of those pipelines
are dependent on a VideoLAN project.
[01:37:11] VLC, obviously, as we've discussed,
a VideoLAN project, uses
[01:37:14] FFmpeg, gives it reach,
exposure to weird files,
[01:37:19] Historically used some
donation money to fund FFmpeg
[01:37:22] development, and we'll talk a bit maybe
about some of the reverse engineering later.
[01:37:27] So it's a binary star system. They work and
feed off each other. Many of the developers are
[01:37:31] shared. There's no central location.
It's a virtuous cycle working together.
[01:37:36] - And we should mention that x264 is the
encoder for H.264 video standard. So
[01:37:43] H.264 is the standard. X264-
[01:37:46] - Is the open source
implementation of the standard
[01:37:49] - ... that's used by basically
everybody- ... for everything.
[01:37:52] It's, that is the main driver of
this. When you think of an MP4
[01:37:56] file that has H.264 codec in it-
[01:37:59] - If it came from a software environment,
like a data center or somewhere,
[01:38:03] the chances are it was created with x264.
[01:38:06] - And that's under the flag of VideoLAN.
[01:38:09] - That's a VideoLAN project. So in the
VideoLAN graphic, it sits in the VideoLAN
[01:38:13] world.
[01:38:14] - And VideoLAN has a, says a
bunch of stuff in it. Go to the
[01:38:17] VideoLAN website, there's
a bunch of icons.
[01:38:21] - Like if you look, there is
so many libraries, right?
[01:38:24] - libdvdcss- ... libdvdnav, libdvdpsi,
libvlc of course, vlc-unity, libblu-
[01:38:35] Blu-ray. Uh, yeah, there's many more.
[01:38:39] - And there is so many more, right?
[01:38:40] Lately, lately the dav1d project
that we might talk about is the
[01:38:44] last project from VideoLAN. It's
everywhere, right? And we do,
[01:38:48] we have a libspatialaudio lately
that we announced. We have a-
[01:38:51] - checkasm.
[01:38:52] - checkasm-
[01:38:53] - We'll talk about that later
[01:38:53] - ... which is like an insane project-
... but amazing. So and x264 is one of
[01:38:59] those VideoLAN projects. And my
opinion, for example, is that
[01:39:04] x264 was, is the most amazing
encoder ever designed,
[01:39:09] and this helped the adoption of
FFmpeg. A lot of people and large
[01:39:12] companies went through FFmpeg
because they wanted to use
[01:39:16] x264, and x264 increased the
popularity of FFmpeg. But
[01:39:20] also VLC had its popularity because
[01:39:24] it's played so many files that were
done by FFmpeg, right? So it's,
[01:39:28] it's many projects that are
intertwined and work together.
[01:39:32] - Yeah. Unfortunately, there's a, there's
a thing on X where VLC is mentioned and
[01:39:36] there's people, "A quick reminder that it's FFmpeg
inside doing the actual work." And that, and
[01:39:40] that's like I said, it's not, that's
not the case. We work together.
[01:39:46] - And to give you an idea, right? When I
compiled VLC for Windows, I compiled
[01:39:50] around 16 million lines
of code, right? One
[01:39:54] million of those are inside the VLC repository,
and FFmpeg in total is probably two,
[01:40:00] around two, right? But so it means that
so many dependencies are outside. And
[01:40:04] if you also look at FFmpeg
per se, FFmpeg also is
[01:40:08] integrating third-party
libraries like x264, but
[01:40:11] LibOpus and so many others, right?
So we all depend on each other.
[01:40:15] - Uh, yeah, that's why I was hoping to
do this episode as we are doing that
[01:40:19] just kind of joins FFmpeg and VLC-
[01:40:23] ... because it's really, it's, it's
really two of the same, like you said,
[01:40:27] binary star system and we're all just
orbiting it. Can we give a shout-out
[01:40:31] to some of the people along the
way? We didn't really quite talk
[01:40:34] about the history of FFmpeg, so-
[01:40:38] maybe can you tell me about
Fabrice? Can you tell me about
[01:40:42] Michael Niedermayer? Can you tell me
about some of the key figures here?
[01:40:46] - Let's just talk about the eras
of FFmpeg, because there's
[01:40:49] key eras and key people that made this
[01:40:52] possible. Uh, Fabrice Bellard,
as you mentioned, creating the
[01:40:56] concept, and then probably in the
2000 era, I would call the era,
[01:41:00] eras tour of FFmpeg is the 2000
era was Michael Niedermayer. So
[01:41:05] key things he got done was
exhaustive support for DivX and
[01:41:09] Xvid at the time, and all sorts
of weird variants of what's known
[01:41:13] as MPEG-4 Part 2. So this predates the
[01:41:17] MPEG-4 Part 10 that we're used
to. So this was 2000 era video
[01:41:21] codecs where there were, oh, flavor
after flavor of weird decoders.
[01:41:27] At the time in the 2000s, you needed a new
player to play every different type of file
[01:41:31] format. So there was Windows Media Player
to play Windows Media formats. There
[01:41:34] was RealPlayer to play RealMedia formats.
And those were the other, the other
[01:41:38] key thing in FFmpeg at the time were native
decoders for those. I actually do remember
[01:41:42] being a teenager, I must have been,
[01:41:46] figuring out there was this
one player that could play,
[01:41:49] could decode these files without having
separate bloated players. Because
[01:41:53] at the time when you downloaded RealPlayer, there
was a ton of other stuff in there, a ton of ads, a
[01:41:57] ton of other things, and
just having a simple library
[01:42:00] that was fast led to that. And then
I think 2008 was a, 2008 onwards
[01:42:08] was a big change because that's when
H.264 got its maturity and I think
[01:42:14] something hopefully we'll talk about a bit more.
This was the beginning of high definition video.
[01:42:19] So H.264 was the key decoder of that.
[01:42:22] So I'd call that the late 2000s and
2010s, and that's when the big reverse
[01:42:26] engineers came along and
really did astonishing work.
[01:42:30] The beginning was a single player
that could play Xvid, DivX,
[01:42:35] Windows Media, and RealPlayer was already a
massive achievement in itself without codec
[01:42:39] packs, without weird stuff you had to download
that had weird ads and weird spyware.
[01:42:43] - VLC 1.0 was out on those
times, 2000, 2009, 2010.
[01:42:49] And this is like where it exploded.
[01:42:53] - Yeah, without codec packs, it just
works- ... across all these different-
[01:42:57] - It, de facto, it's just like all the
codec packs are FFmpeg inside VLC,
[01:43:01] plus we have other modules
for all the type of codecs.
[01:43:03] - But back at the time that wasn't, is there
were weird, in the 2000s, there were weird
[01:43:07] codec packs with DLLs coming from
this place, DLLs coming that-
[01:43:11] - With a lot of spyware
[01:43:12] - ... with spyware, with you know what. It wasn't
reliable, you didn't know, and having a single
[01:43:16] player that was open source or
single playback module/player that
[01:43:20] could do this that was open source.
But I think the thing to emphasize is
[01:43:24] this task in the 2000s that Michael
did was Sisyphean. It was really,
[01:43:28] the number of edge cases are poor
beyond comprehension in terms of
[01:43:32] you could have a Chinese CCTV
system that did one weird variant
[01:43:36] of MPEG-4 Part 2, what's
known as MPEG-4 ASP,
[01:43:40] and that was a weird variant, and you had to
fix that without breaking everybody else-
[01:43:44] ... times a million.
[01:43:45] - So that's, so you said that's where a lot
of the reverse engineering was happening.
[01:43:49] - It started in the 2000s with the
Windows Media stuff because that was-
[01:43:52] ... proprietary. It started with the
RealMedia, so with Benjamin Larsson.
[01:43:56] - Kostya Shishkov.
[01:43:57] - Kostya Shishkov, that era. Those
were the key, that was the key
[01:43:59] groundwork. And then in
the 2010s was kind of
[01:44:04] the Paul Mahol, Kostya era
building, doing some of the
[01:44:08] most difficult codecs. JB maybe
can talk about GoToMeeting 4 and
[01:44:11] GoToMeeting 5, and-
[01:44:13] - What? What's the GoToMeeting?
[01:44:15] - So, like, let's talk about this
[01:44:18] amazing Ukrainian guy called Kostya, who
was at that time living in Germany, and who
[01:44:25] was in love with Sweden, right? He—
And the guy was the most... He's like,
[01:44:33] like a lot of the people in the
community are very clever. He's
[01:44:38] one of those who are, like,
borderline geniuses, right?
[01:44:41] He was able to reverse engineer
extremely complex codecs,
[01:44:45] And he does that, and we
do a bit of engineers with
[01:44:48] Kieran, but clearly not at this level.
[01:44:50] - No, no, yeah.
[01:44:51] - Um, he reverse engineered binary
blobs, which are 20 megabytes?
[01:44:56] - Yeah, so just for reference, one
megabyte binary blob to reverse
[01:45:00] engineer is probably order of magnitude
a month of work, and this guy is doing
[01:45:04] 20, 30 megabyte blobs. Maybe we'll
talk about that in a minute, about the
[01:45:08] subtleties of how you do that. But this guy is
doing it for very difficult and very obscure
[01:45:12] codecs.
[01:45:13] - And did that for fun, right? And so
GoToMeeting was a big problem with VLC
[01:45:19] because that was like the number one
[01:45:23] feature request for a long time, so I put
a bounty. And the guy at some point said,
[01:45:27] "Okay, JB, I'm going to do
it." And in a matter of two
[01:45:31] months, and then he explained how he did it.
He was just like, "Oh, I looked at the code,
[01:45:35] like this looked like a DCTs
that I used to see on WMV
[01:45:39] and so on." He did that, and
the funniest part is that
[01:45:43] the code he's written
is a ton of jokes. And
[01:45:47] there is, there is a ton of
JB, right, my name, and, and
[01:45:51] Kempf and Kempf and Kostya jokes inside
the code. The code is beautiful, right?
[01:45:57] - So one of the things I wanna
comment is I've gotten a chance to
[01:46:01] speak to some of the developers,
some of the assembly language level
[01:46:05] People, and they all always make
everything sound like it's kinda easy.
[01:46:10] There's a kind of humility because, maybe
[01:46:15] just the level of what's
required to do this stuff is so
[01:46:18] high that everything else seems easy, I
guess is the lesson to take away from that.
[01:46:23] - So in the community, like some of the
most impressive people are the ones doing
[01:46:27] reverse engineering- ... and the other
ones doing the assembly folds, right?
[01:46:31] Um, and both of those type of people are
[01:46:35] amazing. x264, for example, became amazing
because, of a guy called Loren Merritt—
[01:46:42] ... who is, was from University
of Washington, I think.
[01:46:44] - At the time, yeah.
[01:46:45] - And who was, like, who made everything
great and fast doing a ton of assembly.
[01:46:51] Um yeah. So this is like the
[01:46:55] the golden era, I guess, where
so many things got done.
[01:46:57] - So, yeah, if you look at Kostya, for example, he
looked at the world as a binary specification.
[01:47:01] He didn't need documentation or anything.
It's, "I have a binary and I can
[01:47:05] figure all of this out." And he
regularly used the phrase binary
[01:47:08] specification. "Ah, you know, it's not a problem."
And he would go away, and he would come back, and
[01:47:13] he would do interesting stuff.
[01:47:15] - Can you actually speak to
the details or add color and
[01:47:18] texture to what it takes to
reverse engineer a blob?
[01:47:22] - Yeah. So let's look at GoToMeeting,
for example, is a good one because,
[01:47:26] um, I record a meeting on
GoToMeeting, for example.
[01:47:30] How do I play it back without
needing this GoToMeeting
[01:47:33] player? There may not even be a player. I may,
I may need to send a recording of a meeting to
[01:47:37] someone that doesn't have
a player or whatever.
[01:47:40] So first of all, there's a ton of other
stuff there. There's an actual video
[01:47:44] conferencing client. You need to go and find, it
may be easy, it may not be easy to find the actual
[01:47:48] module doing the decompression.
You need a way to
[01:47:52] actually dump the YUV data
from the module. So often it
[01:47:56] involves opening in a disassembler,
trying to guess where the hooks are
[01:48:01] to incorporate that module
and run that module natively
[01:48:05] to decode a sample file. So figure
out where this module is doing
[01:48:09] the decoding process and
find a way to hook in and
[01:48:13] output the raw YUV data,
'cause you will need that-
[01:48:16] ... as a point of comparison for when you actually do
the reverse engineering, 'cause you'll need to be bit
[01:48:20] exact or in some cases close to bit exact.
And then you open up your disassembler,
[01:48:27] use a lot of intuition to go and figure
out, you know, where the DCT is,
[01:48:31] where's entropy coding.
There, there is a kind of,
[01:48:35] not a rule book, but there's always
a pattern of some sort. For example,
[01:48:39] GoToMeeting, you know it will be
a s- a lot of screen codec tools.
[01:48:43] There's also different variants, so often
I think there's, what, GoToMeeting 4, 5-
[01:48:46] - Well, 2 or 3, 4, I think.
[01:48:48] - 2, 3, 4.
[01:48:49] - So as you mentioned here, going to
Perplexity, GoToMeeting uses its own
[01:48:52] proprietary codec for older s- recorded
sessions historically stored in
[01:48:57] WMV files that require a special
decoder to play properly on
[01:49:01] Windows. Without this decoder
installed, Windows Media
[01:49:05] Player and some editors cannot
decode the video track, so you
[01:49:09] may only hear audio or see a
black screen. Boy, do I remember
[01:49:12] that. But this is reverse
engineering that.
[01:49:16] - This is key, right? Because the GoToMeeting
is something that not many people know
[01:49:20] anymore, right? Well, you know about Zoom
and, and Teams and so on. But like, now
[01:49:24] let's fast-forward 10 years,
15 years, and like this is a
[01:49:28] GoToMeeting.exe for Windows 32
bits, right? Which is like, oh
[01:49:32] yeah, but I'm on Android, I'm on an iPad,
I'm somewhere else, right? How are you
[01:49:36] going to do that? I'm going to be on
RISC-V, on Arm. Those are blocked,
[01:49:40] but there are tons of files we
need support for the future.
[01:49:44] And this is why those type of work are—
exceptionally useful for humanity.
[01:49:51] - I just have to say, though, that reverse
engineering process is mind-blowing.
[01:49:56] It's crazy. It's like,
[01:49:58] it's a kinda like, you know, I've
been reading a lot and interview
[01:50:02] archeologists. I mean, you
just have so little signal.
[01:50:05] Yes, yes, you know over time
you get so much experience, you
[01:50:09] understand the structure of the original
code, so you can kinda start inferring
[01:50:13] basics. But you're like-And
we like archaeologists with a
[01:50:18] little brush trying to reconstruct
the entire human civilization
[01:50:22] - Kieran is too humble, but Kieran has
done some reverse engineering also.
[01:50:24] - Of CineForm, yeah, at the time, um-
[01:50:26] - CineForm, nice
[01:50:27] - ... yeah, at the time before actually led
to the open sourcing of that work. Um,
[01:50:32] so in parallel to doing the binary side,
you obviously have samples. In many
[01:50:36] cases, you don't have many samples so
you have to figure out what all the
[01:50:40] different flavors are, and you may have a
s- So CineForm, for example, is actually a
[01:50:43] collection of different approaches and
toolkits within that codec 'cause often
[01:50:47] it grows naturally. And the hard part is
finding a sample that gets you kind of
[01:50:53] somewhere to start without having to
implement 10 different other things. So
[01:50:58] start there.
[01:50:59] I think thankfully at the time I found a sample
by pure chance that had a lot of flat blocks.
[01:51:03] It was animation, so that
really helped a lot because
[01:51:06] it wasn't using particularly complex coding
tools, et cetera, and you could kind of get
[01:51:10] somewhere and then, and then build up and
build up until you figure, "Hey, here's a few
[01:51:14] bits here. I missed this. I missed this, this if
branch that it does," and go, "Oh." So when we
[01:51:18] say samples, you mean sample videos-
[01:51:20] ... and then, and then you're tracking,
trying to infer, like, what is this
[01:51:24] codec doing- ... by observing the
sample and then looking at what, at
[01:51:29] the lo- at, at the machine lo-
[01:51:30] - The machine code saying-
[01:51:31] - At the machine code
[01:51:31] - ... "Ah, I have byte, this byte is six.
Take this branch." And in a different
[01:51:35] sample, oh, it's-
[01:51:36] - That's nuts, man.
[01:51:37] - And-
[01:51:38] - That is nuts
[01:51:39] - ... so you see, this is nuts. Then
you go to things like GoToMeeting.
[01:51:42] - Yeah, yeah.
[01:51:42] - It's like-
[01:51:43] - Mine was easy, right?
[01:51:44] - ... imagine-
[01:51:45] - Yeah, right
[01:51:45] - ... two order of magnitude of
more complexity. A guy alone
[01:51:51] somewhere in Germany doing that.
[01:51:53] And for a long time, you work, you're
in a black box because a decoder,
[01:51:57] for a long time, because there is so many
steps from the entropy decoding, the intra
[01:52:02] prediction, the motion prediction,
the IDCT, and so on. For a long
[01:52:06] time, you don't see anything, right?
So you're debugging purely in memory.
[01:52:10] - Debugging guesswork.
[01:52:10] - And you may have the buffer that the
coefficients are stored in completely wrong,
[01:52:14] and so you may be going down a complete
rabbit hole thinking it's this and then,
[01:52:18] oh damn, that's not, that's,
that's something else, and-
[01:52:21] - And you're doing that on binaries
that are tens of megabytes,
[01:52:25] millions of instructions, right?
[01:52:27] - So you're stepping through the debugger,
[01:52:29] like one by one, you know, instruction by instruction
going, "Hey, this instruction changes this.
[01:52:33] This does this."
[01:52:34] - Pausing the program on
the CPU level. Like it's-
[01:52:36] - Pausing it, yeah, on the CPU level, watching
what's going on, trying to figure out-
[01:52:39] - Sometimes you need to, like, be in a
VM, so yeah, that you can pause the VM.
[01:52:43] - Yeah, pause the VM, dump the memory, 'cause there
could, some of the codecs could have encryption.
[01:52:46] There could be like a DRM on
there. So you need to dump the
[01:52:50] memory from a virtual machine.
[01:52:52] - Like when I joined École
Centrale Paris in 2003, Jon Lech
[01:52:56] Johansen basically broke the
DVD specification and created
[01:52:59] DeCSS, showed us how he was breaking a
[01:53:03] DRM, which was MP4 FairPlay
from Apple. What he did
[01:53:07] on his laptop, and I was young, I
was 21, was just like mind-blowing
[01:53:11] because he was basically debugging
Windows inside a type of VM
[01:53:15] with ex- Like, wow. It's incredible. It's
[01:53:18] mind-blowing and inspiring.
Does it get, like from your
[01:53:22] experience and from what you've seen in
the community, does it get discouraging?
[01:53:25] Does it get-
[01:53:26] - People help you. People send you samples.
People are keen. Sometimes you don't
[01:53:30] have access to an encoder, so
[01:53:32] this is even more difficult because
you just, you just ask and you have to
[01:53:36] ask for samples. I remember VideoLAN
used to tweet for samples at one
[01:53:40] stage. "Hey, I need this
obscure sample," and-
[01:53:42] - For a long time I was, "Oh, I need
this codec, and I need this codec."
[01:53:45] - And if you were really lucky, you would
find like... If you were unlucky, you'd get
[01:53:49] like one or- you'd get nothing or you'd get one or
two, and then they would... Sometimes you'd find a
[01:53:52] goldmine. It's like, "Yeah, my company has 100,000
of these files 'cause we're dependent on it for
[01:53:56] some reas-" Um, and so those are the,
those are kind of the best if, if...
[01:54:00] Because then they can test bit exactness
across the huge range of coding tools.
[01:54:06] - Can you explain bit exactness?
[01:54:07] - Bit exactness, so most but not all video
[01:54:11] codecs, certainly from
about the 2000s onwards,
[01:54:16] have a bit exact definition, so
every implementation must produce
[01:54:20] exactly the same bits,
bit for bit, in exactly
[01:54:24] the same data that comes out of a decoder.
[01:54:26] - For like a large number of samples?
[01:54:28] - For a given sample. So Lex's
implementation, JB's implementation, and my
[01:54:32] implementation of H.264 must
match bit exactly. That
[01:54:36] wasn't the case in the '90s of
MPEG-2, probably fair to say
[01:54:40] one of the biggest mistakes the video industry
made, and I think people who were in the
[01:54:44] room in '92, I don't think, most or both
of us were in diapers, I suspect- ... but
[01:54:48] have acknowledged I would give
a shout-out to Yuri Reznik.
[01:54:53] He's acknowledged that was one
of the big mistakes of the era.
[01:54:56] - And you're saying the encoders needed to be
able to run tests and then the bit exactness.
[01:55:00] the bit exactness. I mean, that's
a nice thing to guarantee.
[01:55:04] Like there's a parallel sort of
development here on the way the web
[01:55:08] browser works, which is a, you
know, takes HTML and displays
[01:55:12] it, and there's no bit exactness
there across the different engines.
[01:55:15] - I would point out actually FFmpeg
is unique in the sense that it's,
[01:55:20] it has been a winner-takes-all scenario.
You have... Browsers is a good analogy
[01:55:24] because it has to parse a lot of different
content and render it in a particular way, like a
[01:55:27] decoder.
[01:55:29] But there still are multiple browser engines. There's
Firefox's one, there's Chrome's one, there's a
[01:55:32] few Japanese ones that are pretty decent.
[01:55:35] That's not been the case in
multimedia in general across a
[01:55:39] wide range of codecs. FFmpeg has kind of
[01:55:42] won it all, I suppose, in a sense because
of, because of the fact that you can get
[01:55:46] every new codec added is actually worth
more than the value of that codec itself
[01:55:50] because it makes the whole thing better.
[01:55:52] - Man, this is really cool. Going
to Perplexity. Yuriy Reznik is a
[01:55:56] multimedia and signal processing
researcher, got his PhD in computer science
[01:56:00] from Kyiv University with over
150 papers and more than 80
[01:56:04] granted US patents, contributor
to major multimedia standards
[01:56:08] including H.264, MPEG-4,
AVC-H.265 MPEG-4 ALS, G.718, and-
[01:56:17] - G.71 is telco stuff. Telco.
[01:56:19] - Oh. And so he was more
connected to companies.
[01:56:21] - RealAudio, RealVideo, right? That was-
[01:56:23] - Oh, yeah
[01:56:24] - ... very important at that time
[01:56:25] - ... Zencoder, Brightcove, Contex.
This, man, I need to hang out with
[01:56:29] Yuriy. He's legit. And he's like
one of the most nice person-
[01:56:33] - Slack guy, yeah
[01:56:33] - ... ever, right? Like for
example, for my for my
[01:56:37] startup that I'm doing right now called
Kyber, right? I met Yuriy because
[01:56:41] I met him every year at the Mile High
Video Conference, which is in Denver.
[01:56:45] And he gave me like so much good ideas
[01:56:49] and good things. He's like
really amazing person.
[01:56:52] - He tells us how, how, you know-
How great it is to be, you know,
[01:56:56] even know us. And then we just like, you know,
you look at that and it's, I think it's the other
[01:57:00] way around, Yuriy
[01:57:01] - That reminds me of a thing that you
mentioned to me about FATE testing and,
[01:57:05] like, the insanely rigorous
process that's used to
[01:57:09] test everything that's incorporated
into into FFmpeg. Can you take
[01:57:13] me through the testing process?
[01:57:14] - Yeah. So FFmpeg has a system called FATE,
FFmpeg Automated Testing Environment.
[01:57:19] Because FFmpeg runs on so many different
OSs and can be compiled with so
[01:57:23] many different compilers,
[01:57:25] there's been a crazy number of
configurations. So you can see the
[01:57:30] absurd combination of compiler
variants, operating system variants,
[01:57:36] instruction sets. You can see at
the top macOS has tons of different
[01:57:40] variants because it has iOS, it has tvOS.
[01:57:42] - Well, I'm looking at a
page fate.ffmpeg.org.
[01:57:47] 81 minutes ago, 76 minutes
ago, looking at the
[01:57:51] different architectures, the operating
systems, the different compilers, Apple Clang
[01:57:55] version...
[01:57:57] - Combinations are crazy.
[01:57:58] - ... the combination is insane. RISC-
[01:58:00] - So these are all run by volunteers, so these
are all volunteer systems. The ones at the top,
[01:58:04] for example, the Macs I host
in my office, for example,
[01:58:07] Host all sorts of different stuff.
Other people host other things. So
[01:58:12] it's really there to make sure...
because FFmpeg does quite complex C
[01:58:15] code, for example, you do have
miscompilations. So the compiler
[01:58:19] will sometimes compile C code
incorrectly. For example, this
[01:58:23] happens once in a while.
[01:58:25] - Oh, there's like, there's a
log of all the compilations.
[01:58:28] - Yeah, log of all the compilations, all the tests. I
think one of the other ones will show all the tests
[01:58:32] passing.
[01:58:33] - If you click, you can see all the
tests- ... back. All tests successful.
[01:58:37] - In logs test, yeah. So you see
all those tests are passing
[01:58:43] of all the different codecs, all the
different filter transformations, all the-
[01:58:47] The level of scale is quite crazy.
[01:58:50] - Oh, that's nuts.
[01:58:50] - On all the combinations. It's not just a
matrix at this point. It's like a pivot table
[01:58:54] of different combinations.
[01:58:56] - That's nuts.
[01:58:57] - And it's a key part of what we do because
you may be able to test something
[01:59:01] locally, you make a change,
but actually that breaks
[01:59:05] GCC version 11 on Mac or
something like that, and you're
[01:59:08] able to then fix that. We also have
miscompilation, so the C code,
[01:59:12] sometimes the compiler can have a bug in
it where it creates the wrong output,
[01:59:16] and that can have quite a big effect
sometimes on a video because of the
[01:59:20] way frames have dependencies.
Even a small change in the output
[01:59:24] can cascade to actually
quite big glitches.
[01:59:27] - You see PowerPC, you
see RISC, you see ARM.
[01:59:31] - There was PowerPC, there was RISC, there
was weird stuff in the past like DEC Alpha.
[01:59:34] There was—
[01:59:35] - You see Visual Studio, different
versions of Clang or GCC.
[01:59:37] - Visual Studio, Intel compiler,
Apple Clang, you name it.
[01:59:40] - What are some of the pain
points? Like maybe do you have
[01:59:44] emotional triggers maybe
nightmares about a
[01:59:48] particular operating system, a particular
container, codec combination of-
[01:59:53] - I mean, for me, it's really easy
because I have a day job. My company
[01:59:57] builds... The company I started builds
equipment for broadcasting sports matches
[02:00:02] between TV stadiums and
studios, for example.
[02:00:05] We have to work with 10-bit video, and
10-bit video has a set of challenges that
[02:00:11] you can't process 10-bit data
natively on a CPU. So that means you
[02:00:15] have to stick it in 16
bits. So that means you
[02:00:19] have six wasted bits. So there's different
packing formats to actually pack
[02:00:23] the data more efficiently because
when you send that over a network,
[02:00:27] you lose... 'Cause you need to
save that 40%. For example, on PCI
[02:00:31] Express, you may only have bus bandwidth
to do that. And so I think internally we
[02:00:35] have about... Some are industry
ones and some are internal to our
[02:00:39] own hardware that we build. We have a,
I think a 5 by 5 or 6 by 6 matrix of
[02:00:45] every single format to every single
other format conversion. In fact, one,
[02:00:49] one of them I sent you, and they're all written
in handwritten assembly, and they're all
[02:00:52] written, and they all support
different CPU generations.
[02:00:57] So this is really traumatic, handling
all these different combinations
[02:01:01] times a million.
[02:01:02] - By the way, the company you're talking
about is Open Broadcast Systems.
[02:01:04] - Yeah, so no, no relation to the
free OBS streaming service.
[02:01:08] But JB and I have started companies
[02:01:11] broadly speaking around the FFmpeg
VLC ethos, so that's really
[02:01:15] low-level work. So in most companies,
this wouldn't be written in
[02:01:19] assembly. It would be
accepted that C is fast.
[02:01:23] As you can see from that, C is not fast.
[02:01:26] - So here it says 62 times faster than C.
[02:01:31] - Yeah. So it's taking
those, the ethos of doing
[02:01:34] low-level programming,
real-time programming,
[02:01:39] and using that for commercial applications,
and JB and I have started companies around
[02:01:43] that, in many cases hiring developers
from the open source community
[02:01:48] to use that ethos. And so
that's a great example
[02:01:52] of some of the things we're doing. In
most companies, it would be, say, "Oh,
[02:01:56] I'll write this in C and it's fast and we're
done," but actually you can get a lot better.
[02:01:59] - For me, like, some of the headaches we have
is around some OS that are difficult to
[02:02:07] support, right? Because if you look at
VLC and thanks to FATE and FFmpeg, we run
[02:02:14] on... The last version of
VLC runs on Windows XP
[02:02:19] and still run there and runs on Windows
11. We work on macOS 10.7 to the
[02:02:26] latest macOS, whatever it is, right, 26.
[02:02:30] We work on iOS since iOS
9, well, we are actually
[02:02:34] iOS 26, right? We support many types
of Linuxes, BSD, Solaris. The last
[02:02:42] version still runs on OS/2,
right? Like there is maybe 10
[02:02:46] users of OS/2 in the world, and one
of them is maintaining VLC. Then you
[02:02:50] realize that this very small
team around VLC and using FFmpeg
[02:02:54] codecs and all the other ones support more
[02:02:58] OSs than Microsoft or Google or Apple, and
they have infinite amount of power and
[02:03:06] resources. But for
example, the worst is iOS.
[02:03:11] For in order to build on
iOS 9, we need to do some
[02:03:15] very clever mixing of several versions of
the Xcode IDE and SDK from Apple, from
[02:03:22] several versions, and do a type
of Frankenstein version of that
[02:03:26] so that we can still support iOS 9,
which is not supported at all by the
[02:03:30] compiler of Apple in order to
still run on Arm32 on iOS 9. And
[02:03:38] you've seen on FATE that it was
still supporting iOS 9, right? So,
[02:03:42] My headaches are mostly
related to the support
[02:03:46] of so many OSs. And it's
important because, like, we
[02:03:50] receive so many people saying, "Hey,
thank you. I still have my iPad 2 to
[02:03:54] watch movies," and it still
works on iOS 9, right?
[02:03:58] And it's also an impact of, like,
not forcing people to buy new
[02:04:02] hardware when it works fine if you
optimize it correctly. Which brings us
[02:04:06] to what we were saying about
assembly. It's also fighting, like,
[02:04:10] the fact that you need to buy something
new nonstop while you could optimize
[02:04:14] more, which is a lost art.
[02:04:18] - You gotta tell me about
this lost art or this, uh-
[02:04:23] ... the carriers of the
flame of assembly. What
[02:04:28] what is, what is assembly?
Why is it beautiful?
[02:04:31] Why is it challenging? How does it work?
[02:04:34] - So when you write assembly code, you
write this using the instructions the
[02:04:38] actual processor is using directly.
So most of the time you would
[02:04:42] write in a language, let's take C as a good
example. The compiler would use that to
[02:04:46] create assembly language and machine code
[02:04:49] instructions for you
based off your C code.
[02:04:53] And there's a specific flavor of assembly
that we use in FFmpeg that's called
[02:04:57] SIMD, SIMD, single instruction, multiple
data. So this means, for example,
[02:05:03] say I want to add five to a number in
[02:05:07] scalar assembly, so this is what's known
as you work on an individual element.
[02:05:11] So I wanna have a number of-- I have the number
ten and I want to add five. I use the add
[02:05:14] instruction, and I add five to
ten, and I get 15. With SIMD, with
[02:05:20] SIMD, I can have a whole vector of 16 different
numbers. They could all be different.
[02:05:25] If I want to add five to that,
I can run one instruction,
[02:05:29] and that one instruction sums all
16 elements. And that, as you can
[02:05:35] imagine, lends itself
very well to video. Video
[02:05:39] is, you know, pixel grid, so
I can perform operations on
[02:05:43] multiple pixels at the same time. The
key thing that we do differently in
[02:05:46] FFmpeg is we don't use any
abstractions or any major
[02:05:50] abstractions on top of that. So there's
a part of the world that uses what's
[02:05:54] known as intrinsics. So these
are C functions that behave very
[02:05:57] similarly but not quite the same
to writing assembly by hand.
[02:06:02] So the registers that data is stored in
[02:06:06] on the CPU, the compiler
allocates those for you.
[02:06:10] And so the key thing to understand
was when we write SIMD is we have
[02:06:13] a 10x, and not percentage, 10x to 50x
speed improvement. That, that function is
[02:06:20] 62x, um—
[02:06:21] - That's nuts.
[02:06:22] - ... on the FFmpeg account, as you know, posts
and tweets a lot about that to try and say,
[02:06:26] "Hey, we are doing this stuff."
[02:06:29] - You are a person who sees the
beauty in assembly, but it's also
[02:06:32] extremely useful for these kinds
of application to actually-
[02:06:35] ... significantly outperform
even C, which is crazy.
[02:06:40] - It is necessary. Right? Because, like,
one of the projects that we need to talk
[02:06:45] about is called dav1d, right? So dav1d is
a decoder for the format that was done by
[02:06:53] Alliance for Open Media which is
an, a video decoder called AV1.
[02:06:58] - So if, for people who don't know,
we've been talking about H.264.
[02:07:02] AV1 is another hugely popular standard
and codec that is increasingly taking
[02:07:10] over the internet.
[02:07:12] - And when this format was launched
many people said, especially
[02:07:16] even from the Alliance for Open Media,
right, which is Google, Netflix, Amazon,
[02:07:20] uh, Mozilla, say, "Well, this
format is so complex, it must be
[02:07:24] done in hardware to do
decoding," right? And well, I
[02:07:28] arrived with a few other people mostly
[02:07:32] Ronald Henrik, and Martin, and
we said, "We need to have an
[02:07:36] extremely good software decoder
because it's going to take
[02:07:40] time to have hardware." And so we wrote this
project, which is beyond insane. We are
[02:07:47] talking about 30,000 line of C, but 240,000
lines of handwritten Assembly, right?
[02:07:56] - Handwritten Assembly, 240,000 lines.
[02:08:02] That's incredible. That mean-- I mean, some of
the stuff we're talking about is probably the
[02:08:05] biggest Assembly code bases.
[02:08:09] - To give you an idea, and Kieran can
correct me, but I think the FFmpeg has
[02:08:14] 100,000 lines of Assembly
for all the codecs.
[02:08:17] - For all codecs. Mm-hmm.
[02:08:17] - And just this one has 240,000. It's
a VideoLAN project, of course. And
[02:08:24] it is optimized at the maximum because the
[02:08:28] motto when we're starting
the project is every cycle
[02:08:32] matters, right? Every cycle
matters because David is
[02:08:36] used in VLC and in some
software AV1 playback stacks.
[02:08:40] We are talking about probably
3 billion devices which
[02:08:44] are going to decode video nonstop
because, for example, 30% of the
[02:08:48] video from Netflix are now
in AV1, 50% of YouTube,
[02:08:52] right? So, and you often don't have
a hardware decoder because not
[02:08:56] many devices have a hardware decoder.
And with dav1d, we realized that
[02:09:00] with one or two cores you were able to
decode 720p correctly. So it is—literally—
[02:09:08] - Yeah, that's dav1d
[02:09:08] - ... incredible, right?
[02:09:09] - That's dav1d. Look at that Lex.
[02:09:10] - Uh, yeah, so this is
another spicy tweet from
[02:09:14] you. This is what peak video codec
should look like, 79.9% assembly—
[02:09:20] - That's almost
[02:09:20] - ... 19.6% C and 0.5% other.
[02:09:25] - And what's incredible is with those
tweets, which is factual, people get
[02:09:31] crazy. They are unhappy, right? They say-
[02:09:33] - For a year, for the last two years they go crazy,
"No, intrinsics is fine. The compiler is..." Oh, they
[02:09:37] go, "I have never-"
[02:09:37] - "You can optimize your compiler,
auto-vectorization, it's your fault, you don't
[02:09:41] understand." And we've
tried that forever, right?
[02:09:44] - For two years, and two years later,
showing hundreds of examples
[02:09:49] of handwritten assembly. "No, no, no, you're
doing it wrong. The compiler can do this."
[02:09:52] - So we should actually just articulate a little
clearer. So the intuition there from the
[02:09:56] software engineering folks, when you have
code like... Okay, let's just take an
[02:10:00] example, C++. There's a compiler that's
doing a lot of the optimization.
[02:10:05] - Yes.
[02:10:06] - And the presumption is if you have a
good enough compiler, if you continue to
[02:10:10] improve the compiler, you're
going to generate code-
[02:10:13] ... that can perform like optimal
performance. You cannot possibly beat it.
[02:10:18] - Yeah. Yes.
[02:10:18] - And you're consistently challenging
that thought that if you do-
[02:10:21] - By orders of magnitude
[02:10:22] - ... by orders of magnitude- ...
handcrafted assembly can outperform C.
[02:10:27] - The two things that they tell us
is, yeah, but modern compilers
[02:10:31] have auto-vectorization, right?
Because SIMD that we're doing is
[02:10:34] vectorization. And like
it's not even close, right?
[02:10:38] It's not even close, right?
It's not like 5%, 10% slower.
[02:10:41] It's multiple times slower.
[02:10:43] - So can we... I don't know if you can say something philosophically, because
there's a lot of great software engineers, great engineers, great machine learning
[02:10:47] lot of great software engineers, great
engineers, great machine learning
[02:10:51] people. Karpathy will listen to this
and say, "What's the intuition he's
[02:10:55] supposed to get from this?
What are we supposed to..."
[02:10:57] - Karpathy learnt assembly because of the tweets by the
way. I just... He start- He went, he's like, "Oh, I
[02:11:01] think this is a movement."
[02:11:01] - He's like, "Let me figure
out what's happening here."
[02:11:02] - No, no, he, and you know the way
he documents his work and so.
[02:11:05] - Philosophically, what's
important to realize is that we
[02:11:09] passed the time where hardware
was going so much faster, right?
[02:11:13] We are at the end of Moore's law.
We have limitation for for AI,
[02:11:17] for memory. You need to go
down in the stack and optimize
[02:11:21] more to get more power from
what you have, because our
[02:11:25] request for power, CPU power, GPU power
[02:11:29] are exploding while the hardware
is not exploding in speed, right?
[02:11:35] So you- what people do is that they add
more cores, right? But that's basically
[02:11:39] like at some point you can add
250 cores, right? So what we
[02:11:43] do is to take every inch of the machine.
[02:11:46] - Not just that, not just that. We
abuse the machine. We go and use, we
[02:11:50] use the machine in ways that the,
[02:11:53] that the creator didn't expect. Sometimes we use
an instruction that's completely unrelated to
[02:11:57] what we do. We use a cryptography instruction
in video processing to do nothing
[02:12:01] related.
[02:12:01] - And one of other things that we do,
for example in dav1d, which is a bit
[02:12:05] crazy, is that we don't use the function
[02:12:10] calling convention from
the operating system.
[02:12:13] - We should explain that.
[02:12:14] - That is extremely-
[02:12:15] ... complex. But basically, usually
when you do move from one function in,
[02:12:19] in code to another, there is a
way to save the registers, the
[02:12:23] state of the CPU to enter another
function. And this is like standard.
[02:12:28] - It's a bit complex. I would
simplify this a bit. So,
[02:12:31] so dav1d does things to abuse the calling
convention. You could define the calling
[02:12:35] convention as
[02:12:36] I've written a function and I want to
call another function. How is the data
[02:12:40] shared between the functions? Because there's
a convention, what's known as a calling
[02:12:44] convention, and what dav1d
does for optimal reasons is
[02:12:49] create its own calling convention
sometimes. So if I wanna call Lex
[02:12:53] Fridman's library, we got, we've got to
agree on a convention so that I can share
[02:12:57] data with you in the assembly language
space. And one of the challenges
[02:13:01] in assembly is every operating s- well, not every
operating system, but there are, well, at least
[02:13:05] four that I can think of on
x86, Linux 32-bit, Windows
[02:13:08] 32-bit, Windows 64, Linux 64.
They all have their own calling
[02:13:12] conventions. And so one of the amazing things
Loren Merritt did, who we talked about
[02:13:16] before, was create a very lightweight
abstraction layer, so you could write your
[02:13:20] assembly code once and it handled all
the calling convention stuff for you,
[02:13:25] which was always a problem because you had
to manage four different variants. But
[02:13:29] dav1d takes this even further, for speed
reasons it does its own calling convention,
[02:13:34] within itself to bypass the
kind of rules, the rules
[02:13:38] of, the rules of sort of functions and say,
"Okay, actually I'm gonna call a function this
[02:13:42] way because I know it's
within my library."
[02:13:45] - Does it have to be special to
every single operating system?
[02:13:48] - Well, if it's custom, no. But
the, the, the challenge is
[02:13:51] in general, yes, and in terms of, in
terms of each instruction set. So the
[02:13:55] thing to also emphasize is we do this
on every instruction set. So every
[02:13:59] instruction set has its own handwritten
assembly, which is even more crazy. And
[02:14:03] that, that, that matrix has got
bigger in recent years because
[02:14:07] of RISC-V, because of ARM64, because
of the new SVE. There's SME. x86 has
[02:14:14] AVX-512, AVX. So we do runtime
[02:14:18] processor detection. We see what the
machine FFmpeg is running on or dav1d's
[02:14:22] running on is capable of, because
you could be on a laptop from 2008
[02:14:26] where this isn't there. Runtime detection,
we set function pointers accordingly.
[02:14:31] And then from then on, off you go.
[02:14:34] - Or you could be on a machine with RISC-V.
[02:14:36] - Yes. And in all that, we don't
even respect the calling
[02:14:39] convention of the operating system in
order to be faster, because we know that
[02:14:44] we are going to be called from within
our binary, so we can share data
[02:14:47] without saving all the registers in
the common way, because that can lead
[02:14:51] to loading and saving
registers on the L1 and
[02:14:55] L2 CPU and gets us faster. So that's why I
said that understanding CPU architecture,
[02:15:03] computer architecture is key. And this is
also why it's handwritten. I don't know
[02:15:07] anyone, I've never heard any other
project than dav1d doing that. This
[02:15:11] is why Kieran calls it, calls
it an art, right? It is an art.
[02:15:14] - I think in a mass world, there isn't
something on billions of devices.
[02:15:18] I know there are some specialist industries. I
know in high-frequency trading, they take this
[02:15:22] really seriously, where they're receiving
feeds from a market, and they need to react
[02:15:26] within X number of microseconds, and so
the instructions matter. But that's not
[02:15:30] a mass, you know, a mass-produced thing
that's on a billion devices. That's
[02:15:33] hyper-specialized, running on
hyper-specialized hardware. We're running on
[02:15:37] all hardware from-
[02:15:39] - Sorry to linger on it,
but, like, that's a really
[02:15:42] counterintuitive, almost,
like, revolutionary
[02:15:46] idea here, that there's a huge
amount of value to assembly.
[02:15:50] Like, what are we supposed to take away from that? Like,
what... You know, there's a bunch of people listening
[02:15:54] to this, they're basically
like, sorry, for myself
[02:15:58] included, you know, I programmed
for many, many years in C/C++,
[02:16:02] going up the standards of C++, fell in love
with C++, even meta programming and so
[02:16:06] on, and then transitioned more and more
because of machine learning about 15
[02:16:10] years ago to Python. And so, like, for
me in this Python world, JavaScript
[02:16:15] world, now vibe coding,
where I'm just using natural
[02:16:19] language, sitting in my jacuzzi, drinking a
drink... and just talking to the computer,
[02:16:24] re- like, like record
stops. Why is the value
[02:16:28] to go back all the way down to the low
level? Like, what's the intuition?
[02:16:31] - Because you can get more power per dollar
[02:16:35] invested, right? And
sometimes it's going to be a
[02:16:38] problem that is limited by your hardware.
[02:16:41] A good analogy is what
you see in quantization
[02:16:45] in LLMs, right? And people are doing,
"Oh, I'm going to do that in FP8
[02:16:49] or FP4 or some crazy things like
Microsoft Phi, who did it in 1.5,"
[02:16:55] because you're constrained by memory, because
you're constrained by the machine you
[02:16:59] can run. Because at some
point we are doing real time,
[02:17:03] and I believe this is going to happen
on AI inference also, is that at
[02:17:07] some point you need to get faster,
and you cannot always get harder,
[02:17:11] More powerful hardware,
right? So you need to
[02:17:14] analyze code and see
where, like, where is the
[02:17:18] mission critical, where is the
things that are called nonstops. And
[02:17:22] for example, dav1d is a good
example. It's going to be run
[02:17:26] billions of hours per day.
[02:17:28] That makes sense. It doesn't make
sense to be on the glue of FFmpeg-
[02:17:33] - No
[02:17:33] - ... uh, CLI. It makes sense over there.
[02:17:35] - Yeah, and this has to do, also we'll talk
about it more, but your new effort, your
[02:17:39] new company, Kyber, is doing
that kind of thing for
[02:17:43] ultra-low latency, so the slogan
being, "Every millisecond counts." And
[02:17:47] when you actually extremely highly
constrained in some dimension-
[02:17:53] - We are also arriving at
a point where we've done
[02:17:57] so many great things, but the hardware
is getting back to us, right? Because
[02:18:01] cost is increasing, because we
need more power, and so you're
[02:18:05] limited by either your
CPU, your RAM, or your
[02:18:09] networking, and you need to
optimize, and this is where
[02:18:13] value is going to be. Especially
because, like, doing AI is going to help
[02:18:17] do the programming of, like,
business, right? And so
[02:18:21] the core thing that you
will not be able to vibe
[02:18:25] code are optimization for the hardware
to be as fast as is possible.
[02:18:31] - I'd love to talk to you about who and how
[02:18:34] should learn assembly, but first,
I think we need a bathroom break.
[02:18:39] Quick ten-second thank you to our sponsors.
Check them out in the description. It really
[02:18:43] is the best way to support this podcast. Go
to lexfridman.com/sponsors. And now back
[02:18:49] to the episode. All right, and we're
back. There's this nice repo with the
[02:18:55] assembly lessons. First of all,
do you think developers should
[02:18:59] learn how to program in assembly, and how
would you go about learning it? What is
[02:19:05] this asm-lessons?
[02:19:08] - So I personally wasn't happy with the way
[02:19:11] assembly is taught in books
and online, 'cause it's very
[02:19:15] grammar-focused, and you don't,
in general, learn a language from
[02:19:20] learning the grammar and the
structure. You learn a language by
[02:19:24] asking someone what their name is, and you start
from there, and you go and solve real problems,
[02:19:28] That you have when you want to
communicate. You don't learn sentence
[02:19:32] structure, and this is the interrogative and the
adverb, and all, all the assembly books seem to be
[02:19:35] doing like that, going through every instruction,
even ones that aren't really relevant,
[02:19:40] explaining what they all do and how they...
It, it actually doesn't really change much.
[02:19:43] So,
[02:19:44] and the other problem that we have in our community
is assembly is taught sort of hand to hand,
[02:19:49] like person to person, like blacksmithing
one by one. That's, that's the only logical
[02:19:53] sort of analogy, and that doesn't
really scale online. It doesn't
[02:19:57] do other things. So this...
I've started a set of assembly
[02:20:00] lessons in the, in the way it's done in
FFmpeg, which is a little bit different to the
[02:20:04] way assembly in general
[02:20:08] for... I don't know. I'm trying to think the
other good big use case of assembly is in
[02:20:11] embedded devices, in really low
power, cheap devices, and that's
[02:20:15] completely different to
what we're doing here.
[02:20:17] I think it would be good if you could highlight
the requirements, which are quite simple.
[02:20:20] It's high school mathematics and C. And
actually not even C, really, really
[02:20:24] it's pointers. To emphasize, yes, we've
talked about how brilliant this stuff is,
[02:20:28] but high schoolers like
Daniel Kang have written
[02:20:33] assembly in FFmpeg. I think there's been
contributions because of these lessons.
[02:20:38] So it's really about
[02:20:40] trying to get this dying art to
continue, because we've shown it's
[02:20:43] possible with dav1d to
produce something amazing.
[02:20:46] There's still a lot of codecs in
FFmpeg that are only maybe partially
[02:20:49] assembly optimized.
[02:20:53] And so it really, it really starts with basics and
continues, explains a lot of the jargon, a lot of
[02:20:57] the syntax. It doesn't really
try and explain to you, you
[02:21:01] know interrupt handlers and interrupt
instructions and all of these
[02:21:05] different jump targets actually
makes this really vector focused.
[02:21:08] - And describes all kinds of registers:
general purpose registers, vector registers,
[02:21:15] Really nice examples. Oh, this is cool.
[02:21:18] - It's a classic, yeah, it's a
classic example of FFmpeg. But
[02:21:21] some of this assembly language is really
beautiful, and I think it's beautiful
[02:21:25] because it's kind of like
flying a Spitfire. It's
[02:21:27] really aviation at its purest, but also
[02:21:31] pushing the aircraft beyond
what the designer thought was
[02:21:35] possible. So we're abusing, for example,
sometimes cryptography instructions to
[02:21:39] do certain things, and there's
a level of beauty and art where
[02:21:43] it's really you and the processor. There's
nothing in between. It's you and the
[02:21:50] joystick of the cockpit, and you move that
joystick, and it's physically connected to the
[02:21:53] ailerons, and you can push that plane beyond
what it can normally do, and there's a
[02:21:58] level of, yeah, beauty and amazingness
to go that. But I don't think
[02:22:05] the sort of person-by-person assembly that is...
someone taught me, and I've taught multiple people,
[02:22:09] is gonna work long run
[02:22:13] just because of the particular
flavor and the way that we do it.
[02:22:16] - It's literally no, I
should... I was gonna say
[02:22:20] wizards handing it down. Um, I
realize I look like a wizard-
[02:22:23] ... wearing this hat. But you're
basically just like the sages, the wise
[02:22:27] sages handing- ... down the craft.
Can I ask you about LLMs? Like-
[02:22:31] ... can they help?
[02:22:32] - They had more of an understanding than
I expected, but they are still...
[02:22:36] I've asked it questions,
and it still goes and
[02:22:39] starts hallucinat- not hallucinating,
but making modifications, and then I go,
[02:22:43] "Is it bit exact?" "No." "Fix it." And then
it just goes and does the same thing, and
[02:22:47] it's going, it... There isn't the
corpus of information like Stack
[02:22:51] Overflow to work on.
[02:22:52] - There is not enough data to train on.
[02:22:55] And this is the biggest issue.
Um, I started my career
[02:22:59] actually doing some assembly for Itanium,
[02:23:03] right? So the Itanium is a dead
processor type, right, which was done
[02:23:07] by Intel and HP a long time ago
when they wanted to do 64 bits.
[02:23:11] Well, they lost, and then
we got AMD, who did it, AMD
[02:23:15] 64, which became x86-64. But Itanium was
[02:23:19] extremely interesting in
the sense that those were
[02:23:23] processors who had a ton of
computing power to do floats,
[02:23:27] FMAs, which is similar to what we
need now for, for LLMs, right?
[02:23:31] And you could pack three operations per
[02:23:35] line that could be loaded. So
basically, you had an output
[02:23:38] of basically six billion
of operation per second,
[02:23:42] but the bus, the memory bus only allowed
[02:23:46] 1.5, right? So your, your CPU
was four times faster, so
[02:23:50] you had to do crazy things to,
to pack things in memory or
[02:23:54] reuse the registers, and those
type of semantics, no language
[02:23:58] could do that, right? So like I have
[02:24:02] the Itanium programming book
because Intel did amazing books,
[02:24:06] but that's exactly what Kieran says.
If you don't know what you're,
[02:24:10] you're going to do, it's impossible to
read, right? It's a ton of jargon and
[02:24:14] so on. While those lessons
[02:24:17] are amazing because they are targeted to a
real problem, and you can do it yourself.
[02:24:21] - And people have. People have. There are patches, and they
said, "Oh, I studied your lessons, and here's my first
[02:24:25] changes."
[02:24:26] - That's amazing.
[02:24:27] - And part of that in the
lessons is a framework called
[02:24:31] x86inc, written by Loren
when, when he was working
[02:24:35] on x264, and it allows you
to do more things about
[02:24:39] that to create a type of like
not caring too much about
[02:24:42] different calling convention. And
we had a lot of students who,
[02:24:48] Gave code to x264 using that
a long time ago, right?
[02:24:52] So it's really doable, and I believe it's
[02:24:56] necessary to understand
assembly language, even if
[02:25:00] you don't do it much, to understand
what's going on inside your computer,
[02:25:04] and that will make you a better
programmer. And I assure you that
[02:25:08] because doing that, you will understand
some of the architecture of the memory
[02:25:12] inside your computer, right?
Understanding register, L1, L2,
[02:25:16] L3, RAM, SSD, disk, and so on,
[02:25:20] which are very important
because then you have a good
[02:25:24] programming culture that will
make you a better programmer.
[02:25:27] - Uh, what do you think about the Rust programming
language? 'Cause that's a bit of a meme.
[02:25:31] - We have very different
opinions with Kieran.
[02:25:33] - I think it's valuable what they're doing
in terms of memory safety as a concept.
[02:25:37] - Can it achieve some of the speed
up that assembly achieves?
[02:25:42] - Oh, not assembly by hand, no. I think
that that's a given. C potentially,
[02:25:46] but I see it very... It has
a very big Esperanto vibe
[02:25:49] about it. It's like we're gonna solve
this, and we're doing this in a particular
[02:25:53] way.
[02:25:54] - Meaning it's a bit too utopian?
[02:25:56] - There's a lot of focus on the self-importance
rather than solving real-world problems.
[02:26:00] It reminds me of the Sinclair C5.
Sir Clive Sinclair of Sinclair
[02:26:04] Computers built a car, and he said,
"Oh, everyone will be traveling around
[02:26:08] in one of these electric cars." And it
was... Rust reminds me of that, where
[02:26:15] I think the community doesn't
quite understand that
[02:26:19] in order to get people to move, you have to
build something that's as good as, if not
[02:26:22] better than what you have now. Yes, people
are doing Rust rewrites, but if they're,
[02:26:29] if they only do 85, 90% of the feature set
[02:26:33] of what we need, like things
like coreutils, that last
[02:26:36] 1% takes 99% of the time. To use
[02:26:40] Elon's famous quote, "Prototypes are easy." Like
this kind of stuff is easy. But this, to get
[02:26:44] a real electric car, you have to make a car as
good as, if not better than what we have now, and
[02:26:48] Rust isn't in that stage yet.
I don't think anyone would
[02:26:52] object to seeing Rust code in FFmpeg,
[02:26:56] but it needs to work as well and support
the same unit testing as everything
[02:27:00] else. It needs to be flawless. It can't just
randomly break. They can't just randomly
[02:27:04] break ABI when they want to.
It needs to have, I think,
[02:27:08] more-- I think it still has only
one compiler implementation.
[02:27:12] So it, it's got to be as good as, if
not better, and saying, "Hey, here's
[02:27:17] my utopia of memory safety,"
isn't enough, even though we
[02:27:21] probably all agree that that's the goal.
[02:27:24] - So I've done a ton of
Rust, and the two major
[02:27:28] topics I had was adding
Rust modules inside VLC.
[02:27:32] One of the reasons VLC got popular
and which was one of the main
[02:27:36] architectural decision, is that
VLC is a very small core and a
[02:27:40] ton of modules, right? And so
you can write modules in C, in
[02:27:45] C++, in Objective-C, and anything
that is basically interoperable
[02:27:49] with C. And so we did some Rust
[02:27:53] modules, and so I have experience on
that, and I wrote some of it. And also,
[02:27:57] like, my new startup called
Kyber, is an open source project
[02:28:01] mainly done in Rust. What Rust
is extremely good in, in the
[02:28:07] sense that it's a better C++ that cares
about memory and allows you to do
[02:28:13] things about memory ownership
that no one else can do so far.
[02:28:19] However, it's great when you start
a new project from scratch, and you
[02:28:23] do everything in Rust. But
it's very not good when
[02:28:27] you interop with existing part.
And some part of the Rust
[02:28:31] community believes that they need to rewrite
everything, and everything will be better with
[02:28:35] Rust. And the answer is like, no.
Like, I'm almost always, in all my
[02:28:41] years of being engineer, manager, CTO of
startup and so on, don't rewrite, right?
[02:28:47] - Is that-- That's the initial instinct
for a lot of people when they
[02:28:51] show up to a code base
probably before LLMs, is
[02:28:55] like probably because
they don't understand
[02:28:59] the wisdom of the way things have been done
in the past. They say, "Well, we need to
[02:29:03] rewrite it." Hence why there's a
thousand JavaScript frameworks.
[02:29:06] - But the reason is the following,
[02:29:09] and this is very important to
understand. It is an order of
[02:29:12] magnitude easier to write
code than read code.
[02:29:17] And you see that also with LLM. They
can write code, but analyzing is a lot-
[02:29:22] ... more difficult. And so
when you arrive and when
[02:29:26] you arrive to a very complex piece
of code, right? You don't understand
[02:29:30] it, right? Because it's so much
more effort to understand the code
[02:29:34] from someone else because you don't
have the thought process. Um,
[02:29:38] And often I joke about some languages
[02:29:42] mostly Perl, for example
which has very complex
[02:29:46] syntax. And imagine I am at my maximum
[02:29:49] intellectual efficiency
in programming, right?
[02:29:53] And I write the best code ever.
I will not be able to understand
[02:29:56] myself six months later, right? Because
reading code is more difficult. So
[02:30:02] very often you arrive, you don't understand
all the wisdom, all the business logic,
[02:30:06] the reasons that were done that is maybe
not documented. And you say, "Well,
[02:30:10] I'm going to write it." And the
thing is, no, you don't, right?
[02:30:14] Because that's, as Kieran said, right? I'm
going to rewrite coreutils in Rust. And
[02:30:18] then, of course, you arrive
very quickly at eighty percent
[02:30:22] then ninety percent, takes a bit more time,
and then you got the last ones, right?
[02:30:27] On the other side, right? So for new
projects, it's great. Everything related
[02:30:31] to parsing files networking because of the
[02:30:35] memory checker, boundary checker, it's
amazing, and there is nothing else.
[02:30:40] To answer a bit differently for us,
[02:30:44] imagine I take a piece of
software like dav1d or
[02:30:48] x264, right? Which has a ton
of runtime in assembly, right?
[02:30:52] Um, I rewrite the C part in Rust,
right? So it's more secure.
[02:30:56] Yes. But then you arrive into
the assembly, and you can jump
[02:31:00] anywhere in the memory because we
are doing handwritten assembly. So
[02:31:04] even if I rewrite the C
part in Rust, for security
[02:31:08] reason, you break all
the security when you
[02:31:12] you write handwritten assembly
because we can jump anywhere.
[02:31:16] So in my opinion, we need
to do something that is
[02:31:20] secure assembly, right? So which
is compile time, check the
[02:31:24] assembly, which is similar to
the checkasm projects that we're
[02:31:28] doing on dav1d and x264 with VideoLAN,
is to start instrumenting your
[02:31:35] assembly at compile time to check that
it's not jumping anywhere in the memory.
[02:31:39] Because else you might rewrite
a part of C in Rust, but if
[02:31:43] you want to have the same performances, you're going
to have inline assembly, and so you destroy your whole
[02:31:47] security model. So that's a
bit what I think about Rust.
[02:31:51] - No, I just wanna... I would say on
a personal level, I'm so in awe
[02:31:55] about assembly. I actually--
[02:31:58] Once in a... It never gets old, the
speed improvements to show sixty-two
[02:32:02] x. So there are months, on
a personal level, I run
[02:32:05] our internal test suite at work and just
see I'm still in awe at the gains we have.
[02:32:10] - Well, there's a source of joy and happiness
with programming for different reasons.
[02:32:15] But I think one of the greatest happinesses
is in the optimization of code.
[02:32:21] And it sounds like you're, like,
at the cutting edge of that.
[02:32:24] - I was like, "Whoa, that was cool."
[02:32:25] - And in the community, I want to
speak about two people who are
[02:32:30] wizards of assembly, right? The
two of them are actually working
[02:32:34] living in north of Europe
Sweden and Finland. And
[02:32:42] Henrik Gramner knows so much about Intel
x86 assembly that when we ask questions at
[02:32:50] Intel about things, they tell, like,
"Why are you asking us, Intel?
[02:32:54] You have Henrik. Henrik knows
better." He knows all the cycles
[02:32:58] of almost all the SIMD
instruction by all the CPU
[02:33:03] generation. "Oh, yes, this is a P4, this is
a Nehalem, this is a Core 2," et cetera.
[02:33:08] That person is, like, the best
person on assembly in the world.
[02:33:12] And he's the nicest
person that you've seen,
[02:33:16] like, very... He arrives,
you don't see he's
[02:33:20] amazing. And the other
one is called Martin,
[02:33:24] Martin Storsjö, and he's--
they're doing mostly the same
[02:33:28] on Arm, right? So Neon, right? And iPhones
and Androids and so on. And he codes in
[02:33:35] assembly on his phone, editing
it with the crappy keyboard,
[02:33:43] like virtual keyboard you
have while watching his kids
[02:33:47] play in the playground, right?
Like, like this is just like
[02:33:51] wizard level. So those
two people are like-
[02:33:55] - Yes. So when you're
programming assembly at
[02:33:59] that high level, a part of that is knowing
the architecture that you're programming on.
[02:34:03] - Yes. On Arm in particular, yes
[02:34:04] - ... Arm in particular. But x86, I mean,
these are complicated architectures, right?
[02:34:09] - Yeah. But Arm in some ways
is more com... x86 with,
[02:34:13] Out of order execution is not so bad. Arm,
you really need to understand all the
[02:34:17] different generations of Arm processor
because they're all different. There's A72,
[02:34:22] ... et cetera, et cetera. And there's the Apple variant, there's
this variant, there's that, and you need to write code that
[02:34:26] works
[02:34:27] efficiently on all of them. x86, well, broadly
speaking, you have Intel, AMD, and you have
[02:34:31] sub-variants, but generally
speaking, there's...
[02:34:36] Something fast is gonna remain fast on all
of the variants, whereas in Arm it's a
[02:34:39] completely much more complicated ballgame.
[02:34:43] - We're taking a nonlinear journey
through history here, but we're
[02:34:46] talking about Michael
Niedermayer. And I wanted to ask
[02:34:52] about this. For a time there was
a split in FFmpeg and Libav.
[02:35:00] - Yes. So in open source projects
sometimes you disagree, right? Um-
[02:35:10] - You have such a nice way
of putting it, yeah.
[02:35:12] - And the good thing is because of the
license, you're allowed to basically do your
[02:35:16] own, right? Um, and this is normal, and
this has happened all the time, right? At a
[02:35:21] point there was a GCC at the time of GCC 2
and EGCS which became then GCC 3, right?
[02:35:29] There is what we told KHTML
with WebKit, with Blink. Um,
[02:35:34] it is a same process. And also,
like when I want to do a new
[02:35:37] feature today in VLC, I fork, I do
my thing on my own, and then I merge
[02:35:41] back to the community. So there was a
split in the open source community on
[02:35:45] FFmpeg, which become Libav and
FFmpeg. And after a few years,
[02:35:49] well, the community merged back and
people moved on. It's a bit, um,
[02:35:54] drama that is normal in open
source community, but forks
[02:35:58] are even... They're important
because they change the,
[02:36:02] the status quo of a community. Um
[02:36:06] not talking about FFmpeg and
Libav here, but the, or the GCC
[02:36:10] fork made GCC a ton
better because the, some
[02:36:13] people wanted to change the
architecture fundamentally to make it
[02:36:17] faster. And of course, it's
always question of people and
[02:36:21] so on, but in the end you
realize that FFmpeg today is
[02:36:25] better than it was before the fork. And
[02:36:29] now, well, we're back all
together, right? And I spent a
[02:36:33] lot of time, and, and Kieran can
say in the, in, in the community.
[02:36:37] It's not often, to be honest, very
[02:36:40] well explained because a ton of
the reasons are not very public.
[02:36:45] But I think that's, that's
normal and that's good.
[02:36:49] - Yeah. I mean, you're making it sound really
nice, but there is battle, there's pretty heated
[02:36:53] battles inside open source projects. I
mean, it is a very passionate community and
[02:36:57] you're kind of in a distributed way
have to define the direction of things.
[02:37:01] So here looking at
Perplexity, "FFmpeg and Libav
[02:37:05] split in 2011 mainly over project
governance, leadership style, and
[02:37:09] development processes, not because of
a fundamental technical disagreement.
[02:37:13] Uh, FFmpeg effectively
absorbed Libav's work
[02:37:17] while Libav withered and most
distributions and developers moved back to
[02:37:21] FFmpeg." Yeah, that was a, that was a weird
experience 'cause, you know, I'm a Linux user,
[02:37:24] perspective, that was a weird experience
'cause, you know, I'm a Linux user,
[02:37:29] so, you know, whether it's Ubuntu and so
on, all of a sudden, I think for, for a
[02:37:33] for, for a little bit, Ubuntu,
I feel like, am I remembering
[02:37:37] correctly, switched to Libav and-
[02:37:39] - 12, 14, something like that.
Yes. Something like that.
[02:37:41] - And then they switched back to FFmpeg.
I was like, "What is happening?"
[02:37:45] So on the sort of you get
to feel the ripple effects
[02:37:49] of the different internal
debates that are happening.
[02:37:53] - To be fair, on Apple, when you type
GCC, you get Clang. Like they, they did
[02:37:57] something like that as well, so.
[02:37:58] - Yeah. So, so to me it's like the fork
was like heated drama, but most of the
[02:38:05] development from Libav was
merged back into FFmpeg, right?
[02:38:08] So de facto FFmpeg got a a superset around
[02:38:12] Libav, and so that gave the user, because
in the end we work the user, for the
[02:38:16] users, a, a larger set of features and a
ton of things that were, um, discussed.
[02:38:22] For example, the debate on
reviews, on, on how we push are
[02:38:26] something that now is completely settled in
FFmpeg and is following what mostly what
[02:38:33] everyone in the community agrees,
right? So de facto, everyone who
[02:38:37] was active on Libav came back in work on
[02:38:40] FFmpeg because the
disagreements were fixed, and
[02:38:44] in the end, FFmpeg is stronger than
it, it was before, right? And-
[02:38:49] ... I know people love drama, but, um-
[02:38:52] - Well, my main concern, I
understand, and I think
[02:38:56] looking at the, the long
history, it's all for the good.
[02:39:02] But I do... I am concerned
because there's so few humans
[02:39:06] that are critical to the success of open
source projects that I have seen it,
[02:39:11] Be a psychological toll on folks
[02:39:16] and, you know, sometimes leads to burnout. So
you have these incredible people that are at
[02:39:20] the core of open source projects.
There is a moment that happens
[02:39:24] 'cause, like, what is the motivation of doing it?
Ultimately, it's because you're passionate about it
[02:39:28] and it makes you happy. Then at a certain point,
you wake up and it's like, "This's been a
[02:39:32] bit too much heat from the
drama. So, like, at the, at
[02:39:36] the project level, the project
continues and often flourishes.
[02:39:40] But sometimes there's these
individual humans that are just like-
[02:39:44] - But-
[02:39:44] - ... I've had enough.
[02:39:45] - Yeah, but it's not just about forks,
right? So it's a g- very, uh-
[02:39:48] ... what, what you, what
you are referring to is
[02:39:52] one of the most challenging and most
interesting part of open source
[02:39:55] today is maintainers burnout, right?
[02:40:00] And AI is a problem because
of that. And Daniel
[02:40:04] Stenberg, which is the maintainer
of curl who's probably one
[02:40:08] of the best promoter of
open source in the world.
[02:40:12] He's, by the way, a member of the European
Open Source Academy with me, so I'm
[02:40:16] very, like, humbled to be on the same
community as him, right? He's against what
[02:40:20] he call AI slop, right? Because it
gives a ton of, um fake reports or-
[02:40:27] ... bad reports, bad patches, and
then a lot of maintainers have
[02:40:31] a lot of burden to maintain the
software. And this is straining the
[02:40:39] mine of open source developers
much more than forks.
[02:40:42] Uh, and for example, the XZ
fiasco was because there was
[02:40:46] one guy maintaining it, and he
got basically hammered by two
[02:40:50] attackers who were asking him
questions nonstop at weird times at
[02:40:54] night to block him, and at some point he
got fed up and says, "Okay, I can't do
[02:40:58] that," and gave the commit
access to the attacker.
[02:41:01] Um, so burnout in open source community is
[02:41:05] something that exists but mostly it's
about maintaining things, right?
[02:41:11] - No, for sure. But I wonder how do we
help that, 'cause those people are so
[02:41:15] important. The-
[02:41:16] ... the human beings are so important
to the core of these pro- projects.
[02:41:19] - So, so for example, now I am maintaining
a ton of multimedia and non-multimedia
[02:41:23] library- ... as maintainer
because the maintainers
[02:41:27] got fed up, right? Some on
VideoLAN, some outside of VideoLAN,
[02:41:31] Because it's sometimes you need a tough
[02:41:35] skin, right? Because you get, like,
it's not really attacks, but oh, this
[02:41:39] is not working, this is not working,
and you feel it personally. And this is
[02:41:43] also why resources or the,
the Google fiasco is,
[02:41:48] was a problem, right? They don't
realize that in the end you have,
[02:41:52] You know, it's like the same graph where you
see, like, everything and it's just like
[02:41:56] one random open source project
that is maintaining the whole-
[02:41:59] - The Nebraska thing, yeah
[02:42:00] - ... internet. You see the one, right? The-
[02:42:01] - Yeah, this is the meme. I mean, it applies
to, to a lot of open source projects.
[02:42:05] But this is
[02:42:07] the all modern digital multimedia
infrastructure, and then that thing at the very
[02:42:11] bottom that everything
relies on is FFmpeg. It's
[02:42:15] true. And then there's usually, you know,
a handful of folks that are maintaining
[02:42:19] that.
[02:42:19] - And FFmpeg or VLC, right, you
have a community of 10, 15
[02:42:23] core developers, are not the
worst open source project. XZ,
[02:42:27] which is even in more installations, is
one person, right? There is one guy-
[02:42:32] - libxml is, uh-
[02:42:34] - Yeah, libxml, right? There was a
big stop. No one is maintaining-
[02:42:37] ... libxml anymore, which is like parser,
the only library that is able to parse XML
[02:42:41] everywhere.
[02:42:41] - All the crazy edge cases of XML under
ridiculous circumstances, and they
[02:42:45] get attacked by security researchers
because there's one other
[02:42:49] crazy edge case that they haven't thought
of, and it's like, yeah, but the body of
[02:42:53] knowledge to actually
resolve that is massive.
[02:42:56] - There is one guy maintaining all the
time zones for everyone who is in the
[02:43:00] middle of, I think, was it Nebraska or-
[02:43:02] - Yeah, it could be, yeah
[02:43:02] - ... South Dakota? Like, the mental health
[02:43:06] of the open source maintainers
is something that large
[02:43:09] corporations don't care or don't see,
right? It's just like, "Oh, yeah, I'm just
[02:43:13] doing an open source report," and so on.
[02:43:16] - Mm. Some of it is financial,
but some of it, and
[02:43:20] people should definitely support open source
financially— ... all across the board.
[02:43:24] But some of it is also, like, spiritual on
a basic human level. There's something that
[02:43:28] happens,
[02:43:29] like, with this image of F- FFmpeg and
so much of the internet depending on it,
[02:43:34] where people almost,
like, talk down to the
[02:43:38] folks who are carrying these
projects forward and maintaining it.
[02:43:40] - In the security community, they certainly did. That
was one of, that was one of the things I think that
[02:43:44] argument came out is
[02:43:47] there was, there was a portion of the security
community who's like, "No, these guys write crap code.
[02:43:51] They need to fix their crap code." I'm like,
"No, no, no, no. This is a guy's hobby project.
[02:43:55] You've, you've have a security bot that's
gone and found some AI-generated stuff.
[02:43:59] That guy didn't write crap code. It's just
[02:44:02] an edge case to the 99.99999 percentile he
[02:44:06] didn't think about because it's his
hobby project decoding Star Wars games."
[02:44:10] - Forget the hobby project aspect of it.
It's, it's just hard work, and it's
[02:44:14] it's beautiful, and it's like the, the right
approach there is to celebrate people-
[02:44:18] ... for doing incredible,
incredible work. It's, it's just
[02:44:22] incredible that humans step up-
[02:44:25] ... not getting really paid at, at
first or maybe ever, and then they're
[02:44:29] doing it out of the love of it,
and we need to, like, human
[02:44:32] civilization runs on people like
that. We need to celebrate them.
[02:44:36] - To, to give you an idea, I received death
threats on VideoLAN, right? And, um—
[02:44:40] - You mentioned that to me. Like,
what, what is, what is behind that?
[02:44:43] - So that must be, what, 2009, 2010, right?
Um Apple is moving from PowerPC to Core
[02:44:50] Duo, um, that probably in 2006, and by
[02:44:54] 2009 or 2010, I decide that we are not going
to do new versions of VLC for PowerPC.
[02:45:02] At that time, like VLC, we
were close to the number 1.0
[02:45:06] release. We were four of us, right?
Like, just like, "No, this is not
[02:45:10] possible." So I receive a death
threat with some powder in it,
[02:45:14] right? It-- Remember there was
some- ... anth- anthrax threats-
[02:45:17] ... at that time, right?
And it was because I had
[02:45:22] taken the decision to not
maintain the PowerPC port
[02:45:25] anymore. And of course, it wasn't
anthrax, of course. It was some type of
[02:45:29] flour and so on. But I received
that as a, with a letter of like,
[02:45:33] "You, you piece of shit, you should die,
PowerPC forever," and so on. And it was 2009 or
[02:45:41] 2010, right? I was, I was young. I
was just like, "Why? What did I do?"
[02:45:47] - Yeah, that can break your
spirit. It's like, why-
[02:45:49] - My mother freaked out, right? We had to
go to see the police and so on. And now,
[02:45:53] like, I'm going to say that I'm
quite happy that this happened
[02:45:57] at that time. It forged
me a lot, right? I am...
[02:46:01] I can see, I can take a lot of hate
on me. I'm okay with it, right?
[02:46:07] - It sucks that that's part of reality,
'cause all the people that love VLC,
[02:46:11] all the people that love FFmpeg,
like me, you know, I legitimately
[02:46:19] hundreds—probably thousands of
times in my life had a smile on my
[02:46:23] face because FFmpeg made
me happy, period. And how
[02:46:27] many times did I get a chance
to say that? Zero. Until I
[02:46:30] realized there's a Twitter account.
And every once in a while I'm, like,
[02:46:34] messaging it.
[02:46:35] - One of the things I like on the Reddit meme
about me, which I don't like this meme
[02:46:39] for a lot of reasons, but... And
someone says, "Oh, JB is on, is on
[02:46:43] Reddit," which I am, right? And I say, and
say hello, right? And then I got so many
[02:46:47] people who say, "Oh, thank you for VLC."
And, like, I take pictures, and then
[02:46:51] I share that to the Signal, to IRC.
Uh, yes, we use IRC on different-
[02:46:58] - I saw as a quick tangent, you
mentioned IRC is like Slack for old
[02:47:01] people. So you still use IRC?
[02:47:03] - Of course.
[02:47:03] - Yeah. I have it on my phone as well.
[02:47:05] - Of course.
[02:47:05] - Every day.
[02:47:06] - Works fine.
[02:47:07] - Wow. It works fine, huh?
[02:47:08] - Works fine, yes.
[02:47:08] - You have to power with a crank, I guess.
[02:47:10] - No, but there's no-
[02:47:12] - There's AOL. There's AOL
as your social media.
[02:47:13] - There's no ads, there's no tracking,
there's nothing. Like, it's, uh-
[02:47:16] - The biggest issue, to be honest, right,
compared to Slack is that it doesn't have
[02:47:20] threads.
[02:47:20] That's annoying. It doesn't have emojis
for reaction. Sometimes it, it would be
[02:47:24] nice.
[02:47:24] - IRCv3 has.
[02:47:25] - Yes, v3, but no one does it, and
you cannot edit your messages.
[02:47:29] Right? And the rest, it works
perfectly fine forever.
[02:47:31] - But how do you communicate without emojis?
[02:47:33] - Well, that's, that's why I
said it's for old people.
[02:47:35] - Old people. All right.
[02:47:37] - And we do emojis with like- ...
you know, the colons and dash and-
[02:47:41] ... parentheses, right? So.
[02:47:43] - Old school. So anyway, you communicate on
IRC. What were you even talking about?
[02:47:46] - Yeah, we are talking
about death threats and-
[02:47:48] - Oh, damn
[02:47:49] - ... but having people
thanking you, and sometimes-
[02:47:51] ... they got people who send me a message
and, and, "Oh, thank you for VLC."
[02:47:55] And I always answer because I want to
[02:47:59] validate the fact that you need to
thank the open source community.
[02:48:03] - Yeah, please, everybody
listening to this, celebrate,
[02:48:07] celebrate FFmpeg, celebrate
VLC, celebrate all the
[02:48:11] incredible open source
projects, Linux, everything.
[02:48:15] There's so many, there's so many... And
you know what? I mean, even outside of
[02:48:19] open source, just celebrate companies that
[02:48:22] create software that
you use a lot and love.
[02:48:26] - Celebrate human endeavor. Celebrate the
human effort to not just build something
[02:48:30] that's okay- ... build
something that is damn good.
[02:48:34] - Yes, this is important, right? Like,
because as we said, right, we work for
[02:48:38] technol- we do something very complex for
[02:48:42] the normal people. Like, we want our
excellence in tech to be useful for everyone.
[02:48:48] And this is why, like, this is why we
work, right? This is why I wake up in the
[02:48:52] morning is because I want
people to use our stuff-
[02:48:56] ... Because it's making
everyone's life easier.
[02:48:58] - Want to solve hard problems. Work on something
interesting, work on some interesting
[02:49:02] technical challenges.
[02:49:02] - As we are engineers, we love to build things,
right? When I was young, like very early, I knew I
[02:49:06] wanted to build, to be an engineer. I wanted
to do cars, right? Maybe at some point I
[02:49:10] will go back to cars,
right? But this is like we
[02:49:14] want to build things that are cool
and useful. And they need to be
[02:49:18] challenging, right? Because you
want your brain to turn on.
[02:49:21] - When did the two of you first fall in
love with programming, with building,
[02:49:25] with engineering?
[02:49:27] - When is the first time
you programmed, Kieran?
[02:49:29] - Microsoft QBasic. As I was on Windows
3.1 and Windows 95 Microsoft QBasic.
[02:49:34] - Oh, wow. Wow. What'd you build?
[02:49:36] - Uh, like a multiplication, just
counting loops like 10, 20, 30, 40.
[02:49:40] - Nice.
[02:49:41] - Then I thought I could do everything after that.
I wanted... I jumped from doing that to I want
[02:49:45] to create a soccer, no, a
football, soccer video game.
[02:49:48] And I drew all the, I drew everything out. I was like,
"I'm gonna do it." And I didn't quite grasp that
[02:49:52] actually, didn't grasp actually it's a
massive piece of work to jump from BASIC and
[02:49:57] drawing some pictures to a
video game, but there we go.
[02:49:59] - Yeah. I think I did also BASIC and
then, uh, Turbo Pascal when I was,
[02:50:08] yeah end of elementary school. But
[02:50:12] mostly the first time I actually did
some serious programming was the
[02:50:15] first year of you call that
middle school when you're 11?
[02:50:22] Um, I was I lived in Italy for
a year in Florence and it was
[02:50:27] amazing year. And like the maths teacher
[02:50:31] told us to, to work in a programming
language called Logo, where you had a
[02:50:35] turtle that was designing things-
[02:50:38] ... On the screen, and you would turn left
and right. And in the end, we used that to
[02:50:41] do a very complex programming because
of course you could do things.
[02:50:45] And, and this changed,
like, as I knew I wanted to
[02:50:49] do things with computers and program.
[02:50:51] - I don't think we quite talked about E-
H.264 properly. We talked about David.
[02:50:56] Can we return-
[02:50:57] - Sure
[02:50:57] - ... backtrack a little bit to
H.264, this thing that powers
[02:51:01] basically all of the video on the internet?
So, uh can you tell me the story of
[02:51:08] H.264? And Kieran, you're
actually a contributor-
[02:51:11] - Yeah to H.264. So, so H.264 is
a video encoder for the H.264
[02:51:16] video standard. It dominates
internet video, but also other areas
[02:51:20] such as Blu-ray discs. And Blu-ray discs are interesting
because the people that make them really want the
[02:51:24] highest quality,
[02:51:25] and there's some really cool high-end films
that have been encoded broadcasting and all
[02:51:29] sorts of other areas. H.264
was a big step change
[02:51:34] 'cause it kinda happened at the right time
as well. A lot of the development took place
[02:51:38] when HD video was coming out.
Intel Core 2 and Nehalem
[02:51:42] CPUs were getting fast. You could
do real-time video. But the most
[02:51:46] important thing was a key
sort of focus on visual
[02:51:51] metrics. So industry and
academia for 20 years
[02:51:55] before, was obsessed with mathematical
[02:51:59] metrics or what's known as peak signal-to-
noise ratio. So mean squared error,
[02:52:03] logarithm of mean squared error, and that
led to tons of issues because mean squared
[02:52:07] error leads to blurring because you actually
want to, you want to minimize-- You want to
[02:52:11] add a little bit of error to everything to, to reduce
the mean squared error as opposed to having a big
[02:52:15] error, and that led to loads and loads of
blurring. So but hobbyists bucked that trend.
[02:52:19] It was for their own personal
videos, mostly anime.
[02:52:22] So there were two, there were two things they did differently,
and there was a big iterative feedback loop with the
[02:52:26] community. They did some stuff differently.
Two, two big things, psychovisual
[02:52:31] rate distortion, so using
block energy, trying to
[02:52:35] compensate for human perception
when making decisions.
[02:52:38] - So the psychovisual distortion,
that's the critical-
[02:52:42] ... thing. That's the thing. I mean,
it's kind of revolutionary, like,
[02:52:47] that we can, like, rethink.
[02:52:50] Don't, don't make it, like,
this kind of theoretic thing-
[02:52:53] ... of compression. Make it all about-
[02:52:56] - Being pleasing visually to the eye.
[02:52:57] - Yeah, yeah. So compressing in a way that
loses the least amount of information
[02:53:02] for the stuff that matters for us humans.
[02:53:04] - Yes, exactly. As opposed to what industry--
Some parts of industry are still
[02:53:08] obsessed by this, which is
mathematical numbers that don't look
[02:53:12] good in reality. And then adaptive
quantization was the other big one
[02:53:15] where it was biasing bits against,
[02:53:19] complex areas and redistributing
them to less complex areas like
[02:53:23] grass. Grass has some high
frequencies, but it's kind of--
[02:53:27] it's less complex overall compared to more
complicated things. And this came around by
[02:53:32] ParkJoy. So ParkJoy was really
the canonical sample that
[02:53:35] was... Is the running around in the park.
[02:53:37] - This one.
[02:53:38] - Yeah. So this guy was really the--
[02:53:42] So this was created by Swedish
television in the beginning of
[02:53:46] HD, and it was done on film, and
it was no expense spared in terms
[02:53:50] of production quality, and it was
given away for free. This was really--
[02:53:54] And this is the sample really that sorts
the men from the boys in terms of it has
[02:53:58] so many challenges with the
trees, with the water, with the
[02:54:02] grass, with the motion, with
the... I don't think there's still
[02:54:06] been any public test sequence
as good as that these days.
[02:54:11] - So for people who are just listening, we're
looking at a bunch of humans running-
[02:54:16] ... along a river, as you have the
reflection, a lot of really high
[02:54:21] information textures everywhere, the
leaves and the lighting playing with
[02:54:25] the leaves and all of this.
[02:54:27] - You could show clearly that
encoders with high PSNR-
[02:54:30] - Will blur everything
[02:54:31] - ... will blur everything, and you could see actually
I could turn on psychovisual stuff, I could turn on
[02:54:35] adaptive quantization, and
[02:54:37] it would just look so much better. But
your metrics-- And these metrics are at
[02:54:41] the time were considered so holy.
[02:54:44] These are the holy metrics that are
untouchable. PSNR is the most important thing.
[02:54:48] - Uh, can you speak to how do you
measure psychovisual stuff?
[02:54:52] Like, how do you turn how pleasing
a compression is for a human eye-
[02:54:57] ... into a number? Is that even possible?
[02:54:59] - That's what, that's what Netflix have been trying
to do with VMAF. They said they've used a machine
[02:55:03] learning model.
[02:55:04] - That's a more recent thing. But
back in when x264 was being
[02:55:08] developed, that's by eye you're basically-
[02:55:10] - It was by eye. It was developers on their
laptops. So it's not like even with
[02:55:14] big companies with professional
screens or anything, it's-
[02:55:17] And that was actually one of the goals, which
was I don't-- The developers at the time,
[02:55:20] Loren Merritt in particular, said, "I don't wanna
test this on a thirty thousand dollar screen.
[02:55:24] It's-- I want this to look good
on someone's laptop at home."
[02:55:27] - Yeah. Brilliant.
[02:55:28] - Um, there is another sample which is--
[02:55:31] ... A sample that is Planet Earth's
killer sample that I absolutely love.
[02:55:37] And you are going to see why, right?
[02:55:39] - Yeah, you're going to love this.
[02:55:39] - Uh, it's a ton of birds, right, flying,
and the more it goes, the more there are
[02:55:47] birds, and at the end,
right, it's almost like
[02:55:51] you have millions of birds.
It's the most complex thing
[02:55:55] ever to encode, right? And well, you're
watching it on YouTube, and you see how
[02:55:59] bad the YouTube encoding
is actually, right? Um,
[02:56:03] and this is, like, phenomenal
to, to optimize and
[02:56:07] get perfect quality in
a constant bit rate.
[02:56:11] There was a lot of optimization,
mostly by Loren also, um-
[02:56:15] ... on anime, right? For a long
time, anime was very badly
[02:56:19] encoded because there was a ton of
banding, right? And so you see those
[02:56:23] those issues, and there
was a ton of things. So
[02:56:27] x264 is, like-- And today
it's still the reference
[02:56:31] to any encoder, new encoder, AV1, AV2,
VVC, HEVC, everyone compares to x264.
[02:56:38] - One of my favorite films, Cinema
Paradiso, I know the engineer
[02:56:42] who created the Blu-ray, and he showed
me the comparisons of x264 versus
[02:56:46] others, and the... it's
completely different. And I think
[02:56:50] a bunch of guys in the Blu-ray world
started using x264. Um, I think the big
[02:56:54] one was Chris Henderson from Warner Brothers.
He did the whole Fringe box set with that.
[02:56:58] So quite, like, a thing a person on the street
actually watches and wants to look good.
[02:57:02] And so they kind of took a risk in their
jobs doing that because they're in a big
[02:57:05] company. That big company can buy whatever they
want. And they said, "No, no, no, I want to use this
[02:57:09] free and open source thing so
that things look good for my, my
[02:57:13] customers and build the best." And to
this day, I personally still try and
[02:57:17] avoid watching the most
cinematic films on streaming
[02:57:20] services and buy the physical
discs because they look,
[02:57:24] they look good without even having to buy an
expensive TV. I think that's the key thing.
[02:57:28] - And x264 is yet another example of
open source project. It was started by
[02:57:33] Laurent Ehrsam when he was at École
Centrale Paris, where VLC was born.
[02:57:37] And then you got a generation of
people like Loren, like Jason, like,
[02:57:41] uh, Måns, like so many-
[02:57:43] - Henrik from-
[02:57:44] - Henrik, uh-
[02:57:45] - Anton, uh
[02:57:45] - ... and this is-- Anton, and
this is where the assembly
[02:57:49] thing that we use now on FFmpeg,
dav1d and so on, was born, right? So
[02:57:53] x264 is, like, amazing project with
people who were really all over the
[02:57:57] world, and I think most of
them never met each other.
[02:57:59] - But all of them, according to
Kieran, or large percentage, love
[02:58:03] anime. There's several things I've
never got into, and one of them
[02:58:07] is anime, and I need to
[02:58:09] - I watch anime so much, especially at
the time. Like, at the time it was like
[02:58:17] a lot of anime content doesn't
exist commercially, right? We
[02:58:21] are before Crunchyroll, right? So
what happens is usually people who
[02:58:25] love anime, who take some
things, some DVDs in
[02:58:28] Japan and rip them because there
is no commercial offering. And-
[02:58:33] ... some of the people who are, what
we call fan subbers, are basically
[02:58:37] translating themselves to make
subtitles, right? And at that time,
[02:58:41] you download completely illegally. It
was the only way to do that, right?
[02:58:45] And so all of that was
handcrafted, and it fits the open
[02:58:49] source community, right? Because they
needed tools to encode, to do fan subbing,
[02:58:53] right? One of the most amazing open
source projects for subtitles is called
[02:58:57] Aegisub, and it's a subtitle... It's
[02:59:00] done for anime, for, for South
Asian and Japanese languages.
[02:59:06] - There are weird textures in
anime that I don't think you get
[02:59:10] in real life content. I think that was a
key one, which was optimizing these weird
[02:59:14] textures that you get- ... because
anime is not done in a normal fashion.
[02:59:17] - Yeah. The way you produce it is not--
You, you mostly produce it, like,
[02:59:21] on screens, right? Since a bit of time,
and you have all those gradients,
[02:59:26] right? In colors, because they are very
easy to produce digitally, very complex
[02:59:30] to produce in real life. And the
[02:59:33] subtitles also are very complex
because you need to have often the
[02:59:37] Japanese and then you need to
have the diacritics, right?
[02:59:41] The what we call the rubi, right? Which
is the hiragana and the katakana for the
[02:59:45] kanji. And then because of course
you, so that you have the official
[02:59:49] subtitling, but you also need the English
subtitles or the French subtitles because you
[02:59:53] want to learn that, right? And there
is so many things crazy on, on
[02:59:57] subtitles and we had like crazy
samples on, on subtitles that
[03:00:00] we've seen all around.
So this is an important
[03:00:04] part of the, the culture, but
also because there was no
[03:00:08] official offering. There
was no way of doing that.
[03:00:11] - Uh, can you speak to the difference
between H.264 and AV1 and then
[03:00:16] x264 and dav1d? This is this big
[03:00:20] step. Can you help people understand,
are some of the streaming sites
[03:00:24] moving more towards that direction of AV1?
[03:00:26] - Let's be honest, all of
those codecs since MPEG-2
[03:00:32] video are the same concepts. The same
concept about inverse transform, about intra
[03:00:39] prediction, motion compensation,
entropy coding, all of them.
[03:00:44] However, each generation gives you a bump
between twenty-five and fifty percent
[03:00:51] more compression for the same quality.
[03:00:54] And so you had the MPEG-2, you had the
DivX era, you have H.264, which was, like,
[03:01:02] changing, right? H.264 improved so
much. And then you had more, right?
[03:01:06] You had HEVC, you had VP9 at the same time
of HEVC. VP9 is a bit similar to HEVC in
[03:01:14] terms of quality compression,
but it's royalty-free.
[03:01:17] Because in multimedia there
is ton of patents and the
[03:01:21] licensing after H.264
became out of hand, right?
[03:01:24] And could cost hundreds of millions
of dollars per year. So it made no
[03:01:28] sense. So Google did this
VP9 and the Alliance for
[03:01:32] Open Media did this new codec called
AV1. So you can imagine that AV1 saves
[03:01:39] between forty and sixty percent
less bandwidth than H.264-
[03:01:45] ... for the same quality, visual quality.
[03:01:48] - At a given bitrate.
[03:01:49] - At a given bitrate, right? So
that's really like you increase
[03:01:53] the quali- either you set the bitrate and
you increase the quality, or you set the
[03:01:56] quality and you decrease your bitrate.
But because now you move from, from
[03:02:01] SD to HD and HD to 4K and 4K to 4K HDR,
like you increasing the size by like two,
[03:02:09] factor two, three, four, right? So you
need to have better compression to
[03:02:13] keep it in terms of something
that is manageable.
[03:02:16] - It's more coding tools,
bigger blocks, lots more
[03:02:20] sub-partitions in each block. It's
just exponentially more complex.
[03:02:23] - It's more complex because
the encoder needs to search
[03:02:27] more possibilities, right?
So you, for example
[03:02:31] one of the things that is easy to
understand is to predict a block,
[03:02:35] a color block to another, you have
directions, right? So you can go
[03:02:39] left, right, bottom, up,
and then in terms of
[03:02:43] Like the other quadrants,
right? What I call north,
[03:02:46] northeast, northwest, and so on, right? But
that's eight directions. Then you can do
[03:02:50] more direction. You can do sixteen
or sixty-nine or one hundred and
[03:02:54] twenty-eight, right? You can-- And every
time your encoder is going to spend
[03:02:58] more time to see, oh, well,
this block is exactly this one
[03:03:02] and those type of tools that you
can bring, and the encoder needs to
[03:03:06] check which of the tools are going
to compress you better. And so
[03:03:11] I guess that AV1 encoding is two order of
[03:03:15] magnitude more than H.264 in terms of CPU
cycle, right? Order of magnitude, right?
[03:03:21] - Yeah. And as we discussed, CPUs are not getting
faster. You're just throwing more cores at the
[03:03:25] problem.
[03:03:25] - But also it's a fact that you encode
once and you have hundreds of millions
[03:03:29] of users, right?
[03:03:30] So for example, YouTube, a very good
example. YouTube encodes almost
[03:03:34] everything in H.264, but the popular video
[03:03:38] gets re-encoded in AV1
because it costs more, of
[03:03:42] course, to encode, but you encode once
and you send that to millions, right?
[03:03:46] So it's a trade-off between
encoding time and complexity-
[03:03:50] ... and CPU usage on the server
side and on the client side.
[03:03:54] Because at the end, if you're distributing
a video to hundreds of thousands of
[03:03:58] people and the size is
half of the other, then
[03:04:02] it's better. It's better for your battery, it's
better for your modem, et cetera, et cetera.
[03:04:06] - So we can lay out, let's say, the
top five codec container combos
[03:04:14] would be H.264 inside MP4 containers,
AV1 inside MP4 WebM containers,
[03:04:23] ProRes for nonlinear editing,
[03:04:27] Inside MOV containers. So for people
who don't know, I guess ProRes is
[03:04:32] - It's Apple's codec for editing,
originally for Final Cut Pro, and
[03:04:36] it's designed to be fast to decode, fast to
seek, because an editor will need to move
[03:04:40] very quickly. So it's a different use
case to the distribution element.
[03:04:45] - There's no or very minimal
temporal compression in the-
[03:04:48] - There's none, yeah. There's none in ProRes.
So you can cut, so you can do cuts.
[03:04:52] - This is what we call
intra-only codecs, right? So
[03:04:56] I'm going to explain
quickly what is IPB frames.
[03:04:59] - Yes, please.
[03:05:00] - Um, so I-frames, often key frames, but
[03:05:06] is complete frames. It's like an image.
It's a JPEG, right? You have... You can
[03:05:10] start, you see everything, right? And then
[03:05:14] you, the next image can be a P frame,
which is a predicted frame. So you take
[03:05:20] some part of the previous image saying,
"Well, I need the block five and seven
[03:05:24] and forty-two,"
[03:05:25] and you replace it, and then you just
give the extra information, right?
[03:05:29] But that means that in order to decode
this P frame, you need to have access to a
[03:05:33] previous I frame, right?
[03:05:35] And then, of course, you have more
complex one, which are B frames,
[03:05:39] which are B-predicted
frames, which can depend on
[03:05:44] different type of frames, some
in the past, some in the future.
[03:05:49] And so ProRes is an intra-only codec.
For the people who can see, this is-
[03:05:54] - Yeah, that's a good one
[03:05:54] - ... a very good one, right? So
I-frames are complete frames. Um
[03:05:58] P-frame basically depend only on I-frame,
and B-frames can depend on in front.
[03:06:04] - And this GOP, group of pictures, I
think the default for actually FFmpeg
[03:06:11] for H.264 is like two hundred and
fifty frames, something like this.
[03:06:19] - Yes.
[03:06:19] - And to me, it's just, it's like
magic, that you could predict
[03:06:23] that you could have a
complete frame every-
[03:06:26] - Several seconds, that means
[03:06:28] - ... several seconds, and then you could
still, you could have this chain of
[03:06:31] predictions you make, and the fact that
you can-- The fact that somebody like me
[03:06:36] can can use FFmpeg to compress
something and not notice
[03:06:39] that the result still plays
back smoothly is like magic.
[03:06:43] - You can even have, and we use that in tons
on Kyber, is what we call intra-refresh,
[03:06:50] where basically it's there
is no I-frames present.
[03:06:54] - You have no I... You have
one at the beginning.
[03:06:56] And you never send an I-frame. You get a-
[03:06:57] - How does that work? What is it?
[03:06:58] - You build up an I-frame gradually
across as the stream continues, so-
[03:07:02] - Ah. So you refresh certain
parts- ... of the image.
[03:07:05] - But so you never have an I-frame. Like
this is intra-refresh that we use, right?
[03:07:09] - That's even smarter.
[03:07:10] - But for me, for me the biggest mind-blown
when I started was the B-frames.
[03:07:15] B-frames means B-predicted
frames can depend
[03:07:19] on frames that are coming in the future.
[03:07:23] That means that in order to decode this
B-frame, you need to wait for the next
[03:07:28] frame that is dependent-
[03:07:31] - Yeah
[03:07:31] - ... buffer that, decode that one,
so that you can decode the B-frame,
[03:07:35] right? So the way you
decode the frame, the
[03:07:39] decoding order is not the
same as the display order.
[03:07:42] Right? That means the encoder
needs to be very clever and decide
[03:07:46] that, "Well, you know, I'm going to
depend on things like in the future."
[03:07:50] So this is like-
[03:07:51] - It's incredible
[03:07:51] - ... mind-blowing.
[03:07:53] - The fact it works so smoothly every day
is kind of miraculous in some ways. It,
[03:07:57] it works so... You can
have a stream that works
[03:08:01] across the world on their decoder
versus one in the US versus one here of
[03:08:05] different manufacturers, and they produce
bit for bit exactly the same material.
[03:08:10] That's quite remarkable, and do quite complex
things, and getting more and more complex
[03:08:14] and still be bit exact. There's a
lot of work that goes into that.
[03:08:18] - There's a lot of knobs you can control in this
whole process. There's a lot of really fascinating
[03:08:22] parameters that I've gotten to know
more and more over the years that
[03:08:26] FFmpeg gives you complete access to. Maybe
you could speak to some of them. So first of
[03:08:30] all, like obviously, we can lower the
resolution, we can lower the frame rate,
[03:08:34] we can use different kinds of codecs,
as we mentioned, from H.264 to AV1.
[03:08:39] There's ways to tune the
trade-off between bitrate and
[03:08:43] quality, as we've kind of spoken to. You
know, you could do constant bitrate,
[03:08:47] you can do constant quality, say RCQ, QP.
You can do the longer or shorter group of
[03:08:55] pictures, GOP, that we mentioned. I mean,
all that kind of stuff. It's crazy.
[03:08:59] Number of B-frames.
[03:09:00] - Yeah. What is crazy is
that a ton of people's job
[03:09:06] is to optimize those parameters, right?
[03:09:09] A ton of people that you see at YouTube,
at Netflix, at Meta, and so on,
[03:09:13] they're not writing codecs. They're
just like finding the right
[03:09:17] parameters for the file they
have, for the format they
[03:09:21] have, right? Because like something
that is for a movie or something that
[03:09:25] is user-generated content from
your phone or a screen recording
[03:09:29] or something that you're going to video
edit, you don't want the same things.
[03:09:33] And there are thousands of people whose
job is just to optimize all that.
[03:09:38] - Yeah. They're wizards. Hats off to them.
[03:09:42] Uh, YouTube like to deliver, all the
streaming sites actually, to deliver
[03:09:46] at scale. And like YouTube is
really magical because it's
[03:09:50] not just doing like what
Netflix does, which is one way
[03:09:53] broadcasting type thing. It
also has to upload videos from
[03:10:01] all the places. So they're
also doing encoding at scale-
[03:10:04] ... for videos that are gonna
be watched by like five people.
[03:10:07] And it still has to deliver
them re- like on a moment's
[03:10:10] notice. No, no delay, nothing.
No... I mean, very minimal latency.
[03:10:15] And also serve it in all
[03:10:19] different resolutions. Like YouTube
is basically the web version of VLC.
[03:10:25] - Yeah. Well, actually, it's funny
because, like Google Video, which
[03:10:29] was something they did
before they acquired YouTube
[03:10:33] was actually using the VLC
plugin so that you could run VLC
[03:10:37] inside the web browser using the ActiveX
[03:10:40] plugin. And so it worked
in Internet Explorer,
[03:10:44] and you were actually running
VLC inside your browser.
[03:10:49] Which is funny because today we have the
opposite, where we have VLC WebAssembly, where
[03:10:53] we compile all VLC and FFmpeg
to decode, to run VLC in
[03:10:57] inside the JavaScript virtual
machine with WebAssembly.
[03:11:04] - Okay, there's this legendary
story that you pointed me to
[03:11:09] that it was discovered via
[03:11:12] WikiLeaks release of all seven
documents. The CIA was using a modified
[03:11:16] version of VLC to basically try and
trick people, what? To steal their data?
[03:11:23] - Yes, exactly.
[03:11:23] - So can you explain what
the heck happened? What...
[03:11:27] - So, so this was a surprise, right?
Because at some point, WikiLeaks,
[03:11:31] uh mentioned some documents. There
were a few ones with something related
[03:11:35] to Blu-rays and VLC, but the,
the most interesting one was the
[03:11:39] CIA Vault 7, which, if
I understand correctly,
[03:11:43] Was the CIA had, like, a custom version of
[03:11:46] VLC where they had a
specific plugin. Yeah,
[03:11:50] exactly. This is-- Like, we had to,
to write a press release on that.
[03:11:53] - Uh, VideoLAN wrote a press release
saying the only safe source for getting
[03:11:57] VLC media player is the official
VideoLAN website. I mean, I
[03:12:01] suppose that's a security
vulnerability for
[03:12:04] basically any piece of open source
software. Somebody can trick you.
[03:12:09] - To download in a fake website-
[03:12:12] ... or targeted advertisement, right? That
was a targeted advertisement, to watch a
[03:12:16] specific file you need to
watch with this custom
[03:12:20] version of VLC. And it was the
normal binaries of VLC, except they
[03:12:23] added one DLL, I think it was psapi.dll-
... which was basically reading your,
[03:12:31] your document folder, encrypting
that, and sending that. And
[03:12:35] the thing is, this is very clever,
to be honest because once you're
[03:12:39] watching a movie, right, you're going to do that
for two hours, and you're not going to touch your
[03:12:43] computer. And sometimes it's normal
because it's HD that your, your
[03:12:47] fans are going up and say, "Vroom," and there
is ton of CPU usage because you're using
[03:12:50] VLC, right? That's normal. But the thing
is, what you don't see is that actually
[03:12:54] a powered version of VLC that is used
by CIA. We had exactly the same problem
[03:13:02] with Chinese hackers that were targeting
[03:13:06] Indian people, and that
got VLC banned from India
[03:13:10] until I had to, to fight
in courts in India, the
[03:13:14] Indian government, to unban
VLC. They didn't use VLC.
[03:13:18] They took just one DLL, because
we signed the DLL correctly,
[03:13:22] And they used that DLL
to do another program.
[03:13:26] So you had the vlc.exe and was
calling libVLC, but it was
[03:13:30] calling it into a fake one. And
they used that to target. Um,
[03:13:35] there is not much we can do actually
to block those type of hacks.
[03:13:39] - Yeah, and I think people should, for
all open source software, for all
[03:13:43] software in general, people should pay
attention where they download the thing.
[03:13:46] - Yes, because that means that they were
not downloading it from our website.
[03:13:50] - Do the search engines help you?
[03:13:52] - No, they don't.
[03:13:53] - Just to clarify, 'cause you can,
you know, to prevent threats from
[03:13:57] people manipulating SEO to get up
there on the links and try to-
[03:14:00] - Absolutely not, right? We have a big
issue for, like, more than ten years,
[03:14:04] is that there is a fake version of VLC in
[03:14:07] Germany that was reported
for now for 12 years,
[03:14:12] and Google basically decides to
not-- They know what's in it,
[03:14:16] but the binary is too big
for their virus analyzer to
[03:14:19] analyze it. And so while if you're
in Germany, you can go to a
[03:14:23] website that is a fake version
of VLC with a custom installer,
[03:14:27] and it's very popular in Germany because
their website is in German, and Google
[03:14:32] mentioned that before VideoLAN. And the
weirdest thing is that it doesn't do
[03:14:36] anything on your machine for three weeks.
[03:14:38] Because that's how they do the detection.
And after three weeks, there is a small
[03:14:42] program that is a service that install at the
same time that wakes up after three weeks,
[03:14:46] and it start downloading spyware and
adware. And Google knows about it.
[03:14:50] They've decided not to do
anything. The guys use dark SEO in
[03:14:54] Germany to do that at some point.
And this is very damaging, right?
[03:15:01] Because one of the things that they are downloading
is actually something that is replacing
[03:15:05] your ads inside your machine, right?
[03:15:08] - It's actually quite
surprisingly effective.
[03:15:11] Whoever is doing it with
Twitter and X. With X,
[03:15:16] I'll get emails about, "Your X
account has been hacked." And
[03:15:19] however they phrase it, it
gets me to, like, at least
[03:15:23] click on the email, not to follow
the thing, and then you're like,
[03:15:27] "Man, whatever they're doing with
the psychology to try to trick you,
[03:15:31] they're quite good."
[03:15:32] - There is a security v-version of VLC, right?
You received an email saying, "Hey, there
[03:15:36] is a security version update on VLC.
Think about updating right now because-
[03:15:40] ... it can hack your computer." You come.
It's a website that looks decent, and, uh-
[03:15:45] ... and you download. It's a new version of VLC.
Great. You don't know. A month later, you're hacked.
[03:15:49] You have no idea. You're part of a botnet.
[03:15:51] - Yeah. So make sure wherever you're
downloading stuff, it's legitimate.
[03:15:56] I'm part of the botnet. Speaking
of which, so you've mentioned
[03:16:00] that VLC sandboxing is some- is
something you're working on,
[03:16:05] and it's actually something quite challenging.
Why is it important? Why is it hard?
[03:16:09] - So VLC is a core with around
[03:16:13] 500 plugins, right? One of them
is FFmpeg, but we have, we
[03:16:17] support so many other
formats. We support new
[03:16:20] protocols, we support new filters,
we support weird architectures.
[03:16:24] And in this release of VLC, you have
[03:16:28] modules that are going to
call your drivers, right?
[03:16:31] Uh, mostly the hardware decoders,
which are going to call
[03:16:35] your Intel, your NVIDIA, your AMD driver.
And all calling FFmpeg, right? And
[03:16:43] there might be a security issue. There
might be a security issue in the shader,
[03:16:47] there might be a security issue in
VLC, in FFmpeg that is going to
[03:16:51] basically crash. The
issue is that you running
[03:16:54] VLC like every, every other program,
like Adobe, right? You're running it
[03:17:00] on your machine, and it has access
to all your documents, right? So
[03:17:04] the idea is to be sure that
you do a sandbox so that we
[03:17:07] can protect from ourselves,
because inside the
[03:17:11] VLC process is running some code that
is not even ours. Either it's open
[03:17:15] source for other projects that we
integrate in VLC, or it's your
[03:17:19] GPU driver or something that
is provided by someone else
[03:17:23] inside. And so when we
crash, we want to not
[03:17:26] allow people to do bad things, right?
Because one of the common way of hacking
[03:17:30] people is to crash a program,
very often done with a
[03:17:34] web browser, very often
done with PDF files,
[03:17:37] less often with multimedia, but that could
happen. And when you crash, you launch something
[03:17:41] on the machine of the person.
Could be a ransomware, could
[03:17:45] be a botnet, right? So security of
desktop application is important.
[03:17:50] On mobile, it's a bit different because most
of the mobile application are running on
[03:17:54] inside their own sandbox. But for VLC, we
[03:17:58] could run it inside one sandbox, but
the problem is that we need access to
[03:18:02] so many things that it's
basically we would do-- we
[03:18:06] would have all the permissions,
right? And so if you have a sandbox
[03:18:10] and you put some holes everywhere,
it defeats the purpose, right?
[03:18:14] So what we are trying to do, and
we're actually doing, is splitting
[03:18:17] VLC into several processes.
One is decoding, one
[03:18:21] is demuxing, one is filters, and all of
them run into their own sandbox so that the
[03:18:29] whole VLC, a part of VLC
crash, like Chrome crashes
[03:18:33] on some tab, right? It
crashes, but it does
[03:18:37] not crash the whole program. And this
is what we're trying to do. And it's
[03:18:41] difficult because it's a sandbox that
needs to sustain gigabits per second-
[03:18:45] ... of mem copies. Now, it's not a
website which is five megabytes or
[03:18:49] 10 megabytes. We're talking about hundreds
of megabits per second. So this is
[03:18:53] why it is quite challenging. And
this is a research topic that
[03:18:57] we are working on in order to have
multimedia player that is secure.
[03:19:03] - This is all the kind of stuff you have to
think about when millions of people are using.
[03:19:06] You've mentioned something somewhere
where like all the different
[03:19:10] features of VLC, when you have that
many people using it, somebody will use
[03:19:16] every single feature, and
they will tell you about it.
[03:19:20] - Best feature in VLC is called
the puzzle filter, right?
[03:19:24] So you click the puzzle
filter, and it transforms your
[03:19:28] video into a jigsaw puzzle, right?
[03:19:30] - Nice.
[03:19:30] - And you can click and
move the pieces, right?
[03:19:34] It's very, very useful when you're watching
a French movie, right? You're bored,
[03:19:39] ... because it's like very long things
or a love triangle, right? We've seen
[03:19:43] that so many times, right? But, but you
need to watch it because someone, your wife
[03:19:47] or-- ... told you to do that-
[03:19:49] - To catch up
[03:19:49] - ... or your boyfriend told you to do
that. So you're doing that, right?
[03:19:52] And you can click and
move the pieces around.
[03:19:55] It's absolutely useless, right?
Like, who cares about that?
[03:19:59] First, it was done by a
math teacher in high school
[03:20:04] in south of France to teach his
students about Bézier curves, which
[03:20:08] is something that-
[03:20:08] ... everyone should know about, right?
It's very useful. But the code was clean,
[03:20:12] so it got in VLC. It was merged
in 2010. Five years later, I
[03:20:16] receive an email saying, "Hello,
JB. I have a problem with VLC.
[03:20:20] The puzzle is too simple."
And I was just like, "What?"
[03:20:24] And yes, the puzzle was
in the UI maximums by 16
[03:20:29] by 16, right? Only 256
pieces. And he says, "I'm
[03:20:33] sorry, but in a movie I love
puzzled, this is too simple," right?
[03:20:37] So there is a commit of me, you can
check it online which is JB changing
[03:20:41] that the dimensions are 256 by 256.
[03:20:45] - Right.
[03:20:45] - But my point is, so many unused features
[03:20:50] are used by a few people, right?
There is a way to watch VLC
[03:20:54] movies in command line
without any UI, right? It's-
[03:20:57] - I saw that. You can do ASCII.
[03:20:59] - ASCII art. Is it useful?
Very useful. Imagine you're
[03:21:03] debugging... imagine you're debugging
a multicast network, right?
[03:21:07] You have thousands very complex,
[03:21:09] very complex networking stack,
right? You can SSH to all of the
[03:21:13] routers and put VLC on it with
no UI, and you're going to see
[03:21:17] whether it's black or it's not black, right?
So you see if or it's all green or not
[03:21:21] all green, right? So you can see-
[03:21:22] - Amazing.
[03:21:23] - Yeah, right.
[03:21:23] - This is fun.
[03:21:24] - People don't realize there is so many things
in VLC, that are useful and they are--
[03:21:32] they have users, because once you
have hundreds of millions of users,
[03:21:36] you have people who use every feature.
[03:21:40] - I would love to sort of
[03:21:42] zoom in and talk a little bit more
about the distinction between kind of
[03:21:47] downloading a file and
watching it offline versus
[03:21:50] streaming. So the complexities,
the challenges of streaming.
[03:21:55] Is there something we could
say about what it takes to,
[03:21:58] stream files? Because we've
been talking about codecs-
[03:22:01] ... and I think a lot of that implies
encoding and decoding without the
[03:22:09] having to communicate-
... over the network.
[03:22:11] - Sure.
[03:22:11] - Sure. So can you elaborate, like, what's
required to do over network stuff?
[03:22:16] - Yeah, but it is less complex than it
seems compared to everything that we've
[03:22:20] talked about. Especially
because the most complex thing
[03:22:24] is not about streaming in terms of, uh,
[03:22:28] streaming services, but
it was what was done to
[03:22:32] actually broadcast through
satellites. Because in, in
[03:22:37] most of the modern, uh,
broadcasting services, you can
[03:22:40] pause and you can go on. But when you're
sending live streaming, whether it's
[03:22:44] broadcast or live for streaming
services which are live, this is
[03:22:48] much more difficult because you
need to encode in real time. You--
[03:22:52] When you go on a satellite, you have a
specific size of the link, right? You
[03:22:56] cannot have a burst-
[03:22:58] ... of bandwidth even for a second,
right? Because you don't have the
[03:23:01] space for that in your total
file. However, there is
[03:23:05] different types of challenges, which
are interesting challenges, but
[03:23:09] I think they are less complex
than the one we've seen with late
[03:23:13] '90s and early 2000s about broadcasting
and streaming through satellite.
[03:23:18] - They're different. They are control systems challenges,
whereas, whereas some are more mathematical.
[03:23:22] I think that's the difference.
[03:23:23] - In the streaming world, what you have is called,
what we call adaptive streaming, because the
[03:23:27] difficulty-- And it's not really a
video problem, it's mostly a CDN
[03:23:31] problem, is that you might have too many people
watching the same thing at the same time,
[03:23:34] and it's a congestion of
the network, right? So your
[03:23:38] player has difficulty downloading
things fast enough to play
[03:23:42] them. So what happens is that locally,
the player is going to read a lower
[03:23:49] resolution-
[03:23:50] ... of it. But there are some very clever
algorithms to do that, but most of it
[03:23:57] is quite basic, to be honest.
[03:23:59] - Even on the buffering
side, it's pretty basic.
[03:24:02] - Yeah, you start to download a
segment, what we call a segment,
[03:24:06] and then you time, right? And
if it takes more than 50%
[03:24:10] of the time to download a segment, you
go down to... Right. And the difficulty
[03:24:14] is more about when do you go
up in bandwidth, in quality.
[03:24:18] But this is not very complex to do.
When you encode, you're going to
[03:24:22] encode seven resolutions, right?
And, and you're going to give the
[03:24:26] bitrate. The difficulty is to have
your encoder gives the same bitrate,
[03:24:30] but it's not as strict as
it, it used to be. So-
[03:24:34] - Uh, probably YouTube has to
figure out how the human
[03:24:38] psychology side of that, like
how pissed off do you get
[03:24:43] when it's like very low bitrate and,
[03:24:48] How long should it wait before it increases
the bitrate even though the connection
[03:24:52] is better? Because maybe the, the
changes in the bitrate is what, like,
[03:24:57] affects you psychologically.
[03:24:58] - No, I think actually the
interesting one is the audio.
[03:25:01] - That's true.
[03:25:01] - The-- You can kind of
notice when they move from
[03:25:05] full fat AAC to the there
are compressed versions of
[03:25:09] AAC that use Spectral Band Replication. You
can kind of see it goes a bit tinny, and
[03:25:13] that up and down is very
jarring. The video side
[03:25:16] is a lot smoother, and there's less notice. It's
really the audio you can definitely, you can
[03:25:20] definitely feel it from when it's moved you from
a different audio profile to one or the other.
[03:25:24] I don't know. We're surprisingly
tolerant at skipping audio glitches. I,
[03:25:28] I'm surprised people I know who
are not video engineers, how
[03:25:32] tolerant they are, how tolerant
they are to watching sports at
[03:25:36] 30 FPS, for example, whereas
it should really be 60.
[03:25:39] The world is a lot more tolerant to that, but audio
people are very-- There's-- It's an immediate
[03:25:43] feedback mechanism of,
"Oh, something's changed."
[03:25:44] - If you hear a glitch,
you realize it directly.
[03:25:48] I get to fully realize that, I suppose. One
of the things I'm afraid of when I listen to
[03:25:52] audio more and more, that I get to
notice every single tiny detail,
[03:25:56] and that you can over-obsess when people,
people in general are able to kinda,
[03:26:02] kinda blur their consumption. They can,
they can look past certain imperfections.
[03:26:08] - But then when you combine like
[03:26:11] an event that is, for example, a sport
event that is probably going through
[03:26:16] satellite or-
[03:26:17] ... somewhere else and goes to a central
place for encoding, and then you
[03:26:21] need to encode this older resolution
in real time. You don't have
[03:26:25] time for QA. You need to push
that to CDNs. You need to add
[03:26:29] probably DRM for protection.
You need to have that
[03:26:32] over a ton of different devices.
Then yes, it is complex. But--
[03:26:40] And also, like you're in the web
browser or in very much different
[03:26:44] devices that you use for
television, where you had like a,
[03:26:47] defined set-top box or cable box
that, that you know where you
[03:26:51] control end-to-end. So it's a
challenge, but it's less...
[03:26:55] I think the networking part while you
[03:26:59] agree to have 10, 20 seconds of latency,
I don't think this is very difficult.
[03:27:05] - Speaking of networking
and latency, so your new
[03:27:09] effort, as we mentioned, is Kyber, which
is aimed at ultra-low latency. As you say,
[03:27:17] every millisecond counts,
and you're applying that to
[03:27:21] remote control machines like robots, drones,
computers. Can you tell me about it?
[03:27:25] - Sure. If you start from where
we used to be, right? You used
[03:27:29] to use FFmpeg to encode files, right? And
then we used FFmpeg and VLC to encode in
[03:27:37] streaming services, right?
And then you need to go
[03:27:41] lower and lower. And the question
was where up to where can we go?
[03:27:46] And this question is very important
because there are many use cases
[03:27:49] where you need to be fast,
and it's when you have
[03:27:53] feedback interaction, right? We are not just
listening to something, you're actually
[03:27:57] controlling it, right? Because-- And that's
the biggest difference that compared to
[03:28:01] what we've done so far,
is that I need video
[03:28:05] to have a feedback on something that is
happening live, whether it's a drone flying,
[03:28:10] whether it's controlling
a humanoid robot from
[03:28:13] distance, whether it's controlling
a hover, whether it's playing a
[03:28:17] video game in the cloud
gaming, because this is,
[03:28:20] What I did on a previous
job, right? I was CTO of a
[03:28:24] cloud gaming startup. And
this is a very interesting
[03:28:28] topic because you push to
the limit the network.
[03:28:32] You need to be-- to care not about the
[03:28:36] quality like we've done on video, and we've
talked about with H.264. You care about
[03:28:42] latency, because a milliseconds is
[03:28:45] meaningful when you're controlling a
car, right? For-- Well, you've-- you've
[03:28:49] seen, you've used Waymos, right?
When Waymos don't work, and
[03:28:53] that happens even if one percent of the
time, there is someone that is basically
[03:28:57] remote controlling that.
And this is exactly
[03:29:01] the stuff that we're building. It's
really an SDK platform to do end-to-end
[03:29:09] control of machines.
[03:29:10] - So the-- this comes up quite a lot in a
lot of different contexts in robotics.
[03:29:14] So obviously, teleoperation,
teleop is becoming more and more
[03:29:17] important including for training,
Robots via machine learning.
[03:29:25] - Yes. And what we do is a bit
different from everyone else, is that
[03:29:30] we take only one socket, one
connection, which is a QUIC
[03:29:33] protocol based on UDP which
is interesting because
[03:29:37] it's done for low latency. It doesn't have
two of the, what we call the TCP head of line
[03:29:41] problem and the HTTP head of line
problem. It's ciphered by default, but on
[03:29:45] the same wire, we send multiple
streams, like multiple tracks. We send
[03:29:49] audio, we send video, but we also
send the commands, right? Uh,
[03:29:53] mouse, keyboard, gamepad,
and so on. And we do
[03:29:57] that while maintaining coherence,
right? Synchronization. Because
[03:30:01] what people don't realize
is that all the clocks
[03:30:05] actually drift. And when you're
controlling a robot, a robot is
[03:30:09] going to have, like, two cameras, five
cameras, ten cameras, a ton of captors,
[03:30:13] GPS, and so on. And if you
want to train correctly your
[03:30:16] robotic AI model, you need to
have all those that are in
[03:30:20] sync and current. And what we've done,
and it's all the stuff that we learn
[03:30:24] on VLC in broadcast in real time,
and MPEG-TS that Kiran's know
[03:30:28] well, is that we account for clock drifting.
And so when I record a Kyber stream,
[03:30:36] a robot, I am sure that it's going
to be predictive in the way you
[03:30:40] play it back. And so when you're
going to do recording and training
[03:30:44] of your AI model, you need to
be sure that every time you
[03:30:47] retrain based on the data,
it-- the data is going to stay
[03:30:50] coherent. And clocks actually drift. Like,
[03:30:54] the existing solution works with one
camera. Once you're going to a five or
[03:30:58] six, it's more complex.
[03:31:00] - Uh, so you wanna make sure that the visual
[03:31:04] snapshot perfectly matches the
time it actually happened.
[03:31:08] - Exactly. And also, if you're going to
control, right, I do something on robot, I
[03:31:12] need to be sure that it is actually
happening at that precise time,
[03:31:16] right? And so we have on the, the
server, which would be a robot, a
[03:31:20] time of, like, re-timestamping mechanism
accounting for clock drift for
[03:31:24] that, right? So that's one of
the use cases of Kyber to, to
[03:31:27] control robots. Um, I
also think, like, remote
[03:31:31] drones, remote whether it's
defense or non-defense, remote
[03:31:35] cars, remote submarines. There is many
places in industry or remote surgery where
[03:31:43] the expert cannot go everywhere
the machine is because it's either
[03:31:47] dangerous or it's too costly, right? So
you, you allow people to have machines
[03:31:53] next to you, right? The goal of
Kyber is to make distance disappear
[03:31:57] because it's either projection of
skills or projection of power,
[03:32:01] right? So imagine we are all
like— you've seen the Meta
[03:32:05] Ray-Ban and, and everyone else, right? You need
to stream there, right? Because you're not
[03:32:09] going to run anything over there, right? So you
need GPU power whether it's on a cloud, on a
[03:32:13] phone to stream that. And so
all of these use cases needs to
[03:32:16] be not about extremely low
latency, but real-time latency for
[03:32:20] video. And so that means you need--
[03:32:24] we're toying with the encoders so
that the encoders encode a frame in
[03:32:28] four milliseconds. And, and, and
Kieran with his company also goes
[03:32:32] under those type of latency,
because you need to optimize
[03:32:38] at max the local latency, right?
Because it's the decoder, the
[03:32:44] encoder and so on. Because this time is
going to be added to your networking time.
[03:32:52] So-- And it's not just about low latency,
it's also about, like, reliability. We do
[03:32:57] clever things like forward error
correction, right? So forward error
[03:33:01] correction is you over-transmit
a bit of data, right, a
[03:33:05] few percent and while
over-transmit, you're allowed to
[03:33:09] lose some packets. Because
all of that is very difficult
[03:33:13] over an internet network where you're
going to do things very far away. And
[03:33:20] if you check that all packets are
delivered, you add a ton of latency. If you
[03:33:24] don't want latency, what we
do is that we over-transmit
[03:33:28] some data that you can retrans--
reconstruct on the client
[03:33:31] side when there is things
that are broken, right? So
[03:33:35] And we a few, a few days,
weeks ago, we were doing the
[03:33:39] demo around Las Vegas for
the CES about we had a,
[03:33:43] a, a rover that is fully 3D printed. It's
very simple. It's a car, right? It's a
[03:33:47] small car with a telescopic arm, and it
[03:33:51] was actually controlled from
France, right? And the, the video
[03:33:55] was with a webcam and a very
small server, right? A small, a
[03:33:59] small PCB was basically
running and send that to
[03:34:03] someone that is on the
other side of the planet.
[03:34:06] And so there is so many use
cases. You can also think about
[03:34:09] having AI who are going to control
many drones and so on. And
[03:34:13] technically, we need to be amazing
in video, we need to be amazing
[03:34:17] at networking, we need to care
about any milliseconds in
[03:34:21] networking, in encoding time, in
decoding time, and also you need to
[03:34:25] integrate very low level.
[03:34:26] - So sync everything together well.
But how-- Like, what kind of latency
[03:34:30] can you get to? Like, why-- When you say
milliseconds, what, what's the goal?
[03:34:34] - So my goal is four milliseconds
glass-to-glass latency.
[03:34:38] - What's glass-to-glass mean?
[03:34:40] - So it's easy, right? You have a computer
which is running a program, right? Probably a
[03:34:43] video game, and this one is actually
running, right? It could be--
[03:34:47] it's an example of a robot, right?
And you have the replicate that is-
[03:34:53] ... done through the
network. And, and you want,
[03:34:56] if you take a, a one thousand
hertz camera, you can take a
[03:35:00] picture, and you want that to be at four
milliseconds. Four milliseconds means two
[03:35:03] hundred and forty hertz, right?
[03:35:06] - Yes. Nuts.
[03:35:07] - So far we achieve seven milliseconds
[03:35:11] from a Windows to Windows
or Windows to Mac. And
[03:35:15] if you look in the timing, most
there is around three point
[03:35:19] five milliseconds inside the NVIDIA
[03:35:23] hardware encoder and around
two milliseconds on the Intel
[03:35:27] decoder, right? So, like, the encoder
plus the decoder is already six
[03:35:31] milliseconds, right? So in order
to go down, we need either to
[03:35:34] have some other type of codecs, or
some better encoder that are faster.
[03:35:41] But four milliseconds
is, would be the grail.
[03:35:44] - That's pretty nuts. I love it, though. I
don't think anyone's ever achieved that,
[03:35:48] right? That's fast.
[03:35:49] - You can achieve that with custom hardware-
[03:35:53] ... with SDI, with professional hardware.
[03:35:56] But I want that to work
over the internet. I want
[03:35:59] that to work with any robots where
you're going to have a small Jetson
[03:36:03] Nano in it or a N150, right? I want
[03:36:07] that because there is going
to be millions of robots or-
[03:36:11] ... drones are just rolling robots or
flying robots or, or swimming robots,
[03:36:15] right? It's just you, a machine
that you control. And in order...
[03:36:20] Either you need to teleoperate them
[03:36:23] or when everything will be
fully autonomous, you need to
[03:36:26] teleobserve them, right? You
need to check what's happening.
[03:36:29] And in my view, in the future,
like, all those remote
[03:36:33] cars will be teleobserved by an AI
[03:36:37] model, which is just going to say, "Well,
everything is good." And when it's not good,
[03:36:41] say, "Hey, there is a problem," and then
you have an operator, right? And this is
[03:36:45] going to be about safety, right? When you have
your humanoid taking care of your grandma or my
[03:36:49] grandma,
[03:36:50] I want to be sure that everything goes
well, and I'm not in those type of horrible
[03:36:54] scenarios where the robot is
dangerous. Or when I'm driving, I,
[03:36:58] I want, like, the car to stop
when it should stop, and if
[03:37:02] needed, someone takes care of that,
right? And so there is so many ca-
[03:37:06] cases, scenarios about real time, and so
the goal of Kyber is to make real time
[03:37:12] control of machine. Distances appear.
[03:37:15] - It's incredible. And some of the same technology,
some of the same ideas that we're talking about
[03:37:19] is connected to what you're doing.
[03:37:22] - And for me, it's amazingly challenging,
right? Because I would say that on
[03:37:25] video I'm doing okay, but
networking I have so much
[03:37:29] more to learn, right? It's
um, about, like, congestion
[03:37:33] protocols, bitrate adaptation
in real time. But it's,
[03:37:37] it's quite funny. And so I
created this project and
[03:37:41] we have fundraised in the US, of
course. But it's open source, right?
[03:37:45] This is important, right? Like, we've not
said that, right? But everything on Kyber
[03:37:49] is open source.
[03:37:50] - So how do you make money?
[03:37:51] - It's a dual license, commercial and
AGPL, right? You remember what you said-
[03:37:55] ... about licenses. Basically, if you
[03:37:59] want to use Kyber in your product, you
must have your full product open source.
[03:38:04] If you want to use this amazing
technology but not open source,
[03:38:08] you pay the commercial license,
right? So the small people or the
[03:38:12] hobbyist and the very small guys
who want to do that, they can use
[03:38:16] the technology. They build something
that is open source and cool.
[03:38:18] - That's awesome.
[03:38:19] - And if you're a large company, you're
going to have the support, all the IP,
[03:38:23] the right modification,
and so on. So yeah,
[03:38:26] it's really cool and also I'm building
robots, and I love that, right?
[03:38:32] Like we have-- Like the rover
we have is 3D printed. We are
[03:38:36] finishing a demo where it's an actual
wing, right? Like a type of drone wings
[03:38:39] that is also fully 3D printed. We are
trying to do a sailboat that is 3D printed.
[03:38:47] And we'll work on some humanoids.
Of course, they are not going to
[03:38:51] be very good robots, right? It's
not our job, but we're here
[03:38:55] for everyone to make robots. Cool.
[03:38:57] - Ah, you're talking to the right guy. I
love robots. There's a bunch of them
[03:39:00] upstairs. And teleop is gonna
be really, really important,
[03:39:04] especially as the number of robots scales
across the world. So 100%. Let's talk
[03:39:08] about the future of multimedia.
FFmpeg, VLC, but some of the
[03:39:14] codecs, we didn't really
mention AV2. So can we just
[03:39:18] lay out what is AV2? What is the
hope for it? What is H.265, H.266?
[03:39:26] - So AV1 is this codec that is
done by the Alliance for Open
[03:39:29] Media, right? Where there
is Google, Netflix, Amazon,
[03:39:33] Apple VideoLAN, where we try to make a
[03:39:36] royalty-free very good codec,
right? And now it's being deployed.
[03:39:40] But actually, the codec was finished
in 2018, but a codec takes years to be
[03:39:48] used in wide scenarios, right? So,
[03:39:52] AV2 is the next generation of this
codec. It's 30% better, right? So
[03:39:57] if you keep the same quality, you get
30% bandwidth reduction compared to AV1.
[03:40:03] - What's the connection
with the dav1d and AV2?
[03:40:06] - We are going to do a dav1d 2,
right? That I call Devid because
[03:40:11] de is two in French. Um-
[03:40:13] - Ah, well done
[03:40:13] - ... And you have to know that dav1d is an
actual what we call recursive acronym,
[03:40:17] right? Because it means D, dav1d,
is an AV1 decoder, right? So
[03:40:23] - Oh, nice. Nice. I didn't even
think of that. And people should
[03:40:27] know that dav1d is spelled with a one.
[03:40:29] - Yes. It's... And so dav1d 2-
[03:40:32] - It's gonna be spelled with
a two. Please tell us
[03:40:33] - ... is going to be D-A-V-2-D. Sorry,
I don't know how you pronounce that.
[03:40:38] And again, we did a demo at the CES
of VLC running the first demo of AV2.
[03:40:44] - So can you clarify to me the specification
of AV2? And then the encoding and the
[03:40:51] decoding
[03:40:52] - Sure. So the specification is like the
[03:40:56] document which explains how the
codec is supposed to work, right?
[03:41:00] - And that's really AV2.
[03:41:02] - That is AV2, like H.264.
[03:41:04] Right? Then you have an encoder.
The current encoder is called AVM,
[03:41:09] and there will probably be other
encoders, probably one called
[03:41:12] SVT-AV2, and those are
the encoder. The same way
[03:41:16] x264 is an encoder to H.264, the same way
that x265 is an encoder for the H.265
[03:41:23] codec. And the decoders for
AV1 is dav1d. The decoder for
[03:41:31] AV2 is dav1d2. The decoder for H.264 is
[03:41:37] ffh264 inside FFmpeg. The decoder
for HEVC is ffhevc inside
[03:41:45] FFmpeg. And there is a
next generation codec
[03:41:50] from the MPEG world after H.264, H.265.
There is one that is called H.266,
[03:41:56] also known as VVC.
[03:41:59] - So HEVC is H.265. VVC is H.266. Why is
H.266 super sexy- ... and so much better?
[03:42:10] - So the question often we have
is why are there two names?
[03:42:13] Because most of the time it is a
conjunct work from the ISO world
[03:42:19] and the ITU, which is the
International Telecommunication Union.
[03:42:24] - These are these two regulatory bodies.
[03:42:26] - No, one is a private entity
and one is the United Nations.
[03:42:28] - Which one is the private?
[03:42:29] - ISO is private.
[03:42:31] - In theory, H.264 is MPEG-4 Part 10,
H.264/AVC. And this is the full name.
[03:42:44] - So it's the concatenation of
the ISO name and the ITU name-
[03:42:48] ... even though they work together. This
is, this is politics, historical, you know-
[03:42:53] - And for HEVC, it's MPEG-H, H.265, HEVC.
[03:42:59] And there is H.266,
which is also named VVC.
[03:43:02] - Is there a high-level thing to
say about the improvement of-
[03:43:05] - 30% each generation is a best summary.
[03:43:09] - This is true both for the AV- ...
codecs and the- ... H.264, 5, 6.
[03:43:15] - So the professionals who are listening to us are
going to kill us because they say, "No, it's
[03:43:19] 35%, 25%-
[03:43:20] - "No, it's 50, 60"
[03:43:21] - ... it's 50," blah, blah, blah. But
globally, you need to know that HEVC is
[03:43:24] 30% better than H.264. H.266 is 30%
[03:43:28] better than H.265 because there are
so many cases and so many scenarios.
[03:43:32] For example, there are cases, especially
for screen recording, where the gains are
[03:43:39] humongous because you arrive, you have
the right tool that is done for that.
[03:43:43] And so for a specific video, a new
generation is going to give you
[03:43:47] 70% gain or 80% gain.
[03:43:50] Right? But there used to be a
ton more codecs, but now the two
[03:43:53] main codecs for transmission are the H.264,
H.265, H.266, and the other is AV1, AV2.
[03:44:00] - And I guess the major difference
would be the cost of encoding.
[03:44:04] - Yes, and the royalty of the patents.
[03:44:08] And this is the reasons why you
see the AV version of codecs, is
[03:44:11] because they try to be as royalty-free,
[03:44:15] which means no cost for the
patents as much as possible.
[03:44:19] Because what you need to know, and
we've not talked about that so far, is
[03:44:23] that multimedia is what we
call a patent minefield.
[03:44:27] There is two places where you
have the most patents. It's
[03:44:30] everything related to 3G,
4G, 5G, RF, and multimedia.
[03:44:36] Um, because it's very mathematical, and
you can get great gains and so on. So
[03:44:42] Google and Meta and Netflix
wanted something where it was
[03:44:45] royalty-free. There are people who said that
they have patents outside, but they are
[03:44:49] fringe patents, right? So it's
mostly true that it's patent-free.
[03:44:53] - Oh, you should extend. Patent
checking was done as part of the
[03:44:57] standardization process in AV1, AV2,
whereas patents are not even discussed
[03:45:04] in the MPEG world. Patents
are off-topic completely.
[03:45:08] - Can you educate me at the patents side?
[03:45:10] - So usually, so MPEG does a
format, right? And then there is,
[03:45:14] Everyone comes around and say, "Well, I
have all those patents for the format,"
[03:45:18] and they do usually a
union called what's called
[03:45:22] MPEG LA, MPEG Licensing
Association. And you
[03:45:26] put all your patents in, and
then you ask everyone who's
[03:45:30] using this format to pay for it.
[03:45:31] - Wait, can you elaborate? What does it mean to have
a patent of a codec? Why is there many patents?
[03:45:36] - Uh, imagine I'm doing
something where I'm going to
[03:45:40] instead of doing blocks which are square,
I'm going to do rectangles, right?
[03:45:44] - Oh, so every idea- ...
somebody patents it. Oh, man.
[03:45:52] Oh, man. People and their...
How many lawyers are-
[03:45:56] - I mean, it pays for a lot
of lawyers, right? Like-
[03:45:58] - The biggest issue is not the following, right?
Because at time of H.264, the patents were,
[03:46:02] let's call it, like, sane. But
there was so much money in that-
[03:46:09] ... that for HEVC, a lot-
[03:46:12] there were a ton of things that were pushed
inside the specification, which are not
[03:46:15] useful in 99.9% of the time, but so
[03:46:19] just one could add a patent
on it. And so it became
[03:46:23] that for HEVC licensing, there was MPEG LA
[03:46:27] plus another patent pool
called HEVC Advance. Plus-
[03:46:31] - That one
[03:46:31] - ... um, I think Nokia was
outside of the patent pool.
[03:46:34] - Yeah, a few of them are outside,
and some other one that's-
[03:46:36] - And so it was impossible to license,
right? And I think that several months
[03:46:40] ago, HP decided that they were
going to remove support from
[03:46:44] HEVC in their Windows laptops because the
cost was increasing of those patents.
[03:46:51] And it arrived- ... where a point where--
And there was uncapped patent. And so for
[03:46:56] YouTube or Netflix, we could
talk about hundreds of
[03:47:00] millions of dollars of
licensing for patents per
[03:47:04] year. And they said, "You
know what? At hundred million
[03:47:08] per year, you know, I could create my own codec,"
and this is what they did. And so that's why we
[03:47:12] have the Open Media alliance,
Alliance for Open Media, where we
[03:47:16] are part of, that is, that created AV1 and
creates AV2. We create also audio codecs.
[03:47:23] But yes. So the main difference
would be that, and because you need
[03:47:26] to work around the patents or go do
some things that are not patented,
[03:47:32] a lot of things are different, right?
The basic things that were done in
[03:47:36] MPEG-2 thirty years ago are,
of course, out of patents. But
[03:47:40] so for example, there is things
like a golden frame, a S
[03:47:43] frame or, or different type of-
[03:47:46] - These are all patented ideas.
[03:47:48] - Yeah, no, it's I can't believe it's not
butter. I can't believe it's not a B frame.
[03:47:52] It's, I mean, it's kind of what
it is. In some ways, it's like a-
[03:47:55] - Oh, so it's a different
variant of a B frame.
[03:47:57] - Yeah, that's to try and
sidestep. Things like that.
[03:48:00] - And so you need to have double
creativity, right? Creativity in terms of
[03:48:04] being more efficient, but creativity
of being sure that you don't
[03:48:08] infringe existing patents.
And so, for example, VVC
[03:48:12] is, has all the patents of HEVC
plus new ones, right? It's
[03:48:16] why AV2 tries to be as
royalty-free as possible.
[03:48:20] - To what degree does FFmpeg and VLC have
to think about this kind of stuff?
[03:48:24] - We don't, and one of the reasons
why VLC was in France is
[03:48:28] that France rejects software
patents. So most of those patents
[03:48:33] are illegal in France because
I once made the calculus that
[03:48:40] if I had to pay all the licensing
fee for VLC, I needed to pay more
[03:48:44] than two hundred euros per user,
right? It's the same in dollars.
[03:48:48] But most of those patents
are invalid in Europe
[03:48:52] because those are called, it's
basically mathematical patents or idea
[03:48:56] patents, and they are not valid in Europe.
[03:49:00] - Uh, let me just at a high level,
just out of curiosity. So the
[03:49:03] meme online and the interwebs
on X and Twitter and so
[03:49:07] on, and my own, I have friends in Europe,
[03:49:13] this, the sense is that Europe is
not friendly to entrepreneurship.
[03:49:17] They over-regulate, there's
too much bureaucracy, and so
[03:49:20] on. Is there anything positive to say?
Is there hope for entrepreneurship-
[03:49:26] - Yes
[03:49:26] - ... in the future of Europe? Is
Europe over from a tech perspective?
[03:49:32] - Just look at the two of us, right? It's
notable that there's two people from
[03:49:36] the European continent on this podcast
talking about video. It's fair to
[03:49:40] say the community is weighted heavily.
[03:49:42] - What you probably don't
see yet is that there is a
[03:49:46] new generation of
entrepreneurs in Europe and
[03:49:50] mostly in France. UK has done
it since a long time because,
[03:49:54] well, it's more, it's
more Anglo-Saxon type of
[03:49:58] business, look at business. But
especially like what happened in
[03:50:02] in France, and of course, sometimes a bit
overdone with everything called French tech,
[03:50:06] but today, most of the people who
come on the market want to create
[03:50:10] startups. Fifteen years ago,
it wasn't the case. Everyone
[03:50:14] wanted to work on big companies
because when you failed in
[03:50:18] in France, for example, twenty
years ago, fifteen years ago,
[03:50:22] and you destroy your company, which
is normal for startup, right? You,
[03:50:26] you were not allowed to create a new company,
right? There was a lot of stigma. The
[03:50:29] stigma is gone.
[03:50:32] ... there is so many things happening
on AI in France and so on, right?
[03:50:35] So there is sure, over-regulations. I,
[03:50:40] I know that, right? I'm an entrepreneur.
But it has some good things also.
[03:50:45] - I mean, is there some paralyzing
aspects? You know, if I look at
[03:50:49] the case of somebody I've
become close with, Pavel Durov,
[03:50:54] you know, he was blamed directly by the
French government for the kind of things
[03:51:02] his, quote, "platform" was hosting.
[03:51:05] I could see the same kind of stuff
basically, just as an example,
[03:51:09] VLC being blamed for the kind of
videos that people are watching.
[03:51:13] - But they tried, right? Like
we had, we had issues. Like-
[03:51:19] - I mean, is that, that's the pressure that people
worry about because if you have to think about
[03:51:23] that kind of stuff when you're
kind of just obsessed about-
[03:51:25] - No, you don't think about it- ... and
that's, that's okay, right? Like-
[03:51:29] - But what if they come in? When,
what if they show up and-
[03:51:31] - There is no office. VideoLAN
doesn't have an office.
[03:51:33] - I mean, this is what happened with Pavel.
They arrested him, right? So arrested him for
[03:51:37] particular videos or, or a particular
content that's being shared on the platform.
[03:51:42] - Sure. I don't have any platform.
Everything is on the client side.
[03:51:45] - Yeah, but they're, they
can still arrest you.
[03:51:47] - On what ground? I'm not sharing anything.
I'm not-- The content doesn't go through
[03:51:51] my stuff.
[03:51:52] - For sure, but it's still lawyer
fees. That's the problem.
[03:51:55] - Yes, that's correct.
[03:51:55] - It's paperwork. So like, actually, if
you had infinite trillions of dollars,
[03:52:02] You would win easily because you're on
the right side. But the thing is, there
[03:52:08] is a degree to which they suffocate you
with paperwork. That's the downside
[03:52:12] of bureaucracy, through
paperwork, through process.
[03:52:15] You know, it's the Kafkaesque thing.
[03:52:17] - You have to realize that one of
the good things, for example in
[03:52:21] in France or most of Europe, is that the--
[03:52:27] Answering to a court order does not
make you bankrupt, right? It's not like
[03:52:31] in the US, where it can actually
bankrupt you, right? There is-- The
[03:52:35] way the law system works is that, like
[03:52:39] I receive lawyers' letters every week,
right? And I can tell you that the cost
[03:52:46] of lawyer fees for VideoLAN is less than
ten thousand dollars per year, right?
[03:52:52] Right? So that's not really scary.
[03:52:53] - I mean, similar with Pavel. The
intelligence agencies tried to like
[03:52:57] say, "Can you put a backdoor in VLC?"
[03:52:59] - Yes. Two of them.
[03:53:01] - What, what do you say?
[03:53:02] - No. Well, I was a lot less polite.
[03:53:05] - I see you... Yeah, yeah. You're
basically saying, "Hell no."
[03:53:09] - Like, if we had to compromise our software,
we would shut it down. This is clear.
[03:53:13] - And what's the definition of
co- compromise? Like allowing a
[03:53:17] government to do a backdoor-
[03:53:19] - There is no code that gets into
VLC that we don't control,
[03:53:23] and the way we compile VLC, you
would call me completely paranoid.
[03:53:28] Like, we compile on
boxes that are offline,
[03:53:32] where we start by compiling
the compiler. We do everything
[03:53:36] offline on places that have
never been connected to the
[03:53:39] internet. We-- The way we
do signing, there is double
[03:53:43] signature. And especially
because, for example, we've
[03:53:47] seen, and we believe it's a
governmental agency that is
[03:53:51] not from the Western world
who tried to push a fake
[03:53:54] binary into our own servers
and that scared us a
[03:53:58] lot. And VideoLAN is open
source. How can you kill it?
[03:54:03] Like, I move to where, right? I move
to Malta. I move to I don't know,
[03:54:07] Cayman Islands, and I change
the domain name, and I
[03:54:11] start again, right? Like, VLC is a
tool. It's a tool that is going to help
[03:54:18] people doing things.
We are not a platform.
[03:54:22] And for patents, well, I'm
sorry, but most of the
[03:54:26] patents... Like, you shouldn't
be able to patent math and
[03:54:29] matrices. Like, this is wrong.
[03:54:32] - So does VLC ever, like,
censor the kind of videos it
[03:54:35] can play and not based on
the content of the video?
[03:54:39] - No, never. We never do that.
[03:54:42] Because, like, VLC is completely
offline. It doesn't talk to
[03:54:46] any server, so we don't know anything
that you're using the software for.
[03:54:49] - So again, there's no government
that can say, you know,
[03:54:54] like the French government come
in and say, "We don't want,
[03:54:57] uh... I think anime is destructive
to society. We don't want any
[03:55:01] anime not allowed to be..."
[03:55:02] - No, they cannot, they cannot do that. And
also what they tried is to say, "Hey,
[03:55:06] I want to know if that person watched that
type of video." And the answer is like,
[03:55:10] "No idea."
[03:55:11] - So no on that too. So
for surveillance, no.
[03:55:14] - No, no, because the only infrastructure
we have is a downloading infrastructure.
[03:55:18] There is no telemetry in VLC, right?
[03:55:20] - It, it would be difficult 'cause
of the international nature.
[03:55:23] It would be difficult for you to incorporate that
code because there would be someone in the UK and
[03:55:27] someone in Germany and someone in
the US as part of VideoLAN who'd
[03:55:31] be able to see that. It would
be extremely difficult.
[03:55:33] - The only thing that we can do, which happened,
is like we had the issue-- We had the
[03:55:37] case with some police in the US who
said, "We have a murder case," right?
[03:55:41] "Uh, and the file is destructed or doesn't
play in that version of VLC. Could
[03:55:45] you help us?" Right? We never have access to
the video. It's like a normal support, right?
[03:55:50] - Oh, it's really about playing the file?
[03:55:51] - Yes. And, like, I remember in the
middle of the Afghan War, right? I
[03:55:55] received an email from
someone in the army, right? I
[03:55:59] don't remember the grades, right? It was just
like, "We have a big issue with the latest
[03:56:03] version of VLC because it doesn't play
[03:56:07] correctly the file on an RTSP
server that we have where there is
[03:56:11] all the movies." And he says
VLC is very important for the
[03:56:14] morale on the troop on the ground, right? Because
at night I think it might be boring, right?
[03:56:18] So they have a collection of videos to
watch or movies over there, right? So and,
[03:56:22] and of course I did an update,
and I broke some support of RTSP,
[03:56:26] right? So I gave them another version
just for them, right? Because it was
[03:56:30] important. And because VLC
is completely open source, I
[03:56:34] think it is allowed on the US
Army laptops, right? Because I
[03:56:38] guess someone in, in the, in
the US military actually looked
[03:56:42] at it and say, "Well, okay, this is okay,"
right? And the way we document how we
[03:56:46] process, that was okay, right?
So the only way we work with
[03:56:50] authorities is to help them doing support.
[03:56:53] - That's amazing. That's
an amazing story. Yeah.
[03:56:56] - We don't see anything happening on how
people use VLC, and this is strong.
[03:57:00] - Do you feel the stress of this? So
first of all, millions of people
[03:57:04] using it. Second of all,
the military using it.
[03:57:09] Maybe sometimes pressure from governments.
[03:57:11] - Yes.
[03:57:11] - Does that, does that... That's
a, that's a small team, right?
[03:57:16] - Yeah, but-
[03:57:16] - How big is VLC- like the
core contribu- how many?
[03:57:21] - Six, eight. But everything legally is only
me. Everything that is legal is only me.
[03:57:28] - You're not stressed about this?
[03:57:30] - I used to stress about that a lot.
[03:57:32] But the thing is, we're doing what we
can for everyone, for the greater good.
[03:57:38] We work that we make some
extremely complex technology
[03:57:41] easy for everyone. We're a tool, and every
[03:57:45] tool is going to be used for great things
and for bad things, right? You, you
[03:57:49] cannot blame a tool, I think. And this
[03:57:53] is, like, very important
for us. Um, I used to
[03:57:57] be a lot, in a lot of stress.
I'm not anymore, right?
[03:58:00] - What's the secret to your zen? I mean-
Over and over in the chats I've had
[03:58:05] with you in the conversation
today about every
[03:58:09] even tense topic, you're very
zen. What's the source of zen?
[03:58:14] - I have a way of thinking about what is
the worst case scenario, always, right?
[03:58:22] And the answer is, at the end, if I take
like a, like a chess player, right?
[03:58:27] In the end, am I dead? Yes or no? Right?
And, and I do that nonstop, right?
[03:58:33] And that's also how I do my,
my startups, right? Is that
[03:58:37] I'm here to get something right.
What is the worst case? It goes
[03:58:40] bankrupt. That's life. A company
lives, a company dies. That's
[03:58:44] okay, right? Like, and so my
moral way is always like,
[03:58:48] am I dying in the end? Am I
hurting someone? If the answer
[03:58:52] is no, then too bad, right? Like,
oh, some lawyers are going to be
[03:58:56] unhappy. What are they going to do?
Take all the money of VideoLAN?
[03:58:59] Wow. They're going to have 50 grand.
Amazing, right? What are they
[03:59:03] going to do with that? The source
code is out there. It's not
[03:59:07] stoppable. Also because what we do
is good and it's done for everyone.
[03:59:14] - That's beautiful. Uh, Kieran, you
said that there's an active archiving
[03:59:19] preservation community?
[03:59:20] I think that's super fascinating. You wrote
that they're stretched in budget, but they
[03:59:24] see the extreme importance
of FFmpeg as a Rosetta
[03:59:27] Stone so that multimedia
can be played a thousand
[03:59:31] years from now. I mean, that's
a beautiful way to see FFmpeg,
[03:59:35] VLC as a tool for preserving
visual knowledge.
[03:59:41] - Yes, that's right. One of the
coolest communities in open source
[03:59:45] multimedia, mainly led by someone called Dave
Rice, I'll give him a shout-out, I think
[03:59:49] from City University of New York, is
the archiving community. They've done
[03:59:53] so much stuff. They value the open
source, one, because yes, they lack
[03:59:57] budgets, but two, they see the fact that
archiving video is important for the world,
[04:00:04] and but being able to play that is
a big problem. Famously in the UK,
[04:00:08] there was something called the New
Domesday Book, and they archived
[04:00:12] lots of stuff on BBC microcomputers.
Within 10 to 15 years, no one
[04:00:16] had the right software to play that. I
think it was 20 years or something like
[04:00:20] that, and someone had to go and reverse
engineer this, and that was like 20 years.
[04:00:23] Imagine that in a thousand years.
[04:00:26] I think one of the great things about
FFmpeg is it's written in C. C is
[04:00:30] the closest to mathematics you're probably
gonna get. The closest to logic is-
[04:00:34] - Do you think in 1,000 years
we'd still have C compilers?
[04:00:37] - Yes. We have languages that exist that
haven't changed too much. We have
[04:00:40] mathematical notation that
exists. It will be like Latin. C
[04:00:44] will be like Latin. It will
be a thing that you learn
[04:00:47] from the past, but it will still
be usable in certain contexts.
[04:00:51] So the archiving community are really
great practically. They, again, limited
[04:00:55] funds. They funded the development
of the FFV1 codec, so that's a
[04:00:58] lossless codec. So the archiving
community is really scared about the
[04:01:03] act of compression losing things, and this
could-- They have a fair point in this, you
[04:01:06] know. If they compress too
hard, it could change the
[04:01:12] view of the material. There could be something
slightly different here and there, so they're really
[04:01:16] concerned about things need to be not
just compressed well, but lossless
[04:01:20] and be fast. And so they worked with
FFmpeg to develop a whole new codec
[04:01:24] designed for fast software-based encoding.
[04:01:27] They're really concerned about
resilience, so if they're storing on
[04:01:31] tapes or other hard disks,
I lose some bits, I need to
[04:01:35] recover quickly. I can't lose a
whole GOP because I've lost a bit-
[04:01:39] ... something like that.
[04:01:41] So they're a really great bunch of people.
They funded GPU encoding in FFmpeg
[04:01:45] to make FFV1 encode faster.
And it's really about
[04:01:48] preserving the world's
multimedia heritage in a way
[04:01:53] that's usable, and there's a lot of
great teams and a lot of archival
[04:01:57] groups across the world who've,
who've chosen FFmpeg and
[04:02:00] FFV1 as their archiving
solution. And they can
[04:02:04] really provide us also super
specialist advice. They can-
[04:02:08] ... explain, "Ah, in the 1950s,
colorimetry was done like this on this
[04:02:13] certain type of tape, and so there is
[04:02:17] this special case that you need to handle,
and you'll never get this anywhere else."
[04:02:20] - You see, they know things
on video that we don't.
[04:02:24] Like, every time I talk to, was it Dave-
[04:02:26] - Dave Rice
[04:02:27] - ... or the people from the British, uh-
[04:02:29] - British Film, uh
[04:02:30] - ... Film, it's just like every time I just learn
something new, and I've been doing video for 20
[04:02:34] years. They have, especially
on colorimetry and colors.
[04:02:39] - Storage, these other things.
[04:02:40] - I mean, they have a deep, deep
appreciation of the content itself, of the
[04:02:44] video itself. And like, especially
when you're thinking of lossless,
[04:02:49] they're terrified of losing
something essential-
[04:02:52] ... about the thing, and in so doing,
they're deeply understanding the
[04:02:56] thing that is to be preserved, which you
sometimes might not be thinking about when
[04:03:00] you're- ... obsessing about the actual
technology of the encoding and so on.
[04:03:03] - And when you enter the rabbit hole of
film scanners, right? So you take those-
[04:03:10] ... those things to make to
digital, like, it's like-
[04:03:13] ... a huge topic that, like, would
take another five hours of podcast-
[04:03:18] ... just on that topic.
[04:03:18] - On film, and there's a lot of film that needs to be
archived. Film is degrading. It's maybe not stored
[04:03:22] in the right environment. The other thing is they
can... What they also do is, because it's open
[04:03:26] source, they give this away, their
workflows, to countries who can't afford
[04:03:30] to have archiving institutions, where
archiving is done by volunteers, it's done
[04:03:34] by other things. They go and teach, you know,
in India, they teach children to do, to
[04:03:38] do FFmpeg commands. They're
really great. They're really,
[04:03:43] They're really the model community, the
model ethos of what we're trying to achieve.
[04:03:46] They are
[04:03:48] such a great bunch of people, so interested
in participating and being part of
[04:03:52] something much bigger because they realize
the work they're doing in a thousand
[04:03:56] years is gonna tell a lot.
[04:03:59] You know, in a thousand years we
may be drowning in AI slop. This
[04:04:03] stuff needs to be important and, you
know, archived well. What was life like?
[04:04:07] - Yeah, it feels like capturing the
20th century and the 21st century is
[04:04:10] essential because it feels like a transition
point, where we went from scarcity
[04:04:17] of data to slop- ... oceans of slop, and
that transition point is good to archive.
[04:04:24] - It's important, yeah.
[04:04:25] - But people don't realize we are
losing today a ton of films.
[04:04:29] There is a ton of things from the '30s,
from the '40s, and the '50s that where
[04:04:36] there is no value-
[04:04:37] - And tape. '70s and '80s, there's tape,
and there's not enough tape heads in the
[04:04:41] world-
[04:04:41] - To read all the tapes
[04:04:42] - ... left to redo, so they have to decide what they
want to archive and throw away the rest of the
[04:04:45] tapes. There's huge moral hazard, I guess
for want of a better phrase, around this
[04:04:50] topic because
[04:04:52] this is a digital record of human
history and they have to make decisions
[04:04:57] that... And there's digital stewardship, I suppose, for
want of... I made that phrase up. That's not a real phrase.
[04:05:01] Um, to make sure the world can have this
information in something that's playable
[04:05:06] by everybody, not-
[04:05:08] ... playable on some device that,
well, it doesn't exist anymore.
[04:05:13] - And then there's like, realistically
speaking, there's a needle in a haystack
[04:05:16] where there's a lot of
value in archiving all that
[04:05:20] footage, and then over time finding the
gems- ... that we don't know are there.
[04:05:25] - Hey, there was something in that
corner that we just didn't-
[04:05:28] - Yeah. Uh-huh.
[04:05:28] - And that, that would've been compressed away
because it was some little thing. Oh, wow, there's
[04:05:32] something there.
[04:05:33] - That's it.
[04:05:33] - And, and that's... They've made sure
that it's lossless. They can prove
[04:05:36] mathematically that it's
lossless. They can run different
[04:05:40] trade-offs for if there's bit fro- if
they lose a bit, a single bit flips, I
[04:05:44] can make sure that I only lose a portion
of a given frame. We can do error
[04:05:48] they can do error recovery on previous frames.
They can do all sorts of different things.
[04:05:52] - Do you think VLC and FFmpeg will
be here 100 years from now?
[04:05:57] - FFmpeg, yes.
[04:05:58] - Yep, FFmpeg, yes.
[04:05:59] - VLC, maybe.
[04:06:01] - What's the future of...
Where is FFmpeg going?
[04:06:05] Where is VLC going? Like in the
next... If you think about, like, five
[04:06:08] years, 10 years, 20 years.
[04:06:10] - Five years, 10 years is easy. The question
is after that, right? The question is-
[04:06:16] ... do we arrive at something
called holograms, right?
[04:06:19] - Yeah, so will VLC and FFmpeg
expand- ... to whatever-
[04:06:26] - Multimedia
[04:06:27] - ... multimedia-
[04:06:27] ... so multimedia might become, I'm
sorry for the pothead expansion of
[04:06:31] topic, but, you know if
you look at something
[04:06:35] like Neuralink with brain computer
interfaces, it's very possible that
[04:06:39] we start to consume what
multimedia means is whatever
[04:06:45] codec, whatever data that our
brain wants to consume through the
[04:06:48] brain computer interfaces. That's
one. Then virtual reality, of course.
[04:06:52] - You will have VLC for Neuralink.
[04:06:55] - Yep, and you'll have FFmpeg
-i input format human brain.
[04:06:58] - Yeah. There's gonna be
codecs for the brain.
[04:07:01] - Sure, 100%.
[04:07:03] - Of course.
[04:07:03] - Yeah, to compress neural
information, yeah.
[04:07:05] - I mean, today there is like,
there are new codecs for-
[04:07:07] - Whoa
[04:07:07] - ... for example, what we call point cloud,
right? Or volumetric videos, right?
[04:07:11] There is a ton of research on what
we call RGBD, right? So codecs for
[04:07:15] depths that is useful for
robotics and for 3D things.
[04:07:19] - Nice.
[04:07:19] - There is a ton of codecs for
compression of 3D elements.
[04:07:22] - Compression for astronomy.
[04:07:23] - Uh, for example, on VLC, we also
have already a VR and XR version of
[04:07:27] VLC. And also on Kyber, right? We
talk about Kyber. On Kyber, we also
[04:07:31] like do streaming of XR content
on for the glasses who cannot
[04:07:35] have enough power or inside
the Apple Vision or the Quest.
[04:07:39] So we already work on streaming 3D,
XR, interactive, low latency. There is
[04:07:47] something called volumetric video,
point cloud videos, so it's
[04:07:51] not stopping. And yes, at some
point it will manage 3D data
[04:07:54] inside VLC and FFmpeg,
right? It's obvious.
[04:07:58] - So that's where it is moving,
like the community is open.
[04:08:01] - Not everyone in the community
sees that, but like, as Kieran
[04:08:05] and I, we are entrepreneurs, we know
where it's going. We see that, right?
[04:08:10] - So I suppose that there is a tension
probably inside FFmpeg. It's like,
[04:08:14] "Hey, listen, folks, we're really
good at doing video and audio,
[04:08:20] so like why expand? Like let's do the
thing we're really good at doing."
[04:08:25] - In order to answer that
question, we need to answer the
[04:08:28] definition of what is multimedia.
[04:08:31] And multimedia is a digital
representation of several
[04:08:38] streams for the human senses. And we will
do that, right? So imagine there is now a
[04:08:46] way to not have a mic, but have an odor
sensor- ... and a diffuser of odors.
[04:08:52] It will get into FFmpeg.
[04:08:54] - So your demuxer is coming up.
[04:08:56] - Yes. Yes.
[04:08:57] Of course, your demuxer has a new track
type that is basically odors, right?
[04:09:01] And you already have-
[04:09:02] - Smell, touch.
[04:09:03] - It's like audio. You'll have a left and right nose
track. You have a left and right audio pair. It's easy.
[04:09:07] - Yes, of course.
[04:09:09] - Stereo smell.
[04:09:09] - Stereo smell, yeah.
[04:09:10] - So in VLC, for example, we already
have a plugin for haptic. It's mostly
[04:09:14] for what we call 4D cinemas, right?
You know, those ones on hydraulic,
[04:09:18] I don't know how you say
that. All the hydraulic-
[04:09:21] - Hydraulic arms. Hydraulic, um-
[04:09:22] - Arms. And where everything is moving,
like you have in theme parks, right?
[04:09:25] And there is a data feed
synchronized where,
[04:09:29] which is basically
transporting this information.
[04:09:32] - Is there yet a standard for that?
[04:09:33] - There are many standards, right? Um-
[04:09:35] - This is... You make me so happy.
[04:09:38] - And so of course, like we have a plugin
which is not in the normal version of VLC-
[04:09:43] - That's good.
[04:09:43] - ... that is basically transporting those type
of movements, which is physical movements,
[04:09:47] which is haptic movements, right? It
is a human sense, so it will get in.
[04:09:54] - That's such an exciting future.
Was it... I mean, it's a small
[04:09:57] community of developers.
How do you pull that off?
[04:10:01] Like if you're a contributor
to FFmpeg or VLC, it feels
[04:10:05] stressful. Like it, just
looking on Twitter,
[04:10:09] it's like it's a huge
amount of work to make
[04:10:13] it work on all these different operating
systems, an incredible effort.
[04:10:17] - No, see it in the other
direction. We are not
[04:10:21] the contributors. We are the maintainers,
[04:10:24] right? So we maintain for everyone. Meaning
that, for example, every year there is
[04:10:31] around 150 people who
contribute to VLC and maybe
[04:10:34] 300 on FFmpeg, right? Our
goal as a small team is
[04:10:38] to get all the contribution
in. So if there is more
[04:10:42] usage, there will be more
contributions, and those people will
[04:10:46] do the right module, the new
format, and so on. We care
[04:10:50] about the architecture of VLC, the
architecture of FFmpeg, right?
[04:10:54] Now we're doing things in VLC, which
is spatial audio, right? We did the
[04:10:58] demo not long ago. There was
[04:11:02] changes needed on the architecture,
and we did the first spatial audio
[04:11:06] module. When it's going to add the second one, it's
going to be easy, or the third one is going to be easy,
[04:11:10] right? Our goal, and it's going
to be the same for others or
[04:11:14] haptic, right? We need to work the
architecture so that modules can
[04:11:18] be added to add future capabilities.
[04:11:21] So yes, we are going... We are
multimedia framework, so that's not
[04:11:25] just audio and video. It's everything
that is timed and-Represent
[04:11:32] something that you can sense. And if it's
brainwaves, it's going to be brainwaves.
[04:11:36] - I think that's inevitable. Sorry.
[04:11:38] - I love this on so many fronts
because, so FFmpeg and VLC are
[04:11:43] pushing companies and pushing the world to
[04:11:47] standardize. So for
example, to standardize-
[04:11:49] ... brainwaves, right? So
standardize... It would push,
[04:11:53] like I hope Neuralink comes up with
a standard for, for multimedia
[04:12:00] via brain computer interfaces
or for robots with haptic.
[04:12:05] - By experience, what happens
is always the same, right?
[04:12:08] You start, it's a new topic. There
is like five different standards
[04:12:12] because everyone starts to do this. The
hype goes down because every time the hype
[04:12:16] goes down, then people start to say,
"Well, you know what? You, we need to do a
[04:12:20] standard." People, because two or three
companies, usually not the leader, but
[04:12:24] the two or three followers do a standard,
[04:12:27] and then we implement the standard and,
and then it's the end of the curve.
[04:12:31] It starts to be more paper.
[04:12:32] - And then the leader's kind of pressured
into it because it is better to do a
[04:12:36] standard. Yeah.
[04:12:36] - Example, 3D audio, right?
[04:12:39] Six or seven years ago, it was everything
about 3D. You go, you had the Cardboard on
[04:12:43] Android. You had two audio
formats. They're all dead, right?
[04:12:47] And now it's coming back with
actual use cases, and we learn
[04:12:51] from the mistakes of the past standard.
So it will be the same everywhere.
[04:12:56] - And not try to avoid closed.
I saw somewhere you,
[04:13:00] you didn't have too many nice
things to say about Dolby.
[04:13:03] - No, I don't. Um-
[04:13:04] - What is can you educate me on why,
[04:13:09] where they went, what, what did
they do bad that made you mad?
[04:13:13] - It used to be an amazing
company doing tons
[04:13:17] of great things with amazing engineers.
They defined what sound was.
[04:13:22] And now it's mostly-
[04:13:25] - Lawyers
[04:13:25] - ... lawyers and licensing things.
[04:13:27] - Oh, so they're, yeah, it's, they're closing stuff
off. They're trying to make money on licensing.
[04:13:30] - No, it's just like they don't
innovate as much as they did-
[04:13:33] - I see
[04:13:33] - ... and so on. It's a bit like I'm
sorry to say, right, like HP, right?
[04:13:38] - Very true.
[04:13:40] - Oh, since we talked about Twitter a bunch
in different contexts, do you have a,
[04:13:44] do you have a favorite, do you have a, and
least favorite, most embarrassing tweet
[04:13:50] on either VideoLAN or FFmpeg Twitters?
[04:13:53] - The two, my two favorites are, "Talk is
cheap, send patches." I think that, that-
[04:13:57] ... embodies a lot of the stuff doesn't
get, as we've talked about, stuff
[04:14:01] doesn't get built unless someone does it.
It doesn't just appear from the ether.
[04:14:05] The other one that I like is "FFmpeg,
nothing is beyond our reach."
[04:14:10] I think that comes from a US military satellite
patch where I think they, they invented some
[04:14:14] kind of monitoring system that could see
the whole world, and this was released.
[04:14:19] - Wasn't there something where FFmpeg
was running on a rover on Mars also?
[04:14:22] - Yeah, so FFmpeg is used by
the Mars rover the Mars 2020
[04:14:26] rover to compress pictures.
They really wanted—they
[04:14:30] wrote a paper about it, and they really wanted to
use as much commercial off-the-shelf technology as
[04:14:34] possible.
[04:14:34] - Oh, that's cool.
[04:14:35] - FFmpeg runs on Mars, so we are a
multi-planetary open source library.
[04:14:39] - Nice.
[04:14:41] - Very often we've seen—
[04:14:43] - Nice
[04:14:44] - ... Tweets for people using VLC in weird
[04:14:48] places. A lot of the
people doing Formula 1
[04:14:52] are in all the paddocks, they use
VLC to play the live feed. We've
[04:14:55] seen the European Space Agency.
We've seen SpaceX, like,
[04:14:59] monitoring the launches with
VLC, and, like, it, like,
[04:15:03] fills you with joy, right? So-
[04:15:05] - I've seen a particle accelerator.
[04:15:07] - Oh, yeah, yeah. We had one of
the most amazing things that I
[04:15:12] went for was to go to the CERN at the LHC
because they were using VLC to monitor all
[04:15:19] the sensors on the ring because
the ring is 27 kilometers.
[04:15:23] And so they had some analog cameras-
[04:15:27] ... and they were using some of the
capture cards to go to analog to
[04:15:30] VLC, so VLC could stream on their
multicast network for the whole CERN
[04:15:34] to access that. And, like, I visited
that in 2010 with Laurent and—
[04:15:43] like, we fixed their issue in an hour or
something like that, right? Because it was
[04:15:47] some parameters maybe not
well documented at that time.
[04:15:51] And he said, "Okay, for the whole day, what do you
want to do?" And we visited everything. Like- ...
[04:15:55] things with antimatter
and—and colliders and so on.
[04:16:00] And that was, like, one of the most
amazing days of my physics background.
[04:16:06] - Yeah, it's used, like, everywhere.
Any tweets, uh, Kieran, you regret?
[04:16:12] - Tweets I regret?
[04:16:14] - Or is it like that, how does the
French song go? Regret nothing.
[04:16:17] - "Je ne regrette rien." Yeah.
[04:16:19] - Yes. Uh, that's very
important for me, right?
[04:16:21] Don't regret anything.
No, it's because regrets
[04:16:26] are a tax on your mind, right? So learn
from your mistakes, but don't regret.
[04:16:31] Because you've done it, so unless you
have a time machine to go back in time,
[04:16:37] don't regret, right? It's going to just
tax your brain. Learn from your mistake,
[04:16:41] sure. Don't regret.
[04:16:43] - It's like it reminds me, it's beautiful. It's a tax
on your brain. It reminds me of the Johnny Depp
[04:16:47] quote I saw where he was
saying, "Hate, you know, I
[04:16:51] don't hate. That's, hate is
a very expensive emotion."
[04:16:56] - Are you comparing me to Johnny Depp?
Because that would be your first one.
[04:17:00] - Well, gentlemen like I said, I'm eternally
[04:17:03] grateful for the software that,
you know, the two of you and
[04:17:07] the bigger community have been part of
building with FFmpeg and VLC and everything
[04:17:11] else. I'm eternally grateful for
the spicy tweets. Never stop.
[04:17:17] And I'm grateful that you would
talk with me today and give me this
[04:17:23] sexy hat. I feel like a wizard.
I feel special. And I feel
[04:17:28] special to get a chance to talk and celebrate the
piece of software that brought me so much joy over
[04:17:33] the years. So thank you for everything,
and thank you for talking today.
[04:17:36] - Thank you for having us.
[04:17:37] - Thank you so much.
[04:17:38] - Thanks for listening to this conversation
with Jean-Baptiste Kempf and Kieran Kunhya.
[04:17:43] To support this podcast, please check out our
sponsors in the description where you can
[04:17:47] also find links to contact me, ask
questions, give feedback, and so on.
[04:17:51] And now let me leave you with some words
from the legendary Linus Torvalds.
[04:17:57] "Most good programmers do programming
not because they expect to get
[04:18:01] paid or get adulation by the public,
but because it is fun to program."
[04:18:08] Thank you for listening, and
I hope to see you next time.