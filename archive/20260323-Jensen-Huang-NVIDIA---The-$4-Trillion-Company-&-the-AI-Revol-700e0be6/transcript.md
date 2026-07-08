---
source_url: "https://www.youtube.com/watch?v=vif8NQcjVf0"
platform: youtube
uploader: "Lex Fridman"
title: "Jensen Huang: NVIDIA - The $4 Trillion Company & the AI Revolution | Lex Fridman Podcast #494"
upload_date: "20260323"
duration: 8758
fetched_at: "2026-06-18T08:05:04.096535Z"
transcript_source: youtube-transcript-api
---

[00:00:00] - The following is a conversation
with Jensen Huang,
[00:00:03] CEO of NVIDIA, one of the most
important and influential
[00:00:07] companies in the history
of human civilization.
[00:00:11] NVIDIA is the engine powering
the AI revolution, and a lot
[00:00:15] of its success can be directly
attributed to Jensen's sheer force of
[00:00:19] will and his many brilliant bets and decisions
as a leader, engineer, and innovator.
[00:00:26] This is Lex Fridman Podcast. And now
dear friends, here's Jensen Huang.
[00:00:33] You've propelled NVIDIA into a new era in
[00:00:37] AI, moving beyond its focus on chip
scale design to now rack scale
[00:00:41] design. And I think it's fair to
say that winning for NVIDIA for a
[00:00:45] long time used to be about building
the best GPU possible, and you still
[00:00:49] do, but now you've expanded
that to extreme co-design of
[00:00:53] GPU, CPU memory, networking,
storage, power cooling,
[00:00:57] software, the rack itself, the pod
that you've announced, and even the
[00:01:01] data center. So let's talk about
extreme co-design. What is the
[00:01:05] hardest part of co-designing
system with that many complex
[00:01:08] components and design variables?
[00:01:11] - Yeah, thanks for that question.
[00:01:12] So first of all, the reason why extreme
co-design is necessary is because the
[00:01:16] problem no longer fits inside one
computer to be accelerated by one GPU.
[00:01:24] The problem that you're trying to
solve is you would like to go faster
[00:01:28] than the number of computers
that you add. So you added
[00:01:32] you know, 10,000 computers, but you
would like it to go a million times
[00:01:36] faster. Then all of a sudden
you have to take the algorithm,
[00:01:43] you have to break up the algorithm,
you have to refactor it,
[00:01:46] you have to shard the pipeline, you have
to shard the data, you have to shard the
[00:01:50] model. Now all of a sudden when you
distribute the problem this way,
[00:01:56] not just scaling up the problem, but
you're distributing the problem,
[00:02:00] then everything gets in the
way. This is the Amdahl's Law
[00:02:04] problem where the amount of
speed up you have for something
[00:02:09] depends on how much of the
total workload it is. And so
[00:02:13] if computation represents 50% of the problem,
and I sped up computation infinitely
[00:02:21] like a million times,
[00:02:23] you know, I only sped up the total
workload by a factor of two.
[00:02:27] Now all of a sudden, not only
do you have to distribute a
[00:02:30] computation, you have to, you
know, shard the pipeline somehow.
[00:02:34] You also have to solve
the networking problem
[00:02:38] because you've got all of these
computers are all connected together.
[00:02:42] And so distributed computing
at the scale that we do,
[00:02:47] the CPU is a problem, the GPU is a
problem, the networking is a problem, the
[00:02:51] switching is a problem. And
distributing the workload across all
[00:02:55] these computers is a problem.
[00:02:57] It's just a massively complex computer
science problem. And so we just
[00:03:00] gotta bring every technology to bear.
Otherwise, we scale up linearly or we
[00:03:09] scale up based on the capabilities
of Moore's Law, which has
[00:03:13] largely slowed because
Dennard scaling has slowed.
[00:03:16] - I'm sure there's trade-offs there.
Plus you have a complete disparate
[00:03:20] disciplines here. I'm sure you have specialists
in each one of these high bandwidth
[00:03:24] memory, the network and the NVLink,
the NICs, the optics and the
[00:03:28] copper that you're doing, the power delivery, the
cooling, all of that. I mean, there's like world
[00:03:31] experts in each of those. How do you get
'em in a room together to figure out-
[00:03:34] - That's why my staff is so large.
[00:03:37] - What's the process—can you take me through
the process of the specialists and the
[00:03:41] generalists? Like how do you put
together the rack when you know the
[00:03:45] s- the set of things you have
to shove into a rack together?
[00:03:48] Like what does that process look
like of designing it all together?
[00:03:51] - Yeah. There's the first question,
which is: what is extreme co-design?
[00:03:55] You're, you, we're optimizing
across the entire stack of software
[00:03:59] from architectures to chips, to
systems, to system software, to the
[00:04:02] algorithms, to the applications. That's
one layer. The second thing that you and
[00:04:06] I just talked about is goes
beyond CPUs and GPUs and
[00:04:10] networking chips and scale up
switches and scale out switches.
[00:04:15] And then of course, you gotta
include power and cooling and all
[00:04:19] of that because, you know, all
these computers are extremely,
[00:04:23] extremely power hungry. They do
a lot of work and they're very
[00:04:27] energy efficient, but they in
aggregate still consume a lot of
[00:04:31] power. And so that's one. The
first question is, what is it?
[00:04:34] The second question is, why is it, and
we just spoke about the reason, you
[00:04:38] know you want to distribute the
workload so that you can exceed
[00:04:42] the benefit of just increasing
the number of computers.
[00:04:47] And then the third question is,
how is it, how do you do it?
[00:04:51] And that's the, that's kind
of the miracle of this
[00:04:55] company. You know, when you're designing a
computer, you have to have operating system of
[00:04:59] computers. When you're
designing a company,
[00:05:02] you should first think about what is it that you
want the company to produce. You know, I see
[00:05:06] a lot of companies organization
charts, and they all look the same.
[00:05:09] Hamburger organization charts,
soft organization charts, and car
[00:05:13] company organization charts.
They all look the same.
[00:05:16] And it doesn't make any sense to me. You
know, the goal of a company is to be the
[00:05:20] company is to be the machinery, the
mechanism, the system that produces
[00:05:25] the output. And that output is the
product that we like to create.
[00:05:29] It is also designed, the architecture
of the company should reflect
[00:05:33] the environment by which it
exists. It almost indirectly
[00:05:37] says what you should do with the
organization. My direct staff is 60 people.
[00:05:43] You know, I don't have one-on-ones with 'em because it's
impossible. You can't have, you can't have 60 people
[00:05:47] on your staff if you're, you
know, gonna get work done and-
[00:05:51] - So you still have 60 reports.
You still have across-
[00:05:53] - More, yeah.
[00:05:54] - More. And most stars at least
have a foot in engineering.
[00:05:59] - Almost all of them.
[00:06:01] There's experts in memory, there's
experts in CPUs, there's experts in
[00:06:05] optical. All, all—
[00:06:06] - That's incredible.
[00:06:06] - Yeah, GPUs and— Architecture,
algorithms, design, um—
[00:06:11] - So, you constantly have an eye on the
entire stack, and you're having to, like,
[00:06:15] intense discussions about the
designer of the entire stack?
[00:06:18] - And no conversation is ever one
person. That's why I don't do
[00:06:22] one-on-ones. We present a problem
[00:06:24] and all of us attack it. You know,
because we're doing extreme co-design.
[00:06:30] And literally, the company is doing
extreme co-design all the time.
[00:06:33] - So, even if you're talking about a
particular component, like cooling,
[00:06:38] networking, everybody's listening in?
[00:06:40] - Yeah, exactly.
[00:06:41] - And they can contribute, "Well, this
doesn't work for the power distribution.
[00:06:44] This doesn't-"
[00:06:45] - Exactly.
[00:06:45] - "... This doesn't work for the
memory. This doesn't work for this."
[00:06:49] - Exactly. And whoever wants to tune out,
tune out. You know what I'm saying?
[00:06:54] And the reason for that is because the
people who are on the staff, they know
[00:06:58] when to pay attention. There's supposed...
You know, it's something they could have
[00:07:01] contributed to, they didn't contribute to,
"I'm going to call them out." You know?
[00:07:04] And so, "Hey, come on, let's get in here."
[00:07:07] - So, as you mentioned, NVIDIA is this
company that's adapting to the environment.
[00:07:11] So, at which point can you say,
did the environment change and
[00:07:15] began adapting sort of secretly-
[00:07:19] ... in the early days from
GPU for gaming, maybe the
[00:07:23] early deep learning revolution to we're
now going to start thinking of it as an AI
[00:07:27] factory? What does NVIDIA do? It produces
AI, let's build a factory that makes AI.
[00:07:32] - Uh, I could, I c- you, you could- I could
reason through what just systematically.
[00:07:35] We started out as a, as
an accelerator company.
[00:07:39] But the problem with accelerators is that
the application domain's too narrow.
[00:07:43] It has the benefit of being
incredibly optimized for the
[00:07:47] job. You know, any specialist has
that benefit. The problem with
[00:07:51] intense specialization is that, of
course, your market reach is narrower,
[00:07:57] but that's, that's even fine. The
problem is, the market size also
[00:08:03] dictates your R&D capacity. And your
R&D capacity ultimately dictates
[00:08:10] the influence and impact that you can
possibly have in computing. And so,
[00:08:14] when we first started out as an
accelerator, very specific accelerator,
[00:08:19] we always knew that had- that was going
to be our first step. We had to find a
[00:08:23] way to become accelerated computing.
But the problem is, when you become a
[00:08:27] computing company,
[00:08:29] it's too general purpose and it takes
away from your specialization. The
[00:08:33] tur- I connected two
words that are actually
[00:08:37] have fundamental tension. The better
computing company we become, the
[00:08:41] worse we became as a specialist.
The more of a specialist, the less
[00:08:45] capacity we have to do
overall computing. And so,
[00:08:49] that... And I connected those two words
together on purpose, that the company
[00:08:53] has to find that really narrow path,
step by step by step, to expand our
[00:09:01] aperture of computing, but not
give up on the most important
[00:09:05] specialization that we had. Okay, so
the first step that we took beyond
[00:09:09] acceleration was, we invented
a programmable pixel shader.
[00:09:13] So, that was the first step towards
programmability. You know, it was our
[00:09:17] first journey towards moving into the world
of computing. The second thing that we
[00:09:21] did was we created we put
[00:09:25] FP32 into our shaders. That FP32 step,
IEEE-compatible FP32, was a huge step
[00:09:33] in the direction of computing. It was the
reason why all of the people who were
[00:09:39] working on, on stream
processors and, you know,
[00:09:43] other types of data flow processors
discovered us. And they said, "Hey, all of
[00:09:47] a sudden, you know, we might be able to use
this GPU that's incredibly computationally
[00:09:51] intensive, and it's now, you
know, compliant with IEEE."
[00:09:55] I can take my software that I was
writing, you know, previously on
[00:09:58] CPUs, and I can, you know, see about,
you know, using the GPU for that.
[00:10:04] And which led us to
create, put C on top of
[00:10:08] FP32, what's called, we
call Cg. The Cg path
[00:10:12] took us to eventually CUDA.
CUDA, step by step by step
[00:10:17] We... Well, putting CUDA
on GeForce, that was
[00:10:22] a strategic decision that was very,
very hard to do, because it cost the
[00:10:25] company enormous amounts of our
profits, and we couldn't afford it
[00:10:29] at the time. But we did it anyways
because we wanted to be a computing
[00:10:33] company. A computing
company has a computing
[00:10:37] architecture. A computing architecture
has to be compatible across all of
[00:10:41] the chips that we build.
[00:10:42] - Can you take me through that decision? So,
putting CUDA on GeForce, could not afford to
[00:10:46] do? Can you explain that decision? Why,
why boldly choose to do that anyway?
[00:10:52] Can you explain that decision?
[00:10:53] - Yeah, excellent. That was, that was
the first... I would say that that was
[00:10:57] the first strategic decision that is
as close to an existential threat.
[00:11:06] - For people who don't know, it
turned out to be, spoiler alert,
[00:11:10] one of the most incredibly
brilliant decisions ever made
[00:11:14] by a company. So, CUDA turned out to be
[00:11:18] an incredible foundation for computation
in this AI infrastructure world. So-
[00:11:23] - Thank you
[00:11:24] - ... just setting the context. It
turned out to be a good decision.
[00:11:27] - Yeah, it turned out to have been a good
decision. I think the... So, here's the way it
[00:11:31] went. So, we invented this
thing called CUDA, and
[00:11:35] It expanded the aperture of applications
[00:11:38] that, that we can accelerate with our
accelerator. The question is, how do we,
[00:11:44] how do we attract developers to CUDA?
[00:11:48] Because a computing platform is all
about developers. And developers
[00:11:54] don't come to a computing platform
just because, you know, it
[00:11:58] could perform something interesting. They
come to a computing platform because the
[00:12:02] install base is large.
[00:12:04] Because a developer, like anybody
else, wants to develop software that
[00:12:07] reaches a lot of people. So,
the install base is, in fact,
[00:12:11] the single most important
part of an architecture. The
[00:12:14] architecture could attract enormous
amounts of criticism. For example,
[00:12:20] no architecture has ever
attracted more criticism than the
[00:12:23] x86.... you know, as a less than, less than
elegant architecture, but yet it is the
[00:12:31] defining architecture of today. It
gives you an example that in fact
[00:12:35] so many RISC architectures which
were beautifully architected,
[00:12:42] incredibly well-designed by some of the
brightest computer scientists in the
[00:12:46] world, largely failed.
And so I've given you two
[00:12:49] examples where one is, you know,
one is elegant, the other one's
[00:12:53] barely aesthetic, and so yet x86
survived and the reason for-
[00:12:58] - Install base is everything.
[00:12:59] - Install base defines an
architecture. Not... Everything else
[00:13:03] is secondary, okay? And so there were
other architectures at the time.
[00:13:07] CUDA came out, OpenCL was here. There were...
You know, there's several other competing
[00:13:11] architectures. But the thing that...
The decision that we made that was good
[00:13:15] was we said, "Hey, look,
ultimately it's about,
[00:13:19] Install base and what is the
best way we could get a new
[00:13:23] computing architecture into the world?"
[00:13:26] By that timeframe, GeForce had
become successful. We were already
[00:13:30] selling millions and millions
of GeForce GPUs a year, and we
[00:13:33] said, "You know, we ought
to put CUDA on GeForce
[00:13:38] and put it into every single PC
whether customers use it or not,
[00:13:43] and use it as a starting point of
cultivating our install base."
[00:13:48] Meanwhile, we'll go and
attract developers, and
[00:13:52] we went to universities
and wrote books and taught
[00:13:56] classes and put CUDA everywhere.
And eventually people discover...
[00:14:00] And at the time, the PC was the primary
computing vehicle. There was no
[00:14:04] cloud, and we could put a
supercomputer in the hands of every
[00:14:07] researcher in school, every scientist, you
know, every engineering school, every...
[00:14:11] or every student in school, and
eventually something amazing will happen.
[00:14:15] Well, the problem was
CUDA increased our cost
[00:14:19] of that GPU, which is a consumer
product, so tremendously,
[00:14:23] it completely consumed all of the
company's gross profit dollars.
[00:14:29] And so at the time, the company was probably,
you know, worth, I don't know, at the time,
[00:14:33] eight...
[00:14:36] Was it like $8 billion or something? Like
six, $7 billion or something like that.
[00:14:40] After we launched CUDA, I recognized
that it was going to add so much cost,
[00:14:47] but it was something we believed in.
[00:14:50] You know, our market cap went down to like
one and a half billion dollars. And so
[00:14:54] we were down, we were down
there for a while and we
[00:14:58] clawed our way way back
slowly, but we carried
[00:15:01] CUDA on GeForce. I always say
that NVIDIA is the house that
[00:15:05] GeForce built, because it was
GeForce that took CUDA out to
[00:15:09] everybody. Researchers, scientists, they
discovered CUDA on GeForce because they were
[00:15:17] all, you know... Many of 'em were
gamers. Many of them built their own
[00:15:21] PCs anyways. In a university
lab, many of them built
[00:15:25] clusters themselves, you know,
using PC components. And,
[00:15:29] and so that, you know, that's
kind of how we got going.
[00:15:31] - And then that became the platform and the
foundation for the deep learning revolution.
[00:15:35] - That was also another great,
great observation. Yeah.
[00:15:38] - That existential moment, do you
remember... Like, what were those meetings
[00:15:42] like? What were those discussions like,
deciding as a company, risking everything?
[00:15:48] - Well I had to make it clear to the
board what we're trying to do, and
[00:15:56] the management team knew our gross
margins were gonna get crushed.
[00:16:00] So you could imagine a world
where GeForce would carry
[00:16:04] the burden of CUDA and
none of the gamers would
[00:16:08] appreciate it and none of the gamers
would pay for it. You know, they only pay
[00:16:12] certain price and it doesn't matter what
your cost is. And so the... You know,
[00:16:16] we, we increased our cost
by 50% and that con-
[00:16:20] consumed... And we were a 35%
gross margin company, and so it,
[00:16:24] it was a... It was quite a
difficult decision to make. But
[00:16:28] you could imagine that someday this would
go into workstations and it would go into
[00:16:31] supercomputers and, and in those segments,
maybe we can capture more margin.
[00:16:37] so you could, you could reason your
way into being able to afford this,
[00:16:42] But it still took... It took a decade.
[00:16:45] - But that, but that's more of, like, conversation
with the board convincing them, but you
[00:16:48] psychologically- ... as NVIDIA's
continued to make bold bets
[00:16:56] that predict the future, and in part,
especially now, define the future.
[00:17:01] So I'm almost looking for wisdom about
[00:17:05] how you're able to make those decisions,
to make leaps- ... like that as a company.
[00:17:14] - Well, first of all I'm informed
by a lot of curiosity.
[00:17:21] At some point, there's a
reasoning system that,
[00:17:26] that convinces me, so clearly this outcome
will happen. That this will happen.
[00:17:34] And so I believe it in my mind,
and when I believe it in my mind,
[00:17:38] you know, you know how it is.
You manifest a future and that
[00:17:42] future is so convincing,
there's no way it won't happen.
[00:17:48] There's a lot of suffering in between, but
you've gotta believe what you believe.
[00:17:52] - So you envision the future-
[00:17:55] ... and you essentially, from a sort of
engineering perspective, manifest it?
[00:17:59] - Yeah. And you, you reason about how
to get there. You reason about why
[00:18:03] it, it must exist. And, you
know, I reason... We all
[00:18:09] reason it here. The management team would
reason about it. All the people that I...
[00:18:13] We spend a lot of time reasoning about
it. The thing, the thing that... The next
[00:18:17] part of it is probably a
skill thing, which is,
[00:18:20] you know, oftentimes in
leadership the leadership
[00:18:24] stays quiet or they learn about something,
and then they do some manifesto,
[00:18:28] and it's a brand-new year, and somehow
at the end of the year, next year,
[00:18:32] we're gonna have a brand-new plan.
Big huge layoff this way, big huge
[00:18:36] organization change this way, new mission
[00:18:39] statement... brand new logos
you know, that kind of stuff.
[00:18:43] Um, we've just never, I never do things
that way. When I learn about something
[00:18:48] and it's starting to influence how
I think, I'll make it very clear to
[00:18:52] everybody near me that, you
know, this, this is interesting.
[00:18:57] This is going to make a difference.
This is going to impact that.
[00:19:01] And I reason about things step by step by
step. Oftentimes, I've already made up
[00:19:05] my mind, but I'll take
every possible opportunity,
[00:19:09] external information, new
insights, new discoveries,
[00:19:13] New engineering, you
know, revelations, new
[00:19:16] milestones developed, I'll take
those opportunities and I'll use
[00:19:20] it to shape everybody else's
[00:19:24] belief system. And I'm doing
that literally every single day.
[00:19:28] I'm doing that with my board, I'm doing that
with my management team, I'm doing that with
[00:19:32] my employees. I'm trying to shape
[00:19:35] their belief systems such that when I come
the day I say, "Hey, let's buy Mellanox,"
[00:19:43] it's completely obvious to everybody
that we absolutely should.
[00:19:48] On the day that I said, "Hey guys, let's
[00:19:52] go all in on deep learning,"
and let me tell you why. I've
[00:19:56] already been laying down the
bricks to different organizations
[00:20:00] inside the company. Every
organization and everybody,
[00:20:05] many of the people might
have heard everything.
[00:20:08] Most of the company hears,
of course, pieces of it.
[00:20:11] And on the day that I announce it,
[00:20:14] everybody's kind of bought
in to many pieces of it.
[00:20:19] And in a lot of ways, I like to
announce these things, and I imagine,
[00:20:25] that the employees are kind of saying,
"You know, Jensen, what took you so long?"
[00:20:30] And in fact, I've been shaping their
belief system for some time, and therefore
[00:20:34] leadership. Sometimes it looks
like you're leading from behind,
[00:20:39] but you've been shaping their, you know, to
the point where on the day that I declared it,
[00:20:43] 100% buy-in. But that's what you
want. You want to bring everybody
[00:20:47] along. You know, otherwise, we announce something
about deep learning and everybody goes, "What
[00:20:51] are you talking about?" You know, you
announce something about let's go all in
[00:20:55] on this thing, and your
management team, your
[00:20:59] board, your employees, your customers, they're
kind of like, "Where's this coming from?
[00:21:02] You know, this is insane." And so, so GTC
[00:21:06] effect, if you go back in time,
you look at the keynotes,
[00:21:11] I'm also shaping the belief
system of my partners in the
[00:21:15] industry and I'm using that to
shape, you know, the belief
[00:21:19] system of my own employees. And so by
the time that I announce something,
[00:21:24] like for example, we just announced Grok.
[00:21:27] We've been late... I've been talking about
the stepping stones for two and a half
[00:21:32] years.
[00:21:33] You just go back and go, "Oh my gosh,
they've been talking about it for two and a
[00:21:37] half years." And so I've been laying
the foundation step by step by step,
[00:21:41] so when the time comes you announce it, everybody's
saying, "You know, what took you so long?"
[00:21:44] - But it's not just inside the company. You're
shaping the landscape, the broader global landscape
[00:21:48] of innovation. Like, putting those ideas
out there, you really are manifesting
[00:21:52] reality.
[00:21:53] - We don't build computers. We actually
don't build clouds. We don't... As
[00:21:57] it turns out, we're a computing
platform company. And so nobody can
[00:22:00] buy anything from us. That's the
weird thing. You know, we vertically
[00:22:06] design, vertically integrate to
design and optimize, but then
[00:22:10] we open up the entire platform
at every single layer
[00:22:14] to be integrated into other
companies' products and services and
[00:22:18] clouds and supercomputers
and OEM computers
[00:22:21] and so the amazing thing
is, I can't do what I
[00:22:25] do without having convinced
them first. And so most of
[00:22:29] GTC is about manifesting
a future that by the
[00:22:33] time that we... My product is ready,
they're going, "What took you so long?"
[00:22:39] - Yeah. So one of the things you've
been a believer for a long
[00:22:43] time is scaling laws,
broadly defined. So are
[00:22:47] you still a believer in the scaling laws?
[00:22:49] - Yeah, yeah. Yeah, we have
more scaling laws now.
[00:22:51] - So I think you've outlined four of them
with pre-training, post-training, test
[00:22:55] time, and agentic scaling. What do you
think, when you think about the future,
[00:23:01] deep future and the near-term
future, what are the blockers
[00:23:06] that you're most concerned about that keep
you up at night that you have to overcome
[00:23:10] in order to keep scaling?
[00:23:12] - Well, we can go back and reflect on
what people thought were blockers.
[00:23:16] So in the beginning, we were the
first... The pre-training scaling
[00:23:20] law. You know, people
thought well rightfully
[00:23:24] so, that the amount of data that
we have, high-quality data that we
[00:23:28] have will limit the intelligence that
we achieve. And that scaling law
[00:23:32] was an important, very important
scaling law. The larger the model, the
[00:23:35] correspondingly more data
results in a better... With a
[00:23:39] results in a smarter AI. And
so that was pre-training. And
[00:23:43] Ilya Sutskever, Ilya said, "We're out of data,"
or something like that. "Pre-training is
[00:23:47] over," or something like
that. The industry panicked,
[00:23:51] you know, that this is the end of AI.
And of course, of course that, that's
[00:23:56] obviously not true. We're gonna keep
on scaling the amount of data that we
[00:24:00] have to, to train with. A lot of that
data is probably gonna be synthetic,
[00:24:04] and that also confused people,
you know? And what people don't
[00:24:08] realize is they've kind of
forgotten that most of the data
[00:24:12] that, that we are training that
we teach each other with, inform
[00:24:15] each other with, is
synthetic. You know, I...
[00:24:19] It's synthetic because it
didn't come out of nature.
[00:24:23] You created it. I'm consuming
it. I modify it, augment it,
[00:24:30] I regenerate it, somebody
else consumes it. And so, so
[00:24:33] we've now reached a level where AI is able
to take ground truth, augment it......
[00:24:43] Enhance it, synthetically
generate an enormous amount of
[00:24:46] data. And that part of post-training
[00:24:50] continues to scale, and so the
amount of data that we could use
[00:24:53] that is human generated will be
smaller, and smaller, and smaller.
[00:24:57] The amount of data that
we use to train model,
[00:25:02] is going to continue to scale to the
point where we're no longer limited...
[00:25:07] Training is no longer limited by...
Data is now limited by compute. And the
[00:25:11] reason for that is most of the data
is synthetic. Then the next phase
[00:25:15] is test time, and
[00:25:19] I still remember people telling me
that, "Inference? Oh, yeah, that's
[00:25:23] easy. Pre-training, that's hard." These
are giant systems that people are talking
[00:25:26] about. Inference must be easy. And so
inference chips are gonna be little tiny
[00:25:30] chips, and
[00:25:32] ... you know, they're not, they're not like
NVIDIA's chips. Oh, those are gonna be
[00:25:35] complicated and expensive, and, you
know, we could make... And this is-
[00:25:39] in the future, inference is gonna be the
biggest market, and it's gonna be easy, and
[00:25:43] we're gonna commoditize it. You know,
everybody can build their own chips. And,
[00:25:47] and that was always illogical to
me because inference is thinking,
[00:25:53] and I think thinking is hard.
Thinking is way harder than reading.
[00:25:59] You know, pre-training is just
[00:26:01] memorization and generalization, you know,
and looking for patterns in relationships.
[00:26:05] You're reading and reading, versus thinking,
reasoning, solving problems, taking
[00:26:14] unexplored experiences,
new experiences, and
[00:26:18] breaking it down into...
Decomposing it into, you
[00:26:22] know, solvable pieces that we
then go off, either through first
[00:26:26] principle reasoning, or, you
know, through previous examples,
[00:26:30] prior experiences. You know, or just uh,
[00:26:34] exploration and search and,
you know, trying different
[00:26:38] things. And that whole process
of, of test time scaling,
[00:26:44] Inference, is really about
thinking. And it's about
[00:26:47] reasoning, it's about planning, it's about
search, it's about... And so how could that
[00:26:51] possibly be compute light? And
we were absolutely right about
[00:26:55] that. You know, so test time scaling
is intensely compute intensive.
[00:27:01] Then the question is, okay, now we're at inference
and we're at test time scaling, what's beyond that?
[00:27:06] Well, obviously, we have now created,
you know, one agentic person,
[00:27:12] and that one agentic person has a
large language model that we've now
[00:27:16] now, you know, developed. But
during test time, that agentic
[00:27:20] system goes off and does
research and bangs on
[00:27:24] databases, and it goes out
and, you know, uses tools,
[00:27:27] and one of the most important things it
does is spins off and spawns off a whole
[00:27:31] bunch of sub-agents. Which means
we're now creating large teams.
[00:27:36] It's so much easier to scale NVIDIA by
[00:27:40] hiring more employees than
it is to scale myself.
[00:27:44] And so the next scaling law is the
agentic scaling law. It's kind of
[00:27:47] like multiplying AI.
[00:27:51] Multiplying AI, we could spin off agents
as fast as you want to spin off agents.
[00:27:55] And so, you know, I... You
know, I have four scaling laws.
[00:27:59] And as we use the agentic
systems, they're gonna create a
[00:28:03] lot more data, they're gonna create a lot
of experiences. Some of it we're gonna say,
[00:28:07] "Wow, this is really good.
We ought to memorize this."
[00:28:12] That data set then comes all
the way back to pre-training.
[00:28:15] We memorize and generalize it. We
then refine it and fine-tune it
[00:28:20] back into post-training. Then
we enhance it even more with
[00:28:24] test time, you know, and the
agents, agentic systems,
[00:28:28] you know, put it out to the
industry. And so this loop, this
[00:28:32] cycle, is gonna go on and on and on.
It kinda comes down to basically
[00:28:37] intelligence is gonna scale by
one thing, and that's compute.
[00:28:41] - But there's a tricky thing there that you
have to anticipate and predict, which
[00:28:45] is some of these components, it requires
[00:28:49] different kind of hardware to
really do it optimally. So you have
[00:28:53] to anticipate where the AI innovation's
going to lead. For example, a mixture of-
[00:28:57] - Perfect
[00:28:58] - ... experts with sparsity.
[00:28:59] - Perfect.
[00:29:00] - With hardware, you can't just
pivot on a week's notice. You
[00:29:04] have to anticipate what that's
going to look like. It has some-
[00:29:06] - So good
[00:29:07] - ... that's so scary and
difficult to do, right?
[00:29:09] - For example, These AI model architectures
are being invented about once every six
[00:29:15] months. Right? And system architectures
and hardware architectures
[00:29:23] kind of every three years.
[00:29:26] And so you need to anticipate
what likely is going to happen,
[00:29:30] you know, two, three years from now.
[00:29:33] And there's a couple ways that you could do that. First of
all, we could do research internally ourselves, and that's one
[00:29:37] of the reasons why we have basic
research, we have applied research.
[00:29:40] We create our own models.
And so we have hands-on life
[00:29:44] experience right here. This is part of
the co-design that I'm talking about.
[00:29:48] We're also the only AI company in the world that
works with literally every AI company in the world.
[00:29:51] And so to the extent that we
can, we try to get a sense
[00:29:55] of what are the challenges
that people are experiencing.
[00:29:59] - So you're listening to the whispers
across the industry, the AI labs.
[00:30:02] - That's right. You got to listen and
learn from everybody. And have a...
[00:30:06] And then the last part is to
have an architecture that's
[00:30:10] flexible, that can adapt and move
with the wind. And one of the
[00:30:14] benefits of, of CUDA is that
it's, you know, on the one hand,
[00:30:18] an incredible accelerator. On the
other hand, it's really flexible.
[00:30:22] And so that balance,
incredible balance between
[00:30:26] specialization, otherwise we
can't accelerate the CPU,
[00:30:31] versus generalization, so that we
can adapt with changing algorithms,
[00:30:35] that's really, really important.
That's the reason why CUDA has
[00:30:39] been so resilient on the
one hand, and yet we
[00:30:43] continue to enhance it. We're
at CUDA 13.2, and so we're
[00:30:47] evolving the architecture
so fast that we can stay
[00:30:51] with, you know, with
the modern algorithms.
[00:30:55] For example... When mixtures
of experts came out,
[00:30:59] That's the reason why we had
NVLink 72 instead of NVLink eight.
[00:31:04] We could now take an entire four
trillion, 10 trillion parameter model
[00:31:08] and put it in one computing domain
as if it's running on one GPU.
[00:31:13] Um, people probably didn't
notice, I said it, but
[00:31:19] if you look at the architecture of
[00:31:22] the Grace Blackwell racks,
it was completely focused on
[00:31:26] doing one thing, processing the LLM.
[00:31:30] All of a sudden, one year later,
you're looking at a Vera Rubin rack.
[00:31:34] It has storage accelerators. It has
this incredible new CPU called Vera.
[00:31:41] It has Vera Rubin and NVLink 72 to run the
[00:31:45] LLMs. It also has this new
additional rack called Rock.
[00:31:49] And so this entire rack
system is completely
[00:31:53] different than the previous
one, and it's got all these new
[00:31:57] components in it. And the reason for that
is because the last one was designed to run
[00:32:02] MoE large language models, inference.
And this one is to run agents and agents
[00:32:08] bang on tools, and-
[00:32:10] - Obviously, the design of the system had
to have been done before Claude Code,
[00:32:17] Codex, OpenClaw. So you were
anticipating the future, essentially.
[00:32:21] And that comes from what? From the whispers,
from understanding what all the state-
[00:32:25] - No
[00:32:25] - ... of the art is about?
[00:32:26] - No, it's easier than that. You just reason
about it. First of all, you just reason.
[00:32:34] no matter, no matter what
happens, at some point in order
[00:32:38] for that large language model to
be a digital worker... Let's just,
[00:32:42] let's just use that metaphor. Let's
say that we want the LLM to be a
[00:32:46] digital worker. What does that have to do?
[00:32:49] It has to access ground truth.
That's our file system. It has
[00:32:53] to be able to do research. It doesn't know
everything. We don't have... And I don't wanna
[00:32:57] wait until this AI becomes,
you know, universally
[00:33:01] smart about everything, past,
present, and future before I
[00:33:05] make it useful. And so therefore, I
might as well let it go do research.
[00:33:09] It's obviously, if it wants to
help me, it's gotta use my tools.
[00:33:13] You know, a lot of people would say,
"You know AI is gonna completely
[00:33:17] destroy software. We don't need software anymore.
We don't even need tools anymore." That's
[00:33:20] ridiculous. Let's use the...
Let's use a thought experiment.
[00:33:25] And you could just sit there,
enjoy a glass of whiskey, and,
[00:33:29] and think about all these things, and it
would become completely obvious. Like, if I
[00:33:33] were to create the most amazing- the
[00:33:37] most amazing agent that we can
imagine in the next 10 years.
[00:33:41] Let's say it'd be a humanoid robot. If
that humanoid robot were to be created,
[00:33:46] is it more likely that the
humanoid robot comes into my house
[00:33:50] and uses the tools that I have to
do the work that it needs to do?
[00:33:54] Or does this hand turns
into a 10-pound hammer in
[00:33:58] one instance, turns into a
scalpel in another instance,
[00:34:02] and in order to boil water, it
beams, you know, microwaves out
[00:34:06] of its fingers? You know, or is it more
likely just to use a microwave, you
[00:34:10] know? And the first time it
goes up to the microwave,
[00:34:13] it probably doesn't know how to use it.
But that's okay. It's connected to the
[00:34:17] internet. It reads the manual of this
[00:34:21] microwave, reads it,
instantly becomes an expert.
[00:34:24] And so it uses it. And
so I think the... I just
[00:34:28] described, in fact, almost all
of the properties of OpenClaw.
[00:34:35] You know, that it's gonna use tools, that it's
gonna access files, it's gonna be able to do
[00:34:38] research. It has I/O subsystem.
And when you're done
[00:34:42] reasoning through it, reasoning
about it in that way,
[00:34:46] Then you say, "Oh, my gosh, the impact
to the future of computing is deeply
[00:34:53] profound." And the reason for that is, I
think we've just reinvented the computer.
[00:34:57] And then now you say, "Okay, when did
we reason about that? When did we
[00:35:01] reason about OpenClaw?" If you take the
OpenClaw schematic that I used at GTC,
[00:35:08] you'll find it two years ago. Literally,
two years ago at GTC, I was talking about
[00:35:15] agentic systems that exactly
reflect OpenClaw today.
[00:35:21] And, of course, the confluence of
[00:35:25] many things had to happen. First
of all, we needed Claude and
[00:35:29] GPT and, you know, all of these
models to reach a level of
[00:35:33] capability. So their innovation and
their breakthroughs and their continued
[00:35:36] advances was really important.
[00:35:39] And then, of course, somebody had
to create an open source, you
[00:35:43] know project that was sufficiently robust,
you know, and sufficiently complete
[00:35:51] and that we can all put to
work. And I think OpenClaw
[00:35:55] did for, did for agentic
systems what ChatGPT did for
[00:35:59] generative systems. And I just
think it's a very big deal.
[00:36:02] - Yeah, it's a really special moment.
I'm not exactly sure why it
[00:36:05] captured so much of the
world's attention, but it did,
[00:36:09] more than Claude Code and Codex and so on.
[00:36:12] - Because consumers could reach it.
[00:36:13] - Sure, yeah. But there's also
so much of this is vibes.
[00:36:17] And Peter, I had a
podcast with him, he's a
[00:36:21] wonderful human being. So part of it is
also the humans that represent the thing.
[00:36:25] - Yeah, no doubt.
[00:36:25] - Part of it is memes and the— 'Cause
we're all trying to figure it out.
[00:36:28] There's really serious and
complicated security concerns
[00:36:31] about when you have such powerful
technology, how do you hand over your data
[00:36:35] so they can do useful stuff? But then
there's scary things associated with that.
[00:36:39] And we, as a civilization, as individual
people and as a civilization, figuring out how
[00:36:43] to find that right balance.
[00:36:44] - Yeah, we jumped on it right away and we
sent a bunch of security experts this way.
[00:36:49] And we did this thing called
OpenShell. It's already been
[00:36:53] integrated into, into OpenClaw.
[00:36:55] - And NVIDIA put forward NemoClaw.
[00:36:58] - Yep, exactly.
[00:36:59] - They install super easy. It
makes sure that it's secure.
[00:37:03] - We give you two out of three
rights. Agentic systems can access
[00:37:07] sensitive information, it can
execute code, and it can communicate
[00:37:10] externally. We could keep things safe
if we gave you two out of those three
[00:37:17] capabilities at any
time, but not all three.
[00:37:21] And out of those two out of three
capabilities, we also give you access control
[00:37:25] based on whatever rights that
you're given by enterprise.
[00:37:29] And then we connect it to a policy engine
that all these enterprises already have.
[00:37:33] And so we're going to try to do our best
to help OpenClaw become a better claw.
[00:37:40] - So you eloquently explained
how we have a long history of
[00:37:44] blockers that we thought were going to be blockers,
and we overcame them. But now looking into the
[00:37:48] future, what do you think might be the
blockers now that it's clear that agents
[00:37:52] will be everywhere?
[00:37:53] So obviously we're going to need
compute. So what is going to be the
[00:37:57] blocker for that scaling?
[00:37:59] - Power is a concern, but it's not the
only concern. But that's the reason why
[00:38:04] we're pushing so hard on extreme co-design,
so that we can improve the tokens
[00:38:11] per second per watt orders of magnitude
[00:38:15] every single year. And so in
the last 10 years, Moore's
[00:38:19] Law would have progressed computing
about 100 times in the last
[00:38:23] 10 years. We progressed
and scaled up computing by
[00:38:27] a million times in the last 10 years.
And so we're gonna keep on doing that
[00:38:31] through extreme co-design. So
energy efficiency, perf per watt,
[00:38:36] completely affects the
revenues of a company. It
[00:38:40] affects the revenues of a
factory. And we're just going to
[00:38:44] push that to the limit so that we
can keep on driving token costs
[00:38:47] down as fast as we can. You know, the
[00:38:51] our computer price is going
up, but our token generation
[00:38:56] effectiveness is going up so
much faster that token cost is
[00:38:59] coming down. It's just coming down
an order of magnitude every year.
[00:39:04] - So power, that's an interesting
one. So the way to try
[00:39:07] to get around the power blocker
is to try to, with the tokens per
[00:39:11] second per watt, try to make
it more and more efficient.
[00:39:14] Of course, there's the question
of how do we get more power.
[00:39:16] - We should also get more power.
[00:39:17] - That's a really complicated one. You've talked
about small modular nuclear power plants.
[00:39:21] There's all kinds of ideas for
energy. How much does it keep you
[00:39:25] up at night? The bottlenecks
in the supply chain of AI,
[00:39:29] like ASML with EUV lithography
machines, TSMC with advanced
[00:39:33] packaging like CoWoS, and SK Hynix
with the high bandwidth memory?
[00:39:38] - All the time, and we're working on it
all the time. No company in history
[00:39:44] has ever grown at a scale
that we're growing while
[00:39:47] accelerating that growth. It's incredible.
[00:39:50] And it's hard for people
to even understand this.
[00:39:53] In the overall world of AI
computing, we're increasing
[00:39:57] share. And so supply chain, upstream and
downstream, are really important to us.
[00:40:04] I spend a lot of time informing all the
[00:40:08] CEOs that I work with, what are the
dynamics that's going to cause,
[00:40:12] The growth to continue or even
accelerate? It's part of the reasons
[00:40:16] why to the entire right-hand
side of me were CEOs of
[00:40:22] practically the entire IT industry
upstream and practically the entire
[00:40:29] infrastructure industry downstream.
[00:40:32] And they were all... There
were several hundred CEOs.
[00:40:36] And I don't think there's ever been keynotes
where several hundred CEOs show up.
[00:40:40] And part of it is, I'm telling them
about our business condition now.
[00:40:46] I'm telling them about the growth drivers
in the very near future and what's
[00:40:49] happening. And I'm also describing
where are we going to go next
[00:40:53] so that they could use all of this
information and all of the dynamics that are
[00:40:57] here to inform how they
want to invest. And
[00:41:01] so I inform them that way like
I inform my own employees.
[00:41:06] And then of course, then
I make trips out to them
[00:41:09] and make sure that, "Hey, listen, I
want you to know this quarter, this
[00:41:13] coming year, this next year, these
things are going to happen."
[00:41:17] And if you look at the
CEOs of the DRAM industry,
[00:41:21] The number one DRAM in the world was
DDR memory for CPUs in data centers.
[00:41:30] About three years ago, I was able to
convince several of the CEOs that
[00:41:36] even though at the time HBM memory was
used quite scarcely, you know, and,
[00:41:40] and barely by supercomputers
that this was going to be a
[00:41:44] mainstream memory for data centers in
the future. And at first it sounded
[00:41:48] ridiculous, but several of the
CEOs believed me and decided
[00:41:52] to invest in building HBM memories. Another
memory was rather odd to put into a data
[00:41:59] center, is the low power memories
that we use for cell phones.
[00:42:03] And we wanted them to adapt them
for supercomputers in the data
[00:42:07] center. And they go, "Cell phone
memory for supercomputers?"
[00:42:11] And I explained to them why.
Well, look at these two memories,
[00:42:14] LPDDR5, HBM4. The volumes are
[00:42:18] so incredible. All three of them had
record years in history, and these
[00:42:22] are, these are 45-year companies. And so,
[00:42:27] you know, I... That's part of my job, is
to inform and shape, inspire, you know.
[00:42:36] - So you're not just manifesting
the future and maybe
[00:42:39] inspiring NVIDIA, the different
engineers of the company, you're,
[00:42:44] you're manifesting the supply chain of the
future. So you're having conversations with
[00:42:48] TSMC, with ASML.
[00:42:50] - Upstream, downstream.
[00:42:51] - Upstream, downstream. So that's the thing.
[00:42:53] - GEV, Caterpillar. Yeah, that's downstream
from us. Yeah, yeah, there you go.
[00:42:59] - Yeah, the whole thing. I
mean, but that's so...
[00:43:02] There's so much incredibly
difficult engineering that
[00:43:05] happens in the entire semiconductor
industry, and it just feels scary
[00:43:12] how intricate the supply chain
is, how many components there
[00:43:16] are, but it works somehow.
[00:43:18] - Exactly, the deep science. The
deep engineering, the incredible
[00:43:22] manufacturing, and so much of the
manufacturing is already robotics,
[00:43:26] but we have a couple of hundred
suppliers that contribute
[00:43:30] the technology that goes into
our 1.3 million component rack.
[00:43:36] Each rack is 1.3, one and a half million
components. There are 200 suppliers
[00:43:43] across the Vera Rubin rack.
[00:43:45] - So it's interesting that you don't list that as the
thing that keeps you up at night in the list of
[00:43:48] blockers.
[00:43:49] - But I'm doing, I'm doing all
the things necessary to-
[00:43:52] - Okay
[00:43:52] - ... yeah, see?
[00:43:54] I can go to sleep because I checked it
off. I said, okay, you know, I go, I
[00:43:58] yeah, I can go to sleep and I go,
well, let's see, what re- let's reason
[00:44:02] about this. What's important for us?
[00:44:03] Um, because okay, let's
reason about this. Because we
[00:44:08] changed the system architecture
from the original DGX-I that
[00:44:12] you remembered to NVLink-72
rack scale computing-
[00:44:16] ... what's gonna... What does
that, what does that mean?
[00:44:19] What does that mean to software? What does
that mean to engineering? What does that
[00:44:23] mean to how we design and test? How,
and what does that mean to the supply
[00:44:27] chain? Well, one of the things that
it meant was we moved supercomputer,
[00:44:33] supercomputer integration
at the data center
[00:44:37] into supercomputer manufacturing in the
supply chain. If you're doing that,
[00:44:44] you also have to recognize
you're gonna move one... And if,
[00:44:48] if you're, if you're, you
know, total footprint of
[00:44:52] whatever data center you're gonna build,
let's say you would like to have, you know,
[00:44:58] 50 gigawatts of supercomputers
that are running simultaneously,
[00:45:02] and it takes one week
to manufacture that 50
[00:45:06] gigawatts of supercomputers,
then each week in the
[00:45:10] supply chain, the supercomputers are
gonna need a gigawatt of power. And so,
[00:45:14] so we're gonna need the supply chain
to increase the amount of power it has
[00:45:18] to build, test, to build and test the
[00:45:21] supercomputers in the supply
chain before I ship it.
[00:45:25] Well, NVLink-72 literally builds
supercomputers in the supply chain and
[00:45:28] ships 'em two, three
tons at a time per rack.
[00:45:32] It used to be—they used to come in
parts and we used to assemble 'em
[00:45:36] inside the data center. But that's impossible
now because NVLink-72 is so dense.
[00:45:41] And so that's an example. And I
would have to go and to, you know,
[00:45:45] I've... Fly into the supply chain, go meet
my partners saying, "Hey," I said, "guess
[00:45:48] what? So here's what I'm going to do
with... This is the way we used to build
[00:45:52] our DGXs. We're gonna build them this way.
This is gonna be so much better because
[00:45:56] we're going to need 'em for inference."
The market for inference is, you know,
[00:46:02] coming. The inflection point for inference
is coming. It's gonna be a big market.
[00:46:05] And so I first explain to them what's
going on, why it's gonna happen, and
[00:46:09] then I ask 'em to make several billion
dollars of capital investments
[00:46:15] each. And because they, you
know, they trust me and I'm very
[00:46:21] respectful of 'em, and I give 'em
every opportunity to question me and
[00:46:25] I spend time to explain things to people
and I reason about it. I draw on pictures
[00:46:29] and I reason about it in first
principles. And by the time
[00:46:33] I'm done with them, they know what to do.
[00:46:35] - So it's a lot of it is about relationships
and building a shared view of the future.
[00:46:41] Uh, but do you worry about certain
bottlenecks? I mean, what are the
[00:46:45] biggest bottlenecks in the supply chain?
Are you, are you worried about ASML's EUV
[00:46:49] tooling? Are you, are you worried about
the packaging, CoWoS packaging of
[00:46:53] TSMC, about how fast it could
scale? Like you said, you're
[00:46:57] not only growing incredibly fast,
you're accelerating your growth. So
[00:47:01] it feels like everybody in the
supply chain, and those are
[00:47:05] certainly bottlenecks, would have to scale
up. Are you having conversations with them,
[00:47:09] like, how can you scale up
faster? Do you worry about it?
[00:47:13] - No.
[00:47:13] - Okay.
[00:47:14] - Because, because I told 'em what
I needed. They understood what I
[00:47:18] need. They told me what they're gonna go do,
and I believe them what they're going to do.
[00:47:22] - Interesting.
[00:47:22] That's great to hear. So maybe if we can
just linger on the power for a little
[00:47:26] bit. What are your hopes for how
to solve the energy problem?
[00:47:30] - One of the areas, Lex, that I'm
[00:47:34] that I would love, I would love us to
talk about and just get the message out,
[00:47:38] you know our power grid is designed
[00:47:44] for the worst case condition
with some margin. Well,
[00:47:50] 99% of the time we're nowhere near the worst
case condition because the worst case condition
[00:47:54] is a few days in the winter,
a few days in the summer,
[00:47:57] and extreme weather. Most
of the time we're nowhere
[00:48:01] near the worst case condition and
we're probably running around, call it
[00:48:05] 60% of peak. And so 99% of
the time, our power grid
[00:48:13] has excess power, and they're just
sitting idle, but they have to be there
[00:48:17] sitting idle because just in case,
when the time comes, hospitals have to
[00:48:21] be powered and, you know, infrastructure has to be
powered and airports have to run and so on and so
[00:48:25] forth. And so the question that I
have is whether we could go and,
[00:48:31] Help them understand and
create contractual agreements
[00:48:35] and design computer architecture systems,
data centers, such that when they need,
[00:48:42] The maximum power for
infrastructure in society,
[00:48:46] that the data centers would get less.
[00:48:49] But that's in a very rare instance anyways.
And during that time, we either have a
[00:48:53] backup generator for that little part of
it, or we just have our computers shift the
[00:48:57] workload somewhere else, or we
have the computers just run
[00:49:00] slower. You know, we could
degrade our performance,
[00:49:03] reduce our power consumption and provide
[00:49:07] for a, you know, slightly longer
latency response, you know, when
[00:49:10] somebody asks for, you know, asks
for an answer. And so I think that
[00:49:14] that way of using computers,
of building data centers,
[00:49:18] instead of expecting 100% uptime-...
[00:49:22] and these contracts that are
really, really quite rigorous, it's
[00:49:26] putting a lot of pressure on the grid
to be able to... Now, they're gonna
[00:49:30] have to increase from their maximum.
I just wanna use their excess.
[00:49:35] It's just sitting there.
[00:49:36] - Yeah, that's not talked about
enough. So what's stopping there?
[00:49:40] Is it regulation? Is it bureaucracy?
[00:49:43] - I think it's a three-way
problem. It starts with the end
[00:49:47] customer. The end customer
puts requirements
[00:49:51] on the data centers that they can never
[00:49:55] not be available, okay? So that the
end customer expects perfection.
[00:50:00] Now, in order to deliver that
perfection, you need a combination of
[00:50:04] backup generators and your grid power
[00:50:07] supplier to deliver on perfection. And
so everybody's gotta have six nines.
[00:50:13] Well, I think first of all,
[00:50:15] right now, we ought to have everybody understand
that when the customer asks for these
[00:50:19] things, you have somebody in
your data center operations
[00:50:23] team disconnected from the CEO. I
bet the CEO doesn't know this. I'm
[00:50:27] gonna talk to all the CEOs.
The CEOs are probably
[00:50:30] not paying any attention to the
contracts that are being signed, and
[00:50:34] so everybody wants to sign the best
contract, of course. And they go down to
[00:50:39] cloud service providers, and the
contract, the... The two contract
[00:50:42] negotiators that are... You,
I could just see them now.
[00:50:46] You know, negotiating these multi-year
contracts. Both sides want,
[00:50:50] you know, the best contract. As a result,
[00:50:55] the CSPs then have to go down to the
utilities, and they expect the nine,
[00:50:59] the six nines. And so I think
the first thing is just make
[00:51:02] sure that all of the customers,
the CEOs and the customers
[00:51:06] realize what they're asking for.
[00:51:09] Now, the second thing is we have to build
data centers that gracefully degrade.
[00:51:13] And so if the power, if the utility, if the
grid tells us, "Listen, we're gonna have
[00:51:17] to back you down to about 80%," we're
gonna say, "That's no problem at all."
[00:51:21] We're just gonna move our workload around.
We're gonna make sure that data's never
[00:51:25] lost, but we can reduce the
computing rate and use less
[00:51:30] energy. The quality of service degrades
a little bit. For the critical
[00:51:34] workloads, I shift that
somewhere else right away
[00:51:38] so I don't have that problem, and so,
you know, whoever, whichever data
[00:51:42] center still has 100% uptime, and so...
[00:51:44] - How difficult of an engineering problem is that,
that smart, dynamic allocation of power in a data
[00:51:48] center?
[00:51:49] - As soon as you could specify, you
could engineer it. U- beautifully put.
[00:51:54] So long as it obeys the laws of physics
on first principles, I think we're good.
[00:51:58] - What was the third thing
you were mentioning? Um...
[00:52:00] - So the second thing is the data
centers. And the third thing is we
[00:52:04] need the utilities to also recognize
that this is an opportunity-
[00:52:10] ... and instead of saying, "Look
it's gonna take me five years
[00:52:14] to increase my grid capability," uh, if
[00:52:18] you, if you have, if you're willing to
take power of this level of guarantee,
[00:52:25] I can make them available for you
next month and at this price.
[00:52:29] And so if utilities also offered more
segments of power delivery promises,
[00:52:36] then I think everybody will
figure out what to do with it.
[00:52:39] Yeah, but there's just way too much waste in
the grid right now. We should go after it.
[00:52:44] - Uh, you've highly lauded Elon and xAI's
[00:52:47] accomplishment in Memphis, in
building Colossus supercomputer,
[00:52:53] probably in record time in just
four months. It's now at 200,000
[00:52:57] GPUs and growing very quickly. Is
there something that you could speak
[00:53:01] to the understand about his approach
that's instructive to, broadly
[00:53:05] to all the data center creators that's
[00:53:08] that enabled that kind of accomplishment? His
approach to engineering, his approach to the
[00:53:12] whole management of
construction, everything?
[00:53:15] - First of all, Elon is deep in
so many different topics. Um,
[00:53:20] Yet he's also a really
good systems thinker.
[00:53:24] And so he's able to think through
multiple disciplines, and,
[00:53:29] and he obviously pushes things,
[00:53:34] questions everything, where they're,
number one, is it necessary?
[00:53:39] Number two, does it have to be done this way?
And then numbers, you know, does it have,
[00:53:43] does it have to take this long? And,
and so, so he, he has, he has the a- he
[00:53:49] has the ability to question everything,
[00:53:53] To the point where everything
is down to its minimal amount
[00:53:57] that's necessary, you can't take
anything else out. And yet the,
[00:54:04] the necessary capabilities
of the product remains, you
[00:54:08] know? And so he's, he is as minimalist
as you could possibly imagine,
[00:54:12] and he does it at a system scale. I
think... I also love the fact that he is
[00:54:19] he is represented. He is
present at the point of action.
[00:54:25] You know, he'll just go there. If
there's a problem, he'll just go there
[00:54:29] and then, "Show me the problem." You know,
when you do all of this in combination,
[00:54:34] you overcome a lot of previous,
"This is just the way we do it."
[00:54:38] "Um, you know, I'm waiting for them.
[00:54:42] Uh," You know, I mean, it's just,
everybody has a lot of excuses. And
[00:54:46] so, and then the last thing is
when you act personally with
[00:54:50] so much urgency it causes everybody
else to act with urgency,
[00:54:54] you know? And every supplier has a lot
of customers going on. Every supplier
[00:54:58] has a lot of projects going on,
[00:55:00] and he made it his... He makes
it his business that he's
[00:55:04] the top priority of everybody else's, you
know, projects. And so he does that by
[00:55:08] demonstrating it.
[00:55:09] - Yeah, I've been in a bunch of those meetings. It's
just, it's fun to watch, 'cause really, not enough
[00:55:13] people ask the question like, "Okay, so,
can this be done a lot faster, and how?
[00:55:20] Why does it have to take this long?"
[00:55:21] - Yeah, right.
[00:55:22] - And then in the... That becomes an engineering
question often. And yes, I think when
[00:55:26] you get the ground truth
of actually... I remember,
[00:55:29] one of the times I was hanging out with
him, he literally is going through the
[00:55:33] entire process of how to plug
in cables into a rack. He's,
[00:55:37] he's working with an engineer on the
ground that's doing that task, and he's
[00:55:41] just trying to understand what does that
process look like so it can be less
[00:55:44] error-prone. And just building up that
intuition from every single task involved in,
[00:55:50] putting together a data center— ...you
start to immediately get a sense at the
[00:55:56] detailed scale and at the
broad systems scale of
[00:56:00] where the inefficiencies are, and so you can
make it more and more and more efficient.
[00:56:04] Plus you have the big hammer of being able
to say, "Let's do it totally different-"
[00:56:08] - Yeah. That's right.
[00:56:09] - "... and remove all possible blockers."
[00:56:10] - That's right.
[00:56:11] - Is there parallels in the NVIDIA Extreme
Systems co-design approach that you
[00:56:15] see in the way Elon approaches
systems engineering?
[00:56:18] - Well, first of all, co-design is an
ultimate systems engineering problem.
[00:56:22] And so we approach, we approach the work
that we do from that first, from that
[00:56:26] The other thing that we do and this
is, this is a philosophy, a thought,
[00:56:35] a state of mind, I guess, a method,
[00:56:39] That I started 30 years
ago, and it's called the
[00:56:43] speed of light. The speed of light is not just
about the speed. The speed of light is, is
[00:56:46] my shorthand for what's what's the
[00:56:51] limit of what physics can do.
And so every single, everything,
[00:56:55] everything that we do is compared against
the speed of light. Memory speed,
[00:56:59] Math speed, power, cost, time,
effort, number of people,
[00:57:06] manufacturing cycle time. And when you
think about latency versus throughput,
[00:57:12] When you think about cost
versus throughput, cost
[00:57:16] versus capacity, all of these things,
You test against the speed of light to
[00:57:23] achieve all of these different constraints
separately. And then when you consider it
[00:57:30] together, you know you have
to make compromises because a
[00:57:34] system that achieves extremely low
latency versus a cheap, a system that
[00:57:37] achieves very high throughput are
architected fundamentally differently.
[00:57:42] But you want to know what's the
speed of light of a system that
[00:57:45] achieves high throughput, what's
the speed of light of a system that
[00:57:50] achieves low latency?
[00:57:52] And then when you think about the total
system, you can make trade-offs. And so
[00:57:56] I force everybody to think about what's
the, what the first- the first principles,
[00:58:00] the limits- ... the physical limits,
For everything before we, you know,
[00:58:06] before we do anything.
And we test everything
[00:58:10] against that. And so that's
a good frame of mind.
[00:58:13] I don't love the other methods,
which is continuous improvement.
[00:58:19] The problem with continuous
improvement, it...
[00:58:23] First of all, you should engineer something
from first principles at the speed,
[00:58:27] you know, with speed of light thinking.
Limit it only by physical limits,
[00:58:32] and physics limits. And after that, of
course you would improve it over time. Um,
[00:58:40] but I don't like going into a problem and
somebody says, "Hey, you know, it takes 74 days
[00:58:44] to do this today-" "... Right now.
And we can do it for you in 72 days."
[00:58:50] You know, I'd rather strip
it all back to zero-
[00:58:52] ... and say, "First of all, explain
to me why 74 days in the first place.
[00:58:56] And let's note, let's think about
what's possible today. And if I were
[00:59:00] to build it completely from scratch,
you know, how long would it take?"
[00:59:04] Oftentimes, you'd be surprised.
It might come to six days.
[00:59:08] Now, the rest of the six
days, the 74, could be
[00:59:12] very well-reasoned and
compromises, and, you know, cost
[00:59:16] reductions, and all kinds of different
things. But at least you know what they are.
[00:59:20] And then now that you know
that six days is possible,
[00:59:24] then the conversation from 74 to six,
surprisingly much more effective.
[00:59:30] - In such incredibly complex systems that
you're working with, is simplicity sometimes
[00:59:34] a good heuristic to reach
for? I mean, if I can just...
[00:59:40] I mean, the pod, the Vera Rubin pod
that you announced is just incredible.
[00:59:44] We're talking about seven chips,
seven chip types, five purpose-built
[00:59:48] rack types, 40 racks, 1.2 quadrillion
transistors, nearly 20,000 NVIDIA dies,
[00:59:56] over 1,100 Rubin GPUs, 60 exaflops, 10
petabytes per second of scale bandwidth.
[01:00:01] That's all just one...
[01:00:03] - That's just one pod.
[01:00:04] - That's just one pod.
[01:00:06] - Yeah, that's just one pod.
[01:00:07] - I mean, in- ... so you have the...
And then even the NVL 72 rack
[01:00:11] alone is 1.3 million components,
[01:00:15] 1300 chips, 4,000 pods crammed
into a single 19-inch wide rack.
[01:00:19] - And Lex, we're probably gonna have to
crank out about 200 of these pods a week,
[01:00:24] just to put it in perspective.
[01:00:25] - The amount of different components,
I suppose simplicity is impossible,
[01:00:30] but is that a metric that you kind of
reach for in trying to design things?
[01:00:35] - You know, the phrase, the phrase
that I use most often is, we-
[01:00:39] we need things to be as complex as
necessary, but as simple as possible.
[01:00:43] And so the question is, is
all that complexity there
[01:00:47] necessary? And we ought to test for that.
[01:00:50] And we got to challenge that. And then
after that, everything else above it,
[01:00:54] you know, is gratuitous.
[01:00:56] - But it's still almost incredible. Semiconductor
industry broadly, but what NVIDIA is
[01:01:00] doing,
[01:01:03] some of the greatest engineering in
history. So these systems are just truly,
[01:01:08] truly marvels of engineering.
[01:01:10] - It is the most complex computer
the world has ever made.
[01:01:13] - Yeah, the engineering teams, I mean-
[01:01:14] ... I don't, it's not a competition, but I
don't know. If it was like an Olympics of
[01:01:18] engineering teams, I mean, TSMC does
incredible engineering. Like I said,
[01:01:22] ASML at every scale, but NVIDIA is
gonna give them a run for their money.
[01:01:27] Just incredible, incredible teams.
[01:01:28] - Well, it's gold medalists in every
single, in every single sport, all
[01:01:32] assembled right here.
[01:01:33] - And have to work together.
[01:01:35] And report directly to you. This is
wonderful. You recently traveled to China.
[01:01:41] so it's interesting to ask
you China's been incredibly
[01:01:45] successful in building up its
technology sector. What do you
[01:01:49] understand about how
China's able to, over the
[01:01:53] past 10 years, build so many
incredible world-class companies,
[01:01:57] world-class engineering teams, and
just this technology ecosystem-
[01:02:01] ... that produces so many
incredible products?
[01:02:05] - A whole bunch of reasons for, well, first
of all, let's start with some facts.
[01:02:09] 50% of the world's AI researchers
are Chinese, plus or minus, and
[01:02:16] they're mostly in China
[01:02:18] still. We have many of them here, but
there's amazing researchers still in China.
[01:02:23] They, their tech industry showed
up at precisely the right time.
[01:02:30] At the time of the mobile
cloud era their way of
[01:02:33] contributing was software, and so this
is a country's incredible science
[01:02:37] and math. Really well-educated kids.
[01:02:42] Their tech industry was created
during the era of software.
[01:02:48] They're very comfortable
with modern software.
[01:02:52] China is not one giant economic country.
[01:02:56] It's got many provinces
and cities with mayors all
[01:02:59] competing with each other. That's
the reason why there's so many EV
[01:03:03] companies. That's the reason why there's so many
AI companies. That's the reason why there's so
[01:03:07] many, every company you could imagine,
they all create some of them. And as
[01:03:15] a result, they have insane
competition internally.
[01:03:19] And, you know, what remains
is an incredible company.
[01:03:24] They also have a social culture where
it's family first, friends second, and
[01:03:32] company third. And so, the amount
of conversation that goes back and
[01:03:42] forth between... They're essentially
open source all the time.
[01:03:47] So the fact that they contribute
more to open source is so sensible
[01:03:51] because they're probably, "What are we
protecting?" You know, my engineers,
[01:03:55] their brothers are in that company, their
friends are in that company, and they're all
[01:03:59] schoolmates. You know, the schoolmate
concept. There's a, you know, one
[01:04:03] schoolmate, you're brother
for life. And so they,
[01:04:08] they share knowledge very, very quickly.
[01:04:12] And so there's no sense keeping technology
hidden. You might as well put it on
[01:04:16] open source. And so the open
source community then amplifies,
[01:04:20] accelerates the innovation process. So you
get this rapid, incredible great talent,
[01:04:26] rapid innovation because of open source
and just, you know, the nature of friends,
[01:04:32] and insane competition. Among comp-
[01:04:36] among the company, what emerges
is incredible stuff. And so
[01:04:41] this is the fastest innovating
[01:04:44] country in the world today, and this is something
that has everything that, everything that I've just
[01:04:48] said is fundamental to just
how the kids were grown,
[01:04:52] the fact that they have excellent
education, the fact that they, parents
[01:04:56] want them to do well in school, the
fact that they, their culture is that
[01:04:59] way. These are, you know, these are
just the thing about their country,
[01:05:04] and they showed up at precisely the time
when technology is going through that
[01:05:07] exponential.
[01:05:09] - Plus culturally, it's pretty
cool to be an engineer.
[01:05:12] It connects to all the components
that you're mentioning...
[01:05:16] - It's a builder nation.
[01:05:18] - It's a builder nation.
[01:05:19] - Yeah, it's a builder nation.
Our country's leaders,
[01:05:22] incredible, but they're mostly
lawyers. Their country's
[01:05:25] leaders, and because we're, they're trying
to keep us safe, rule of law, governing,
[01:05:31] their country was built
out of poverty. And so
[01:05:37] most of their leaders are incredible
engineers. Some of the brightest minds.
[01:05:43] - To take a small tangent, because you
mentioned open source, I have to
[01:05:47] go to Perplexity here, who you
have been a fan of a long time.
[01:05:51] - Love it, yeah.
[01:05:52] - And thank you for releasing
open source Nemotron 3 Super,
[01:05:56] which you can also use inside
Perplexity to look stuff up.
[01:05:59] Now, which is 120 billion
parameter open weight MoE model.
[01:06:05] What's your vision with open
source? So you mentioned China with
[01:06:12] DeepSeek and MiniMax, with
all these companies really
[01:06:16] pushing forward the open source AI
movement, and NVIDIA is really leading the
[01:06:21] way in close to state-of-the-art open
source LLMs. What's your vision there?
[01:06:28] - First, if we're gonna be a great AI computing
company, we have to understand how AI
[01:06:35] models are evolving. One of the things that
I love about Nemotron 3 is it's not a,
[01:06:40] just a pure transformer model, it's
transformer and SSMs. And we were early in,
[01:06:48] Developing the conditional GANs, which,
[01:06:52] that progressive GANs, which led
step-by-step to diffusion. And so,
[01:06:56] The fact that we're doing basic research
[01:06:59] in model architecture
and in different domains
[01:07:03] gives us visibility into, you
know, what kind of computing
[01:07:07] systems would do a good job for
future models. And so it is part
[01:07:11] of our extreme co-design strategy. Second,
um, I think we rightfully recognize
[01:07:19] that on the one hand, we want world-class
[01:07:23] models as products, and
they should be proprietary.
[01:07:27] On the other hand, we also want AI to diffuse
into every industry and every country,
[01:07:34] every researcher, every student.
[01:07:37] And if everything is proprietary,
it's hard to do research
[01:07:41] and it's hard to innovate
on top of, around, with.
[01:07:46] And so...Open source is fundamentally
necessary for many industries to join the AI
[01:07:52] revolution. NVIDIA has the
scale and we have the motives
[01:07:58] to not only skills, scale, and
motivation to build and continue to
[01:08:05] build these AI models for
as long as we shall live.
[01:08:10] And so therefore, we ought to
do that. We can open up, we can
[01:08:12] activate every industry, every researcher,
[01:08:17] you know, every country to be
able to join the AI revolution.
[01:08:21] There's the third reason,
which is from that, to
[01:08:25] recognizing that AI is not just language.
These AIs will likely use tools and
[01:08:33] models and sub-agents that were
[01:08:36] trained on other modalities
of information. Maybe it's
[01:08:40] biology or chemistry or you know,
[01:08:43] laws of physics, or you know,
fluids and thermodynamics, and not
[01:08:48] all of it is in language structure.
[01:08:50] And so somebody has to go make
sure that weather prediction,
[01:08:55] biology, AI, AI for biology, physical AI,
all of that stuff stays, can be pushed
[01:09:03] to the limits and pushed to the frontier.
We don't build cars, but we wanna make sure
[01:09:07] every car company has access
to great models. We don't,
[01:09:11] discover drugs, but I wanna make
sure that Lilly has the world's best
[01:09:15] biology AI systems, so that they can
go use it for discovering drugs.
[01:09:19] And so these three
fundamental reasons, both in,
[01:09:23] recognizing that AI is not just
language, that AI is really broad,
[01:09:27] that we wanna engage everybody into the
world of AI, and then also co-design of AI.
[01:09:32] - Well, I have to say, once again,
thank you for open sourcing,
[01:09:36] really truly open sourcing
Nemotron 3 and ...
[01:09:39] - Yeah, I appreciate you were saying that. We open sourced
the models, we open sourced the weights, we open
[01:09:43] sourced the data, we open sourced how we
created it. Yeah, it's pretty amazing.
[01:09:48] - Uh, it's really, it's really incredible.
[01:09:51] You're originally from Taiwan and
have a close relationship with TSMC.
[01:09:56] So I have to ask, TSMC I think
[01:10:00] also is a legendary company in terms of
the engineering teams, in terms of the
[01:10:03] incredible engineering
work that they do. What
[01:10:07] what do you understand about TSMC
culture and their approach that
[01:10:10] explains how they're able
to achieve this singular
[01:10:14] unmatched success in everything
they're doing with semiconductors?
[01:10:19] - You know, first of all, the deepest
misunderstanding about TSMC is that
[01:10:29] their technology is all they have.
That somehow they have a really great
[01:10:36] transistor, and if somebody shows
up another transistor, game over.
[01:10:41] It's the technology
[01:10:43] and of course, you know, I don't mean
just the transistor, the metallization
[01:10:47] systems, the packaging, the 3D
packaging, the silicon photonics,
[01:10:51] the, you know, all of the technology that
they have. That technology is really what
[01:10:55] makes the company special. Their
technology makes the company special.
[01:10:59] But their ability to orchestrate
[01:11:04] the demands, the dynamic demands of
hundreds of companies in the world as
[01:11:11] they're moving up, shifting out,
[01:11:14] you know, increasing, decreasing,
push, pushing out, pulling
[01:11:17] in changing from customer to customer,
Wafer starting, wafer stopping,
[01:11:26] Emergency wafer starts,
you know, all of this
[01:11:30] dynamics of the world's
complexity as the world is
[01:11:34] shape-shifting all the
time, and somehow they're
[01:11:38] running a factory with high
throughput, high yields,
[01:11:42] really great costs,
excellent customer service.
[01:11:46] They take their work, they take their
promises seriously. They, when your
[01:11:50] wafer, because they know that they're helping
you run your company, when the wafers,
[01:11:54] when the wafers were promised to show up, the
wafers show up, you know, so that you could
[01:11:58] run your company appropriately.
And so their system, their
[01:12:02] manufacturing system is completely
miraculous, I would say. Then
[01:12:06] the second thing is their culture.
This culture is simultaneously,
[01:12:10] Technology focused on one
hand, advancing technology,
[01:12:14] simultaneously customer service
oriented on the other hand. A lot of
[01:12:19] companies are very customer service
oriented, but they're not very
[01:12:23] technology excellent. They're not
at the bleeding edge of technology.
[01:12:27] There are a lot of companies who are tech, at the bleeding
edge of technology, but they're not the best customer
[01:12:31] service oriented company. And so it
just depends on somehow they've,
[01:12:34] they've balanced these two and
they're world-class at both.
[01:12:39] And then probably the third thing
is the technology that I most
[01:12:43] value in them that they
created this, you know, this,
[01:12:48] Intangible called trust. I trust them to
put my company on top of them. That's a
[01:12:54] very big deal.
[01:12:55] - When they trust, I mean, there's a really close
relationship there that you've established, and that trust
[01:12:59] is established based on many years
of performance, but there's human
[01:13:03] relationships involved there as well.
[01:13:05] - Three decades, I don't know how many
tens, hundreds of billions of dollars
[01:13:09] of business we've done through
them, and we don't have a contract.
[01:13:14] That's pretty great.
[01:13:15] - Amazing. Okay, there's this story
[01:13:18] ... ... That in 2013, the
founders of TSMC, Morris Chang
[01:13:22] offered you the chance to
become TSMC's chief executive,
[01:13:26] And you said you already had
a job. Is this story true?
[01:13:30] - Story is true. I didn't dismiss it. Um but
I was deeply honored and, and of course,
[01:13:38] of course uh, I knew then as I
know now, TSMC is one of the
[01:13:42] most consequential companies in history.
[01:13:45] And, and Morris is one of the
highest regarded executive and,
[01:13:50] and business and personal friend
that I've had in my life.
[01:13:55] And, um ...Uh, for him to ask is, uh um,
I was humbled and, and really honored.
[01:14:05] But, but the work that I'm doing here
is really important, and I've seen,
[01:14:09] you know, in my mind's eye, what NVIDIA
[01:14:13] was going to be and what the
impact that we could have.
[01:14:17] And uh, it was really important work.
[01:14:20] And it's my responsibility, you know,
my sole responsibility to make this
[01:14:24] happen. And so I uh, I
declined it, You know,
[01:14:31] not, not because it wasn't
an incredible offer.
[01:14:34] It's an unbelievable offer but,
but I simply couldn't take it.
[01:14:38] - I think NVIDIA, both
NVIDIA and TSMC are two
[01:14:42] of the greatest companies in the history
of human civilization. And running either
[01:14:46] one, I'm sure, is incredibly
complicated effort and takes...
[01:14:50] You have to truly be all in.
[01:14:52] Uh, everybody at every scale, not just
at the CEO level. Everybody is really
[01:14:56] truly all in-
[01:14:57] - Yeah. Yeah, no doubt
[01:14:59] - ... To, to accomplish
this kind of complexity.
[01:15:00] - So now I can help both companies.
[01:15:02] - Exactly. So NVIDIA is now the most
valuable company in the world.
[01:15:08] I have to ask, what is the
NVIDIA's biggest moat,
[01:15:13] as the folks in the tech sector say?
[01:15:15] The edge you have that protects
you from the competition.
[01:15:20] - Our single most important
property as a company
[01:15:27] is the install base of
our computing platform.
[01:15:31] Our single most important thing
today is our, is the install
[01:15:36] base of CUDA. Now, the reason why,
[01:15:39] uh, 20 years ago, of course,
there was no install base.
[01:15:46] But what makes... And if
somebody came up with a
[01:15:50] GUDA or TUDA it wouldn't
make any difference at
[01:15:53] all. And the reason for
that is because it's
[01:15:57] never been just about the technology.
The technology, of course, was
[01:16:01] incredible visionary. But it's the fact
that the company was dedicated to it,
[01:16:07] stuck with it, expanded its reach. Um,
[01:16:11] it wasn't three people that
made CUDA successful. It was
[01:16:14] 43,000 people that made CUDA
successful. And the several
[01:16:18] million developers that believed in us,
[01:16:21] That trusted that we were going to
continue to make CUDA 1, 2, 3, 13,
[01:16:27] that they decided to port and dedicate
their software on top of it, their
[01:16:31] mountain of software on top of
it. And so the install base
[01:16:34] is the number one most
important advantage.
[01:16:38] That install base, when you amplify
it with the velocity of our
[01:16:42] execution at the scale that
we're talking about, no
[01:16:45] company in history had
ever built systems of this
[01:16:49] complexity, period. And then to
build it once a year is impossible.
[01:16:56] And that velocity combined
with the install base,
[01:17:02] in the developer's mind, you just
go now, take the developer's mind.
[01:17:06] From the developer's
perspective, if I support CUDA,
[01:17:11] tomorrow it'll be 10 times better. I
just have to wait six months on average.
[01:17:16] Not only that, if I develop it on CUDA,
I reach a few hundred million people,
[01:17:22] computers. I'm in every cloud, I'm in every
computer company, I'm in every single
[01:17:27] industry, I'm in every single country.
[01:17:31] So if I create an open source
package and I put it on CUDA first,
[01:17:36] I get these both attributes
simultaneously. And not only that,
[01:17:43] I trust 100% that NVIDIA is going to
keep CUDA around and maintain it and
[01:17:50] improve it and keep optimizing the
libraries for as long as they shall live.
[01:17:57] You could take that to the bank,
and that last part, trust.
[01:18:00] You put all that stuff together,
if I were a developer today,
[01:18:04] I would target CUDA first.
I would target CUDA most.
[01:18:09] And that's the reason that I
think in the final analysis is
[01:18:13] our first, that's even our first-
[01:18:16] - core advantage. Our second
one is our ecosystem.
[01:18:21] The fact that we vertically integrated
this incredibly complex system,
[01:18:25] but we integrate it horizontally into
every single company's computers.
[01:18:30] - We're into Google Cloud, we're into Amazon,
we're in Azure. You know, we're ramping up
[01:18:34] AWS like crazy right now.
We're in new companies like
[01:18:38] CoreWeave and Nscale. We're
in supercomputers at Lilly.
[01:18:43] We're in enterprise computers.
We're at the edge in radio base
[01:18:46] stations. You know, I mean, it's
just crazy. One architecture is in
[01:18:50] all these different systems. We're in cars, we're
in robots, we're in satellites, we're out in
[01:18:54] space. And so the fact that you
have this one architecture and the
[01:18:58] ecosystem is so broad, it basically covers
every single industry in the world.
[01:19:03] - Well, how does the, how
does the CUDA install
[01:19:06] base evolve into the future
with AI factories as a
[01:19:10] moat? What do you... Do you think it's possible
that NVIDIA of the future is all about
[01:19:14] the AI factory?
[01:19:16] - Well, the unit of computing
used to be GPU to us.
[01:19:20] Then it became a computer,
then it became a cluster. Now
[01:19:24] it's an entire AI factory. When I see
a computer, when I see what NVIDIA
[01:19:28] builds, in the old days, I would,
you know, I visualize the chip.
[01:19:32] And then when I announced the new
product, new generation, like,
[01:19:36] "Ladies and gentlemen, we're announcing
Ampere today," I'd pick up the chip.
[01:19:40] That was my mental model-
[01:19:41] ... of what I was building.
Today, I wouldn't... Picking up
[01:19:45] the chip is kind of still adorable.
But it's adorable. It's not my mental
[01:19:51] model of what I'm doing. My mental
model is this giant gigawatt
[01:19:56] thing that has power generations
connected to the grid. It's got cooling
[01:20:01] systems and networking of
incredible monstrosity, you
[01:20:05] know. 10,000 people are in
there trying to install it,
[01:20:09] hundreds of networking engineers in there,
thousands of engineers behind it trying
[01:20:12] to power it up.
[01:20:14] You know, powering up one of those factories,
as you know, it's not somebody going,
[01:20:18] "It's on now." It takes thousands
of people to bring it up.
[01:20:22] - So mentally, you're actually... When you're thinking
about a single unit of compute, you're like
[01:20:27] literally, when you go to bed at night, you're
thinking now about collection of racks,
[01:20:31] so pods, not individual chips.
[01:20:33] - Entire infrastructure. And I'm hoping my next
click is when I'm thinking about building
[01:20:37] computers, it's, you know, planetary
scale. That'll be the next click.
[01:20:42] - Well, what do you think about
the space angle that Elon has
[01:20:45] talked about, doing compute
in space for solving some
[01:20:49] of the... It makes some of the energy
issues in terms of scaling energy easier.
[01:20:56] - Cooling issues is not easy. Yeah.
[01:20:58] - Cooling. Well, there's a large number of
engineering complexities involved with
[01:21:02] that. So, so what... You know, NVIDIA
has also announced that you're
[01:21:07] already thinking about that.
[01:21:09] - Yeah, we're already there. NVIDIA
GPUs are the first GPUs in space.
[01:21:14] And I didn't realize it,
it was so interesting
[01:21:18] to... I would have declared it maybe.
[01:21:20] We're in space. You know, little, little
astronaut suit on one of our GPUs.
[01:21:27] But we've been in space. It's the
right place to do a lot of imaging.
[01:21:32] You know, because those satellites have,
have really high resolution imaging systems,
[01:21:36] and they're sweeping the Earth,
you know, continuously now. And,
[01:21:40] um, you want, you know,
centimeter scale, imaging
[01:21:43] imaging that is done continuously
for the world, so that,
[01:21:47] you know, you'll basically
have real time telemetry of
[01:21:50] everything. You don't wanna beam that
back down to earth. It's just, you know,
[01:21:57] petabytes and petabytes of data. You
gotta just do AI right there at the edge,
[01:22:01] throw away everything you don't need, you've
seen before, didn't change, and then just
[01:22:05] keep the stuff that, that you need.
And so AI had to be done at the edge.
[01:22:09] Obviously we have, we have a 24/7 solar,
if we put it at the polars. And uh,
[01:22:19] but, you know, there's no
conduction, no convection.
[01:22:23] And so, you know, you're
pretty much just radiation.
[01:22:26] And uh, but, you know, space is big. I
guess, you know, we're just gonna put
[01:22:30] big, giant radiators out there.
[01:22:32] - How crazy of an idea do you think it is?
Like is this, is this five years out, 10
[01:22:36] years out, 20 years out? So we're
talking about blockers for AI scaling.
[01:22:41] - You know, I'm just so much more
practical. I look for where, where, um
[01:22:46] my next, next bucket of
opportunities are first.
[01:22:51] Meanwhile, I'm cultivating
space. And so I send
[01:22:55] engineers to go work on the
problem. We're starting to... We're
[01:22:58] learning a lot about it. How do we deal
with radiation? How do we deal with
[01:23:03] degrading performance? How do
we deal with a continuous,
[01:23:07] Testing and attestation
of, of de- defects?
[01:23:10] And you know, how do we deal
with redundancy? And how do we
[01:23:14] degrade gracefully and things like
that? And so we could, we could do a...
[01:23:18] What about software? How do you think
about software and redundancy and
[01:23:23] performance out in space?
Make it so that the computer
[01:23:27] never breaks, it just
gets slower, you know.
[01:23:31] And I... So we could start
doing a lot of engineer
[01:23:34] exploration upfront. But in the
meantime, my, my favorite answer
[01:23:38] is ge- eliminate waste.
[01:23:41] You know, we've got all that idle power, I
want to evacuate it as fast as possible.
[01:23:47] - Yeah. There's a lot of
low-hanging fruit here on Earth-
[01:23:50] ... That we can utilize for
the AI scaling. Quick pause.
[01:23:56] Quick 30-second thank you to our sponsors.
Check them out in the description.
[01:24:00] It really is the best way to support this
podcast. Go to lexfridman.com/sponsors.
[01:24:06] We got Perplexity for curiosity-driven
knowledge exploration,
[01:24:10] Shopify for selling stuff
online, LMNT for electrolytes,
[01:24:15] Fin for customer service
AI agents, and Quo
[01:24:19] for a phone system, like calls,
texts, contacts, for your business.
[01:24:23] Choose wisely, my friends. And now, back
to my conversation with Jensen Huang.
[01:24:30] Do you think NVIDIA may be worth
10 trillion at some point?
[01:24:36] Let's ask it this way.
What does the future
[01:24:40] of the world look like where that's true?
[01:24:45] - I think that NVIDIA's growth is Extremely
likely, and in my mind, inevitable. And
[01:24:55] let me explain why. We're the
largest computer company in history.
[01:25:00] That alone should beg the question, why?
[01:25:04] And the reason of course... Two reasons.
First, two foundational technical reasons.
[01:25:10] The first reason is that computing went
from being a retrieval-based, file
[01:25:14] retrieval system. Almost everything is
a file... We pre-write something, we
[01:25:21] pre-record something. You know, we draw
something, we put it on the web, we put it
[01:25:24] in a file. And we use a
recommender system, some smart
[01:25:28] filter, to figure out what to
retrieve for you. And so we were a
[01:25:32] pre-recording, human
pre-recording, and file retrieving
[01:25:35] system. That's what a
computer is, largely.
[01:25:39] To now, AI computers
are contextually aware,
[01:25:43] which means that it has to process
and generate tokens in real time.
[01:25:47] So we went from a retrieval-based
computing system to a generative-based
[01:25:51] computing system.
[01:25:53] We're gonna need a lot more processing
in this new world than in the old
[01:25:57] world. We need a lot of storage
in the old world. We need a lot
[01:26:01] of computation in this new world. And so,
[01:26:06] so that's the first part of it. We
fundamentally changed computing and the way
[01:26:10] how computing is done. The only
thing that would cause it to go
[01:26:14] back...... is if this way of computation,
[01:26:18] this way of computing generating
information that's contextually relevant,
[01:26:22] situationally aware, that is
grounded on new insight before it
[01:26:27] generates information, this
computation-intensive way of doing computing
[01:26:33] would only go back if it's not effective.
[01:26:36] So if... For the last 10, 15 years
while working on deep learning,
[01:26:40] if at any single moment
[01:26:43] I would have come to the conclusion
that, "You know what? This is
[01:26:47] not gonna work out.
[01:26:49] I think this is a dead end." Or, "It's not gonna scale,
it's not gonna solve this modality, not gonna be
[01:26:53] used in this application." Then, of course,
I would feel very differently about it,
[01:26:57] but I think the last five years
has given me more confidence
[01:27:02] than the last ten year, previous
ten years. The second idea,
[01:27:07] is computers, because it was a storage
system, it was largely a warehouse.
[01:27:14] We're now building factories.
Warehouses don't make much money.
[01:27:20] Factories directly correlates with
the company's revenues. And so,
[01:27:28] the computer did two things. Not only
did it change the way it did it,
[01:27:33] its purpose in the world changed. It's
no longer a computer, it's a factory.
[01:27:39] It's a factory, it's used
for generation of revenues.
[01:27:45] We're now seeing not only
is this factory generating
[01:27:49] products, commodities that
people want to consume,
[01:27:53] we're seeing that the commodities are so
[01:27:55] interesting, so valuable, so,
to so many different audiences
[01:28:00] that the tokens are starting to
segment, like iPhones. Mm-hmm.
[01:28:04] You have free tokens,
[01:28:06] you have premium tokens, and you
have several tokens in the middle.
[01:28:10] Yeah. And so intelligence,
as it turns out,
[01:28:13] you know, it's a scalable product.
There's extremely high intelligence
[01:28:17] products, tokens that you could... that
are used for specialized things, people be
[01:28:21] willing to pay. You know, the
idea that somebody's willing to
[01:28:24] pay $1000 per million tokens is just around
the corner. It's not if, it's only when.
[01:28:32] And so now we're seeing that the
[01:28:35] commodity that this factory makes is
actually valuable, and is revenue
[01:28:39] generating and profit generating.
How, now the question is how
[01:28:43] many of these factories
can, does the world need?
[01:28:48] How much, how many tokens
does the world need? And
[01:28:54] how much is society willing
to pay for these tokens? And
[01:29:00] what would happen to the world's economy
[01:29:02] if the productivity were to
improve so substantially?
[01:29:07] What would happen... Are we, are we
gonna discover new drugs, new products,
[01:29:11] new services? And so when you take these
things in combination, I am absolutely
[01:29:16] certain that the world's GDP is
going to accelerate in growth.
[01:29:22] I'm absolutely certain the percentage of
that GDP that will be used for computation
[01:29:30] will be 100 times more than
the past... because it's no
[01:29:34] longer a storage unit. It's
a product generation unit.
[01:29:39] And so when you look at it in that context
[01:29:42] and then you back into what
is NVIDIA's, what does NVIDIA
[01:29:46] does NVIDIA do and how much of that
[01:29:50] new economics, new industry
would we have to benefit
[01:29:54] to address, I think we're
gonna be a lot, lot bigger.
[01:29:58] And then the rest of it, to me, is is it
[01:30:02] possible for NVIDIA to be
a, you know, $3 trillion
[01:30:06] revenues company in the near future?
The answer is of course yes. And the
[01:30:10] reason for that is because it's not
limited by any physical limits.
[01:30:15] There's nothing that I see
that says, you know, gosh,
[01:30:19] $3 trillion is not possible. And
[01:30:23] as it turns out, NVIDIA's supply chain is,
the burden is shared by 200 companies.
[01:30:31] And the fact that we scale out on the backs
with the partnership of this ecosystem,
[01:30:38] the question is do we
have the energy to do so?
[01:30:41] And surely we will have the energy to do
so. And so all of these things combined,
[01:30:49] that number is just a number, you
know? And I still remember, NVIDIA
[01:30:53] was a, NVIDIA was a, the first
time we crossed a billion dollars,
[01:30:58] I was reminded of a CEO who told me,
"You know, Jensen, it's theoretically
[01:31:02] impossible for a fabless semiconductor
company to exceed a billion dollars."
[01:31:07] And I won't bore you
with why, but the end,
[01:31:11] of course it's illogical and there's a
lot of evidence we're not. And then,
[01:31:15] somebody told me, "You know, Jensen,
you'll never be more than $25 billion
[01:31:21] because of some other company." Somebody
told me that, "You'll never be, you know,
[01:31:24] because..." And so the, those
aren't first principled thinking.
[01:31:32] And the simple way to think about
that is what is it that we make
[01:31:38] and how large is the
opportunity that we can create?
[01:31:42] Now, NVIDIA is not in the market share
business. Almost everything that I just talked
[01:31:46] about don't exist. That's
the part that's hard.
[01:31:51] You know, if NVIDIA was a $10 billion
[01:31:55] company trying to take market
share, then it's easy to see
[01:31:59] for shareholders that, oh,
yeah, if they could just
[01:32:02] take 10% share, they could be this much
[01:32:05] larger. But it's hard for
people to imagine how
[01:32:09] large we could be because there's
nobody I could take share from.
[01:32:12] You know? And so I think
that that's one of the
[01:32:16] challenges.... for the world
is, is the imagination of the
[01:32:20] future. But I got plenty of time, and I'll
keep reasoning about it, and I'll keep talking
[01:32:24] about it, and every single GTC
will become more and more real.
[01:32:27] You know, and then more and more people will
talk about it, and one of these days, you
[01:32:31] know, we'll get there. But
I'm 100% we'll get there.
[01:32:34] - Yeah, this view of you know, token
factories essentially, this token per
[01:32:39] second per watt, and every
token having value. Like
[01:32:43] it's an actual thing that brings value,
and it brings different kinds of value,
[01:32:47] different amounts of value to different people
with value. That's the actual product, is really
[01:32:51] could be loosely thought of as the token.
And so you have a bunch of token factories.
[01:32:54] And then it's very easy, first principles,
to imagine a future, given all
[01:32:58] the potential things that AI can
solve, that you're going to need an
[01:33:01] exponential number more
of token factories.
[01:33:06] - And what's really interesting, the reason
why I was so excited about it, the
[01:33:10] iPhone of tokens arrived.
[01:33:11] - What do you call it? Wait, are you saying
OpenClaw's iPhone? That's interesting.
[01:33:15] - Agents.
[01:33:16] - Yeah, agents. True.
[01:33:18] - Agents in general.
[01:33:19] The iPhone of tokens arrived. It is
the fastest-growing application in
[01:33:23] history. It went straight
up. Went straight up.
[01:33:26] - That says something.
[01:33:27] - Yep, there's no question OpenClaw
is the iPhone of tokens.
[01:33:31] - Is there something truly, as you know,
[01:33:34] something truly special
happening from about December,
[01:33:38] where people have really woke up to the
power of Claude Code of Codex, of OpenClaw.
[01:33:44] Um, I mean, I'm embarrassed to admit that
on the way here in the airport, I've ...
[01:33:52] It's the first time I've done this in
public. I was programming, quote unquote,
[01:33:57] by talking to my laptop.
[01:33:59] And I was embarrassed because I was pretending
like I'm talking to a human colleague.
[01:34:04] Uh, I'm not sure how I feel about
the future where everybody-
[01:34:07] ... is walking around talking
to their AI, but it's such an
[01:34:11] efficient way to get stuff done.
[01:34:13] - And it's more likely that your AI
is bothering you all the time.
[01:34:18] And the reason for that is because
it's getting stuff done so fast.
[01:34:22] It's reporting back to
you, "I got that done."
[01:34:24] "You know, what do you want me to do next?"
You know, it... That's the part that I think-
[01:34:28] ... most people don't realize is they're
The person who's gonna be chatting with
[01:34:32] them, texting them most,
is their claws or lobster.
[01:34:37] - What an incredible future.
[01:34:39] Uh, I read that you attribute a lot of your
success to your ability to work harder than anyone
[01:34:43] and withstand more suffering than anyone.
[01:34:46] So we can list many of the things that
entails. I mean, dealing with failure,
[01:34:53] the cost and engineering problems
we've talked about. The human
[01:34:57] problems, uncertainty, responsibility,
exhaustion, embarrassment,
[01:35:01] the near-death company moments
that you've mentioned,
[01:35:04] But also the pressure.
Now, as the CEO of this
[01:35:10] company that economies and nations
strategize around plan their,
[01:35:18] Financial allocations
around, plan their AI
[01:35:21] infrastructure around, how do you
deal with this much pressure?
[01:35:26] What gives you strength, given how many
nations and peoples depend on you?
[01:35:38] - I'm conscious about the fact that,
[01:35:42] NVIDIA's success is very
important to United States.
[01:35:47] We generate enormous
amounts of tax revenues.
[01:35:51] We established technology leadership
for our nation. Technology
[01:35:54] leadership is important
for national security.
[01:35:57] National security not just in one aspect
of national security, all aspects
[01:36:01] of national security. When our
country's more prosperous,
[01:36:05] we could do a better job with domestic
policies and helping social benefits.
[01:36:11] Because we're generating so much
re-industrialization in the United States,
[01:36:15] we're creating mountains of jobs.
We're helping shift, how we,
[01:36:23] how we build things back to
the United States in so many
[01:36:27] different plants, chips,
computers, and of course, these AI
[01:36:31] factories. I'm completely aware
[01:36:34] that, that... And I have the
benefit, and this is a real
[01:36:40] a real gift with mainstream investors,
[01:36:45] teachers, policemen who have
somehow, for whatever reason,
[01:36:51] invested in NVIDIA or because
they watched Jim Cramer bought
[01:36:55] some stock and now are millionaires.
And I am completely aware of
[01:37:02] that circumstance. I'm aware of
the circumstance that NVIDIA,
[01:37:07] is central to a very large network of
[01:37:13] ecosystem partners behind
us and downstream from us.
[01:37:16] And so the way I deal with that is
exactly what I just did. I reason about
[01:37:23] what is... what is it that we're doing?
[01:37:26] What is it causing? What's the
impact that has on other people
[01:37:29] benefit, you know, positively or even,
[01:37:33] even through great burden,
for example, to supply chain?
[01:37:38] And the question is, therefore,
what are you gonna do about it?
[01:37:44] In almost everything that I feel, I
break it down, I reason about, "Okay,
[01:37:50] "what's the circumstance? What
has changed? What's hard?
[01:37:54] And what am I gonna do about it?" And I
break it down, decompose the problem,
[01:38:00] and the decomposition
of these circumstances
[01:38:07] turns it into manageable things that I
can do. And the only thing after that
[01:38:11] I could do is, "Did you do it?
Did you either do it or did you
[01:38:15] get somebody else to do it?
And if you didn't do it,
[01:38:18] you reasoned that you need to do it, and you didn't
do it, and you didn't get anybody else to do it,
[01:38:23] then stop crying about it." You
know? And so- ... so I'm fairly
[01:38:31] Tough on myself. And, but I
also break things down so that,
[01:38:35] so that I don't panic. I can go
[01:38:39] to sleep because I've made the list
of things that needed to be done, and
[01:38:43] I've made sure that everything that
could put our company in harm's way,
[01:38:47] could put my partners in harm's way, put
our industry in harm's way, I've told
[01:38:51] somebody. Everything that I feel
[01:38:57] could put anybody in harm's way,
I've told someone. And I've told
[01:39:00] that someone who could do something about
it. And so I've gotten it off my chest
[01:39:05] or I'm doing something about it. And so
after that, Lex, what else can you do?
[01:39:10] - So given all the insane,
intense amount of suffering
[01:39:15] on the journey of building up NVIDIA,
have you hit low points psychologically?
[01:39:22] - Oh, yeah. Oh, yeah. Sure.
All the time. All the time.
[01:39:27] - And there—
[01:39:27] - All the time.
[01:39:27] - ... you just break down
the problem into pieces?
[01:39:31] - Yeah. Yeah.
[01:39:31] - See what you could do about it?
[01:39:33] - And, and part of, and, you know, Lex,
part of it, part of it is forgetting.
[01:39:39] One of the most important attributes
of AI learning, as you know, is,
[01:39:43] right? Systematic forgetting. You,
you need to know when to forget
[01:39:47] some things. You can't memorize everything.
You can't keep everything and, and,
[01:39:51] you know, you, you want to— you don't want to
carry everything. One of the things that I do very
[01:39:54] quickly is decompose the problem,
I reason about the problem, and I
[01:39:58] share the load with it. When
I say I tell everybody,
[01:40:01] I'm essentially sharing that
burden. As quickly as possible.
[01:40:06] Whatever worries me, tell somebody
else. Don't just keep it. You know,
[01:40:10] don't freak them out. Decompose the
problem into smaller parts and get
[01:40:16] people to, so, and, and inspire them to
be able to go do something about it.
[01:40:20] But part of it is just, just
forgetting. You know, like,
[01:40:24] a lot of it is you gotta be tough on
yourself. You know, just come on, stop
[01:40:28] crying about it. Let's get going. You know?
And, and then you get out of bed. And then
[01:40:32] the other part is, is you,
you're attracted to the
[01:40:36] next shiny light, the next future,
you know, the next opportunity, the
[01:40:40] next, "Okay, that's behind
us. Let— what's next?"
[01:40:43] It's a lot, I think, you know, you
watch this with great athletes. They,
[01:40:47] they just worry about the next point.
[01:40:50] The last point is behind them. The
embarrassment, the, you know— the setback.
[01:40:56] You know, and, and then, and because
I do so much of my job publicly,
[01:41:01] you know? Lex, you do a fair amount of your
job publicly too. And so, so I do a lot of my
[01:41:05] job publicly. And so you
know, I say a lot of
[01:41:09] things that, that seem sensible
at the time or funny at the time,
[01:41:13] mostly it's just because it's funny to
me at the time. And then, you know, you
[01:41:17] reflect on it, it's
less funny, but, but...
[01:41:20] - Yeah. No, trust me, I know. But
you basically allow yourself to
[01:41:23] be pulled by the light of the future.
Forget the past and just keep-
[01:41:27] - That's right.
[01:41:28] - ... keep working towards that. I mean,
you did say, there's this kind of
[01:41:32] famous thing you said that if
you knew how hard it would be
[01:41:38] to build NVIDIA it turned
out to be, what is it? A
[01:41:42] million times more hard than you
anticipated that you wouldn't do it.
[01:41:46] - Yeah, right.
[01:41:47] - Um, but isn't... You
know, when I hear that,
[01:41:51] that's probably true about
everything worth doing, right?
[01:41:53] - Exactly. That is, by the way, what I
was trying to explain, is that there's
[01:41:59] a, there's a incredible superpower of
being, being have a, the mind of a child.
[01:42:07] You know? And I say to myself
oftentimes when I look at something,
[01:42:11] and almost, almost everything, My first
thought is, "How hard can it be?"
[01:42:19] You know? And so you get yourself
into that mode, how hard could
[01:42:23] it be? And, and nobody's ever done it. It
[01:42:27] looks gigantic. It's gonna cost
hundreds of billions of dollars.
[01:42:31] It's gonna take, you know, all this... And you
just go, "Yeah, but how hard could it be?"
[01:42:35] You know? How hard could it be?
[01:42:37] And so you gotta get yourself into
that state of mind. You don't
[01:42:41] wanna, you don't wanna
actually over simulate
[01:42:45] everything and all the setbacks and all
the trials and tribulations and all
[01:42:48] the disappointments. You don't wanna simulate
all that in advance. You don't wanna know that.
[01:42:53] You don't, you wanna go into a new
experience thinking it's gonna be perfect,
[01:42:56] it's gonna be great, it's gonna be
incredibly fun. And then while you're there,
[01:43:01] you know, you need to have,
[01:43:03] you need to have endurance, you need to
have grit, so that when the setbacks
[01:43:07] actually happened, and those
setbacks are gonna surprise you, the
[01:43:10] disappointments are gonna surprise
you, you know, the embarrassments are
[01:43:14] gonna surprise you, the humiliations
are gonna surprise you.
[01:43:17] You just can't let... Now you just gotta
turn on the other bit, which is just forget
[01:43:21] about it. Move on, keep moving.
And, and to the extent that,
[01:43:27] to the extent that my assumptions
[01:43:31] about the future and why the
future is gonna manifest,
[01:43:36] so long as those
assumptions and that input
[01:43:40] doesn't change or didn't change
materially, then I should
[01:43:43] expect that the output won't change. And
so my simulated output of the future
[01:43:49] is still gonna happen. And
if it's still gonna happen,
[01:43:53] I'm still gonna go after it. I believe it's
gonna, you know, and so there's a combination
[01:43:57] of two or three human characteristics,
[01:44:01] the ability to go into a, into
an experience fresh-minded,
[01:44:05] the ability to forget the setbacks,
the ability to believe in yourself,
[01:44:11] you know, to believe what you believe
and stay, stay true to that belief.
[01:44:16] But you're constantly reevaluating. This
combination of three, four, five things
[01:44:23] I think is, is really
important for resilience. And,
[01:44:27] and... and, you know, I'm fortunate that,
[01:44:32] that whatever life experiences led
to this, I've got kind of those
[01:44:36] four, five things. You know, I'm
always curious, always learning.
[01:44:40] I'm always learning from everybody,
you know? I'm always asking my...
[01:44:44] And because I'm humble about
everything, I'm always thinking,
[01:44:48] "Gosh, they did that so nicely. They
did that so wonderfully." You know,
[01:44:53] I wonder what they're thinking through.
How do they... You know, so I'm
[01:44:56] simulating everybody. In a lot of ways,
you know, I'm emulating almost everybody
[01:45:00] I watch, right? You're empathetic
towards everything that they
[01:45:04] do that you're observing and
respect. And, and so you're
[01:45:08] constantly learning and, you know.
[01:45:10] - You're now one of the wealthiest
people on Earth. One of the
[01:45:14] most successful humans on Earth.
[01:45:18] Is it harder to be humble and to
be able to... Do you feel the
[01:45:21] effect of money and power and fame
in making it harder for you to
[01:45:28] sort of be wrong in your own head? Enough
[01:45:32] to hear out an opinion of
somebody else when they
[01:45:36] disagree with you and learn from
them? Those kinds of things.
[01:45:41] - Um, surprisingly, no. And I would,
I would actually go the other way.
[01:45:46] Because I do so much of my
work publicly, when I'm wrong,
[01:45:51] pretty much everybody sees it.
[01:45:53] - You get humbled. Fair enough.
[01:45:55] - And when I'm wrong, when I'm
wrong or it didn't turn out that
[01:45:59] way or you know, I mean, most of the
things that, that I say outside I'm fairly
[01:46:07] certain about. And the reason for
that is because, because it's gonna
[01:46:10] impact somebody else and I want to be
quite concerned about that and quite,
[01:46:14] circumspect about that. For stuff that,
that I'm reasoning about inside a meeting,
[01:46:20] you know a lot of things could
turn out differently. And
[01:46:23] so, but it doesn't ever stop me from
reasoning. The way that the way that I
[01:46:27] manage and lead, I,
[01:46:30] you know, I'm constantly reasoning in front of
people. And even when I'm talking to you, you can
[01:46:33] kind of see me kind of
reasoning through things.
[01:46:35] And I want to make sure that you understand
what I'm saying not because I told you-
[01:46:40] ... because I'm so humble about
what I'm about to tell you.
[01:46:43] I kind of show you the
steps that I got there.
[01:46:46] And then you can decide whether you believe
what I said in the end. And so I'm doing that
[01:46:50] all day long in meetings.
[01:46:52] With all of my employees, I'm constantly
reasoning through, "Let me tell you what, how I
[01:46:56] see it." And then I reason through
it. It gives everybody the
[01:46:59] opportunity to intercept and say,
"I disagree with that part."
[01:47:04] The nice thing about reasoning through
things and letting people interact with
[01:47:08] it is that they don't have to
disagree with your outcome.
[01:47:12] They can disagree with
your reasoning steps.
[01:47:15] And they could pull me in different
directions, and then we can reason forward.
[01:47:19] And so we're kind of, you know, collective
[01:47:25] path searching method. And
it's really fantastic.
[01:47:29] - Yeah, you have this
[01:47:30] way about you of ... When you're
explaining stuff, I can feel you
[01:47:34] actually reasoning on
the spot about it with a
[01:47:38] constant open-mindedness where you
could ... I could feel like I could
[01:47:42] steer your thinking.
[01:47:44] And that's a, that's really beautiful that
you've been able to maintain that after so many
[01:47:48] years of success, and pain.
[01:47:50] I think sometimes pain makes you
close, closes you down a bit.
[01:47:55] - Mm-hmm. Yeah.
[01:47:56] - And I think to maintain-
[01:47:57] - Yeah. Tolerance for
embarrassment, I think is...
[01:47:59] - Yes, that's ... The tolerance
... I mean, that's a real thing.
[01:48:03] Is many years of embarrassing
yourself. Even those meetings
[01:48:07] knowing that there's people around
you where you declared one idea and
[01:48:11] it was shown that that idea was wrong-
[01:48:13] ... and be able to admit that and to grow from
that. That's not, that's very difficult on a human
[01:48:17] level.
[01:48:17] - Yeah. Well, you know. They
knew that recently my first
[01:48:21] job was, you know, cleaning toilets, so.
[01:48:25] - I'm glad you maintained
that same spirit of Denny's
[01:48:29] the, the work. I mean, that, that was beautiful.
Your whole journey from, starting from Denny's is a
[01:48:33] beautiful one. Let me ask you about
video games. So I'm a big gaming fan.
[01:48:41] So I have to say thank you to NVIDIA
for many years of incredible graphics.
[01:48:47] - By the way, GeForce is
our still, to this day-
[01:48:51] ... our number one marketing strategy.
[01:48:55] Right. People learn about NVIDIA
while they're in their teenage years.
[01:49:00] And then they go to college and they
know who NVIDIA is and then in beginning
[01:49:03] is just, you know, playing Call of Duty, you
know? You know, Fortnite. And then later
[01:49:08] they're using CUDA, and then later they're
using NVIDIA and, you know, Blender and
[01:49:14] Dassault and Autodesk.
[01:49:16] - Yeah. I mean, I should say I
mentioned to a friend that I'm
[01:49:20] talking with you. He said, "Oh,
they make great gaming GPUs."
[01:49:25] - Yeah, exactly.
[01:49:26] - It's like-
[01:49:26] - Exactly.
[01:49:27] - You know, there's more
to it, but, yeah, yeah,
[01:49:31] people really love the ... It really brought
a lot of joy to a lot of people. The,
[01:49:35] the, the hardware really
brings these worlds to life.
[01:49:38] There was some controversy
around this with DLSS 5.
[01:49:44] Can you explain to me the
drama around this? Uh, I guess
[01:49:48] people, the gamers online were concerned
that it makes games look like AI slop.
[01:49:54] Uh, what do you think of this drama?
[01:49:56] - Yeah. Uh, I think their
perspective makes sense
[01:50:01] and I could see where they're coming from,
because I don't love AI slop myself.
[01:50:05] You know, all of the AI
generated content increasingly,
[01:50:10] um, looks similar and
they're all beautiful,
[01:50:14] and I can... So I can... I'm empathetic
towards what they're thinking.
[01:50:18] That's just not what DLSS 5 is trying
to do. I showed several examples of it.
[01:50:24] But DLSS 5 is
[01:50:27] 3D conditioned, 3D guided. It's ground
truth structure data guided. And so the
[01:50:34] artist determined the geometry.
We are completely truthful.... to
[01:50:40] the geometry maintains
in every single frame.
[01:50:43] It's conditioned by the textures, the
artistry of the artist. And so every single
[01:50:50] frame, it enhances but it doesn't change
[01:50:54] anything. Now, the question is,
the question about enhancing,
[01:50:59] DLSS 5 also lets, because it's,
[01:51:02] the system is open, you could train
your own models to determine,
[01:51:06] and you could even in the future prompt
it. You know, I want it to be a toon
[01:51:10] shader. I want it to look like this
kinda, you know, so you can give it even
[01:51:14] an example. And it would
generate in the style of that,
[01:51:19] all consistent with the
artistry, you know, the
[01:51:22] style, the intent of the artist.
And so all of that is done
[01:51:29] for the artist, so that they can create
something that is more beautiful,
[01:51:34] But still in the style that
they want. I think that
[01:51:38] they got the impression
that the games are gonna
[01:51:42] come out the way the games are
shipped the way they do, and then
[01:51:46] we're gonna post-process it. That's
not what DLSS is intended to do.
[01:51:50] DLSS is integrated with
the artist, and so it's,
[01:51:54] it's about giving the artist
the tool of AI, the tool of
[01:51:58] generative AI. They could
decide not to use it, you know?
[01:52:01] - I think people are very
sensitive to human faces.
[01:52:04] And we're now living in this moment,
which I think is a beautiful one, which
[01:52:08] is people are sensitive to AI slop.
[01:52:11] It puts a mirror to ourselves to
help us realize that what we seek is
[01:52:15] imperfections. What we seek is
sometimes not perfect graphics.
[01:52:20] It helps us understand what we find
compelling in the worlds we create.
[01:52:25] And that's beautiful. And as long as it's
tools that help us create those worlds-
[01:52:28] - Yeah, that's right
[01:52:28] - ... it's wonderful.
[01:52:29] - That's right. Yet, yet another
tool, and they want the generative,
[01:52:33] models to generate the
opposite of photo real.
[01:52:39] Yeah, it'll do that too. And so it's
just yet another tool. I think the
[01:52:43] the gamers might also appreciate that,
that in the last couple of years,
[01:52:50] we introduced skin shaders
[01:52:55] to the game developers. And many
of those games have skin shaders
[01:52:59] that include subsurface scattering that
make skin look more skin-like. And so the
[01:53:06] industries, you know, game developers
are looking for more and more and more
[01:53:10] tools to express their art. And so this
[01:53:14] is just yet more, one more tool,
and they get to decide what to use.
[01:53:16] - Ridiculous question. What do you think
is the greatest or most influential
[01:53:20] game ever made? Maybe from
NVIDIA's perspective?
[01:53:24] - Doom.
[01:53:25] - Doom, unquestionably. That
was the start of the 3D.
[01:53:28] - I would say Doom, from an
art, the intersection of the
[01:53:32] cultural implication as well as the
industry, turning a PC into a gaming device.
[01:53:38] That was a very important moment. Now, now
of course, flight simulation companies were
[01:53:42] before it. And but they just didn't have
the popularity that Doom did to have made
[01:53:48] the industry turn the PC from an office
automation tool into a personal computer for
[01:53:55] families and gamers and things like that.
And so Doom was really impactful there.
[01:53:59] From an actual game technology
perspective, I would say Virtua Fighter.
[01:54:03] And so we're great friends
with both of them, you know?
[01:54:07] - And then there's games more
recently, I mean, Cyberpunk 2077,
[01:54:12] really nice GPU-accelerated
graphics. Like-
[01:54:16] - Fully ray traced.
[01:54:17] - Fully ray traced. Also, I like, I
personally, I'm a huge fan of Skyrim,
[01:54:22] uh, Elder Scrolls, and the, you know,
it's, it's been released a long, long time
[01:54:26] ago, but people release mods and-
[01:54:29] - We love mods
[01:54:30] - ... they create these, these inc- I mean, it-
... it's like a different game and it just
[01:54:34] allows me to replay the game
over and over and get i-
[01:54:37] It makes you realize that
you can re- experience in a
[01:54:41] totally new way the world
you already love. So-
[01:54:45] - That's right
[01:54:45] - ... I do that all the time. One of my
favorite things is just walk across Skyrim.
[01:54:48] - Uh, we created this thing called
RTX Mod. Yeah, it's a modding tool.
[01:54:53] - Awesome.
[01:54:53] - It allows the community to inject the
latest technology into an old game.
[01:55:00] - Of course, like what makes a great video game
is not just graphics, it's also story and
[01:55:04] character development, but-
[01:55:06] - That's right
[01:55:06] - ... beautiful graphics
can add to the immersion.
[01:55:10] The feeling like it's another
place you're transported to.
[01:55:15] Ah, what you said, I think
accurately, that the AGI timeline
[01:55:22] question rests on your definition of AGI.
[01:55:26] So, let me ask you about
possible timelines here.
[01:55:31] Let's, this ridiculous definition
perhaps of what AGI is,
[01:55:35] but an AI system that's able to
essentially do your job. So, run, no,
[01:55:44] start, grow, and run a successful
technology company that's worth-
[01:55:52] - A good one or a one?
[01:55:54] - No. It has to- It has to be
worth more than a billion,
[01:55:58] more, more than a billion dollars. So,
[01:56:02] you know, you know how hard it
is to do all those components.
[01:56:06] So, how far are we away
from that? So, we're
[01:56:10] talking about OpenClaw that does all the
[01:56:14] incredibly complex stuff
that are required to
[01:56:18] to, first of all, innovate, to find
customers, to sell to them, to
[01:56:22] manage, to build a team of
[01:56:26] some agents, some humans, all that
kind of stuff. Is this five, 10,
[01:56:29] 15, 20 years away?
[01:56:31] - I think it's now. I think
we've achieved AGI.
[01:56:35] - Do you think you could have a company
run by an AI system like this?
[01:56:37] - Possible, and the reason for that is
this. You said a billion, and you didn't
[01:56:41] say forever. And so for example,
uh... It is not out of the question
[01:56:48] that a Claw was able to create a web
service, some interesting little app that
[01:56:59] all of a sudden, you know, a few billion
people used for 50 cents, and then
[01:57:07] it went out of business again shortly after. Now, we
saw a whole bunch of those type of companies during the
[01:57:11] internet era, and most of those
websites were not anything more
[01:57:17] sophisticated than what
OpenClaw could generate today.
[01:57:20] - Interesting. Achieve virality
and monetize that virality.
[01:57:23] - Yeah. It's just that I don't know what it
is, but I couldn't have predicted any of
[01:57:27] those companies at the time
either, you know? And -
[01:57:30] - You're gonna get a lot of people
excited with that statement.
[01:57:33] It's like, what do you mean? I can- I
can just, uh - ... launch an agent and
[01:57:37] make a lot of money.
[01:57:38] - Well, by the way, it's happening right now,
right? You know that when, when you go to China
[01:57:42] you're gonna see, you're gonna
see a whole bunch of people
[01:57:46] teaching their, getting their Claws to try
to go out and look for jobs and, you know,
[01:57:51] do work, make money.
[01:57:53] And I'm not, I'm not actually...
I wouldn't be surprised if some
[01:57:57] social thing happened or
somebody created a, a
[01:58:01] digital influencer, super, super cute or
[01:58:04] some social application that,
you know, feeds your little
[01:58:08] Tamagotchi or something like that,
and, and it become an out of the
[01:58:12] blue an instant success.
A lot of people use it
[01:58:16] for a couple of months and it kind
of dies away. Now, the odds of,
[01:58:22] you know, 100,000 of those agents,
Building NVIDIA is zero percent.
[01:58:28] And then the one part
that I will, I won't do,
[01:58:32] And I, I want to make
sure we all do, is to
[01:58:36] recognize that people are really
worried about their jobs.
[01:58:40] And I just want to remind them
that the purpose of your job
[01:58:47] and the tasks and tools
that you use to do your
[01:58:50] job are related, not the same.
I've been doing my job for
[01:58:54] 33 years. I'm the longest running
tech CEO in the world, 34 years.
[01:58:58] And the tools that I've used
to do my job have changed
[01:59:03] continuously in the last 34
years, and sometimes quite
[01:59:07] dramatically, you know, over the
course of a couple, two, three
[01:59:10] years. And the one story that I really
[01:59:14] wanna make sure that everybody
hears is the story that the
[01:59:18] first job that computer
scientists said, AI
[01:59:22] researchers said was gonna
go away was radiology.
[01:59:25] Because computer vision was going to
achieve superhuman levels, and it did.
[01:59:30] CV... Computer vision was superhuman in
2019, 20, maybe a little bit later, 2020?
[01:59:39] Okay? And so it's been a long time since
computer vision has been superhuman. And
[01:59:43] so the prediction was radiologists
would go away because studying
[01:59:47] radiology scans was a thing of
the past. AI will do that. Well,
[01:59:52] they were absolutely right.
[01:59:54] Computer vision is completely
superhuman. Every radiology
[01:59:58] platform and package
today is driven by AI,
[02:00:02] and yet the number of
radiologists grew. And so
[02:00:06] the question is why? And we now have a
shortage of radiologists in the world.
[02:00:11] And so, one, the alarmist warning went
too far and it scared people from
[02:00:20] doing this profession that
is so important to society.
[02:00:23] And so it did harm. Now, why was it
wrong? The reason why is because
[02:00:29] the purpose of a radiologist, the
purpose is to diagnose disease
[02:00:33] and help patients and
doctors diagnose disease.
[02:00:38] And because we're able to
study scans at so much faster
[02:00:41] now, you could study more scans, you
could diagnose better, you could,
[02:00:47] you could inpatient faster,
[02:00:50] you can see people more. The hospitals
are making more money. You have
[02:00:54] more patients in the hospital. You
need more radiologists. I mean, the
[02:00:58] amazing thing is, it's so
obvious this was gonna happen.
[02:01:03] The number of software engineers at
NVIDIA is gonna grow, not decline.
[02:01:08] And the reason for that is because
the purpose of a software engineer
[02:01:12] and the task of a software engineer
coding are related, not the same.
[02:01:16] I wanted my software engineers to solve problems.
I didn't care how many lines of code they
[02:01:20] wrote, you know? But their job, their
purpose of their job didn't change. Solving
[02:01:26] problems, working as a team, diagnosing
problems, evaluating the result,
[02:01:32] looking for new problems to
solve, innovation, connecting
[02:01:35] dots. You know, none of that
stuff is gonna go away.
[02:01:39] - Do you think it's possible that... Let's
even take coding. Do you think the number of
[02:01:43] programmers in the world
might increase, not decrease?
[02:01:45] - Yes. And the reason for that is this.
What is the definition of coding?
[02:01:52] I believe it is... The definition of
coding, as of today, is simply specifying,
[02:01:58] specification, and maybe if you want to be
[02:02:02] rather directive, you could even give
it an architecture of the software
[02:02:06] that you wanted to write. So the question
is, how many people could do that?
[02:02:11] Describe a specification for a
computer to go... Telling the
[02:02:14] computer what to go build. How many
people? I think we just went from 30
[02:02:18] million to probably 1 billion. And so
every carpenter in the future will be
[02:02:26] a coder, except a carpenter
with AI is also an architect.
[02:02:33] They've just increased the value that they
could deliver to the customer. Their,
[02:02:37] their artistry just elevated tremendously.
[02:02:43] I believe that every accountant is,
you know, also your financial analyst,
[02:02:47] also your financial advisor. So,
all of these professions have
[02:02:51] just been elevated.... and, and
if I were a carpenter, I sees a,
[02:02:55] I see AI, I would just
completely go berserk.
[02:02:58] You know, the services I can bring
to my clients if I were a plumber,
[02:03:03] completely go berserk.
[02:03:04] - And the people that are currently
programmers and software engineers, I think
[02:03:08] they're at the cutting edge of understanding
intuitively how to communicate
[02:03:15] with the agents using natural language in
order to design the best kind of software.
[02:03:20] - That's right, exactly.
[02:03:20] - So over time they'll converge, but I think
[02:03:24] there's still value in getting,
I think learning how to program,
[02:03:28] like learning what programming
languages are. The old, the old kind of
[02:03:32] programming, what are good practices for
[02:03:36] programming languages, what are
design principles for programming-
[02:03:39] - That's right
[02:03:40] - ... Languages for large software systems?
[02:03:43] - And the reason for that,
[02:03:45] Lex, and you know, as you're
saying for the audience, I think
[02:03:49] the goal of, the goal of
specification, the artistry of
[02:03:53] specification, the goal
and the artistry of it,
[02:03:56] Is going to depend on what
problem you're trying to solve.
[02:04:01] When I'm thinking, when I'm thinking
about giving the company strategies and
[02:04:06] formulating corporate directions
and things that we should do,
[02:04:11] I describe it at a level
that is sufficiently
[02:04:16] specific that people generally
understand the direction
[02:04:21] and it's actionable. It's specific
enough that they can take action on it,
[02:04:26] but I under specify it on purpose, so that
[02:04:30] enable 43,000 amazing people to make
it even better than I imagined.
[02:04:36] And so when I'm working with engineers
and when I'm working with people,
[02:04:41] I think about who, what problem am I
trying to solve? Who am I working with?
[02:04:47] And the level of specification, the
level of architecture definition
[02:04:54] relates to that. And, and so
[02:04:59] everybody's going to have to learn how,
where in the spectrum of coding they want
[02:05:03] to be. Writing a specification is coding.
[02:05:06] And so you might decide to be quite
prescriptive because there's a very
[02:05:10] specific outcome you're looking for.
You might decide that, you know,
[02:05:14] this is an area you want to be much more
exploratory, and so you might under
[02:05:18] specify and enable you to
go back and forth with the
[02:05:21] AI to even push your own
boundaries of creativity.
[02:05:25] And so this artistry of where you are in
the spectrum, this is the future of coding.
[02:05:31] - But just to linger on it outside of coding,
I think a lot of people, rightfully so,
[02:05:36] are worried about their jobs, have a lot
of anxiety about their jobs, especially in
[02:05:40] the white-collar sector. I don't
think any of us know what to do,
[02:05:50] With tumultuous times that always come
when automations and new technology
[02:05:54] arrives. And I just...
First of all, I think
[02:06:01] we all need to have compassion and the
responsibility to feel sort of the burden
[02:06:06] of what the actual suffering feels like for
individual people and families that lose their
[02:06:10] job. I think whenever you have
transformative technology
[02:06:14] like that's coming with artificial intelligence,
there's going to be a lot of pain,
[02:06:18] and I don't know what to do about
that pain. Hopefully, it creates much
[02:06:22] more opportunities for those same people,
for the same kind of job as the tooling
[02:06:30] evolves and makes them more
productive and makes them more fun,
[02:06:34] hopefully, as it does in the programming.
I've been having so much fun programming,
[02:06:38] I have to say. Like, I've never had this
much fun. So hopefully it makes their job,
[02:06:42] automates the boring parts
and makes the creative parts,
[02:06:46] the ones that the human beings are responsible
for. But still there's going to be
[02:06:50] a lot of pain and suffering.
[02:06:51] - So my first recommendation before...
And this is now how I deal
[02:06:55] with anxiety. In fact, we
just talked about it earlier.
[02:06:59] Enormous anxiety about the future, enormous
anxiety about the pressure, enormous
[02:07:03] anxiety about uncertainty, I first break
it down, and then I'm gonna tell myself,
[02:07:10] "Okay, there are some things you can do something
about, there's some things you can't do anything
[02:07:14] about. But for the stuff that you
can do something about, let's reason
[02:07:18] about it and let's go do it."
[02:07:20] If we were to hire a new college graduate
today, and I have a choice between two,
[02:07:26] one that have, that is no clue what AI is
[02:07:31] and one that is expert in using AI, I would
hire the one who's expert in using AI.
[02:07:38] If I had an accountant,
a marketing person,
[02:07:42] the one that is expert in
using AI, supply chain,
[02:07:45] customer service, a salesperson,
business development, a lawyer,
[02:07:52] I would hire the one who
is expert in using AI.
[02:07:55] And so I would advise that
every college student,
[02:07:59] every teacher should encourage
their student to be, to go use
[02:08:03] AI. Every college student
should graduate and be an
[02:08:07] expert in AI. And everybody,
if you're a carpenter, if
[02:08:11] you're, you know, electrician, go use AI.
[02:08:15] Go see what it can do to
transform your current job,
[02:08:19] elevate yourself. If I were a
farmer, I would absolutely use AI.
[02:08:24] If I were a pharmacist, I would
use AI. I wanna see how, what it
[02:08:28] could do to elevate my job so
that I could be the innovator to
[02:08:33] revolutionize this industry myself.
[02:08:36] And so that would be the first thing
that I would do. And then I would
[02:08:39] also, I would also help them...
[02:08:44] it is the case that the technology will
dislocate and will eliminate many tasks
[02:08:52] if... And because it will
automate it, if your job is the
[02:08:55] If your job is the task, then you're
very highly going to be disrupted.
[02:09:02] If your job's purpose
includes you, certain tasks-
[02:09:08] ... then it's vital that you go learn
how to use AI to automate those tasks.
[02:09:12] And then there's the world
of spectrum in between.
[02:09:14] - And by the way, the beautiful thing
about AI, so the chatbot versions,
[02:09:21] is you can break down... You have anxiety
[02:09:24] and you can break down the
problem by talking to it.
[02:09:28] Like, I've recently... It's really
just incredible how much you can think
[02:09:32] through your life's problems, and through...
And I don't mean, like, therapy problems.
[02:09:35] I mean, like, very practically, "Okay,
I'm worried about my..." Literally,
[02:09:39] "I'm worried about my job. What are the skills? What
are the steps I need to take? How do I get better at
[02:09:43] AI?" Everything you just said, you could
literally ask and it's going to give you-
[02:09:47] ... a point-by-point plan. I mean, it's
just a great life coach, period. This-
[02:09:51] - I don't know how to use AI, and the
AI goes, "Well, let me show you."
[02:09:54] - Exactly. It's very meta, but it's-
[02:09:57] It's kind of incredible. So
people definitely should-
[02:10:00] - You can't walk up to Excel and say, "I
don't know how to use Excel." You're done.
[02:10:03] - I mean, that's really what AI has
done for me in all walks of life,
[02:10:07] is that initial friction of being a beginner
of using a thing for the first time.
[02:10:11] I can literally ask
about any single thing,
[02:10:15] "What are the first steps I need to take?"
[02:10:16] - That's right.
[02:10:17] - And that handholding that it
does, removing the friction
[02:10:21] of all the experiences that
the world offers is... You
[02:10:25] know, like I mentioned to you offline,
you mentioned, "I'm going to China
[02:10:29] and Taiwan."
[02:10:30] - So awesome.
[02:10:31] - Just ask, "Where do I-"
[02:10:31] - So excited for you.
[02:10:32] - "Where do I—what do—" "You know, where do
I go? How do I..." All of those questions—
[02:10:35] ... immediately answered,
and it's beautiful.
[02:10:37] - Well, when you, when you go to
Taiwan, just ask AI- ... "What are
[02:10:41] Jensen's favorite restaurants
in Taiwan?" And it'll actually-
[02:10:45] - You don't know?
[02:10:45] - Oh, yeah.
[02:10:46] - Is it accurate? Okay.
[02:10:47] - Yeah.
[02:10:47] - All right.
[02:10:47] - It's all over Taiwan.
[02:10:50] - Well, you're a rockstar over
there. And like we also mentioned
[02:10:54] offline, maybe our paths will cross, which
would be really wonderful in computing.
[02:10:58] - COMPUTEX. NVIDIA GTC Taiwan.
[02:11:01] - Uh, do you think there's some things about
human nature, about human consciousness
[02:11:08] that is fundamentally non-computational?
Maybe something a chip, no matter
[02:11:14] how powerful, can never replicate?
[02:11:18] - I don't know if the chip will ever get
nervous. And that's the, you know, of course,
[02:11:22] the conditions by which that causes anxiety
or nervousness or whatever emotion. Um,
[02:11:31] I believe that AI will be
able to recognize those
[02:11:36] and understand those. I don't
think my chips will feel those.
[02:11:41] And therefore, the... How
that anxiety, how that
[02:11:45] feeling, how that excitement,
how that, how that, you know...
[02:11:50] All of those feelings manifest in
human performance. For example,
[02:11:54] extremely amazing human performance,
athletic performance, you know,
[02:11:59] average or lesser than
average. That entire
[02:12:02] spectrum of human performance
that comes out of
[02:12:06] exactly the same circumstances
for different people,
[02:12:10] manifesting a different outcome, manifesting
a different performance. I don't think
[02:12:17] there's anything about anything that
we're building that would suggest
[02:12:22] that two different computers
[02:12:24] being presented with all of exactly
the same context would perfo-
[02:12:29] Of course, it would produce statistically
different outcomes, but it's not because
[02:12:33] it felt different.
[02:12:34] - Yeah, the subjective...
[02:12:36] Boy, there's something truly special
about the subjective experience
[02:12:41] that we humans feel. Like I mentioned to
you, I was pretty nervous talking to you.
[02:12:47] Like I mentioned to you, that,
the hope, the fear, the anxiety,
[02:12:51] and just life itself, the richness of
life. How amazing everything is. How
[02:12:55] deeply we fall in love, how
deeply our hearts get broken,
[02:12:59] how afraid we are of death and
how much pain we feel when our
[02:13:03] loved ones pass away. All of that, the
whole thing. I know it's very hard to-
[02:13:09] ... think AI being able to... A
computational device being able to do that.
[02:13:13] But there's so many mysteries about
this whole thing that we're yet to
[02:13:17] uncover, that I am open to be surprised.
I've been surprised a lot over the past-
[02:13:23] ... few months and few years.
Scaling can create some
[02:13:27] incredible miracles in the
space of intelligence.
[02:13:30] Has been truly marvelous to
watch, so I'm open to surprise.
[02:13:34] - And it's just really important
to break down what is
[02:13:37] intelligence. You know, the word,
that word we use all the time, it's
[02:13:41] not a mysterious word. Intelligence
has a meaning, you know?
[02:13:46] And it's a system that... You
know, it's something that we
[02:13:50] do that includes perception
and understanding and
[02:13:54] reasoning and the ability to do
plan. And, you know, that, that
[02:13:58] loop, that loop, is the...
Fundamentally what intelligence is.
[02:14:04] Intelligence is not one word that
is exactly equal to humanity.
[02:14:11] And that's, I think it's really important
to separate the two. We have two words for
[02:14:14] that. I'm not... I don't
over-fantasize about, and I don't
[02:14:20] over-romanticize about
intelligence. Intelligence
[02:14:23] is... And people have heard me
say it before, I actually think
[02:14:27] intelligence is a commodity. I'm
surrounded by intelligent people.
[02:14:33] And I'm surrounded by intelligent people more
intelligent than I am in each one of the
[02:14:37] spaces that they're in. And yet,
[02:14:40] I have a role in that circle. It's
actually kind of interesting.
[02:14:45] They're more educated than I am. They
went to better schools than I did.
[02:14:51] They're deeper than, in any of the
fields that they're in. All of 'em.
[02:14:55] I have 60 of 'em. They're
all superhuman to me.
[02:14:59] And somehow, I'm sitting in the
middle orchestrating all 60 of 'em.
[02:15:03] And so you gotta ask yourself...
Uh, what is, what is
[02:15:06] it about a dishwasher that allows that
[02:15:10] dishwasher to sit in the middle of
superhumans? Does that make sense?
[02:15:15] And so, but that's my point. My point
is intelligence is a functional thing.
[02:15:22] Humanity is not a, not specified
functionally. It's a much, much bigger word.
[02:15:29] And, and our life experience,
our tolerance for
[02:15:33] pain, our determination, those are, those
are different words than intelligence.
[02:15:39] And so the thing that I wanna
help the audience understand,
[02:15:43] if I could give them one thing, is, is
[02:15:46] intelligence is a word that we've
elevated to a very high form over time.
[02:15:50] - The, the word we should
really elevate is humanity.
[02:15:53] - Character, humanity.
[02:15:55] - All those things.
[02:15:55] - All of those things.
Compassion, generosity,
[02:16:00] all of the things that you said just now,
[02:16:03] I believe those are superhuman
powers. And that now
[02:16:07] intelligence is gonna be commoditized.
[02:16:09] Because we've spoken about it, the most
important thing is your education.
[02:16:13] The most... Now, even, even when they said
the most important thing is your education,
[02:16:17] when you went to school, there's more
than just knowledge that you gained.
[02:16:22] And so, but unfortunately, our society
has put everything into one single word,
[02:16:28] and life is more than one word. And I'm
just telling you, my life would suggest
[02:16:34] that being lower on the intelligence
curve than everybody around me
[02:16:41] doesn't change the fact I'm the
most successful. And so, and I
[02:16:45] think, I think that kind of is I'm
trying to hopefully inspire everybody
[02:16:49] else that don't let
this democratization of
[02:16:52] intelligence, this
commoditization of intelligence,
[02:16:57] you know, cause you anxiety.
You should be inspired by that.
[02:17:00] - Yeah. I think AI will help us
celebrate humans more. And certainly
[02:17:07] humanity and human first, and I, I think
what makes this world incredible is humans
[02:17:13] forever will be so, and just AI is
this incredible tool that makes us-
[02:17:18] - That's exactly right.
[02:17:18] - ... humans more powerful.
[02:17:19] - That's exactly right.
[02:17:21] - Uh, so much of the success of NVIDIA
[02:17:25] and the lives of millions of people
that I mentioned depend on you.
[02:17:31] But you're just one
human, like we mentioned,
[02:17:35] a mortal like all of us. Do you think about
your mortality? Are you afraid of death?
[02:17:42] - I really don't wanna die. Um, I have
a great life. I have a great family.
[02:17:48] Uh, I have really important work. Uh,
this is, this is not a once in a,
[02:17:58] once in a lifetime experience suggests
[02:18:02] that it has been experienced
by many people, just not one
[02:18:05] person. This is a once in a humanity
experience, what I'm going through.
[02:18:11] Uh, NVIDIA is one of the most consequential
technology companies in history. We're doing
[02:18:15] very important work. I take
it very seriously. Um,
[02:18:20] And so some of the, some of the
things that, that of course are,
[02:18:24] are practical things, like how do we
think about succession planning? And,
[02:18:31] I'm famous in saying that I don't
believe in succession planning.
[02:18:36] - Man.
[02:18:36] - And the reason, the reason for that,
the reason for that isn't because I'm
[02:18:40] immortal. The reason for that is
because if you're worried about
[02:18:46] succession planning,
[02:18:48] if you're worried, all that anxiety of succession
planning, then what should you do about it?
[02:18:52] Then you break it all the way back down.
[02:18:54] The most important thing you should do
today, if you care about the future of your
[02:18:57] company, post you, is to pass on
knowledge, information, insight, skills,
[02:19:04] experience as often and continuously
as you can, which is the reason
[02:19:08] why I continuously reason about
everything in front of my team.
[02:19:13] Every single meeting is
about a reasoning meeting.
[02:19:16] Every moment I spend inside a
company, outside a company is
[02:19:20] about passing on knowledge to
people as fast as I can. Nothing I
[02:19:24] learn ever sits on my desk
longer than, you know,
[02:19:28] a fraction of a second. I'm passing that
information, that knowl- oh my gosh, this is
[02:19:32] cool. Before I even finish
learning all of it myself, I'm
[02:19:36] already pointing it to somebody else. "Get on
this. This is so cool. You're gonna wanna, you're
[02:19:40] gonna wanna learn this." And
so I'm constantly passing
[02:19:44] knowledge, empowering people,
elevating the capability of
[02:19:48] everybody around me, so that the
outcome that I, that I seek,
[02:19:55] that I hope for, is that I die
on the job, you know? And,
[02:19:59] and hopefully I die on the job
instantaneously, you know?
[02:20:03] And there's no long periods of
suffering, you know? It's, uh —
[02:20:06] - Well, from a fan perspective
given your, your extremely,
[02:20:12] um, your enormous positive impact on
civilization, of course, I hope you keep
[02:20:18] going. But also it's just fun to
watch what NVIDIA is doing, you
[02:20:22] know. It's just the rate of innovation.
And I'm a huge fan of engineering.
[02:20:26] There's so much incredible engineering
being continuously being done by
[02:20:30] NVIDIA. It's just fun to watch. It's a
celebration of humanity, a celebration
[02:20:34] of great builders, a celebration of
great engineering. So, it represents
[02:20:37] something special. So I hope you and
NVIDIA keep going. What gives you hope
[02:20:44] about this whole thing we got going on,
about humanity, about the future of
[02:20:47] humanity? When you look out, when you think
about the future quite a bit, when you
[02:20:51] look out 10, 20, 50, 100 years
from now, what gives you hope?
[02:20:56] - I've always had a great confidence
in the kindness, uh, the generosity,
[02:21:09] uh... the compassion, the human
capacity. I've always been
[02:21:16] extremely confident of that.
Sometimes more so than I should.
[02:21:25] And, and I get taken advantage
of, but it doesn't, it doesn't
[02:21:29] ever cause me not to.
I start with, always,
[02:21:34] That people want to do good. People
want to, um help others. And,
[02:21:44] vastly, I am proven right.
Constantly proven right. And, and
[02:21:51] often it exceeds my expectations.
[02:21:56] And, and so I have complete confidence
in the human capacity. I think the,
[02:22:03] the thing that, the things
that give me incredible hope,
[02:22:07] Is what I see as, as I extrapolate, as
I, what I see now is possible, and as I
[02:22:14] extrapolate, Based on the things that
we're doing, what will very likely happen.
[02:22:22] And, and that there's so many
things that we wanna solve.
[02:22:27] There's so many problems we
wanna solve. There's so many
[02:22:31] things that we wanna build. There's
so many good things that we wanna do
[02:22:35] that are now within our reach, and
within the reach of my, my lifetime.
[02:22:40] You just can't possibly not be romantic
about that. You know what I'm saying?
[02:22:46] - What an exciting time to
be alive. Like, truly-
[02:22:49] - How can-
[02:22:49] - ... truly so.
[02:22:50] - How can you not be romantic
about, about that? The, the
[02:22:54] fact that, that there is a, there,
[02:22:58] it's a reasonable thing to
expect the end of disease. It's
[02:23:02] a reasonable thing to expect.
It's a reasonable thing to expect
[02:23:06] that pollution will be
drastically reduced.
[02:23:09] It's a reasonable thing to expect
that traveling at the speed of light
[02:23:15] is actually in our future.
[02:23:17] And then, you know, not, not for
long distances, but short distances.
[02:23:21] You know, and people ask me how. Well,
first of all, very soon, I'm gonna put a
[02:23:25] humanoid on a spaceship, and it's
gonna be, you know, my humanoid,
[02:23:29] and, and we're gonna send it out as soon,
you know, as soon as possible, and it's
[02:23:33] gonna keep improving and enhancing along
the flight. And then when it's time,
[02:23:39] all of the, all of my consciousness
has already been, you know so much of
[02:23:43] my life has been uploaded in the internet.
Take all my inbox, take everything that I've
[02:23:46] done, everything I've said. You know,
it's been collected and becoming my AI.
[02:23:51] And I'm just, you know, when the time
comes, you know, we'll just send that at
[02:23:55] the speed of light,
catch up with my robot.
[02:24:00] - Oh, that's brilliant. I mean, but for
me, that's sorta application-focused.
[02:24:04] But also, for me, the curiosity-
... Maxing perspective,
[02:24:09] I just, all of those
mysteries. There's so much-
[02:24:12] ... fascinating scientific
questions there.
[02:24:14] - Understanding the biological machine
is right around the corner. It's, it's
[02:24:18] not 10 years. It's five years probably.
[02:24:20] - And then your biological machine,
the human mind and cracking physics,
[02:24:24] theoretical physics
open. It's so exciting.
[02:24:26] - Explaining consciousness,
that one would be awesome.
[02:24:29] - And it's all within our reach.
[02:24:31] Jensen, thank you so much for everything you've done
over the years. Thank you for everything you're doing
[02:24:35] for the world. Thank you for
being who you are. I can tell
[02:24:39] you're a great human being, and
I wish you incredible success
[02:24:45] this year. I can't wait. As a fan, I can't
wait to see what you do next, and hopefully
[02:24:49] I'll see you in Taiwan and thank
you so much for talking today.
[02:24:52] - Thank you, Lex. I had a great time. And
also, if I could just say one more thing.
[02:24:56] - Yes.
[02:24:57] - And thank you for all the
interviews that you do, the depth,
[02:25:01] the respect that you go through
with and the research that you
[02:25:05] do to reveal, you know, for all of us,
[02:25:09] The amazing people that you've
interviewed over the years. I've
[02:25:13] enjoyed I've enjoyed them
immensely. And as an
[02:25:16] innovator, to have created this long form,
[02:25:21] unbelievable, and yet, you
know, it's just captivating. So
[02:25:24] anyways, thank you for everything you do.
[02:25:25] - It means the world. Thank you, Jensen.
[02:25:27] - Thank you, Lex.
[02:25:29] - Thank you for listening to this conversation
with Jensen Huang. To support this
[02:25:33] podcast, please check out our sponsors
in the description, where you can also
[02:25:36] find links to contact me, ask
questions, give feedback, and so on.
[02:25:42] And now, let me leave you with
some words from Alan Kay.
[02:25:46] "The best way to predict the
future is to invent it."
[02:25:51] Thank you for listening, and
hope to see you next time.