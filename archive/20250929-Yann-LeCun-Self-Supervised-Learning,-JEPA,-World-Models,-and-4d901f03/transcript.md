---
source_url: "https://www.youtube.com/watch?v=yUmDRxV0krg"
platform: youtube
uploader: "Harvard CMSA"
title: "Yann LeCun | Self-Supervised Learning, JEPA, World Models, and the future of AI"
upload_date: "20250929"
duration: 4117
fetched_at: "2026-06-22T04:45:47.861964Z"
transcript_source: youtube-transcript-api
---

[00:00:00] - Welcome everyone.
[00:00:01] Can you hear me? I'm Mike Friedman,
[00:00:05] representing the Center for Mathematics
[00:00:08] and Scientific Applications at Harvard,
[00:00:11] and it's my great
pleasure to be introducing
[00:00:15] Yann LeCun, chief scientist
[00:00:19] at Meta. We're running
a conference at CMSA
[00:00:24] on the Geometry of Machine learning,
[00:00:27] and this is actually a lecture
within that conference,
[00:00:31] but it's outside the CMSA building
[00:00:33] because we knew too many people
would show up to carry on,
[00:00:36] so we were able to move
it to the Science Center
[00:00:39] where it's appropriate.
[00:00:43] As soon as we got Yann to
agree to give this talk,
[00:00:46] all the other speakers
accepted immediately.
[00:00:49] So Yann, it was the easiest
conference to organize.
[00:00:54] Yann is one of these
scientists that it would
[00:00:59] anesthetize the audience if I tried to go
[00:01:02] through his awards, and
also I would need a script.
[00:01:06] So I, I'll just mention that
he won the Turing award
[00:01:11] with Bengio and Hinton a few years ago.
[00:01:16] I think of him
interchangeably with the idea
[00:01:20] of convolutional neural nets.
[00:01:23] I'm a geometer as a
mathematician, you know,
[00:01:25] topologist and geometer.
[00:01:27] And I think that's something
we share a confidence in the
[00:01:30] geometric imagination.
[00:01:32] And I know it's something
that Yann has always tried
[00:01:35] to figure out how to weave
into artificial intelligence,
[00:01:38] and it's a, it's a, a vein
of exploration that I've,
[00:01:42] I've greatly admired.
[00:01:45] So we're,
[00:01:48] I think we're all very much
looking forward to this talk.
[00:01:51] So am I, and without further ado,
[00:01:53] let me turn the stage over to y
[00:01:56] - Thank you so much, Mike.
[00:02:03] Well, I have a terrible
confession to make, which is,
[00:02:06] I'm not a mathematician.
[00:02:11] I'm not really a computer
scientist either.
[00:02:14] I never actually study computer science,
[00:02:18] so I'm not exactly sure what I am,
[00:02:19] but I'm, I'm going to talk about
[00:02:23] machine learning this, I
was told this was a bit
[00:02:26] of a more general, general audience
[00:02:27] than the one at the workshop.
[00:02:29] So I mean this a bit more of
a what on your stock than,
[00:02:33] I mean, still technical,
[00:02:36] but not very, a little
light lightweight on the
[00:02:40] series, that's for sure.
[00:02:42] And I want to talk about
[00:02:47] the future of ai
[00:02:49] and how do we get,
[00:02:50] how can we make significant
progress towards more
[00:02:53] intelligent machines beyond
what they are capable of doing.
[00:02:57] And at you right now, there
is a lot of work to do.
[00:03:00] We're nowhere near
matching human intelligence
[00:03:04] or even animal intelligence
with the type of techniques
[00:03:06] that we have access to at the moment.
[00:03:09] So one big question we can ask ourself is,
[00:03:11] do we actually need AI systems
[00:03:13] with human level intelligence?
[00:03:16] And the answer is probably yes,
[00:03:17] because there's a, the future
in which each of us walks
[00:03:22] around with AI assistance kind
[00:03:24] of helping us in our
daily lives at all times,
[00:03:27] perhaps living in, you know,
[00:03:30] wearable devices like s smart glasses,
[00:03:32] like the ones I'm wearing at the moment.
[00:03:34] Actually, you guys need to smile.
[00:03:37] Okay, you are in the box
[00:03:40] and, you know, we'll those
things will be sort of helping,
[00:03:44] helping us at all times.
[00:03:48] And it's like, we'll be their boss.
[00:03:49] So it is kind of like we,
we be kind of running around
[00:03:52] with a team of, with virtual people kind
[00:03:55] of helping us at all times.
[00:03:58] And of course for this, we need AI systems
[00:04:01] that have intelligence that is
in some ways similar to human
[00:04:05] because that's the kind
of in, of, of entities
[00:04:08] that we're the most familiar
with interacting with.
[00:04:13] But the technology is
nowhere near where it needs
[00:04:16] to be at the, at the moment for that.
[00:04:20] So the main issue is
[00:04:23] that current AI architectures
[00:04:25] and machine learning
techniques suck compared to
[00:04:29] what we can observe in humans
[00:04:30] and animals, the type of
efficiency in, in learning
[00:04:35] that we see in animals and humans.
[00:04:37] It's just astonishing. And we're not,
[00:04:38] we're not matching this, at
least at, at the moment in,
[00:04:42] in many instances.
[00:04:44] So, you know, early on
in machine learning, the,
[00:04:47] the main technique was
supervised learning,
[00:04:49] and then there was a big fashion
[00:04:50] around reinforcement learning for a while.
[00:04:53] Now it's used a lot of course
[00:04:54] to fine tune large language models, but,
[00:04:57] but in themselves,
[00:05:00] those two techniques
are really insufficient.
[00:05:02] The, the type of learning
that we observe in humans
[00:05:05] and animals is very different.
[00:05:07] It's neither supervised nor
reinforced for that matter.
[00:05:11] It's more like self supervised learning
[00:05:13] or something that has
really revolutionized AI
[00:05:16] and machine learning over
the last few years, which,
[00:05:20] you know, at the principle, you know,
[00:05:23] underlying principle are very similar
[00:05:24] to supervised learning,
[00:05:26] but there is no clear difference
between input and output.
[00:05:31] I'll come back to this. This
works astonishingly well
[00:05:36] for training a system to
understand the structure
[00:05:39] of sequences of discrete symbols, such
[00:05:43] as language code,
mathematics to some extent.
[00:05:48] But the problem is that it only works
[00:05:50] for sequences of discrete symbols.
[00:05:52] It doesn't really work for
kind of natural signals.
[00:05:55] Self supervised running.
It starts to work,
[00:05:57] but the techniques are very different.
[00:05:59] And that that'll be the main
topic really of this talk.
[00:06:03] There's other limitations
with current AI architectures,
[00:06:06] which is that the type of
inference that they perform is
[00:06:10] basically feed forward propagation
through a fixed number
[00:06:13] of layers of sub neural net.
[00:06:16] And that's computationally limited.
[00:06:18] There's a lot of functions you
cannot represent efficiently
[00:06:21] by just stacking a fixed
number of layers of, you know,
[00:06:25] alternating linear operators
[00:06:27] and non-linear pointwise operators.
[00:06:32] And the idea of, you
know, training a system
[00:06:34] to predict the next
item in a sequence works
[00:06:37] for discreet symbol sequences,
[00:06:39] but not really for, for anything else.
[00:06:45] The other issue also with
current architectures is
[00:06:49] that they use auto aggressive,
auto aggressive prediction.
[00:06:52] So they use their own predictions as input
[00:06:54] to make further predictions,
and that leads to divergence
[00:06:58] or hallucination as people call it.
[00:07:00] So there, there's a lot of
things that really we are missing
[00:07:04] to kind of match the type
[00:07:05] of intelligence we observe
in humans and animals.
[00:07:08] Humans and animals have
mental models to the world.
[00:07:11] The behavior is driven by
objectives, by tasks, goals,
[00:07:16] if you want, they can reason
[00:07:18] and they can plan
complex action sequences.
[00:07:21] All things that chat bots
[00:07:24] and LLMs are essentially incapable of,
[00:07:27] or at least not to the
level that we'd like.
[00:07:28] So we need systems that understand
[00:07:32] the physical world, systems
that have persistent memory
[00:07:37] systems that can plan
complex actions so as
[00:07:41] to fulfill an objective or
accomplish a task systems
[00:07:44] that can reason in particular
they can spend more time
[00:07:47] solving difficult problems
than simple problems
[00:07:50] and systems that are
controllable and safe.
[00:07:53] Okay, so this, let's start
with this idea of world model.
[00:07:58] We have mental models of reality that
[00:08:04] allow us to predict
what's going to happen,
[00:08:08] particularly what's going to happen
[00:08:09] as a consequence of our actions.
[00:08:11] And that this is really
what allows us to plan.
[00:08:13] And the type of learning that
is taking place in humans
[00:08:15] and animals in the
first few months of life
[00:08:18] is a little mysterious.
[00:08:20] So this chart was put
together by my colleague
[00:08:23] and friend Emmanuel Dpu,
who's a county scientist in,
[00:08:27] in Paris, and indicates that what age
[00:08:31] infants learn basic concepts
about the, about the world,
[00:08:36] like object, permanence,
the fact that some objects,
[00:08:39] you know, are stable
when you put them on the
[00:08:42] table, they're not going to fall.
[00:08:45] That objects belong to
different categories.
[00:08:47] Babies that are, you know, five
[00:08:49] or six months, they don't
speak not many language,
[00:08:52] but they certainly know
what the difference is
[00:08:54] between the table and
the chair and the cat
[00:08:55] and the dog without
knowing the names of it.
[00:08:58] And it takes about nine
months for infants to learn
[00:09:02] basic notions of intuitive
physics like gravity, inertia,
[00:09:07] conservation, momentum,
this, this kind of stuff.
[00:09:10] So if you show a six month old,
[00:09:13] the scenario at the
bottom left where a little
[00:09:18] cart is on a platform
[00:09:19] and you push it off the
platform, it appears
[00:09:21] to float in the air, six months old
[00:09:23] won't pay attention much.
[00:09:26] A 10 months old will
be extremely surprised.
[00:09:29] Perhaps look like a little girl here,
[00:09:31] because by then in France
have learned that objects
[00:09:34] that are not supported
are supposed to fall.
[00:09:38] So how do, how do we get
machines to learn like babies?
[00:09:40] And we've not solved that problem.
[00:09:42] And the reason you can
tell that we're not solved
[00:09:44] that problem is, is that, you know,
[00:09:46] we don't have domestic robots.
[00:09:48] We don't have self-driving cars
[00:09:49] that are completely autonomous level five.
[00:09:52] We have them, but we
cheat, but we have systems
[00:09:56] that can pass the bar exam,
they can solve math problems,
[00:10:00] you know, do all kinds of stuff
[00:10:02] that are intellectually
challenging for most of us.
[00:10:05] But, but we still don't
have robots that can do
[00:10:09] what a cat can do, or we can do that
[00:10:11] what a 10-year-old can do.
[00:10:13] The first time the the 10-year-old tries.
[00:10:16] You, you tell a 10-year-old
for the first time, you know,
[00:10:21] clear out the dinner table
if you know the dishwasher,
[00:10:23] a 10-year-old can do it
without being trained to do it.
[00:10:26] Basically the first time. A
17-year-old can learn
[00:10:30] to drive a car in a astonishingly
short time, maybe 10
[00:10:32] or 20 hours of practice without
causing accidents mostly.
[00:10:38] And we have millions of
hours of training data.
[00:10:41] We still don't have self-driving
cars except with cars
[00:10:44] with lots of, you know,
extra sensors like lidars
[00:10:47] and complete mapping on the environment
[00:10:48] and, you know, all kinds of tricks.
[00:10:51] So, you know, obviously
we're missing something big.
[00:10:53] And this is another example of
what's been known as the, the
[00:10:57] paradox, which is that a lot of things
[00:11:00] that we consider intellectually
challenging for humans,
[00:11:03] you know, playing chess, solving
integrals, stuff like that
[00:11:06] turned out to be algorithmically
relatively simple.
[00:11:10] And the same is true for
producing nice sounding text
[00:11:15] or answering a question as
long as you've been trained
[00:11:17] to produce the correct answer.
[00:11:22] Yet we don't have robots
that are near nearly
[00:11:26] as dexterous as a primate or even a cat.
[00:11:33] So this may be explained by the following
[00:11:36] very simple estimate.
[00:11:38] So a typical large
language model is trained
[00:11:41] with something like 30 trillion tokens.
[00:11:43] This is the number I got for Lama three.
[00:11:45] I think a token is like a sub board unit.
[00:11:48] So that's something like
two tenths of the 13 words.
[00:11:52] Each token is three bytes.
[00:11:53] So the total amount of data used
[00:11:55] to train a typical LLM
is about 10 to 14 bytes.
[00:11:59] It would take any of us 400,000 years,
[00:12:03] maybe half a million years
to read through through that.
[00:12:08] It's just an enormous amount of text.
[00:12:10] Now compare this to
[00:12:12] what a human child has seen
a four yearold has seen
[00:12:16] during his or her life.
[00:12:19] Four year, four years of life
is about 16,000 hours for,
[00:12:23] for a young child, which
by the way, a small amount
[00:12:26] of video, it's about 30
minutes of YouTube uploads
[00:12:30] and information.
[00:12:31] Getting to the visual cortex
through the optic nerve
[00:12:37] is about one byte per
second times 2 million.
[00:12:40] We have 2 million optic nerve fibers, each
[00:12:42] of which carries about
one byte per second.
[00:12:45] So during wake hours, it's
about two megabytes per second.
[00:12:49] Multiply this by 16,000 hours,
[00:12:51] and it's about 10 to the 14 bytes.
[00:12:54] Okay? So a 4-year-old
has seen as much data
[00:12:56] as the biggest LMS trained
on all the publicly
[00:12:59] available text on the internet.
[00:13:02] Now, you might say that
[00:13:07] the visual data is much more
redundant than the text on the
[00:13:11] internet, which is true,
[00:13:13] but in fact, that's exactly
what you want to train a system
[00:13:16] to understand, to capture structure
[00:13:19] and dependency in training data
[00:13:22] using self supervised learning.
[00:13:23] You need redundancy. If
you don't have redundancy,
[00:13:26] you can't learn anything,
you can't learn anything from
[00:13:29] completely random bit strings.
[00:13:31] So it tells you a number of things.
[00:13:35] The first thing it tells you
is that we are never going
[00:13:37] to get to human level AI
by just training on text.
[00:13:40] It's not going to happen despite
what you might hear for some
[00:13:43] of the more optimistic sounding CEOs
[00:13:47] of various AI companies in Silicon Valley,
[00:13:49] it's just not going to happen.
[00:13:54] It also means that we need
[00:13:55] to make some serious progress
if we want to have robots
[00:14:00] that, you know, can be useful.
[00:14:03] There is countless companies
that are being formed
[00:14:06] that are building humanoid robots,
[00:14:08] and you see all those videos
[00:14:09] of those robots doing impressive things.
[00:14:11] But in fact, the, the secret
of all that is that none
[00:14:16] of those company has any idea how
[00:14:18] to make those robots
smart enough to be useful,
[00:14:23] except in very narrow tasks
for which they, they have
[00:14:26] to be carefully trained.
[00:14:30] So that's an issue.
[00:14:32] So that gives an opportunity
for, you know, researchers
[00:14:35] and scientists trying to
kind of make progress in ai.
[00:14:38] There's still a lot of work to do
[00:14:40] and it may not require, you
know, hundreds of billions
[00:14:43] of investment in GPUs.
[00:14:45] Okay, there's a second
issue, which is inference.
[00:14:47] So I mentioned that of the,
I mentioned the limitations
[00:14:50] of inference by formal
propagation through a fixed number
[00:14:53] of operations.
[00:14:56] A lot of things that we're doing require
[00:14:58] much more sophisticated
computation than this.
[00:15:00] And in fact, I would submit
that a more powerful way
[00:15:04] to perform inference is
through optimization.
[00:15:07] So instead of a system
computing its output by
[00:15:12] this works by just, you know, propagating
[00:15:14] through a fixed number of layers
in some sort of neural net
[00:15:17] and then producing an output.
[00:15:19] The, the design, I think is much more,
[00:15:21] that's much more preferable,
would be a system that,
[00:15:24] you know, extract information
from the its input,
[00:15:28] produces a representation
of the input if you want,
[00:15:30] but then has another big neural net
[00:15:33] or learning machines learning machine
[00:15:35] with a single scaler output,
let's call it an energy
[00:15:38] that would measure the
degree of compatibility
[00:15:41] or incompatibility between the
input and a proposed output.
[00:15:45] Okay? So propose an output,
[00:15:47] and then this function,
[00:15:49] which may be a very big neural
net compares like tell you to
[00:15:52] what extent this output is
compatible with this input.
[00:15:55] Okay, I put an image of an
elephant, an elephant here,
[00:15:58] and then I put the label elephant.
[00:16:00] And I want the output of
this, the scaler output
[00:16:02] of this function to be, let's say zero.
[00:16:05] If I put another label
table, chair, cat, whatever,
[00:16:09] I want the output to be
large, larger than zero.
[00:16:13] Okay? So a measure of
incompatibility if you want,
[00:16:16] between input and output.
[00:16:18] So the way you perform inference
[00:16:19] with a system like this is through search.
[00:16:21] You basically put an input
[00:16:24] and then you search for an output
[00:16:27] that minimizes the scaler output.
[00:16:29] The output is not represented
in implicit in those kind
[00:16:32] of square boxes.
[00:16:35] You, you search for an output
[00:16:36] that minimizes the energy function.
[00:16:42] And really this type of inference
[00:16:44] by optimization is very classical in AI
[00:16:48] or probabilistic inference
or this kind of stuff, right?
[00:16:50] There is a lot of really
classic, you know, a lot
[00:16:53] of classic work in past planning.
[00:16:57] You know, all kinds of
planning actually, you know,
[00:17:00] shortest path between
cities, sort of circuit
[00:17:03] between cities, sat, you know,
finding values of bullion,
[00:17:08] variables that satisfy bullion
formula, logical inference,
[00:17:11] all of those things can be
reduced to optimization problems,
[00:17:13] but not necessarily to forward propagation
[00:17:17] to a fixed number of layers.
[00:17:20] So this, this kind of inference
by optimization allows for
[00:17:26] what some people call zero
shot learning, which means
[00:17:29] producing answers
[00:17:31] or solution to problems
without being trained
[00:17:34] to produce solutions to that problem.
[00:17:35] Basically just coming up with
a new solution to a problem.
[00:17:38] Okay? This is what search
and optimization can do.
[00:17:44] This is also perhaps a good
model for the type of inference
[00:17:48] that takes place in humans,
that psychological system two.
[00:17:51] So system one is, you know,
decisions you're making
[00:17:53] or actions you're taking instinctively,
[00:17:55] basically without really having
to think about it too much.
[00:17:58] And system two is the, the
type of actions that you,
[00:18:02] or decisions you make deliberately by kind
[00:18:05] of thinking about it and
maybe using your mental model
[00:18:06] of the world to sort
of predict the outcome
[00:18:10] of particular actions you might take.
[00:18:14] Now, this is not what LMS are doing.
[00:18:17] Lms take a a window of
[00:18:23] a sequence over a sequence
of symbols, then run, run
[00:18:28] that through some big neural net
[00:18:29] and produce the next a guess
as to what the next symbol is.
[00:18:36] And then once you have
produced the next symbol,
[00:18:38] you shift it into the input
[00:18:39] and then you produce
a second symbol, shift
[00:18:41] that into the input,
third symbol, et cetera.
[00:18:43] That's called auto reverse prediction.
[00:18:45] And it's very classical,
it's been run with us for,
[00:18:48] you know, seven, seven decades
or something, if not more.
[00:18:55] Nothing new about that. But there is kind
[00:18:56] of a basic limitation with this
type of, of thing, which is
[00:19:00] that there's a fixed amount
of computation devoted
[00:19:02] to producing any single token.
[00:19:05] So the only way you can
entice a system of this type
[00:19:08] to spend more resources, more time
[00:19:12] on complicated question is
[00:19:14] to trick it into producing more tokens.
[00:19:16] This is a trick called
chain of thoughts, right?
[00:19:19] You, you, you tell the
system like, you know,
[00:19:21] tell me all the steps of
your, of your reasoning,
[00:19:25] which may not be reasoning actually.
[00:19:27] And as a consequence, the
system will just spend more,
[00:19:29] re more computation is is
going to produce more tokens.
[00:19:33] So it's going to spend more
[00:19:34] computation, but it's kind of a hack.
[00:19:36] There's another issue which
is perhaps even more dire,
[00:19:39] which is that auto, auto
aggressive generation.
[00:19:44] It's kind of a divergent process.
[00:19:46] You can never exactly predict what token
[00:19:49] or what word follows a particular text.
[00:19:52] What those systems are trying
to produce is basically a,
[00:19:54] a probability distribution
of all possible tokens,
[00:19:57] of which there is typically
about a hundred thousand
[00:19:59] possible tokens, right?
[00:20:01] So it's a big vector with of
numbers between zero and one.
[00:20:04] That's up to what, and you might,
[00:20:09] you know, pick, always pick the, the token
[00:20:12] with the highest variability
[00:20:13] and just generate the sequence this way.
[00:20:14] Or you might, you know,
sample from this distribution.
[00:20:19] Whatever you do, there is
might be some probability that
[00:20:22] at any point the token that's
generated takes you outside
[00:20:26] of the set of sequences of tokens
[00:20:28] that will be correct answers, right?
[00:20:30] So the set of all possible
se sequences of tokens
[00:20:34] is a tree, okay?
[00:20:35] Represented by this
blue disc, essentially,
[00:20:39] where each leaf is kind of
the terminal symbol in a tree.
[00:20:42] They don't have all the same
length, but it's a tree.
[00:20:47] Within this tree there
is a SubT tree, which,
[00:20:52] which corresponds to
all the correct answers
[00:20:55] corresponding to a particular point.
[00:20:57] And there's, there may be some
probability so that every,
[00:21:00] at every token you produce,
the token takes you outside
[00:21:05] of the sub, the correct SubT tree.
[00:21:09] Because it's a tree, there's
no way to come back, right?
[00:21:11] You're out, you're out. So
[00:21:17] if you make a, the
hypothesis, which of course is
[00:21:20] most likely wrong, that this, you know,
[00:21:23] probability is the same for regardless of
[00:21:26] where you are in the sequence
[00:21:27] and the errors are
independent, then the priority
[00:21:30] that a sequence of n
symbols would be correct
[00:21:34] decreases exponentially like
one minus the error rate
[00:21:37] to the power n and its number of tokens.
[00:21:40] Okay? This, this is one
way at LMS hallucinate.
[00:21:46] So you know,
[00:21:47] this is not really fixable
without some major redesign of
[00:21:50] how those systems produce their answers.
[00:21:54] We don't produce answers
[00:21:55] by just blurting one word after another.
[00:21:58] We think about the answer
we're going to produce, we have a,
[00:22:03] an abstract thought that
represents this answer,
[00:22:05] and then we turn it into text.
[00:22:06] Okay? But that's kind of a,
a second step if you want.
[00:22:13] There is an advantage
though to lms, which is
[00:22:15] that they're very easy to train
[00:22:16] and the training scales very well.
[00:22:18] So this is a representation
of GPT style architecture
[00:22:23] where basically secretly
[00:22:29] a large language model is actually trained
[00:22:30] to reproduce its input on its output.
[00:22:32] You give it a, a sequence of symbols
[00:22:33] and you train it to just
reproduce the sequence
[00:22:35] of symbols on its output,
[00:22:37] but it cannot just learn
the identity function
[00:22:39] because the connection is
designed in such a way that
[00:22:43] to produce one particular
symbol, this one, for example,
[00:22:46] this green one, it cannot look at the
[00:22:48] corresponding symbol on the input.
[00:22:49] It has to only compute it or,
[00:22:51] or predict it from the
symbols to the left of it.
[00:22:54] So simplicity is trained
to produce the next
[00:22:57] symbol in the sequence.
[00:22:59] And, but it does this in parallel
over very long sequences.
[00:23:02] It can do this very efficiently.
[00:23:04] So those GBT architecture scale,
[00:23:05] this is why people are
using, using them instead
[00:23:08] of alternatives at the moment,
[00:23:12] but it's very limited, okay?
[00:23:14] What we really want is
perhaps emulate disability
[00:23:18] that humans and animals have
to have a, a mental model
[00:23:21] of the world, a world model, okay?
[00:23:23] What is a world model? World model is
[00:23:27] given a representation of the
current state of the world,
[00:23:31] which you may have
estimated using by observing
[00:23:36] past, you know, observing the world
[00:23:39] and then, you know,
representing the its state,
[00:23:42] let's called it sx, given an action that
[00:23:47] you imagine taking, can you
predict a representation
[00:23:51] of the next state of the world
[00:23:52] that will result from taking this action?
[00:23:56] And the way you can train a
world model is very simple.
[00:23:58] You, you give it, you know,
a bunch of observations
[00:24:04] and then you, you run through
the encoder, the predictor,
[00:24:08] you give it an action that you,
[00:24:10] that you know is taking place there,
[00:24:13] and then you feed it the, the,
[00:24:17] the next state of the world basically.
[00:24:19] I mean, it's not state,
it's an observation.
[00:24:21] You run it through the same anchor
[00:24:22] as you run the previous state
that produces a representation
[00:24:25] for the new state of the world.
[00:24:27] And then you minimize the
prediction error, the difference
[00:24:29] between the representation
of the current state
[00:24:32] of the next state of the world,
[00:24:33] given the prediction obtained
from the previous state
[00:24:37] of the world obtained
[00:24:39] from perception.
[00:24:46] So one idea which is
very natural, which a lot
[00:24:49] of people have been working on,
including me for many years,
[00:24:52] is to use the same idea as LLMs, which is
[00:24:55] to train a generative model
[00:24:57] to predict what's going to
happen next in a video, right?
[00:25:00] So take a video to a full video,
[00:25:05] corrupt it by masking the
second half of it, let's say.
[00:25:09] Okay? And so this encoder
sees only the first half
[00:25:11] of the video, it produces
a representation of it
[00:25:16] and then runs this through some sort
[00:25:18] of decoder predictor decoder
that given the action
[00:25:21] that you know is taking
place in the video, produces
[00:25:25] the rest of the video at
the pixel level, okay?
[00:25:28] So it just predicts all
the details, everything
[00:25:31] that is supposed to
take place in the video.
[00:25:35] And that's essentially an impossible task.
[00:25:39] It's an impossible task
because there are many things
[00:25:42] that are, that can
plausibly happen in a video
[00:25:47] that may happen in a non-deterministic way
[00:25:49] that you cannot predict.
[00:25:51] And so if you train a neural
net to make a single prediction
[00:25:54] for what's going to happen next,
[00:25:57] the best thing you can do is
predict some sort of average
[00:25:59] or aggregate of all the
possible futures, right?
[00:26:02] And in fact, that's exactly what happened.
[00:26:03] So this is from a old paper,
almost 10 years ago now,
[00:26:07] we trained some, you know,
big neural net for the time
[00:26:11] with four frames
[00:26:12] and then train to predict
the next two frames.
[00:26:14] And the, the predictions
are really blurry.
[00:26:16] You see the same thing
here. So those are kind of
[00:26:19] little like symbolized
videos of cars being,
[00:26:23] being looked at from, from
the top on the highway.
[00:26:26] The central car here is fixed,
[00:26:28] and this is you not trying
to predict what the cars
[00:26:31] around it are going to do.
[00:26:32] And you get those blurry predictions
[00:26:33] because it doesn't know
if the car is going
[00:26:35] to accelerate or break.
[00:26:36] And so it predicts the average.
[00:26:39] Now using various techniques
with latent variables, you,
[00:26:43] you can feed your neural
net with latent variables
[00:26:46] that you either sample from a distribution
[00:26:49] or you optimize in some way.
[00:26:52] And you can correct this,
this flaw to some extent,
[00:26:56] and at least for simple videos,
[00:26:57] like those highways produce
videos that are crisp.
[00:27:00] And depending on the value
of the late end variable,
[00:27:03] we predict multiple
different features, right?
[00:27:05] So with a late end variable,
you can sort of parameterize
[00:27:08] all the potential plausible
[00:27:09] features that will happen in the video.
[00:27:11] Unfortunately, it doesn't
really work for natural videos.
[00:27:16] If I, if I take a, a video of this room
[00:27:19] and I pointed on this side
and I kind of rotate slowly
[00:27:23] and I stop here and I asked the system
[00:27:24] and predict, you know,
the rest of the video,
[00:27:29] it will predict we are in a room
[00:27:30] and the, you know, the chairs are red
[00:27:33] and there's probably a wall on the side.
[00:27:35] There's no way you can predict
the texture of the floor,
[00:27:37] the texture of the wall,
[00:27:38] and it, it cannot possibly
predict what all of you look like
[00:27:42] and, and where you sit, right?
[00:27:44] I mean, that information
is just not predictable.
[00:27:47] So, so either a system like that has
[00:27:52] to kind of make up some plausible
[00:27:56] instantiation of what may happen
[00:28:01] or predict a
[00:28:06] aggregate of everything that happens.
[00:28:08] But basically the, the
problem of predicting a,
[00:28:11] the pixel level, what goes on
in a, in a natural signals,
[00:28:14] particularly video, is
basically impossible.
[00:28:18] So you say, okay, well
we can do like an LM
[00:28:20] and LMS don't actually
predict a single token.
[00:28:22] They predict the distribution
of the tokens. Okay?
[00:28:24] So what that, what that
means is, is that we need to
[00:28:27] parameterize a distribution
over a high dimensional
[00:28:32] continuous space like the space
[00:28:33] of all possible video frames.
[00:28:35] And that's just
mathematically intractable.
[00:28:38] The best way we can represent
distributions is by,
[00:28:42] we can do, we can do it the
same way physicists do it.
[00:28:45] You write down an energy function
[00:28:46] and then you do ETO is energy function
[00:28:49] and normalize most of the
time that normalization term,
[00:28:53] which is a big integral,
which intractable at least
[00:28:58] for interesting distributions.
[00:29:00] So here's a proposal.
[00:29:02] The proposal is just don't
predict at the pixel level,
[00:29:06] predict at the representation level, okay?
[00:29:08] So we're going to build this
architecture, which I call jpa,
[00:29:11] that means joint embedding
predictive architecture.
[00:29:14] And basically instead of
predicting all the pixels,
[00:29:18] we're going to predict a
representation of the pixels.
[00:29:21] Okay? So we're going to run
the video through an encoder
[00:29:24] and this partially mass
video through an encoder,
[00:29:27] maybe the same encoder and simultaneously
[00:29:29] with the encoder train a predictor
[00:29:31] to minimize this prediction error.
[00:29:33] But the prediction is
going to take place in
[00:29:35] representation space.
[00:29:37] In the representation space.
[00:29:39] It's an abstract representation.
[00:29:40] It may not contain all the
details about the world
[00:29:43] that are just not predictable.
[00:29:46] We might eliminate all the
details that are not predictable,
[00:29:49] making the prediction tasks much simpler.
[00:29:53] So that's the comparison
between those two architectures.
[00:29:58] This is generative architectures,
predict all the details
[00:30:02] of the variables you want to predict,
[00:30:04] and this is the joint
predictive architecture.
[00:30:07] Find a representation within
which you can make predictions
[00:30:10] and that representation will
not contain all the details.
[00:30:15] Now, if you think about this, this is
[00:30:20] how we apprehend the world.
[00:30:22] We find representations that
allow us to make predictions.
[00:30:26] We don't represent the
world in all of it, all
[00:30:28] of its details.
[00:30:29] The entire purpose
[00:30:34] of science even is to
find those representations
[00:30:37] so we can make predictions,
[00:30:40] representations that ignore the details.
[00:30:43] So in fact, if I want to
[00:30:50] predict the trajectory
[00:30:52] of planets viewed from the earth, right?
[00:30:54] They seem kind of complicated
[00:30:56] because sometimes they go
forward, sometimes they'll,
[00:30:57] they go back, et cetera, right?
[00:31:00] And there's some periodicity
[00:31:01] and you know, people in the
intuity kind of figure out
[00:31:04] how, how to predict this.
[00:31:07] But it was kind of complicated
[00:31:08] until the appropriate representation
[00:31:11] for the problem was figured
out, which is that, you know,
[00:31:13] the earth rotates around the sun
[00:31:15] or the other planets rotate around the sun
[00:31:17] and they have elliptical orbits.
[00:31:19] And, and then it all becomes simpler
[00:31:21] and you can predict everything.
[00:31:22] And to predict the trajectory
of any planet like Jupiter,
[00:31:27] where, where is Jupiter going
[00:31:28] to be a hundred years from now?
[00:31:30] You don't need to know all detail,
[00:31:32] all the details about Jupiter.
[00:31:33] As a matter of fact, you only
only need to know six numbers,
[00:31:35] three positions and three
velocities, and that's it.
[00:31:40] So the question of finding
appropriate abstract
[00:31:43] representations that eliminate
all the details in such a way
[00:31:46] that they allow us to make
predictions is really fundamental
[00:31:49] to science and to intelligence in general.
[00:31:52] I, I would argue, in fact,
[00:31:57] to expand a little bit on, on
this dimension, in principle,
[00:32:00] I could describe everything
[00:32:01] that is taking place in this
room at the moment in terms
[00:32:04] of quantum field theory.
[00:32:08] I would have to measure the
wave function of, you know,
[00:32:11] all the quantum field in
this, in this room, which
[00:32:14] of course is an impossible task.
[00:32:15] And then I would have to have
some, you know, super gigantic
[00:32:18] powerful quantum computer
that would allow me to kind
[00:32:20] of make the, make the prediction,
[00:32:23] assuming there is not too
much interaction with the rest
[00:32:25] of the universe, which of
course is not the case.
[00:32:29] So it would be an impossible
task. So what do we do?
[00:32:31] We invent abstractions, okay?
[00:32:34] We have particles, we have
atoms on top of that, molecules
[00:32:39] on top of this in the living
world we have proteins,
[00:32:42] organelles, cells, organisms,
individuals, societies,
[00:32:46] ecosystems, right?
[00:32:49] So we, we have this whole
hierarchy of representations
[00:32:53] and at each level, each
level allows us to make kind
[00:32:57] of bigger, bolder,
longer term predictions,
[00:33:01] while eliminating a lot of
details about the level below.
[00:33:06] In physics, there is actually kind
[00:33:07] of a two systematic ways of doing this.
[00:33:10] One of them is called reorganization.
[00:33:12] Reorganization, or you know,
[00:33:14] with reorganization group theory is a way
[00:33:16] of basically representing
the state of a group of sites
[00:33:20] or particles or spins
[00:33:22] or whatever you want in sort
of a abstract way if you want.
[00:33:27] So as to kind of not have to
deal with like the details of,
[00:33:31] of the actual state.
[00:33:35] And similarly, in physics,
[00:33:39] there's a notion of entropy, right?
[00:33:42] I can make predictions about
the property of a box full
[00:33:46] of gas, pv equals NRT, right?
[00:33:48] If I, if I compress the gas,
[00:33:51] the temperature is going to go
up, you know, things like that.
[00:33:54] But I've ignored the position
of velocities of each
[00:33:58] of the individual molecules in the gas.
[00:34:01] And we call this entropy, right?
[00:34:03] We even have a name for the
information we let we leave
[00:34:06] behind when we go one
level up in the hierarchy.
[00:34:09] What's interesting about this hierarchy is
[00:34:11] that every level in the hierarchy is a
[00:34:13] different field of science.
[00:34:14] So perhaps a field of
science is actually defined
[00:34:17] for natural science at
least is defined by the
[00:34:20] abstraction level that we
choose to make predictions.
[00:34:25] Okay? So metro philosophy, okay?
[00:34:30] So if we have, if we're
able to train a system to,
[00:34:34] to have a, a mentor one model
of the, of the world, right?
[00:34:39] Allows you to predict what's
going to happen perhaps as a,
[00:34:42] as a consequence of its action.
[00:34:44] How can we use this as the
basis of an intelligent system?
[00:34:49] So I wrote this sort of vision paper
[00:34:55] three years ago that I put
online for comments about
[00:35:00] where I see AI research will
go over the next 10 years.
[00:35:04] This was before the edit craze,
[00:35:05] but I haven't changed my mind about this.
[00:35:10] And here's an example of how
this could be implemented.
[00:35:14] So, so this
[00:35:19] is a intelligent AI agent.
[00:35:21] It's observing the world
through a perception system
[00:35:23] that gives it an idea of the
current state of the world
[00:35:26] that it can currently perceive.
[00:35:29] Of course there is a lot that
the agent probably knows about
[00:35:32] the world that is not
currently perceivable.
[00:35:34] Like, you know, we, you know,
we know the state of our house
[00:35:38] to some extent and things like this.
[00:35:39] Like we have, you know,
a complete idea of the,
[00:35:42] the, the state of the world.
[00:35:43] So, which is totally in our memory,
[00:35:45] we don't current currently perceive it.
[00:35:46] So we might want to combine the,
[00:35:49] what we perceive about
the world with the content
[00:35:50] of a memory feed this to our world model.
[00:35:52] And a world model it's going to give,
[00:35:55] it is going to take an
imagined sequence of actions
[00:35:58] that we imagine taking
[00:35:59] and is going to predict
the resulting state
[00:36:04] of the world or sequence of states
[00:36:06] that the world is going to go
through as a consequence
[00:36:08] of the actions that we imagine taking.
[00:36:11] Now what we can do is
feed this predicted state
[00:36:15] to a task objective that
measures to what extent.
[00:36:17] So that's an energy
function that measures to
[00:36:20] what extent a particular
task has been accomplished.
[00:36:23] A goal has been reached. So
this guy will produce a scaler.
[00:36:27] I put zero if the task
has been accomplished
[00:36:32] and a positive larger
number if it's, if it's not,
[00:36:35] and you know, potentially
indicates some distance to the,
[00:36:39] to the objective, but we might
have other cost functions,
[00:36:42] other objectives that are
guardrails, which would, you know,
[00:36:45] prevent the system from
sort of taking actions that
[00:36:49] would not be safe, right?
[00:36:50] So if I have a domestic robot
[00:36:52] and I ask it to, you know,
get me coffee, it goes
[00:36:55] to the coffee machine and there
is someone standing in front
[00:36:57] of the coffee machine, I
don't want the robot to just,
[00:36:59] you know, slash that person
to pieces to get access
[00:37:02] to the coffee machine.
[00:37:03] So, you know, obviously we
need to kind of hardwire some
[00:37:08] guard rail objectives
into, into that robot
[00:37:12] and that robot would not be able to escape
[00:37:17] those guardrails because
the way it operates,
[00:37:20] the way it produces an
output is that it searches
[00:37:24] for an action sequence, which according
[00:37:25] to its internal role model,
[00:37:27] would actually satisfy those objectives,
[00:37:30] the task objective and the guard rails.
[00:37:33] And it can't escape that This
is by construction, okay?
[00:37:35] So if you put a guard rail in it,
[00:37:37] it has no choice but to satisfy it.
[00:37:42] And so this is an example
of this influenced
[00:37:44] by optimization I was
telling you about before.
[00:37:46] Really this, what it says
is planning is an example
[00:37:49] of classical planning as
it is used in robotics.
[00:37:57] Now, if we have a one model
that can make predictions
[00:38:00] to a certain horizon,
[00:38:02] we can probably apply it multiple
times in a auto aggressive
[00:38:05] fashion and feed it with a
sequence of actions every time.
[00:38:10] And so perhaps this one model
is just a mechanical model
[00:38:14] of a robot arm or something.
[00:38:15] And so it's very simple, very simple thing
[00:38:18] and we can, it's a differential
equation for example,
[00:38:20] that we can apply multiple times.
[00:38:23] And in fact, this is a
classical way in optimal control
[00:38:25] of planning a sequence of actions.
[00:38:27] You have a model of the system
you're controlling generally
[00:38:30] a set of handwritten equations,
[00:38:32] but in our case we're going to learn it.
[00:38:34] And then the cost function that
characterize whether whether
[00:38:37] a task is, has been accomplished.
[00:38:39] And then you plan by optimization,
a sequence of controls
[00:38:42] or actions that will
minimize this cost subject
[00:38:45] to maybe some constraints.
[00:38:49] Comput, classical and
optical control is called NPC
[00:38:51] model predictive control.
[00:38:53] But what's complicated about this here is
[00:38:55] that this world model may
be really complicated,
[00:38:58] maybe some big neural net that
is trained from lots of data.
[00:39:02] The input may be video, the
actions may be co complicated.
[00:39:05] There may be some discreet
[00:39:06] and non-continuous behavior
in the, the, the function,
[00:39:12] the cost function in the space
[00:39:15] of those actions may
be extremely irregular
[00:39:17] and maybe non-continuous.
[00:39:18] Maybe even if all those modules
are mostly differentiable,
[00:39:23] they could be kind of
non-continuous thing.
[00:39:25] So for example, if I, if
I want to go from where I,
[00:39:28] where I am standing now
to the other side of the,
[00:39:33] of the desk here, I can choose to go
[00:39:36] to this side and that side.
[00:39:37] And that's a discreet choice,
which will result in two
[00:39:41] completely different costs
[00:39:43] for migrating to the other side.
[00:39:46] Okay? It's going to be more costly
if I go this side than if I
[00:39:48] go from that, that side.
[00:39:51] Yet the difference in action
that I can take to choose
[00:39:54] between those two is, is very small.
[00:39:57] I can change my initial
action from, you know,
[00:40:01] taking a step in this direction
[00:40:03] to keep taking a step in that direction.
[00:40:04] That could be a very small change,
[00:40:06] yet it's going to result in a
discontinuous change in cost.
[00:40:09] So those functions are
going to be very complicated.
[00:40:11] This is going to pose,
since we're supposed
[00:40:15] to talk about geometry, you know, this,
[00:40:18] this is going to pose some like
major issues in optimization
[00:40:21] here that are not really solved that a lot
[00:40:23] of optimization people
have been thinking of
[00:40:25] for many decades actually in
the context of optimal control.
[00:40:28] But, but here it's even more
complicated given the fact
[00:40:32] that those world models might end up
[00:40:34] being very large neural nets.
[00:40:37] The world is not entirely predictable.
[00:40:38] So the, the way you
handle non-determinism is,
[00:40:44] is through latent variables.
[00:40:45] Neural nets are deterministic functions,
[00:40:47] but you can feed them with
latent variables that are
[00:40:50] sampled from a distribution
[00:40:52] or maybe inferred another way,
[00:40:54] which basically parameterize the set
[00:40:56] of plausible predictions.
[00:40:58] And then the planning problem
becomes even more complicated.
[00:41:01] Now because you don't
know the value of latent
[00:41:02] and you have to plan in the context
[00:41:06] of uncertainty, essentially.
[00:41:10] Ultimately what we want to do
is build a model like this.
[00:41:12] And I should tell you right
now, nobody has done this, okay?
[00:41:15] But build a model that is
hierarchical in the way
[00:41:18] that I was describing
earlier in such a way
[00:41:21] that we can use it to, to
do hierarchical planning.
[00:41:24] What does that mean? If I'm
sitting in my office at NYU
[00:41:27] and I decided I want to
be in Paris tomorrow,
[00:41:31] I cannot possibly plan my entire
[00:41:34] trajectory from New York to Paris in terms
[00:41:38] of elementary actions I
can take, which in the case
[00:41:41] of humans are millisecond by
millisecond muscle controls.
[00:41:47] I have to plan on a much
higher level, right?
[00:41:49] Which would be okay, I mean
New York, the best way to go
[00:41:54] to Paris is to go to the airport
[00:41:55] and catch a plane that
requires a, a mentor, one model
[00:42:00] of, you know, what does it
mean to go to the airport
[00:42:02] and to catch a plane
[00:42:05] and what, you know, what a plane
can do and things like that.
[00:42:08] But it's a very abstract
model at a very abstract level
[00:42:12] where the actions are very
high level things like,
[00:42:18] you know, things like taking a taxi
[00:42:21] or something to go to the airport
[00:42:23] or things like, you know,
getting a t airplane ticket
[00:42:28] or something like that and,
and, and jumping on a plane.
[00:42:32] But I have a sub sub goal
now, which is getting
[00:42:36] to the airport and maybe my
sub goal, my my cost function,
[00:42:39] my new cost function is not
my distance to Paris anymore,
[00:42:41] but it's my distance to the airport.
[00:42:44] Okay? So now it's a shorter
objectives objective.
[00:42:49] I want to go to the
airport, I mean New York.
[00:42:51] So I can just go down on the
street and hear the taxi.
[00:42:56] Now my sub goal is going
down on the street.
[00:42:58] How do I go on the street? I'm
sitting in my office, I need
[00:43:00] to go to the elevator, push the button,
[00:43:02] get into the elevator,
walk out the building.
[00:43:06] How do I go to the elevator?
[00:43:07] I need to stand up for
my chair, pick up my bag,
[00:43:09] open the door, shut my door,
avoid all the obstacles,
[00:43:13] you know, say bye bye to my
students, blah, blah, blah.
[00:43:16] There's a point in this hierarchy
[00:43:18] where I have all the information I need
[00:43:21] and I may not actually
need to plan formally,
[00:43:23] I can just take the action
[00:43:25] 'cause I'm kind of used to doing it.
[00:43:28] So I can revert to system
one, which is sort of reactive
[00:43:31] actions, okay?
[00:43:33] So this hierarchical planning
requires hierarchical role
[00:43:38] models that work at different timescales
[00:43:42] and different levels of abstraction.
[00:43:43] This is kind of a level of
abstraction of, you know, going
[00:43:46] to the streets and catching a taxi.
[00:43:50] And this is a high level
of abstraction of going
[00:43:52] to the airport and catching a plane.
[00:43:55] How do we train a system like this
[00:43:57] to learn the appropriate
level of abstractions?
[00:43:59] And then once we have it, how do we use it
[00:44:02] to plan hierarchically?
[00:44:03] The way I just described
this is completely unsolved.
[00:44:05] If you are, I don't know, studying A POG
[00:44:08] and ai, this is a good
problem to start thinking of.
[00:44:12] 'cause it's completely
unsolved, it's wide open.
[00:44:18] So put this whole thing together
[00:44:20] and you arrive at
[00:44:21] what some have called cognitive
architectures, which is kind
[00:44:24] of a way to put all of
those modules together.
[00:44:26] Perception, memory, which is kind
[00:44:28] of like the hippocampus
in the mammalian brain.
[00:44:32] The world model, which is
probably in the prefrontal cortex
[00:44:34] in humans, all kinds
of cost functions, some
[00:44:37] of which are really intrinsic costs
[00:44:39] that were kind of hardwired
into us by evolution,
[00:44:41] but many of them are costs
that we define ourselves.
[00:44:44] Basically some goals and things like this.
[00:44:46] And then a way to sort of
search for action sequences,
[00:44:50] which according to a world model,
[00:44:51] we produce the outcome we want.
[00:44:55] Okay? So we have kind of an overall
[00:44:57] architecture for the AI system.
[00:44:58] How are we going to train
those world models from
[00:45:02] observation using self
supervised learning?
[00:45:06] So the idea of those joint ing
architecture goes back a long
[00:45:08] time, the early nineties,
in fact, it was a, a type
[00:45:13] of model we used to call Siamese networks
[00:45:15] and they've kind of evolved over the,
[00:45:17] the last few years to some extent.
[00:45:20] And basically we have this
sort of architecture with,
[00:45:23] you know, two encoders, which may
[00:45:24] or may not be the same, a
predictor which may be conditioned
[00:45:27] by an action which may depend
on latent variables to account
[00:45:30] for the non-determinism
of the, of the world.
[00:45:35] And then some prediction,
error, cost, function,
[00:45:37] and maybe some other cost
functions that drive the system to
[00:45:41] learn appropriate representations.
[00:45:45] Okay? The way to conceptualize the, the,
[00:45:51] the way we want to train the
system of this type is really
[00:45:55] what a system of this type kind
[00:45:56] of basically produces a
scaler output, which as I said
[00:45:59] before, can be interpreted as an energy
[00:46:02] that measures the
incompatibility between the input
[00:46:04] and the output between X and Y.
[00:46:07] And what we need is a way to train or,
[00:46:10] or system in such a way that
it produces low energy for
[00:46:14] training samples that
we observe pairs of X
[00:46:16] and y that we observe
[00:46:17] and higher energies for
pairs that we do not observe.
[00:46:21] And that's where it becomes complicated.
[00:46:23] So let's imagine that we have
two scaler variables here, X
[00:46:25] and y and we have training samples
[00:46:28] that are those, those black dots.
[00:46:31] And the, what I want
is my learning machine
[00:46:34] to learn an energy function
that takes high values,
[00:46:37] that takes low value on the, you know,
[00:46:39] near the training samples
and higher values outside.
[00:46:43] So basically, you know,
some sort of landscape,
[00:46:46] it could be high dimensional
[00:46:47] because that depends on the,
you know, on the dimension
[00:46:52] of X and Y or at least the
representations of x and Y.
[00:46:56] So how do I do this?
[00:46:58] How do I train a parametrized function
[00:46:59] that produces a scaler
output to gimme low output
[00:47:03] for things I trained it on,
[00:47:05] but higher output for
things I don't train it on?
[00:47:08] There's two methods and,
[00:47:10] and basically a big issue
there is to prevent collapse.
[00:47:13] So if I just train a system like this
[00:47:17] to just minimize the prediction
error, I just show it pairs
[00:47:20] of X and y just minimize
the prediction error,
[00:47:25] it will collapse,
basically it will ignore X
[00:47:28] and y, it will produce SX
and XY that are constant
[00:47:32] and then the prediction
problem becomes trivial.
[00:47:35] And so the prediction error is zero,
[00:47:37] it's going to be zero for everything.
[00:47:39] Okay? Not a good way
[00:47:40] to capture the dependency between X and Y.
[00:47:43] So I need to have a way of making sure
[00:47:45] that their energy is large for things
[00:47:47] that the system is not trained on.
[00:47:50] And the advantage of representing a a, a a
[00:47:54] dependency between variables
as an implicit function
[00:47:57] of this type is that I, I
can represent dependencies
[00:48:01] between X and Y that
are not functions, okay?
[00:48:04] There's no function that maps X to Y here
[00:48:07] because there can be
multiple Ys for a given X.
[00:48:10] And so using an energy function
is basically an implicit
[00:48:14] function that represents
dependency between the two.
[00:48:19] Okay? So this energy
function can collapse if I,
[00:48:22] if I merely train it
to minimize the energy
[00:48:25] of those training samples,
which are those blue beads.
[00:48:28] Let's say this is X and
this is YI might end up
[00:48:31] with a energy surface
that is completely flat.
[00:48:34] So the way to prevent
this from happening is,
[00:48:37] there's two methods that I know about.
[00:48:38] One is contrasting methods.
[00:48:40] So you generate those green
points which are outside the
[00:48:44] manyfold of data if you want,
and you push the energy up.
[00:48:47] So change the parameters
of your neural net so
[00:48:50] that the energy goes
up that, I mean is high
[00:48:52] for those, those green dots.
[00:48:54] And the, the big question is
[00:48:55] how you generate those green dots.
[00:48:56] And then there's another
big question, which is that
[00:48:59] if the dimension of the space
within which you do this is
[00:49:01] high and the learning
machine is fairly flexible,
[00:49:05] then the number of those
contrasty points you're going to have
[00:49:08] to generate is going to go
exponentially with the dimension.
[00:49:11] And that's not a good idea.
It doesn't scale very well.
[00:49:15] I used to be a big fan of
those methods contributed
[00:49:18] to inventing them, but I became
very pessimistic about them.
[00:49:22] What I prefer is regularized methods.
[00:49:24] So those are methods that
basically have a, a term
[00:49:28] regularizing term that tries
to minimize the volume of space
[00:49:32] that can take low energy so
[00:49:34] that when you push down
the energy of certain parts
[00:49:36] of the space, the training
samples, the rest has to go up
[00:49:40] because there is only a, a limited amount
[00:49:42] of low energy volume to go around.
[00:49:46] So those are the two,
those are the two methods,
[00:49:48] the two categories methods,
[00:49:51] and I, I became kind of
more of a fan of the,
[00:49:54] the second category, I'll
come to this in a second.
[00:49:58] So you can
[00:50:02] sometimes turn energy based
models into poly models
[00:50:06] by using a Gibbs distribution,
[00:50:08] take exponential minus
the energy and normalize,
[00:50:11] and you get a properly
normalized conditional
[00:50:14] distribution of a given X.
[00:50:16] The problem is that most of
the time for any reasonable f
[00:50:20] the bottom is intractable.
[00:50:22] Intractable. And so you
don't need to deal with this,
[00:50:25] just deal with the energy directly.
[00:50:30] I made a list of various methods
[00:50:31] that people have proposed
over the decades as to
[00:50:35] they can be interpreted
in this framework in terms
[00:50:37] of whether they're contrastive
or, or regularized.
[00:50:41] I'm not going to go through the list,
[00:50:42] but it's interesting to
go through that exercise.
[00:50:48] So how are we going to use
this self supervised learning,
[00:50:52] perhaps let's say
contrastive to start with,
[00:50:56] to train the system, for
example, to represent images so
[00:50:58] that we can do image
recognition, for example.
[00:51:01] So the, the process is that we're going
[00:51:03] to train this joint embedding
architecture in some way,
[00:51:07] and then once it's trained,
we chop off the predictor.
[00:51:10] We just use the encoder, the encoder
[00:51:13] to produce a representation.
[00:51:15] And then we train a very
simple classifier on top
[00:51:17] of it using a supervised
learning to do, for example,
[00:51:20] image recognition
[00:51:21] or a depth estimation
or something like this.
[00:51:23] Contrastive methods are very
simple eist in showing pairs
[00:51:28] of images that are basically
d different version
[00:51:31] of the same, the same
content using distortion or
[00:51:35] or corruption of some kind.
[00:51:38] And then training the system
to produce a representation
[00:51:42] of the original image from, from the
[00:51:45] distorted or corrupted one.
[00:51:48] And then you have to
have contrastive samples,
[00:51:50] which are pairs of images
that you know are different.
[00:51:53] And then you push the
predicted representation
[00:51:56] and the actual representation
away from each other.
[00:51:58] Okay? So you have some loss
function that is going to pull
[00:52:02] those two guys together is
going to push those together away.
[00:52:07] And this kind of works,
[00:52:08] but it never produces
representations that fill spaces
[00:52:12] that are more than about 200
dimensions when you trend them
[00:52:14] on things like ImageNet.
[00:52:17] There's another type of
method called distillation,
[00:52:19] and those have been
considerably more successful.
[00:52:22] Those are sort of like
regularized methods also,
[00:52:25] although the main issue is
[00:52:26] that we don't really
understand why they work,
[00:52:29] although there is some theoretical work.
[00:52:31] So basically you take a, you
take an input, you transform
[00:52:35] or corrupt it, you get a
different version of it.
[00:52:38] You run this through an encoder
producer representation,
[00:52:41] run this through an encoder
with the same architecture,
[00:52:43] but slightly different weights,
then run through a predictor
[00:52:46] and then minimize his prediction error.
[00:52:48] But you don't back propagate
gradient through this encoder
[00:52:50] because you're not going to trend this.
[00:52:52] The weights of this encoder
through gradient descent,
[00:52:55] the weight of this encoder
are going to be essentially the
[00:52:57] weights of that encoder,
except you're going
[00:53:02] to accept those, those weights.
[00:53:05] This weight vector is
going to be a running average
[00:53:08] of the weight vectors of
that encoder over time.
[00:53:13] Okay? Take the past several
values of the weight vector
[00:53:17] and average them
[00:53:20] and that gives you the
weight of this encoder.
[00:53:22] Basically this encoder, the weight
[00:53:23] of this encoder cannot move as quickly
[00:53:27] as the weight of that ankle.
[00:53:28] This guy gets gradient back propagated
[00:53:30] and updates its weight and
then it basically updates the
[00:53:33] weight of this guy, which kind
of is a pass filtered version
[00:53:38] of the previous weight.
[00:53:41] Somehow this works, somehow
this doesn't collapse. Why?
[00:53:45] I don't know, it's kind of mysterious.
[00:53:49] The idea came from intuitions
from reinforcement planning
[00:53:52] for some, some reason, but
there is a bunch of methods.
[00:53:55] This one came from DeepMind,
those four came from,
[00:54:00] from, from my, my colleagues at at fair.
[00:54:04] And, and there is some
theoretical work also from some
[00:54:07] of my colleagues at fair
and that at Stanford that
[00:54:12] attempt to explain why
this does not collapse all,
[00:54:14] all every time.
[00:54:18] And if you make the
hypothesis that the encoder
[00:54:21] and the predictor are
linear, then you can show
[00:54:23] that there are fixed
points of the gradient
[00:54:25] and dynamics that are not collapsed.
[00:54:28] But that's the best explanation we have
[00:54:29] for, for why this works.
[00:54:31] But it's not entirely satisfactory.
[00:54:33] Also, it's very weird
[00:54:35] because there is no function
that you can monitor
[00:54:38] that goes down as you train
[00:54:41] because you're not actually
minimizing anything,
[00:54:43] even though you're
doing great in this end.
[00:54:45] It's very strange, but
it works really well.
[00:54:47] And so there's a, a technique,
a particular instance
[00:54:50] of this technique called Dino.
[00:54:53] It's made by French people at fair Paris.
[00:54:55] So they pronounce it Dino on
this side of pond de Dino.
[00:54:58] But, and it works really well.
[00:55:00] It produces really good
results when you train it on,
[00:55:04] you know, distorted versions
of ImageNet and whatever.
[00:55:06] And when you scale it up, you
have a very large network,
[00:55:10] a lot of training data.
[00:55:12] This, this paper is a few
months, a few months old.
[00:55:16] You can show that the performance
[00:55:18] of those self supervised
running systems surpasses
[00:55:22] or at least matches the
performance of purely supervised
[00:55:26] systems, but with considerably less data.
[00:55:30] Okay? So this is the first time it is,
[00:55:32] it is only a few months old
where, where it's very clear
[00:55:35] that four image understanding self
[00:55:40] supervised running now
surpasses the the best
[00:55:42] supervised running methods.
[00:55:44] So if you have money to
spend, you're better off kind
[00:55:46] of spending it on scientists to kind
[00:55:49] of fine tune self
supervised running methods
[00:55:51] and collect unsupervised
unlabeled data rather than spending
[00:55:55] it on people to label your data.
[00:55:59] And it wasn't clear until, you know, March
[00:56:01] or April, this Dino model is
really kind of ama amazing.
[00:56:06] It can produce generic
representations of images
[00:56:10] that can be used for all kinds
of applications, not just,
[00:56:14] you know, image like object recognition,
[00:56:16] but all kinds of stuff in medical imaging,
[00:56:18] in biological image analysis,
in astrophysics, in all kinds
[00:56:22] of, all kinds of domain remote
sensing, all kinds of stuff.
[00:56:26] And basically is, you know, produce state
[00:56:29] of the art performance
when you train ahead on top
[00:56:31] of the representation for a
wide variety of visual tasks
[00:56:37] that are either very cal
semantic or all level.
[00:56:40] Okay? But can we use those representations
[00:56:44] to train a world model so
that we can do planning
[00:56:46] as I was explaining earlier.
[00:56:48] And the answer is yes. So this is work by
[00:56:54] led by Lerrel Pinto, who is a colleague
[00:56:56] of mine at NYU Roboticist
[00:56:59] and myself with two of
our students, Gaoyue Zhou
[00:57:02] and Hengkai Pan.
[00:57:06] And what did, what we did
here is take the, the,
[00:57:09] the Dino encoder, so feed
images to the Dino encoder
[00:57:13] and then train a predictor on top of it,
[00:57:16] which is action condition.
[00:57:17] So that you have a view of the world
[00:57:20] and an action that you,
the robot is taking.
[00:57:22] Can you predict a representation,
the Dino representation
[00:57:25] of the, the next view of the world
[00:57:28] that results from taking this action?
[00:57:30] And then can you use it for
planning a trajectory so as
[00:57:32] to arrive at a, at a goal
[00:57:35] and fulfill the task and the answer is
[00:57:36] you can do this in certain cases
[00:57:38] and the performance is better than sort
[00:57:40] of previous systems that
people have worked on.
[00:57:41] Dream V three is a system from deep mind
[00:57:47] and, and this is, you know,
model PT control essentially.
[00:57:49] So start with an initial state, run this
[00:57:52] with a Dino encoder,
then run your world model
[00:57:54] with a hypothesized sequence of actions.
[00:57:57] Measure the distance with
a encoded target image
[00:58:00] and then through optimization,
figure out the sequence
[00:58:02] of actions that will
minimize this distance
[00:58:06] and then, you know,
[00:58:07] take the first few actions
in the actual environment
[00:58:10] and then perhaps replan.
[00:58:12] And this works really well,
let me skip ahead a little bit
[00:58:15] and show you a, a, a demo of
[00:58:19] that system for a particular task here.
[00:58:22] So the predictor has been trained sort
[00:58:23] of relatively generically, but these are
[00:58:26] target things.
[00:58:29] This is the initial state
[00:58:30] and these are the actions that
are planned by the system so
[00:58:33] as to move those blue
chips as close as possible
[00:58:36] to those configurations
[00:58:38] as possible in something like 25 actions.
[00:58:42] Okay? It's limited to 25 action.
[00:58:45] And this, this works pretty well.
[00:58:47] The, the dynamics of
the environment here is,
[00:58:49] is is pretty complicated
[00:58:52] because those blue chips kind
of interact with each other
[00:58:54] and everything and, and the
the same technique kind of,
[00:58:57] you know, works pretty well
for, for a wide variety of
[00:59:01] different environments.
[00:59:07] Let's see.
[00:59:13] Okay, we're going to have
to watch this video again
[00:59:14] because it doesn't want to
switch to the next slide.
[00:59:23] So this is far from perfect
in various respects,
[00:59:26] but it's kind of a good example of kind
[00:59:30] of learning a task zero shot.
[00:59:32] You don't need to train the
system to accomplish a task.
[00:59:35] It has a good role model.
[00:59:36] It will accomplish the task by planning.
[00:59:39] No, no need for training,
for reinforcement learning
[00:59:41] for anything, for learning
a policy or anything.
[00:59:43] Planning purely a similar project done by
[00:59:49] LED by AMIA Barr, who is
until recently a postdoc
[00:59:53] with me at at fair who is now
research scientist at fair.
[00:59:56] There's some demos you
can, you can look at here.
[00:59:59] And this is for navigation.
[01:00:00] So he took videos from mobile robots
[01:00:05] where you get a view from the robot
[01:00:08] and the robot moves, it
translates and rotates
[01:00:11] and you know, the transformation
[01:00:12] because you have a dormitory from the,
[01:00:14] from the wheels, you get a different view.
[01:00:16] Can you predict the next view
[01:00:18] of the world at the representation
level from the previous
[01:00:20] view and the displacement,
[01:00:22] the transformation matrix basically.
[01:00:25] And if you, if you can do
that, can you use it to plan?
[01:00:28] So, you know, can you
tell a robot here, like go
[01:00:31] to the blue trash can.
[01:00:33] It actually is, it's very far in the back,
[01:00:35] but it sees the blue trash can
[01:00:37] and it can sort of, you know,
plan a, a sequence of actions
[01:00:41] to go to the blue trash can.
[01:00:42] And this works pretty well.
[01:00:44] This paper actually won
the, this paper award
[01:00:49] mention at the last CVPR conference.
[01:00:53] It's pretty cool. I mean, I,
I think there is, you know,
[01:00:55] a lot of situations now that
we're going to be able to handle
[01:00:58] with those role models with
slightly more generic ways
[01:01:01] of training them, perhaps
like the ones I'm going
[01:01:04] to tell you about just now.
[01:01:07] So this is work, this is I jpa v jpa
[01:01:11] and V JPA two video JPA
two, which is more recent
[01:01:14] where it's again one of
those distillation type model
[01:01:18] where you, you have two encoders
[01:01:21] and they share the weight
with this exponential moving
[01:01:23] average trick.
[01:01:25] And you, you train the system
to predict a representation
[01:01:29] of a full image from a representation
[01:01:30] of a partial mass image using an encoder.
[01:01:34] And what we, we show
with this experiment is
[01:01:36] that this system, which is
not trained by reconstruction,
[01:01:39] purely joint embedding works, you know,
[01:01:41] trains really quickly
[01:01:42] and produces really good performance
[01:01:45] much better than an
alternative project done
[01:01:47] by our colleagues at fair.
[01:01:49] This is MAE master to encoder
[01:01:51] and this one is trained by reconstruction
[01:01:53] to predict pixels, right?
[01:01:55] So you take an, you take
a an image, you corrupt it
[01:01:58] by removing some patches
[01:01:59] and you train a gigantic system
[01:02:00] to reconstruct the full image.
[01:02:02] This basically was not a big success.
[01:02:05] You, the representations
you learn from this are not
[01:02:07] that great and it takes a long time.
[01:02:09] Also, more recently, there's a version
[01:02:13] of this too that works on video.
[01:02:14] So you take a video, you corrupt
it by masking a whole bunch
[01:02:17] of areas within the, the video
from, from the full video.
[01:02:22] And then you train again,
the system to predict
[01:02:24] the representation of full
video from the representation
[01:02:27] of the partially masked
one to a predictor.
[01:02:29] Perhaps the, the variable that
is fed here is the location
[01:02:33] of the places that are masked.
[01:02:37] And with you get at the end is
[01:02:39] that you get a good
representation of videos
[01:02:41] that you can use for classifying
actions for things like
[01:02:44] that and, and et cetera.
[01:02:47] But what's interesting about this is
[01:02:49] that it can learn some level
of common sense where it's able
[01:02:53] to do, if you show it a video
[01:02:55] where something impossible
occurs, like this ball is be,
[01:02:58] you know, is, is thrown in the air
[01:03:01] and just all of a sudden disappears,
[01:03:04] you apply this video JPA system
[01:03:06] with the sliding window over this video,
[01:03:09] the prediction error will shoot
to the roof when this occurs
[01:03:13] because it knows it's impossible.
[01:03:16] And so that's interesting
because that's kind
[01:03:17] of the first models that we have
[01:03:18] that have learned a little bit
of common sense if you want,
[01:03:22] or intuitive physics
completely unsupervised.
[01:03:25] So we have a long paper
that describes a whole bunch
[01:03:26] of experiments about this,
[01:03:27] which I don't have time to go through.
[01:03:30] And a new version of this
called VJPA version two
[01:03:35] more recent where you can, you
can see some examples there.
[01:03:39] And there there is two phases.
[01:03:40] One where we just train
on video, the other one
[01:03:42] where we train a predictor,
which is action conditions
[01:03:45] that we can use to plan
action sequences for robots.
[01:03:49] And let me show you a
short video of, of that.
[01:03:53] So this is an unfamiliar
environment the system has not been
[01:03:55] trained on and you know,
[01:03:59] it doesn't know a priority like
the, there's no calibration
[01:04:02] of the camera or, or whatever.
[01:04:04] And it's pretty robust
to the particular anatomy
[01:04:07] of the robot and the, and, and
the position of the camera.
[01:04:12] And it basically plans the
sequence of actions so as
[01:04:15] to reach a particular goal,
[01:04:16] which in this case is moving this cup,
[01:04:19] you know, down on the table.
[01:04:25] So let me skip ahead a little
bit, not bore you with tables
[01:04:29] of results of VGIV two.
[01:04:32] One technique that we are working on now,
[01:04:36] and we have some, some,
[01:04:37] some results about this in
the small cases is really how,
[01:04:42] how to prevent those systems from,
[01:04:44] from collapsing using regularized method.
[01:04:45] And one trick is to
basically have an estimate
[01:04:49] of the content, the quantity
[01:04:51] of information coming out of the encoder.
[01:04:53] If you can maximize the
information that comes out
[01:04:56] of the encoder, you'll prevent
the system from collapsing.
[01:05:02] And imagine that you
pass a bunch of samples
[01:05:05] through the encoder.
[01:05:08] So each row in this matrix
is a different sample
[01:05:10] and each column is a different variable
[01:05:12] of the representation
coming out of the ENC coda.
[01:05:15] You have two ways to kind of
maximize the information coming
[01:05:17] out, you know, contained in this matrix.
[01:05:19] One is you can make sure that all the rows
[01:05:21] of this matrix are different.
[01:05:23] So basically every sample has
a different representation.
[01:05:26] They don't all collapse to
having the same representation.
[01:05:29] And so this correspond to contrast methods
[01:05:33] or sample contrast methods.
[01:05:34] And then the alternative is to make sure
[01:05:36] that all the columns of
this matrix are different.
[01:05:39] In other words, every variable
in the representation carries
[01:05:42] a different information.
[01:05:45] Okay, one way to do this
in the first case is
[01:05:49] to compute the gram matrix of this matrix,
[01:05:51] basically the product of
this matrix based transpose
[01:05:54] and make sure that gram matrix
is close to the identity so
[01:05:58] that all the samples are
different or orthogonal.
[01:06:02] And this one is the converse.
[01:06:04] You compute the transpose
of this matrix times itself,
[01:06:09] which is the conveyance matrix,
[01:06:10] and try to make that conveyance
matrix close to identity.
[01:06:15] So this is a way of
basically, you know, kind
[01:06:17] of maximizing information
content in a representation,
[01:06:20] but it's approximate because we like
[01:06:22] to maximize information content
[01:06:23] and we don't have any know
bound on information content.
[01:06:25] We only have upper bounds
for very deep, deep reasons.
[01:06:30] The fact that we can't
kind of model all the,
[01:06:34] all the possible dependencies
between variables.
[01:06:36] All the estimate of information content
[01:06:38] that we have are upper bound,
are, are overestimations.
[01:06:42] And so it's a bit of a, it's
a bit of an issue there,
[01:06:47] but this technique that works
by getting the ance matrix
[01:06:51] with identity works really well.
[01:06:54] Let me skip ahead to the
last slide essentially.
[01:06:59] Okay, so I have a bunch
of recommendations here.
[01:07:03] Essentially, abandoned
generative models in favor
[01:07:06] of those joint embedding
predictive architectures
[01:07:09] that don't predict in the input space
[01:07:10] with predicting representation.
[01:07:11] Space predicting input space
works only if you have discreet
[01:07:16] symbols, but in the real
world, physical world, you have
[01:07:19] to learn representations.
[01:07:24] Use the energy based framework
[01:07:25] to really understand how this works.
[01:07:27] Probably stick modeling
basically leads to intractability
[01:07:32] and, and is unnecessary abandoned
[01:07:36] methods in favor
[01:07:38] of those regularized methods
I was telling you about.
[01:07:42] And I wouldn't say abandoned
reinforcement learning,
[01:07:46] but at least minimize the use
of reinforcement learning.
[01:07:48] 'cause reinforcement learning
is extremely inefficient,
[01:07:50] requires many trials,
[01:07:52] and so it, you have to
use it as a last resort.
[01:07:57] So when I say all of this,
these are all the pillars
[01:08:00] that are the most popular concepts
[01:08:03] in machine learning at the moment.
[01:08:04] Doesn't make me very popular,
particularly the first,
[01:08:09] the first one basically I
have to walk around with,
[01:08:16] with bodyguards in Silicon Valley.
[01:08:19] I'm joking. So basically if you are
[01:08:24] interested in sort of
getting AI to the next level
[01:08:26] to a human level, AI possibly,
[01:08:28] or maybe cat level, don't
work on LLMs, work on Gepa.
[01:08:33] Thank you very much.