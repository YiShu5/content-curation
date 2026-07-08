---
source_url: "https://www.youtube.com/watch?v=7xTGNNLPyMI"
platform: youtube
uploader: "Andrej Karpathy"
title: "Deep Dive into LLMs like ChatGPT"
upload_date: "20250205"
duration: 12683
fetched_at: "2026-06-22T08:01:23.362115Z"
transcript_source: youtube-transcript-api
---

[00:00:00] hi everyone so I've wanted to make this
[00:00:02] video for a while it is a comprehensive
[00:00:05] but General audience introduction to
[00:00:08] large language models like Chachi PT and
[00:00:11] what I'm hoping to achieve in this video
[00:00:12] is to give you kind of mental models for
[00:00:14] thinking through what it is that this
[00:00:17] tool is it is obviously magical and
[00:00:19] amazing in some respects it's uh really
[00:00:22] good at some things not very good at
[00:00:23] other things and there's also a lot of
[00:00:25] sharp edges to be aware of so what is
[00:00:28] behind this text box you can put
[00:00:29] anything in there and press enter but uh
[00:00:32] what should we be putting there and what
[00:00:34] are these words generated back how does
[00:00:36] this work and what what are you talking
[00:00:38] to exactly so I'm hoping to get at all
[00:00:40] those topics in this video we're going
[00:00:42] to go through the entire pipeline of how
[00:00:44] this stuff is built but I'm going to
[00:00:45] keep everything uh sort of accessible to
[00:00:48] a general audience so let's take a look
[00:00:50] at first how you build something like
[00:00:51] chpt and along the way I'm going to talk
[00:00:53] about um you know some of the sort of
[00:00:56] cognitive psychological implications of
[00:00:59] the tools okay so let's build Chachi PT
[00:01:02] so there's going to be multiple stages
[00:01:04] arranged sequentially the first stage is
[00:01:07] called the pre-training stage and the
[00:01:09] first step of the pre-training stage is
[00:01:11] to download and process the internet now
[00:01:13] to get a sense of what this roughly
[00:01:14] looks like I recommend looking at this
[00:01:16] URL here so um this company called
[00:01:20] hugging face uh collected and created
[00:01:23] and curated this data set called Fine
[00:01:26] web and they go into a lot of detail on
[00:01:28] this block post on how how they
[00:01:30] constructed the fine web data set and
[00:01:32] all of the major llm providers like open
[00:01:34] AI anthropic and Google and so on will
[00:01:36] have some equivalent internally of
[00:01:38] something like the fine web data set so
[00:01:41] roughly what are we trying to achieve
[00:01:42] here we're trying to get ton of text
[00:01:44] from the internet from publicly
[00:01:45] available sources so we're trying to
[00:01:47] have a huge quantity of very high
[00:01:50] quality documents and we also want very
[00:01:53] large diversity of documents because we
[00:01:55] want to have a lot of knowledge inside
[00:01:56] these models so we want large diversity
[00:01:59] of high quality documents and we want
[00:02:01] many many of them and achieving this is
[00:02:04] uh quite complicated and as you can see
[00:02:05] here takes multiple stages to do well so
[00:02:08] let's take a look at what some of these
[00:02:09] stages look like in a bit for now I'd
[00:02:11] like to just like to note that for
[00:02:13] example the fine web data set which is
[00:02:14] fairly representative what you would see
[00:02:16] in a production grade application
[00:02:18] actually ends up being only about 44
[00:02:20] terabyt of dis space um you can get a
[00:02:23] USB stick for like a terabyte very
[00:02:25] easily or I think this could fit on a
[00:02:27] single hard drive almost today so this
[00:02:29] is not a huge amount of data at the end
[00:02:31] of the day even though the internet is
[00:02:33] very very large we're working with text
[00:02:35] and we're also filtering it aggressively
[00:02:37] so we end up with about 44 terabytes in
[00:02:39] this example so let's take a look at uh
[00:02:42] kind of what this data looks like and
[00:02:44] what some of these stages uh also are so
[00:02:47] the starting point for a lot of these
[00:02:48] efforts and something that contributes
[00:02:50] most of the data by the end of it is
[00:02:52] Data from common crawl so common craw is
[00:02:56] an organization that has been basically
[00:02:57] scouring the internet since 2007 so as
[00:03:00] of 2024 for example common CW has
[00:03:03] indexed 2.7 billion web
[00:03:05] pages uh and uh they have all these
[00:03:08] crawlers going around the internet and
[00:03:09] what you end up doing basically is you
[00:03:11] start with a few seed web pages and then
[00:03:13] you follow all the links and you just
[00:03:15] keep following links and you keep
[00:03:16] indexing all the information and you end
[00:03:17] up with a ton of data of the internet
[00:03:19] over time so this is usually the
[00:03:21] starting point for a lot of the uh for a
[00:03:24] lot of these efforts now this common C
[00:03:26] data is quite raw and is filtered in
[00:03:27] many many different ways
[00:03:30] so here they Pro they document this is
[00:03:33] the same diagram they document a little
[00:03:35] bit the kind of processing that happens
[00:03:36] in these stages so the first thing here
[00:03:39] is something called URL
[00:03:41] filtering so what that is referring to
[00:03:43] is that there's these block
[00:03:47] lists of uh basically URLs that are or
[00:03:50] domains that uh you don't want to be
[00:03:52] getting data from so usually this
[00:03:54] includes things like U malware websites
[00:03:56] spam websites marketing websites uh
[00:03:58] racist websites adult sites and things
[00:04:01] like that so there's a ton of different
[00:04:02] types of websites that are just
[00:04:04] eliminated at this stage because we
[00:04:06] don't want them in our data set um the
[00:04:08] second part is text extraction you have
[00:04:10] to remember that all these web pages
[00:04:12] this is the raw HTML of these web pages
[00:04:14] that are being saved by these crawlers
[00:04:16] so when I go to inspect
[00:04:18] here this is what the raw HTML actually
[00:04:21] looks like you'll notice that it's got
[00:04:23] all this markup uh like lists and stuff
[00:04:26] like that and there's CSS and all this
[00:04:28] kind of stuff so this is um computer
[00:04:31] code almost for these web pages but what
[00:04:33] we really want is we just want this text
[00:04:35] right we just want the text of this web
[00:04:37] page and we don't want the navigation
[00:04:38] and things like that so there's a lot of
[00:04:40] filtering and processing uh and heris
[00:04:42] that go into uh adequately filtering for
[00:04:45] just their uh good content of these web
[00:04:48] pages the next stage here is language
[00:04:50] filtering so for example fine web
[00:04:53] filters uh using a language classifier
[00:04:56] they try to guess what language every
[00:04:58] single web page is in and then they only
[00:05:00] keep web pages that have more than 65%
[00:05:02] of English as an
[00:05:04] example and so you can get a sense that
[00:05:06] this is like a design decision that
[00:05:07] different companies can uh can uh take
[00:05:10] for themselves what fraction of all
[00:05:12] different types of languages are we
[00:05:14] going to include in our data set because
[00:05:15] for example if we filter out all of the
[00:05:17] Spanish as an example then you might
[00:05:19] imagine that our model later will not be
[00:05:21] very good at Spanish because it's just
[00:05:22] never seen that much data of that
[00:05:24] language and so different companies can
[00:05:26] focus on multilingual performance to uh
[00:05:28] to a different degree as an example so
[00:05:30] fine web is quite focused on English and
[00:05:33] so their language model if they end up
[00:05:35] training one later will be very good at
[00:05:36] English but not may be very good at
[00:05:38] other
[00:05:39] languages after language filtering
[00:05:41] there's a few other filtering steps and
[00:05:43] D duplication and things like that um
[00:05:46] finishing with for example the pii
[00:05:49] removal this is personally identifiable
[00:05:52] information so as an example addresses
[00:05:54] Social Security numbers and things like
[00:05:56] that you would try to detect them and
[00:05:57] you would try to filter out those kinds
[00:05:58] of web pages from the the data set as
[00:06:00] well so there's a lot of stages here and
[00:06:02] I won't go into full detail but it is a
[00:06:05] fairly extensive part of the
[00:06:06] pre-processing and you end up with for
[00:06:08] example the fine web data set so when
[00:06:10] you click in on it uh you can see some
[00:06:12] examples here of what this actually ends
[00:06:14] up looking like and anyone can download
[00:06:16] this on the huging phase web page and so
[00:06:19] here are some examples of the final text
[00:06:21] that ends up in the training set so this
[00:06:24] is some article about tornadoes in
[00:06:27] 2012 um so there's some t tadoes in 2020
[00:06:30] in 2012 and what
[00:06:33] happened uh this next one is something
[00:06:36] about did you know you have two little
[00:06:38] yellow 9vt battery sized adrenal glands
[00:06:41] in your body okay so this is some kind
[00:06:43] of a odd medical
[00:06:46] article so just think of these as
[00:06:49] basically uh web pages on the internet
[00:06:51] filtered just for the text in various
[00:06:53] ways and now we have a ton of text 40
[00:06:56] terabytes off it and that now is the
[00:06:58] starting point for the next step of this
[00:07:00] stage now I wanted to give you an
[00:07:02] intuitive sense of where we are right
[00:07:04] now so I took the first 200 web pages
[00:07:06] here and remember we have tons of them
[00:07:09] and I just take all that text and I just
[00:07:11] put it all together concatenate it and
[00:07:13] so this is what we end up with we just
[00:07:15] get this just just raw text raw internet
[00:07:18] text and there's a ton of it even in
[00:07:20] these 200 web pages so I can continue
[00:07:22] zooming out here and we just have this
[00:07:24] like massive tapestry of Text data and
[00:07:28] this text data has all these p patterns
[00:07:30] and what we want to do now is we want to
[00:07:31] start training neural networks on this
[00:07:33] data so the neural networks can
[00:07:35] internalize and model how this text
[00:07:39] flows right so we just have this giant
[00:07:42] texture of text and now we want to get
[00:07:45] neural Nets that mimic it okay now
[00:07:48] before we plug text into neural networks
[00:07:51] we have to decide how we're going to
[00:07:52] represent this text uh and how we're
[00:07:54] going to feed it in now the way our
[00:07:57] technology works for these neuron Lots
[00:07:58] is that they expect
[00:07:59] a one-dimensional sequence of symbols
[00:08:02] and they want a finite set of symbols
[00:08:05] that are possible and so we have to
[00:08:08] decide what are the symbols and then we
[00:08:10] have to represent our data as
[00:08:11] one-dimensional sequence of those
[00:08:14] symbols so right now what we have is a
[00:08:16] onedimensional sequence of text it
[00:08:18] starts here and it goes here and then it
[00:08:20] comes here Etc so this is a
[00:08:22] onedimensional sequence even though on
[00:08:23] my monitor of course it's laid out in a
[00:08:26] two-dimensional way but it goes from
[00:08:27] left to right and top to bottom right so
[00:08:29] it's a one-dimensional sequence of text
[00:08:32] now this being computers of course
[00:08:33] there's an underlying representation
[00:08:35] here so if I do what's called utf8 uh
[00:08:38] encode this text then I can get the raw
[00:08:41] bits that correspond to this text in the
[00:08:44] computer and that's what uh that looks
[00:08:46] like this so it turns out that for
[00:08:50] example this very first bar here is the
[00:08:53] first uh eight bits as an
[00:08:56] example so what is this thing right this
[00:08:59] is um representation that we are looking
[00:09:01] for uh in in a certain sense we have
[00:09:04] exactly two possible symbols zero and
[00:09:06] one and we have a very long sequence of
[00:09:10] it right now as it turns out um this
[00:09:14] sequence length is actually going to be
[00:09:16] very finite and precious resource uh in
[00:09:19] our neural network and we actually don't
[00:09:21] want extremely long sequences of just
[00:09:23] two symbols instead what we want is we
[00:09:25] want to trade off uh this um symbol
[00:09:29] size uh of this vocabulary as we call it
[00:09:32] and the resulting sequence length so we
[00:09:35] don't want just two symbols and
[00:09:36] extremely long sequences we're going to
[00:09:38] want more symbols and shorter sequences
[00:09:42] okay so one naive way of compressing or
[00:09:44] decreasing the length of our sequence
[00:09:46] here is to basically uh consider some
[00:09:49] group of consecutive bits for example
[00:09:51] eight bits and group them into a single
[00:09:54] what's called bite so because uh these
[00:09:57] bits are either on or off if we take a
[00:10:00] group of eight of them there turns out
[00:10:01] to be only 256 possible combinations of
[00:10:04] how these bits could be on or off and so
[00:10:06] therefore we can re repesent this
[00:10:07] sequence into a sequence of bytes
[00:10:10] instead so this sequence of bytes will
[00:10:13] be eight times shorter but now we have
[00:10:16] 256 possible symbols so every number
[00:10:19] here goes from 0 to
[00:10:20] 255 now I really encourage you to think
[00:10:22] of these not as numbers but as unique
[00:10:25] IDs or like unique symbols so maybe it's
[00:10:28] a bit more maybe it's better to actually
[00:10:30] think of these to replace every one of
[00:10:32] these with a unique Emoji you'd get
[00:10:34] something like this so um we basically
[00:10:37] have a sequence of emojis and there's
[00:10:38] 256 possible emojis you can think of it
[00:10:41] that way now it turns out that in
[00:10:44] production for state-of-the-art language
[00:10:46] models uh you actually want to go even
[00:10:48] Beyond this you want to continue to
[00:10:50] shrink the length of the sequence uh
[00:10:52] because again it is a precious resource
[00:10:54] in return for more symbols in your
[00:10:57] vocabulary and the way this is done is
[00:11:00] done by running what's called The Bite
[00:11:02] pair encoding algorithm and the way this
[00:11:04] works is we're basically looking for
[00:11:06] consecutive bytes or symbols that are
[00:11:10] very common so for example turns out
[00:11:13] that the sequence 116 followed by 32 is
[00:11:17] quite common and occurs very frequently
[00:11:19] so what we're going to do is we're going
[00:11:20] to group uh this um pair into a new
[00:11:24] symbol so we're going to Mint a symbol
[00:11:26] with an ID 256 and we're going to
[00:11:28] rewrite every single uh pair 11632 with
[00:11:32] this new symbol and then can we can
[00:11:34] iterate this algorithm as many times as
[00:11:36] we wish and each time when we mint a new
[00:11:38] symbol we're decreasing the length and
[00:11:40] we're increasing the symbol size and in
[00:11:43] practice it turns out that a pretty good
[00:11:45] setting of um the basically the
[00:11:48] vocabulary size turns out to be about
[00:11:49] 100,000 possible symbols so in
[00:11:52] particular GPT 4 uses
[00:11:55] 100,
[00:11:56] 277 symbols
[00:11:59] um and this process of converting from
[00:12:04] raw text into these symbols or as we
[00:12:07] call them tokens is the process called
[00:12:10] tokenization so let's now take a look at
[00:12:12] how gp4 performs tokenization conting
[00:12:15] from text to tokens and from tokens back
[00:12:18] to text and what this actually looks
[00:12:19] like so one website I like to use to
[00:12:21] explore these token representations is
[00:12:24] called tick tokenizer and so come here
[00:12:27] to the drop down and select CL 100 a
[00:12:29] base which is the gp4 base model
[00:12:32] tokenizer and here on the left you can
[00:12:34] put in text and it shows you the
[00:12:36] tokenization of that text so for example
[00:12:40] heo space
[00:12:43] world so hello world turns out to be
[00:12:46] exactly two Tokens The Token hello which
[00:12:49] is the token with ID
[00:12:51] 15339 and the token space
[00:12:54] world that is the token 1
[00:12:57] 1917 so um hello space world now if I
[00:13:02] was to join these two for example I'm
[00:13:04] going to get again two tokens but it's
[00:13:06] the token H followed by the token L
[00:13:09] world without the
[00:13:11] H um if I put in two Spa two spaces here
[00:13:15] between hello and world it's again a
[00:13:16] different uh tokenization there's a new
[00:13:19] token 220
[00:13:22] here okay so you can play with this and
[00:13:24] see what happens here also keep in mind
[00:13:26] this is not uh this is case sensitive so
[00:13:28] if this is a capital H it is something
[00:13:30] else or if it's uh hello world then
[00:13:35] actually this ends up being three tokens
[00:13:36] instead of just two
[00:13:41] tokens yeah so you can play with this
[00:13:43] and get an sort of like an intuitive
[00:13:44] sense of uh what these tokens work like
[00:13:47] we're actually going to loop around to
[00:13:48] tokenization a bit later in the video
[00:13:50] for now I just wanted to show you the
[00:13:51] website and I wanted to uh show you that
[00:13:53] this text basically at the end of the
[00:13:56] day so for example if I take one line
[00:13:57] here this is what GT4 will see it as so
[00:14:01] this text will be a sequence of length
[00:14:04] 62 this is the sequence here and this is
[00:14:08] how the chunks of text correspond to
[00:14:11] these symbols and again there's 100,
[00:14:16] 27777 possible symbols and we now have
[00:14:19] one-dimensional sequences of those
[00:14:21] symbols so um yeah we're going to come
[00:14:24] back to tokenization but that's uh for
[00:14:26] now where we are okay so what I've done
[00:14:28] now is I've taken this uh sequence of
[00:14:30] text that we have here in the data set
[00:14:32] and I have re-represented it using our
[00:14:34] tokenizer into a sequence of tokens and
[00:14:37] this is what that looks like now so for
[00:14:40] example when we go back to the Fine web
[00:14:41] data set they mentioned that not only is
[00:14:43] this 44 terab of dis space but this is
[00:14:45] about a 15 trillion token sequence of um
[00:14:50] in this data set and so here these are
[00:14:53] just some of the first uh one or two or
[00:14:56] three or a few thousand here I think uh
[00:14:58] tokens of this data set but there's 15
[00:15:01] trillion here uh to keep in mind and
[00:15:03] again keep in mind one more time that
[00:15:05] all of these represent little text
[00:15:07] chunks they're all just like atoms of
[00:15:09] these sequences and the numbers here
[00:15:11] don't make any sense they're just uh
[00:15:13] they're just unique IDs okay so now we
[00:15:17] get to the fun part which is the uh
[00:15:19] neural network training and this is
[00:15:21] where a lot of the heavy lifting happens
[00:15:23] computationally when you're training
[00:15:24] these neural networks so what we do here
[00:15:28] in this this step is we want to model
[00:15:30] the statistical relationships of how
[00:15:32] these tokens follow each other in the
[00:15:33] sequence so what we do is we come into
[00:15:36] the data and we take Windows of tokens
[00:15:40] so we take a window of tokens uh from
[00:15:43] this data fairly
[00:15:44] randomly and um the windows length can
[00:15:49] range anywhere anywhere between uh zero
[00:15:51] tokens actually all the way up to some
[00:15:54] maximum size that we decide on uh so for
[00:15:57] example in practice you could see a
[00:15:58] token with Windows of say 8,000 tokens
[00:16:01] now in principle we can use arbitrary
[00:16:03] window lengths of tokens uh but uh
[00:16:07] processing very long uh basically U
[00:16:10] window sequences would just be very
[00:16:12] computationally expensive so we just
[00:16:15] kind of decide that say 8,000 is a good
[00:16:16] number or 4,000 or 16,000 and we crop it
[00:16:19] there now in this example I'm going to
[00:16:22] be uh taking the first four tokens just
[00:16:25] so everything fits nicely so these
[00:16:28] tokens
[00:16:30] we're going to take a window of four
[00:16:32] tokens this bar view in and space single
[00:16:37] which are these token
[00:16:39] IDs and now what we're trying to do here
[00:16:41] is we're trying to basically predict the
[00:16:42] token that comes next in the sequence so
[00:16:45] 3962 comes next right so what we do now
[00:16:49] here is that we call this the context
[00:16:51] these four tokens are context and they
[00:16:54] feed into a neural
[00:16:56] network and this is the input to the
[00:16:58] neural network
[00:16:59] now I'm going to go into the detail of
[00:17:01] what's inside this neural network in a
[00:17:03] little bit for now it's important to
[00:17:04] understand is the input and the output
[00:17:06] of the neural net so the input are
[00:17:08] sequences of tokens of variable length
[00:17:12] anywhere between zero and some maximum
[00:17:14] size like 8,000 the output now is a
[00:17:17] prediction for what comes next so
[00:17:21] because our vocabulary has
[00:17:23] 100277 possible tokens the neural
[00:17:26] network is going to Output exactly that
[00:17:28] many numbers
[00:17:29] and all of those numbers correspond to
[00:17:30] the probability of that token as coming
[00:17:33] next in the sequence so it's making
[00:17:35] guesses about what comes
[00:17:37] next um in the beginning this neural
[00:17:39] network is randomly initialized so um
[00:17:42] and we're going to see in a little bit
[00:17:44] what that means but it's a it's a it's a
[00:17:46] random transformation so these
[00:17:48] probabilities in the very beginning of
[00:17:49] the training are also going to be kind
[00:17:51] of random uh so here I have three
[00:17:53] examples but keep in mind that there's
[00:17:55] 100,000 numbers here um so the
[00:17:58] probability of this token space
[00:17:59] Direction neural network is saying that
[00:18:01] this is 4% likely right now 11799 is 2%
[00:18:05] and then here the probility of 3962
[00:18:08] which is post is 3% now of course we've
[00:18:11] sampled this window from our data set so
[00:18:13] we know what comes next we know and
[00:18:16] that's the label we know that the
[00:18:18] correct answer is that 3962 actually
[00:18:19] comes next in the sequence so now what
[00:18:22] we have is this mathematical process for
[00:18:25] doing an update to the neural network we
[00:18:28] have the way of tuning it and uh we're
[00:18:30] going to go into a little bit of of
[00:18:32] detail in a bit but basically we know
[00:18:34] that this probability here of 3% we want
[00:18:38] this probability to be higher and we
[00:18:40] want the probabilities of all the other
[00:18:42] tokens to be
[00:18:44] lower and so we have a way of
[00:18:46] mathematically calculating how to adjust
[00:18:48] and update the neural network so that
[00:18:51] the correct answer has a slightly higher
[00:18:53] probability so if I do an update to the
[00:18:55] neural network now the next time I Fe
[00:18:59] this particular sequence of four tokens
[00:19:00] into neural network the neural network
[00:19:02] will be slightly adjusted now and it
[00:19:04] will say Okay post is maybe 4% and case
[00:19:07] now maybe is
[00:19:08] 1% and uh Direction could become 2% or
[00:19:12] something like that and so we have a way
[00:19:14] of nudging of slightly updating the
[00:19:16] neuronet to um basically give a higher
[00:19:19] probability to the correct token that
[00:19:21] comes next in the sequence and now you
[00:19:23] just have to remember that this process
[00:19:25] happens not just for uh this um token
[00:19:29] here where these four fed in and
[00:19:31] predicted this one this process happens
[00:19:33] at the same time for all of these tokens
[00:19:36] in the entire data set and so in
[00:19:38] practice we sample little windows little
[00:19:40] batches of Windows and then at every
[00:19:42] single one of these tokens we want to
[00:19:44] adjust our neural network so that the
[00:19:46] probability of that token becomes
[00:19:48] slightly higher and this all happens in
[00:19:50] parallel in large batches of these
[00:19:52] tokens and this is the process of
[00:19:54] training the neural network it's a
[00:19:55] sequence of updating it so that it's
[00:19:58] predictions match up the statistics of
[00:20:01] what actually happens in your training
[00:20:02] set and its probabilities become
[00:20:05] consistent with the uh statistical
[00:20:08] patterns of how these tokens follow each
[00:20:09] other in the data so let's now briefly
[00:20:12] get into the internals of these neural
[00:20:13] networks just to give you a sense of
[00:20:14] what's inside so neural network
[00:20:17] internals so as I mentioned we have
[00:20:19] these inputs uh that are sequences of
[00:20:22] tokens in this case this is four input
[00:20:24] tokens but this can be anywhere between
[00:20:26] zero up to let's say 8,000 tokens in
[00:20:30] principle this can be an infinite number
[00:20:31] of tokens we just uh it would just be
[00:20:33] too computationally expensive to process
[00:20:35] an infinite number of tokens so we just
[00:20:37] crop it at a certain length and that
[00:20:39] becomes the maximum context length of
[00:20:41] that uh
[00:20:42] model now these inputs X are mixed up in
[00:20:46] a giant mathematical expression together
[00:20:48] with the parameters or the weights of
[00:20:51] these neural networks so here I'm
[00:20:53] showing six example parameters and their
[00:20:56] setting but in practice these uh um
[00:21:00] modern neural networks will have
[00:21:01] billions of these uh parameters and in
[00:21:04] the beginning these parameters are
[00:21:06] completely randomly set now with a
[00:21:09] random setting of parameters you might
[00:21:11] expect that this uh this neural network
[00:21:13] would make random predictions and it
[00:21:15] does in the beginning it's totally
[00:21:16] random predictions but it's through this
[00:21:19] process of iteratively updating the
[00:21:22] network uh as and we call that process
[00:21:24] training a neural network so uh that the
[00:21:28] setting of these parameters gets
[00:21:29] adjusted such that the outputs of our
[00:21:31] neural network becomes consistent with
[00:21:34] the patterns seen in our training
[00:21:36] set so think of these parameters as kind
[00:21:39] of like knobs on a DJ set and as you're
[00:21:41] twiddling these knobs you're getting
[00:21:42] different uh predictions for every
[00:21:45] possible uh token sequence input and
[00:21:49] training in neural network just means
[00:21:50] discovering a setting of parameters that
[00:21:52] seems to be consistent with the
[00:21:54] statistics of the training
[00:21:56] set now let me just give you an example
[00:21:58] what this giant mathematical expression
[00:21:59] looks like just to give you a sense and
[00:22:01] modern networks are massive expressions
[00:22:03] with trillions of terms probably but let
[00:22:06] me just show you a simple example here
[00:22:08] it would look something like this I mean
[00:22:10] these are the kinds of Expressions just
[00:22:11] to show you that it's not very scary we
[00:22:13] have inputs x uh like X1 x2 in this case
[00:22:17] two example inputs and they get mixed up
[00:22:19] with the weights of the network w0 W1 2
[00:22:22] 3 Etc and this mixing is simple things
[00:22:27] like multiplication addition addition
[00:22:29] exponentiation division Etc and it is
[00:22:32] the subject of neural network
[00:22:34] architecture research to design
[00:22:36] effective mathematical Expressions uh
[00:22:39] that have a lot of uh kind of convenient
[00:22:41] characteristics they are expressive
[00:22:42] they're optimizable they're paralyzable
[00:22:45] Etc and so but uh at the end of the day
[00:22:48] these are these are not complex
[00:22:49] expressions and basically they mix up
[00:22:52] the inputs with the parameters to make
[00:22:54] predictions and we're optimizing uh the
[00:22:57] parameters of this neural network so
[00:22:59] that the predictions come out consistent
[00:23:01] with the training set now I would like
[00:23:04] to show you an actual production grade
[00:23:06] example of what these neural networks
[00:23:07] look like so for that I encourage you to
[00:23:09] go to this website that has a very nice
[00:23:11] visualization of one of these
[00:23:13] networks so this is what you will find
[00:23:16] on this website and this neural network
[00:23:19] here that is used in production settings
[00:23:21] has this special kind of structure this
[00:23:24] network is called the Transformer and
[00:23:26] this particular one as an example has 8
[00:23:28] 5,000 roughly
[00:23:30] parameters now here on the top we take
[00:23:33] the inputs which are the token
[00:23:36] sequences and then information flows
[00:23:39] through the neural network until the
[00:23:41] output which here are the logit softmax
[00:23:45] but these are the predictions for what
[00:23:46] comes next what token comes
[00:23:48] next and then here there's a sequence of
[00:23:52] Transformations and all these
[00:23:54] intermediate values that get produced
[00:23:56] inside this mathematical expression s it
[00:23:58] is sort of predicting what comes next so
[00:24:01] as an example these tokens are embedded
[00:24:04] into kind of like this distributed
[00:24:06] representation as it's called so every
[00:24:08] possible token has kind of like a vector
[00:24:10] that represents it inside the neural
[00:24:11] network so first we embed the tokens and
[00:24:15] then those values uh kind of like flow
[00:24:18] through this diagram and these are all
[00:24:20] very simple mathematical Expressions
[00:24:22] individually so we have layer norms and
[00:24:24] Matrix multiplications and uh soft Maxes
[00:24:27] and so on so here kind of like the
[00:24:28] attention block of this Transformer and
[00:24:31] then information kind of flows through
[00:24:33] into the multi-layer perceptron block
[00:24:35] and so on and all these numbers here
[00:24:38] these are the intermediate values of the
[00:24:40] expression and uh you can almost think
[00:24:42] of these as kind of like the firing
[00:24:44] rates of these synthetic neurons but I
[00:24:47] would caution you to uh not um kind of
[00:24:50] think of it too much like neurons
[00:24:52] because these are extremely simple
[00:24:53] neurons compared to the neurons you
[00:24:55] would find in your brain your biological
[00:24:57] neurons are very complex dynamical
[00:24:59] processes that have memory and so on
[00:25:01] there's no memory in this expression
[00:25:02] it's a fixed mathematical expression
[00:25:04] from input to Output with no memory it's
[00:25:06] just a
[00:25:07] stateless so these are very simple
[00:25:09] neurons in comparison to biological
[00:25:10] neurons but you can still kind of
[00:25:12] loosely think of this as like a
[00:25:13] synthetic piece of uh brain tissue if
[00:25:15] you if you like uh to think about it
[00:25:17] that way so information flows through
[00:25:21] all these neurons fire until we get to
[00:25:24] the predictions now I'm not actually
[00:25:26] going to dwell too much on the precise
[00:25:28] kind of like mathematical details of all
[00:25:30] these Transformations honestly I don't
[00:25:31] think it's that important to get into
[00:25:33] what's really important to understand is
[00:25:35] that this is a mathematical function it
[00:25:38] is uh parameterized by some fixed set of
[00:25:41] parameters like say 85,000 of them and
[00:25:44] it is a way of transforming inputs into
[00:25:46] outputs and as we twiddle the parameters
[00:25:48] we are getting uh different kinds of
[00:25:50] predictions and then we need to find a
[00:25:52] good setting of these parameters so that
[00:25:54] the predictions uh sort of match up with
[00:25:56] the patterns seen in training set
[00:25:59] so that's the Transformer okay so I've
[00:26:02] shown you the internals of the neural
[00:26:03] network and we talked a bit about the
[00:26:05] process of training it I want to cover
[00:26:07] one more major stage of working with
[00:26:10] these networks and that is the stage
[00:26:11] called inference so in inference what
[00:26:14] we're doing is we're generating new data
[00:26:16] from the model and so uh we want to
[00:26:18] basically see what kind of patterns it
[00:26:21] has internalized in the parameters of
[00:26:23] its Network so to generate from the
[00:26:26] model is relatively straightforward
[00:26:28] we start with some tokens that are
[00:26:30] basically your prefix like what you want
[00:26:32] to start with so say we want to start
[00:26:34] with the token 91 well we feed it into
[00:26:37] the
[00:26:37] network and remember that the network
[00:26:39] gives us probabilities right it gives us
[00:26:43] this probability Vector here so what we
[00:26:45] can do now is we can basically flip a
[00:26:47] biased coin so um we can sample uh
[00:26:52] basically a token based on this
[00:26:54] probability distribution so the tokens
[00:26:57] that are given High probability by the
[00:26:59] model are more likely to be sampled when
[00:27:01] you flip this biased coin you can think
[00:27:03] of it that way so we sample from the
[00:27:05] distribution to get a single unique
[00:27:08] token so for example token 860 comes
[00:27:11] next uh so 860 in this case when we're
[00:27:14] generating from model could come next
[00:27:16] now 860 is a relatively likely token it
[00:27:18] might not be the only possible token in
[00:27:20] this case there could be many other
[00:27:21] tokens that could have been sampled but
[00:27:23] we could see that 86c is a relatively
[00:27:25] likely token as an example and indeed in
[00:27:27] our training examp example here 860 does
[00:27:29] follow 91 so let's now say that we um
[00:27:34] continue the process so after 91 there's
[00:27:36] a60 we append it and we again ask what
[00:27:39] is the third token let's sample and
[00:27:42] let's just say that it's 287 exactly as
[00:27:44] here let's do that again we come back in
[00:27:47] now we have a sequence of three and we
[00:27:49] ask what is the likely fourth token and
[00:27:52] we sample from that and get this one and
[00:27:55] now let's say we do it one more time we
[00:27:58] take those four we sample and we get
[00:28:00] this one and this
[00:28:02] 13659 uh this is not actually uh 3962 as
[00:28:06] we had before so this token is the token
[00:28:09] article uh instead so viewing a single
[00:28:12] article and so in this case we didn't
[00:28:15] exactly reproduce the sequence that we
[00:28:17] saw here in the training data so keep in
[00:28:20] mind that these systems are stochastic
[00:28:22] they have um we're sampling and we're
[00:28:25] flipping coins and sometimes we lock out
[00:28:28] and we reproduce some like small chunk
[00:28:30] of the text and training set but
[00:28:32] sometimes we're uh we're getting a token
[00:28:35] that was not verbatim part of any of the
[00:28:38] documents in the training data so we're
[00:28:40] going to get sort of like remixes of the
[00:28:43] data that we saw in the training because
[00:28:44] at every step of the way we can flip and
[00:28:47] get a slightly different token and then
[00:28:48] once that token makes it in if you
[00:28:50] sample the next one and so on you very
[00:28:52] quickly uh start to generate token
[00:28:55] streams that are very different from the
[00:28:57] token streams that UR
[00:28:58] in the training documents so
[00:29:00] statistically they will have similar
[00:29:02] properties but um they are not identical
[00:29:05] to your training data they're kind of
[00:29:06] like inspired by the training data and
[00:29:09] so in this case we got a slightly
[00:29:10] different sequence and why would we get
[00:29:12] article you might imagine that article
[00:29:14] is a relatively likely token in the
[00:29:16] context of bar viewing single Etc and
[00:29:21] you can imagine that the word article
[00:29:22] followed this context window somewhere
[00:29:24] in the training documents uh to some
[00:29:26] extent and we just happen to sample it
[00:29:28] here at that stage so basically
[00:29:31] inference is just uh predicting from
[00:29:33] these distributions one at a time we
[00:29:35] continue feeding back tokens and getting
[00:29:37] the next one and we uh we're always
[00:29:39] flipping these coins and depending on
[00:29:42] how lucky or unlucky we get um we might
[00:29:45] get very different kinds of patterns
[00:29:47] depending on how we sample from these
[00:29:49] probability distributions so that's
[00:29:51] inference so in most common scenarios uh
[00:29:55] basically downloading the internet and
[00:29:57] tokenizing it is is a pre-processing
[00:29:58] step you do that a single time and then
[00:30:01] uh once you have your token sequence we
[00:30:04] can start training networks and in
[00:30:06] Practical cases you would try to train
[00:30:08] many different networks of different
[00:30:10] kinds of uh settings and different kinds
[00:30:11] of arrangements and different kinds of
[00:30:13] sizes and so you''ll be doing a lot of
[00:30:15] neural network training and um then once
[00:30:18] you have a neural network and you train
[00:30:19] it and you have some specific set of
[00:30:21] parameters that you're happy with um
[00:30:24] then you can take the model and you can
[00:30:25] do inference and you can actually uh
[00:30:28] generate data from the model and when
[00:30:30] you're on chat GPT and you're talking
[00:30:31] with a model uh that model is trained
[00:30:33] and has been trained by open aai many
[00:30:36] months ago probably and they have a
[00:30:38] specific set of Weights that work well
[00:30:41] and when you're talking to the model all
[00:30:42] of that is just inference there's no
[00:30:44] more training those parameters are held
[00:30:47] fixed and you're just talking to the
[00:30:49] model sort of uh you're giving it some
[00:30:51] of the tokens and it's kind of
[00:30:53] completing token sequences and that's
[00:30:54] what you're seeing uh generated when you
[00:30:57] actually use the model on CH GPT so that
[00:30:59] model then just does inference alone so
[00:31:02] let's now look at an example of training
[00:31:04] an inference that is kind of concrete
[00:31:05] and gives you a sense of what this
[00:31:07] actually looks like uh when these models
[00:31:08] are trained now the example that I would
[00:31:10] like to work with and that I'm
[00:31:12] particularly fond of is that of opening
[00:31:14] eyes gpt2 so GPT uh stands for
[00:31:17] generatively pre-trained Transformer and
[00:31:19] this is the second iteration of the GPT
[00:31:21] series by open AI when you are talking
[00:31:23] to chat GPT today the model that is
[00:31:26] underlying all of the magic of that
[00:31:27] interaction is GPT 4 so the fourth
[00:31:30] iteration of that series now gpt2 was
[00:31:33] published in 2019 by openi in this paper
[00:31:36] that I have right here and the reason I
[00:31:39] like gpt2 is that it is the first time
[00:31:41] that a recognizably modern stack came
[00:31:44] together so um all of the pieces of gpd2
[00:31:48] are recognizable today by modern
[00:31:50] standards it's just everything has
[00:31:52] gotten bigger now I'm not going to be
[00:31:54] able to go into the full details of this
[00:31:55] paper of course because it is a
[00:31:57] technical publication but some of the
[00:31:59] details that I would like to highlight
[00:32:00] are as follows gpt2 was a Transformer
[00:32:03] neural network just like you were just
[00:32:05] like the neural networks you would work
[00:32:06] with today it was it had 1.6 billion
[00:32:10] parameters right so these are the
[00:32:12] parameters that we looked at here it
[00:32:14] would have 1.6 billion of them today
[00:32:16] modern Transformers would have a lot
[00:32:18] closer to a trillion or several hundred
[00:32:20] billion
[00:32:21] probably the maximum context length here
[00:32:24] was 1,24 tokens so it is when we are
[00:32:28] sampling chunks of Windows of tokens
[00:32:32] from the data set we're never taking
[00:32:34] more than 1,24 tokens and so when you
[00:32:36] are trying to predict the next token in
[00:32:38] a sequence you will never have more than
[00:32:40] 1,24 tokens uh kind of in your context
[00:32:43] in order to make that prediction now
[00:32:45] this is also tiny by modern standards
[00:32:47] today the token uh the context lengths
[00:32:49] would be a lot closer to um couple
[00:32:53] hundred thousand or maybe even a million
[00:32:55] and so you have a lot more context a lot
[00:32:56] more tokens in history history and you
[00:32:58] can make a lot better prediction about
[00:33:00] the next token in the sequence in that
[00:33:01] way and finally gpt2 was trained on
[00:33:04] approximately 100 billion tokens and
[00:33:06] this is also fairly small by modern
[00:33:08] standards as I mentioned the fine web
[00:33:10] data set that we looked at here the fine
[00:33:12] web data set has 15 trillion tokens uh
[00:33:14] so 100 billion is is quite
[00:33:16] small
[00:33:18] now uh I actually tried to reproduce uh
[00:33:21] gpt2 for fun as part of this project
[00:33:23] called lm. C so you can see my rup of
[00:33:27] doing that in this post on GitHub under
[00:33:30] the lm. C repository so in particular
[00:33:33] the cost of training gpd2 in 2019 what
[00:33:36] was estimated to be approximately
[00:33:39] $40,000 but today you can do
[00:33:41] significantly better than that and in
[00:33:42] particular here it took about one day
[00:33:45] and about
[00:33:47] $600 uh but this wasn't even trying too
[00:33:49] hard I think you could really bring this
[00:33:51] down to about $100 today now why is it
[00:33:55] that the costs have come down so much
[00:33:57] well number one these data sets have
[00:33:59] gotten a lot better and the way we
[00:34:01] filter them extract them and prepare
[00:34:03] them has gotten a lot more refined and
[00:34:05] so the data set is of just a lot higher
[00:34:08] quality so that's one thing but really
[00:34:10] the biggest difference is that our
[00:34:11] computers have gotten much faster in
[00:34:13] terms of the hardware and we're going to
[00:34:15] look at that in a second and also the
[00:34:17] software for uh running these models and
[00:34:20] really squeezing out all all the speed
[00:34:22] from the hardware as it is possible uh
[00:34:25] that software has also gotten much
[00:34:27] better as as everyone has focused on
[00:34:28] these models and try to run them very
[00:34:30] very
[00:34:31] quickly now I'm not going to be able to
[00:34:34] go into the full detail of this gpd2
[00:34:36] reproduction and this is a long
[00:34:37] technical post but I would like to still
[00:34:39] give you an intuitive sense for what it
[00:34:41] looks like to actually train one of
[00:34:43] these models as a researcher like what
[00:34:44] are you looking at and what does it look
[00:34:46] like what does it feel like so let me
[00:34:47] give you a sense of that a little bit
[00:34:50] okay so this is what it looks like let
[00:34:51] me slide this
[00:34:52] over so what I'm doing here is I'm
[00:34:55] training a gpt2 model right now
[00:34:58] and um what's happening here is that
[00:35:00] every single line here like this one is
[00:35:05] one update to the model so remember how
[00:35:08] here we are um basically making the
[00:35:12] prediction better for every one of these
[00:35:14] tokens and we are updating these weights
[00:35:15] or parameters of the neural net so here
[00:35:18] every single line is One update to the
[00:35:20] neural network where we change its
[00:35:22] parameters by a little bit so that it is
[00:35:24] better at predicting next token and
[00:35:26] sequence in particular every single line
[00:35:28] here is improving the prediction on 1
[00:35:32] million tokens in the training set so
[00:35:35] we've basically taken 1 million tokens
[00:35:39] out of this data set and we've tried to
[00:35:41] improve the prediction of that token as
[00:35:44] coming next in a sequence on all 1
[00:35:46] million of them
[00:35:49] simultaneously and at every single one
[00:35:51] of these steps we are making an update
[00:35:52] to the network for that now the number
[00:35:55] to watch closely is this number called
[00:35:57] loss and the loss is a single number
[00:36:00] that is telling you how well your neural
[00:36:02] network is performing right now and it
[00:36:05] is created so that low loss is good so
[00:36:08] you'll see that the loss is decreasing
[00:36:10] as we make more updates to the neural
[00:36:12] nut which corresponds to making better
[00:36:14] predictions on the next token in a
[00:36:16] sequence and so the loss is the number
[00:36:19] that you are watching as a neural
[00:36:20] network researcher and you are kind of
[00:36:22] waiting you're twiddling your thumbs uh
[00:36:24] you're drinking coffee and you're making
[00:36:26] sure that this looks good so that with
[00:36:28] every update your loss is improving and
[00:36:31] the network is getting better at
[00:36:32] prediction now here you see that we are
[00:36:36] processing 1 million tokens per update
[00:36:38] each update takes about 7 Seconds
[00:36:41] roughly and here we are going to process
[00:36:43] a total of 32,000 steps of
[00:36:47] optimization so 32,000 steps with 1
[00:36:50] million tokens each is about 33 billion
[00:36:52] tokens that we are going to process and
[00:36:54] we're currently only about 420 step 20
[00:36:57] out of 32,000 so we are still only a bit
[00:37:01] more than 1% done because I've only been
[00:37:03] running this for 10 or 15 minutes or
[00:37:05] something like
[00:37:06] that now every 20 steps I have
[00:37:09] configured this optimization to do
[00:37:11] inference so what you're seeing here is
[00:37:13] the model is predicting the next token
[00:37:15] in a sequence and so you sort of start
[00:37:17] it randomly and then you continue
[00:37:19] plugging in the tokens so we're running
[00:37:21] this inference step and this is the
[00:37:23] model sort of predicting the next token
[00:37:25] in the sequence and every time you see
[00:37:26] something appear that's a new
[00:37:29] token um so let's just look at this and
[00:37:34] you can see that this is not yet very
[00:37:35] coherent and keep in mind that this is
[00:37:37] only 1% of the way through training and
[00:37:39] so the model is not yet very good at
[00:37:41] predicting the next token in the
[00:37:42] sequence so what comes out is actually
[00:37:44] kind of a little bit of gibberish right
[00:37:47] but it still has a little bit of like
[00:37:48] local coherence so since she is mine
[00:37:51] it's a part of the information should
[00:37:53] discuss my father great companions
[00:37:55] Gordon showed me sitting over at and Etc
[00:37:59] so I know it doesn't look very good but
[00:38:00] let's actually scroll up and see what it
[00:38:04] looked like when I started the
[00:38:06] optimization so all the way here at
[00:38:10] step
[00:38:12] one so after 20 steps of optimization
[00:38:15] you see that what we're getting here is
[00:38:17] looks completely random and of course
[00:38:18] that's because the model has only had 20
[00:38:20] updates to its parameters and so it's
[00:38:22] giving you random text because it's a
[00:38:23] random Network and so you can see that
[00:38:25] at least in comparison to this model is
[00:38:27] starting to do much better and indeed if
[00:38:29] we waited the entire 32,000 steps the
[00:38:32] model will have improved the point that
[00:38:34] it's actually uh generating fairly
[00:38:36] coherent English uh and the tokens
[00:38:38] stream correctly um and uh they they
[00:38:42] kind of make up English a a lot
[00:38:44] better
[00:38:46] um so this has to run for about a day or
[00:38:49] two more now and so uh at this stage we
[00:38:52] just make sure that the loss is
[00:38:53] decreasing everything is looking good um
[00:38:56] and we just have to wait
[00:38:58] and now um let me turn now to the um
[00:39:02] story of the computation that's required
[00:39:05] because of course I'm not running this
[00:39:06] optimization on my laptop that would be
[00:39:08] way too expensive uh because we have to
[00:39:11] run this neural network and we have to
[00:39:12] improve it and we have we need all this
[00:39:14] data and so on so you can't run this too
[00:39:16] well on your computer uh because the
[00:39:18] network is just too large uh so all of
[00:39:21] this is running on the computer that is
[00:39:23] out there in the cloud and I want to
[00:39:25] basically address the compute side of
[00:39:27] the store of training these models and
[00:39:28] what that looks like so let's take a
[00:39:30] look okay so the computer that I'm
[00:39:32] running this optimization on is this 8X
[00:39:35] h100 node so there are eight h100s in a
[00:39:39] single node or a single computer now I
[00:39:42] am renting this computer and it is
[00:39:44] somewhere in the cloud I'm not sure
[00:39:45] where it is physically actually the
[00:39:47] place I like to rent from is called
[00:39:49] Lambda but there are many other
[00:39:50] companies who provide this service so
[00:39:52] when you scroll down you can see that uh
[00:39:55] they have some on demand pricing for
[00:39:57] um sort of computers that have these uh
[00:40:01] h100s which are gpus and I'm going to
[00:40:03] show you what they look like in a second
[00:40:06] but on demand 8times Nvidia h100 uh
[00:40:10] GPU this machine comes for $3 per GPU
[00:40:13] per hour for example so you can rent
[00:40:16] these and then you get a machine in a
[00:40:18] cloud and you can uh go in and you can
[00:40:20] train these
[00:40:21] models and these uh gpus they look like
[00:40:25] this so this is one h100 GPU uh this is
[00:40:29] kind of what it looks like and you slot
[00:40:30] this into your computer and gpus are
[00:40:32] this uh perfect fit for training your
[00:40:34] networks because they are very
[00:40:36] computationally expensive but they
[00:40:38] display a lot of parallelism in the
[00:40:40] computation so you can have many
[00:40:42] independent workers kind of um working
[00:40:44] all at the same time in solving uh the
[00:40:48] matrix multiplication that's under the
[00:40:50] hood of training these neural
[00:40:52] networks so this is just one of these
[00:40:54] h100s but actually you would put them
[00:40:56] you would put multiple of them together
[00:40:58] so you could stack eight of them into a
[00:41:00] single node and then you can stack
[00:41:02] multiple nodes into an entire data
[00:41:04] center or an entire system
[00:41:07] so when we look at a data
[00:41:12] center can't spell when we look at a
[00:41:15] data center we start to see things that
[00:41:16] look like this right so we have one GPU
[00:41:18] goes to eight gpus goes to a single
[00:41:19] system goes to many systems and so these
[00:41:22] are the bigger data centers and there of
[00:41:23] course would be much much more expensive
[00:41:26] um and what's happening is that all the
[00:41:28] big tech companies really desire these
[00:41:31] gpus so they can train all these
[00:41:33] language models because they are so
[00:41:35] powerful and that has is fundamentally
[00:41:37] what has driven the stock price of
[00:41:38] Nvidia to be $3.4 trillion today as an
[00:41:41] example and why Nvidia has kind of
[00:41:44] exploded so this is the Gold Rush the
[00:41:47] Gold Rush is getting the gpus getting
[00:41:50] enough of them so they can all
[00:41:52] collaborate to perform this optimization
[00:41:55] and they're what are they all doing
[00:41:56] they're all collaborating to predict the
[00:41:59] next token on a data set like the fine
[00:42:01] web data
[00:42:02] set this is the computational workflow
[00:42:05] that that basically is extremely
[00:42:06] expensive the more gpus you have the
[00:42:09] more tokens you can try to predict and
[00:42:10] improve on and you're going to process
[00:42:12] this data set faster and you can iterate
[00:42:15] faster and get a bigger Network and
[00:42:16] train a bigger Network and so on so this
[00:42:19] is what all those machines are look like
[00:42:20] are uh are doing and this is why all of
[00:42:24] this is such a big deal and for example
[00:42:26] this is a
[00:42:28] article from like about a month ago or
[00:42:30] so this is why it's a big deal that for
[00:42:31] example Elon Musk is getting 100,000
[00:42:34] gpus uh in a single Data Center and all
[00:42:38] of these gpus are extremely expensive
[00:42:40] are going to take a ton of power and all
[00:42:42] of them are just trying to predict the
[00:42:43] next token in the sequence and improve
[00:42:45] the network uh by doing so and uh get
[00:42:49] probably a lot more coherent text than
[00:42:50] what we're seeing here a lot faster okay
[00:42:52] so unfortunately I do not have a couple
[00:42:55] 10 or hundred million of dollars to
[00:42:57] spend on training a really big model
[00:42:59] like this but luckily we can turn to
[00:43:01] some big tech companies who train these
[00:43:04] models routinely and release some of
[00:43:06] them once they are done training so
[00:43:08] they've spent a huge amount of compute
[00:43:10] to train this network and they release
[00:43:12] the network at the end of the
[00:43:13] optimization so it's very useful because
[00:43:15] they've done a lot of compute for that
[00:43:18] so there are many companies who train
[00:43:19] these models routinely but actually not
[00:43:21] many of them release uh these what's
[00:43:23] called base models so the model that
[00:43:25] comes out at the end here is is what's
[00:43:27] called a base model what is a base model
[00:43:29] it's a token simulator right it's an
[00:43:32] internet text token simulator and so
[00:43:35] that is not by itself useful yet because
[00:43:38] what we want is what's called an
[00:43:39] assistant we want to ask questions and
[00:43:41] have it respond to answers these models
[00:43:43] won't do that they just uh create sort
[00:43:45] of remixes of the internet they dream
[00:43:48] internet pages so the base models are
[00:43:51] not very often released because they're
[00:43:52] kind of just only a step one of a few
[00:43:55] other steps that we still need to take
[00:43:56] to get in system
[00:43:58] however a few releases have been made so
[00:44:01] as an example the gbt2 model released
[00:44:04] the 1.6 billion sorry 1.5 billion model
[00:44:08] back in 2019 and this gpt2 model is a
[00:44:10] base model now what is a model release
[00:44:13] what does it look like to release these
[00:44:15] models so this is the gpt2 repository on
[00:44:18] GitHub well you need two things
[00:44:20] basically to release model number one we
[00:44:22] need the um python code usually that
[00:44:27] describes the sequence of operations in
[00:44:30] detail that they make in their model so
[00:44:34] um if you remember
[00:44:36] back this
[00:44:38] Transformer the sequence of steps that
[00:44:40] are taken here in this neural network is
[00:44:42] what is being described by this code so
[00:44:45] this code is sort of implementing the
[00:44:47] what's called forward pass of this
[00:44:49] neural network so we need the specific
[00:44:51] details of exactly how they wired up
[00:44:53] that neural network so this is just
[00:44:55] computer code and it's usually just a
[00:44:57] couple hundred lines of code it's not
[00:44:59] it's not that crazy and uh this is all
[00:45:01] fairly understandable and usually fairly
[00:45:03] standard what's not standard are the
[00:45:05] parameters that's where the actual value
[00:45:07] is what are the parameters of this
[00:45:09] neural network because there's 1.6
[00:45:11] billion of them and we need the correct
[00:45:13] setting or a really good setting and so
[00:45:15] that's why in addition to this source
[00:45:17] code they release the parameters which
[00:45:20] in this case is roughly 1.5 billion
[00:45:23] parameters and these are just numbers so
[00:45:25] it's one single list of 1.5 billion
[00:45:27] numbers the precise and good setting of
[00:45:30] all the knobs such that the tokens come
[00:45:32] out
[00:45:33] well so uh you need those two things to
[00:45:37] get a base model
[00:45:39] release
[00:45:41] now gpt2 was released but that's
[00:45:43] actually a fairly old model as I
[00:45:44] mentioned so actually the model we're
[00:45:46] going to turn to is called llama 3 and
[00:45:49] that's the one that I would like to show
[00:45:50] you next so llama 3 so gpt2 again was
[00:45:54] 1.6 billion parameters trained on 100
[00:45:55] billion tokens Lama 3 is a much bigger
[00:45:58] model and much more modern model it is
[00:46:00] released and trained by meta and it is a
[00:46:03] 45 billion parameter model trained on 15
[00:46:07] trillion tokens in very much the same
[00:46:09] way just much much
[00:46:11] bigger um and meta has also made a
[00:46:14] release of llama 3 and that was part of
[00:46:18] this
[00:46:19] paper so with this paper that goes into
[00:46:21] a lot of detail the biggest base model
[00:46:23] that they released is the Lama 3.1 4.5
[00:46:27] 405 billion parameter model so this is
[00:46:30] the base model and then in addition to
[00:46:32] the base model you see here
[00:46:33] foreshadowing for later sections of the
[00:46:35] video they also released the instruct
[00:46:37] model and the instruct means that this
[00:46:39] is an assistant you can ask it questions
[00:46:41] and it will give you answers we still
[00:46:43] have yet to cover that part later for
[00:46:45] now let's just look at this base model
[00:46:47] this token simulator and let's play with
[00:46:49] it and try to think about you know what
[00:46:51] is this thing and how does it work and
[00:46:53] um what do we get at the end of this
[00:46:55] optimization if you let this run Until
[00:46:57] the End uh for a very big neural network
[00:46:59] on a lot of data so my favorite place to
[00:47:02] interact with the base models is this um
[00:47:04] company called hyperbolic which is
[00:47:06] basically serving the base model of the
[00:47:09] 405b Llama 3.1 so when you go to the
[00:47:13] website and I think you may have to
[00:47:14] register and so on make sure that in the
[00:47:16] models make sure that you are using
[00:47:18] llama 3.1 405 billion base it must be
[00:47:22] the base model and then here let's say
[00:47:24] the max tokens is how many tokens we're
[00:47:26] going to be gener rating so let's just
[00:47:28] decrease this to be a bit less just so
[00:47:30] we don't waste compute we just want the
[00:47:32] next 128 tokens and leave the other
[00:47:34] stuff alone I'm not going to go into the
[00:47:36] full detail here um now fundamentally
[00:47:39] what's going to happen here is identical
[00:47:41] to what happens here during inference
[00:47:43] for us so this is just going to continue
[00:47:45] the token sequence of whatever you
[00:47:47] prefix you're going to give it so I want
[00:47:49] to first show you that this model here
[00:47:51] is not yet an assistant so you can for
[00:47:53] example ask it what is 2 plus 2 it's not
[00:47:56] going to tell you oh it's four uh what
[00:47:58] else can I help you with it's not going
[00:47:59] to do that because what is 2 plus 2 is
[00:48:02] going to be tokenized and then those
[00:48:05] tokens just act as a prefix and then
[00:48:07] what the model is going to do now is
[00:48:09] just going to get the probability for
[00:48:10] the next token and it's just a glorified
[00:48:12] autocomplete it's a very very expensive
[00:48:14] autocomplete of what comes next um
[00:48:17] depending on the statistics of what it
[00:48:18] saw in its training documents which are
[00:48:20] basically web
[00:48:22] pages so let's just uh hit enter to see
[00:48:25] what tokens it comes up with as a
[00:48:31] continuation okay so here it kind of
[00:48:32] actually answered the question and
[00:48:34] started to go off into some
[00:48:35] philosophical territory uh let's try it
[00:48:37] again so let me copy and paste and let's
[00:48:39] try again from scratch what is 2 plus
[00:48:45] two so okay so it just goes off again so
[00:48:49] notice one more thing that I want to
[00:48:50] stress is that the system uh I think
[00:48:53] every time you put it in it just kind of
[00:48:55] starts from scratch
[00:48:58] so it doesn't uh the system here is
[00:48:59] stochastic so for the same prefix of
[00:49:02] tokens we're always getting a different
[00:49:04] answer and the reason for that is that
[00:49:06] we get this probity distribution and we
[00:49:08] sample from it and we always get
[00:49:10] different samples and we sort of always
[00:49:11] go into a different territory uh
[00:49:13] afterwards so here in this case um I
[00:49:17] don't know what this is let's try one
[00:49:19] more
[00:49:22] time so it just continues on so it's
[00:49:25] just doing the stuff that it's saw on
[00:49:26] the internet right um and it's just kind
[00:49:29] of like regurgitating those uh
[00:49:31] statistical
[00:49:32] patterns so first things it's not an
[00:49:35] assistant yet it's a token autocomplete
[00:49:38] and second it is a stochastic system now
[00:49:42] the crucial thing is that even though
[00:49:44] this model is not yet by itself very
[00:49:46] useful for a lot of applications just
[00:49:49] yet um it is still very useful because
[00:49:52] in the task of predicting the next token
[00:49:54] in the sequence the model has learned a
[00:49:56] lot about the world and it has stored
[00:49:59] all that knowledge in the parameters of
[00:50:01] the network so remember that our text
[00:50:04] looked like this right internet web
[00:50:06] pages and now all of this is sort of
[00:50:08] compressed in the weights of the network
[00:50:11] so you can think of um these 405 billion
[00:50:15] parameters is a kind of compression of
[00:50:16] the internet you can think of the
[00:50:19] 45 billion parameters is kind of like a
[00:50:21] zip file uh but it's not a loss less
[00:50:25] compression it's a loss C compression
[00:50:27] we're kind of like left with kind of a
[00:50:28] gal of the internet and we can generate
[00:50:31] from it right now we can elicit some of
[00:50:34] this knowledge by prompting the base
[00:50:35] model uh accordingly so for example
[00:50:38] here's a prompt that might work to
[00:50:40] elicit some of that knowledge that's
[00:50:41] hiding in the parameters here's my top
[00:50:43] 10 list of the top landmarks to see in
[00:50:46] the
[00:50:48] pairs
[00:50:50] um and I'm doing it this way because I'm
[00:50:52] trying to Prime the model to now
[00:50:54] continue this list so let's see if that
[00:50:56] works when I press
[00:50:57] enter okay so you see that it started a
[00:51:00] list and it's now kind of giving me some
[00:51:02] of those
[00:51:03] landmarks and now notice that it's
[00:51:05] trying to give a lot of information here
[00:51:07] now you might not be able to actually
[00:51:09] fully trust some of the information here
[00:51:10] remember that this is all just a
[00:51:12] recollection of some of the internet
[00:51:14] documents and so the things that occur
[00:51:17] very frequently in the internet data are
[00:51:19] probably more likely to be remembered
[00:51:21] correctly compared to things that happen
[00:51:23] very infrequently so you can't fully
[00:51:25] trust some of the things that and some
[00:51:27] of the information that is here because
[00:51:28] it's all just a vague recollection of
[00:51:30] Internet documents because the
[00:51:32] information is not stored explicitly in
[00:51:34] any of the parameters it's all just the
[00:51:36] recollection that said we did get
[00:51:38] something that is probably approximately
[00:51:40] correct and I don't actually have the
[00:51:42] expertise to verify that this is roughly
[00:51:44] correct but you see that we've elicited
[00:51:46] a lot of the knowledge of the model and
[00:51:48] this knowledge is not precise and exact
[00:51:51] this knowledge is vague and
[00:51:53] probabilistic and statistical and the
[00:51:55] kinds of things that occur often are the
[00:51:57] kinds of things that are more likely to
[00:51:59] be remembered um in the model now I want
[00:52:02] to show you a few more examples of this
[00:52:04] model's Behavior the first thing I want
[00:52:05] to show you is this example I went to
[00:52:08] the Wikipedia page for zebra and let me
[00:52:10] just copy paste the first uh even one
[00:52:13] sentence
[00:52:14] here and let me put it here now when I
[00:52:17] click enter what kind of uh completion
[00:52:19] are we going to get so let me just hit
[00:52:23] enter there are three living species
[00:52:26] etc etc what the model is producing here
[00:52:29] is an exact regurgitation of this
[00:52:31] Wikipedia entry it is reciting this
[00:52:33] Wikipedia entry purely from memory and
[00:52:36] this memory is stored in its parameters
[00:52:39] and so it is possible that at some point
[00:52:41] in these 512 tokens the model will uh
[00:52:44] stray away from the Wikipedia entry but
[00:52:46] you can see that it has huge chunks of
[00:52:47] it memorized here uh let me see for
[00:52:50] example if this sentence
[00:52:51] occurs by now okay so this so we're
[00:52:55] still on track let me check
[00:52:58] here okay we're still on
[00:53:00] track it will eventually uh stray
[00:53:04] away okay so this thing is just recited
[00:53:07] to a very large extent it will
[00:53:08] eventually deviate uh because it won't
[00:53:11] be able to remember exactly now the
[00:53:13] reason that this happens is because
[00:53:14] these models can be extremely good at
[00:53:16] memorization and usually this is not
[00:53:18] what you want in the final model and
[00:53:20] this is something called regurgitation
[00:53:21] and it's usually undesirable to site uh
[00:53:24] things uh directly uh that you have
[00:53:26] trained on now the reason that this
[00:53:29] happens actually is because for a lot of
[00:53:31] documents like for example Wikipedia
[00:53:33] when these documents are deemed to be of
[00:53:35] very high quality as a source like for
[00:53:37] example Wikipedia it is very often uh
[00:53:40] the case that when you train the model
[00:53:42] you will preferentially sample from
[00:53:44] those sources so basically the model has
[00:53:46] probably done a few epochs on this data
[00:53:48] meaning that it has seen this web page
[00:53:50] like maybe probably 10 times or so and
[00:53:52] it's a bit like you like when you read
[00:53:54] some kind of a text many many times say
[00:53:56] you read something a 100 times uh then
[00:53:58] you'll be able to recite it and it's
[00:54:00] very similar for this model if it sees
[00:54:01] something way too often it's going to be
[00:54:03] able to recite it later from memory
[00:54:05] except these models can be a lot more
[00:54:07] efficient um like per presentation than
[00:54:10] human so probably it's only seen this
[00:54:12] Wikipedia entry 10 times but basically
[00:54:14] it has remembered this article exactly
[00:54:16] in its parameters okay the next thing I
[00:54:18] want to show you is something that the
[00:54:19] model has definitely not seen during its
[00:54:21] training so for example if we go to the
[00:54:24] paper uh and then we navigate to the
[00:54:26] pre-training data we'll see here that uh
[00:54:31] the data set has a knowledge cut off
[00:54:33] until the end of 2023 so it will not
[00:54:35] have seen documents after this point and
[00:54:38] certainly it has not seen anything about
[00:54:39] the 2024 election and how it turned out
[00:54:43] now if we Prime the model with the
[00:54:46] tokens from the future it will continue
[00:54:49] the token sequence and it will just take
[00:54:50] its best guess according to the
[00:54:51] knowledge that it has in its own
[00:54:53] parameters so let's take a look at what
[00:54:55] that could look like
[00:54:57] so the Republican Party kit
[00:54:59] Trump okay president of the United
[00:55:01] States from
[00:55:02] 2017 and let's see what it says after
[00:55:05] this point so for example the model will
[00:55:07] have to guess at the running mate and
[00:55:09] who it's against Etc so let's hit
[00:55:11] enter so here thingss that Mike Pence
[00:55:14] was the running mate instead of JD Vance
[00:55:17] and the ticket was against Hillary
[00:55:20] Clinton and Tim Kane so this is kind of
[00:55:23] a interesting parallel universe
[00:55:25] potentially of what could have happened
[00:55:26] happened according to the LM let's get a
[00:55:28] different sample so the identical prompt
[00:55:31] and let's
[00:55:33] resample so here the running mate was
[00:55:35] Ronda santis and they ran against Joe
[00:55:38] Biden and Camala Harris so this is again
[00:55:40] a different parallel universe so the
[00:55:42] model will take educated guesses and it
[00:55:44] will continue the token sequence based
[00:55:45] on this knowledge um and it will just
[00:55:48] kind of like all of what we're seeing
[00:55:49] here is what's called hallucination the
[00:55:51] model is just taking its best guess uh
[00:55:54] in a probalistic manner the next thing I
[00:55:56] would like to show you is that even
[00:55:58] though this is a base model and not yet
[00:56:00] an assistant model it can still be
[00:56:02] utilized in Practical applications if
[00:56:04] you are clever with your prompt design
[00:56:06] so here's something that we would call a
[00:56:08] few shot
[00:56:09] prompt so what it is here is that I have
[00:56:12] 10 words or 10 pairs and each pair is a
[00:56:16] word of English column and then a the
[00:56:19] translation in Korean and we have 10 of
[00:56:22] them and what the model does here is at
[00:56:25] the end we have teacher column and then
[00:56:27] here's where we're going to do a
[00:56:28] completion of say just five tokens and
[00:56:31] these models have what we call in
[00:56:33] context learning abilities and what
[00:56:35] that's referring to is that as it is
[00:56:37] reading this context it is learning sort
[00:56:40] of in
[00:56:41] place that there's some kind of a
[00:56:43] algorithmic pattern going on in my data
[00:56:46] and it knows to continue that pattern
[00:56:48] and this is called kind of like Inc
[00:56:50] context learning so it takes on the role
[00:56:53] of a
[00:56:54] translator and when we hit uh completion
[00:56:58] we see that the teacher translation is
[00:56:59] Sim which is correct um and so this is
[00:57:03] how you can build apps by being clever
[00:57:05] with your prompting even though we still
[00:57:06] just have a base model for now and it
[00:57:08] relies on what we call this um uh in
[00:57:11] context learning ability and it is done
[00:57:14] by constructing what's called a few shot
[00:57:15] prompt okay and finally I want to show
[00:57:17] you that there is a clever way to
[00:57:19] actually instantiate a whole language
[00:57:21] model assistant just by prompting and
[00:57:24] the trick to it is that we're structure
[00:57:26] a prompt to look like a web page that is
[00:57:29] a conversation between a helpful AI
[00:57:31] assistant and a human and then the model
[00:57:34] will continue that conversation so
[00:57:36] actually to write the prompt I turned to
[00:57:38] chat gbt itself which is kind of meta
[00:57:41] but I told it I want to create an llm
[00:57:43] assistant but all I have is the base
[00:57:45] model so can you please write my um uh
[00:57:50] prompt and this is what it came up with
[00:57:52] which is actually quite good so here's a
[00:57:54] conversation between an AI assistant and
[00:57:55] a human
[00:57:56] the AI assistant is knowledgeable
[00:57:58] helpful capable of answering wide
[00:57:59] variety of questions Etc and then here
[00:58:03] it's not enough to just give it a sort
[00:58:05] of description it works much better if
[00:58:07] you create this fot prompt so here's a
[00:58:10] few terms of human assistant human
[00:58:13] assistant and we have uh you know a few
[00:58:15] turns of conversation and then here at
[00:58:17] the end is we're going to be putting the
[00:58:19] actual query that we like so let me copy
[00:58:21] paste this into the base model prompt
[00:58:25] and now let me do human column and this
[00:58:28] is where we put our actual prompt why is
[00:58:31] the sky
[00:58:32] blue and uh let's uh
[00:58:37] run assistant the sky appears blue due
[00:58:40] to the phenomenon called R lights
[00:58:41] scattering etc etc so you see that the
[00:58:44] base model is just continuing the
[00:58:45] sequence but because the sequence looks
[00:58:47] like this conversation it takes on that
[00:58:49] role but it is a little subtle because
[00:58:52] here it just uh you know it ends the
[00:58:54] assistant and then just you know
[00:58:55] hallucinate Ates the next question by
[00:58:57] the human Etc so it'll just continue
[00:58:58] going on and on uh but you can see that
[00:59:01] we have sort of accomplished the task
[00:59:03] and if you just took this why is the sky
[00:59:06] blue and if we just refresh this and put
[00:59:09] it here then of course we don't expect
[00:59:10] this to work with a base model right
[00:59:12] we're just going to who knows what we're
[00:59:14] going to get okay we're just going to
[00:59:15] get more
[00:59:16] questions okay so this is one way to
[00:59:19] create an assistant even though you may
[00:59:21] only have a base model okay so this is
[00:59:24] the kind of brief summary of the things
[00:59:26] we talked about over the last few
[00:59:28] minutes now let me zoom out
[00:59:32] here and this is kind of like what we've
[00:59:34] talked about so far we wish to train LM
[00:59:37] assistants like chpt we've discussed the
[00:59:40] first stage of that which is the
[00:59:42] pre-training stage and we saw that
[00:59:44] really what it comes down to is we take
[00:59:45] Internet documents we break them up into
[00:59:47] these tokens these atoms of little text
[00:59:49] chunks and then we predict token
[00:59:51] sequences using neural networks the
[00:59:54] output of this entire stage is this base
[00:59:56] model it is the setting of The
[00:59:58] parameters of this network and this base
[01:00:01] model is basically an internet document
[01:00:03] simulator on the token level so it can
[01:00:05] just uh it can generate token sequences
[01:00:08] that have the same kind of like
[01:00:10] statistics as Internet documents and we
[01:00:12] saw that we can use it in some
[01:00:13] applications but we actually need to do
[01:00:15] better we want an assistant we want to
[01:00:17] be able to ask questions and we want the
[01:00:18] model to give us answers and so we need
[01:00:21] to now go into the second stage which is
[01:00:23] called the post-training stage so we
[01:00:26] take our base model our internet
[01:00:28] document simulator and hand it off to
[01:00:29] post training so we're now going to
[01:00:31] discuss a few ways to do what's called
[01:00:33] post training of these models these
[01:00:36] stages in post training are going to be
[01:00:38] computationally much less expensive most
[01:00:40] of the computational work all of the
[01:00:42] massive data centers um and all of the
[01:00:45] sort of heavy compute and millions of
[01:00:47] dollars are the pre-training stage but
[01:00:50] now we go into the slightly cheaper but
[01:00:52] still extremely important stage called
[01:00:54] post trining where we turn this llm
[01:00:57] model into an assistant so let's take a
[01:00:59] look at how we can get our model to not
[01:01:02] sample internet documents but to give
[01:01:04] answers to questions so in other words
[01:01:07] what we want to do is we want to start
[01:01:08] thinking about conversations and these
[01:01:10] are conversations that can be multi-turn
[01:01:13] so so uh there can be multiple turns and
[01:01:15] they are in the simplest case a
[01:01:17] conversation between a human and an
[01:01:19] assistant and so for example we can
[01:01:21] imagine the conversation could look
[01:01:22] something like this when a human says
[01:01:24] what is 2 plus2 the assistant should re
[01:01:25] respond with something like 2 plus 2 is
[01:01:27] 4 when a human follows up and says what
[01:01:29] if it was star instead of a plus
[01:01:31] assistant could respond with something
[01:01:32] like
[01:01:33] this um and similar here this is another
[01:01:36] example showing that the assistant could
[01:01:37] also have some kind of a personality
[01:01:39] here uh that it's kind of like nice and
[01:01:41] then here in the third example I'm
[01:01:43] showing that when a human is asking for
[01:01:44] something that we uh don't wish to help
[01:01:47] with we can produce what's called
[01:01:48] refusal we can say that we cannot help
[01:01:50] with that so in other words what we want
[01:01:53] to do now is we want to think through
[01:01:55] how in a system should interact with the
[01:01:57] human and we want to program the
[01:01:59] assistant and Its Behavior in these
[01:02:01] conversations now because this is neural
[01:02:03] networks we're not going to be
[01:02:04] programming these explicitly in code
[01:02:07] we're not going to be able to program
[01:02:08] the assistant in that way because this
[01:02:10] is neural networks everything is done
[01:02:12] through neural network training on data
[01:02:14] sets and so because of that we are going
[01:02:17] to be implicitly programming the
[01:02:19] assistant by creating data sets of
[01:02:21] conversations so these are three
[01:02:23] independent examples of conversations in
[01:02:25] a data dat set an actual data set and
[01:02:27] I'm going to show you examples will be
[01:02:29] much larger it could have hundreds of
[01:02:31] thousands of conversations that are
[01:02:32] multi- turn very long Etc and would
[01:02:34] cover a diverse breath of topics but
[01:02:37] here I'm only showing three examples but
[01:02:39] the way this works basically is uh a
[01:02:42] assistant is being programmed by example
[01:02:45] and where is this data coming from like
[01:02:47] 2 * 2al 4 same as 2 plus 2 Etc where
[01:02:50] does that come from this comes from
[01:02:51] Human labelers so we will basically give
[01:02:54] human labelers some conversational
[01:02:56] context and we will ask them to um
[01:02:58] basically give the ideal assistant
[01:03:00] response in this situation and a human
[01:03:03] will write out the ideal response for an
[01:03:06] assistant in any situation and then
[01:03:08] we're going to get the model to
[01:03:10] basically train on this and to imitate
[01:03:12] those kinds of
[01:03:14] responses so the way this works then is
[01:03:16] we are going to take our base model
[01:03:17] which we produced in the preing stage
[01:03:20] and this base model was trained on
[01:03:21] internet documents we're now going to
[01:03:23] take that data set of internet documents
[01:03:25] and we're gonna throw it out and we're
[01:03:27] going to substitute a new data set and
[01:03:29] that's going to be a data set of
[01:03:30] conversations and we're going to
[01:03:32] continue training the model on these
[01:03:33] conversations on this new data set of
[01:03:35] conversations and what happens is that
[01:03:37] the model will very rapidly adjust and
[01:03:40] will sort of like learn the statistics
[01:03:42] of how this assistant responds to human
[01:03:45] queries and then later during inference
[01:03:48] we'll be able to basically um Prime the
[01:03:51] assistant and get the response and it
[01:03:54] will be imitating what the humans will
[01:03:56] human labelers would do in that
[01:03:57] situation if that makes sense so we're
[01:04:00] going to see examples of that and this
[01:04:01] is going to become bit more concrete I
[01:04:03] also wanted to mention that this
[01:04:05] post-training stage we're going to
[01:04:06] basically just continue training the
[01:04:07] model but um the pre-training stage can
[01:04:10] in practice take roughly three months of
[01:04:13] training on many thousands of computers
[01:04:15] the post-training stage will typically
[01:04:16] be much shorter like 3 hours for example
[01:04:20] um and that's because the data set of
[01:04:21] conversations that we're going to create
[01:04:23] here manually is much much smaller than
[01:04:26] the data set of text on the internet and
[01:04:28] so this training will be very short but
[01:04:31] fundamentally we're just going to take
[01:04:33] our base model we're going to continue
[01:04:35] training using the exact same algorithm
[01:04:37] the exact same everything except we're
[01:04:39] swapping out the data set for
[01:04:40] conversations so the questions now are
[01:04:43] what are these conversations how do we
[01:04:44] represent them how do we get the model
[01:04:46] to see conversations instead of just raw
[01:04:49] text and then what are the outcomes of
[01:04:52] um this kind of training and what do you
[01:04:54] get in a certain like psychological
[01:04:56] sense uh when we talk about the model so
[01:04:58] let's turn to those questions now so
[01:05:01] let's start by talking about the
[01:05:02] tokenization of conversations everything
[01:05:05] in these models has to be turned into
[01:05:07] tokens because everything is just about
[01:05:08] token sequences so how do we turn
[01:05:10] conversations into token sequences is
[01:05:12] the question and so for that we need to
[01:05:15] design some kind of ending coding and uh
[01:05:17] this is kind of similar to maybe if
[01:05:18] you're familiar you don't have to be
[01:05:20] with for example the TCP IP packet in um
[01:05:23] on the internet there are precise rules
[01:05:25] and protocols for how you represent
[01:05:27] information how everything is structured
[01:05:29] together so that you have all this kind
[01:05:30] of data laid out in a way that is
[01:05:32] written out on a paper and that everyone
[01:05:34] can agree on and so it's the same thing
[01:05:36] now happening in llms we need some kind
[01:05:38] of data structures and we need to have
[01:05:40] some rules around how these data
[01:05:41] structures like conversations get
[01:05:43] encoded and decoded to and from tokens
[01:05:46] and so I want to show you now how I
[01:05:48] would
[01:05:49] recreate uh this conversation in the
[01:05:52] token space so if you go to Tech
[01:05:54] tokenizer
[01:05:56] I can take that conversation and this is
[01:05:58] how it is represented in uh for the
[01:06:01] language model so here we have we are
[01:06:03] iterating a user and an assistant in
[01:06:06] this two- turn
[01:06:08] conversation and what you're seeing here
[01:06:10] is it looks ugly but it's actually
[01:06:11] relatively simple the way it gets turned
[01:06:13] into a token sequence here at the end is
[01:06:16] a little bit complicated but at the end
[01:06:18] this conversation between a user and
[01:06:19] assistant ends up being 49 tokens it is
[01:06:22] a one-dimensional sequence of 49 tokens
[01:06:24] and these are the tokens
[01:06:26] okay and all the different llms will
[01:06:29] have a slightly different format or
[01:06:31] protocols and it's a little bit of a
[01:06:33] wild west right now but for example GPT
[01:06:36] 40 does it in the following way you have
[01:06:39] this special token called imore start
[01:06:42] and this is short for IM imaginary
[01:06:44] monologue uh the
[01:06:46] start then you have to specify um I
[01:06:49] don't actually know why it's called that
[01:06:50] to be honest then you have to specify
[01:06:52] whose turn it is so for example user
[01:06:54] which is a token 4
[01:06:56] 28 then you have internal monologue
[01:07:00] separator and then it's the exact
[01:07:03] question so the tokens of the question
[01:07:05] and then you have to close it so I am
[01:07:07] end the end of the imaginary monologue
[01:07:09] so
[01:07:10] basically the question from a user of
[01:07:13] what is 2 plus two ends up being the
[01:07:16] token sequence of these tokens and now
[01:07:19] the important thing to mention here is
[01:07:20] that IM start this is not text right IM
[01:07:24] start is a special token that gets added
[01:07:27] it's a new token and um this token has
[01:07:30] never been trained on so far it is a new
[01:07:32] token that we create in a post-training
[01:07:34] stage and we introduce and so these
[01:07:37] special tokens like IM seep IM start Etc
[01:07:40] are introduced and interspersed with
[01:07:42] text so that they sort of um get the
[01:07:45] model to learn that hey this is a the
[01:07:47] start of a turn for who is it start of
[01:07:49] the turn for the start of the turn is
[01:07:51] for the user and then this is what the
[01:07:54] user says and then the user ends and
[01:07:56] then it's a new start of a turn and it
[01:07:58] is by the assistant and then what does
[01:08:01] the assistant say well these are the
[01:08:02] tokens of what the assistant says Etc
[01:08:05] and so this conversation is not turned
[01:08:06] into the sequence of tokens the specific
[01:08:09] details here are not actually that
[01:08:11] important all I'm trying to show you in
[01:08:13] concrete terms is that our conversations
[01:08:15] which we think of as kind of like a
[01:08:16] structured object end up being turned
[01:08:19] via some encoding into onedimensional
[01:08:21] sequences of tokens and so because this
[01:08:25] is one dimensional sequence of tokens we
[01:08:27] can apply all the stuff that we applied
[01:08:29] before now it's just a sequence of
[01:08:30] tokens and now we can train a language
[01:08:33] model on it and so we're just predicting
[01:08:35] the next token in a sequence uh just
[01:08:37] like before and um we can represent and
[01:08:39] train on conversations and then what
[01:08:42] does it look like at test time during
[01:08:43] inference so say we've trained a model
[01:08:46] and we've trained a model on these kinds
[01:08:49] of data sets of conversations and now we
[01:08:51] want to
[01:08:52] inference so during inference what does
[01:08:54] this look like when you're on on chash
[01:08:55] apt well you come to chash apt and you
[01:08:58] have say like a dialogue with it and the
[01:09:01] way this works is
[01:09:03] basically um say that this was already
[01:09:06] filled in so like what is 2 plus 2 2
[01:09:07] plus 2 is four and now you issue what if
[01:09:10] it was times I am end and what basically
[01:09:13] ends up happening um on the servers of
[01:09:16] open AI or something like that is they
[01:09:18] put in I start assistant I amep and this
[01:09:21] is where they end it right here so they
[01:09:24] construct this context and now they
[01:09:27] start sampling from the model so it's at
[01:09:29] this stage that they will go to the
[01:09:30] model and say okay what is a good for
[01:09:32] sequence what is a good first token what
[01:09:34] is a good second token what is a good
[01:09:36] third token and this is where the LM
[01:09:38] takes over and creates a response like
[01:09:41] for example response that looks
[01:09:43] something like this but it doesn't have
[01:09:44] to be identical to this but it will have
[01:09:46] the flavor of this if this kind of a
[01:09:48] conversation was in the data set so um
[01:09:52] that's roughly how the protocol Works
[01:09:54] although the details of this protocol
[01:09:56] are not important so again my goal is
[01:09:59] that just to show you that everything
[01:10:01] ends up being just a one-dimensional
[01:10:02] token sequence so we can apply
[01:10:04] everything we've already seen but we're
[01:10:06] now training on conversations and we're
[01:10:08] now uh basically generating
[01:10:10] conversations as well okay so now I
[01:10:13] would like to turn to what these data
[01:10:14] sets look like in practice the first
[01:10:16] paper that I would like to show you and
[01:10:17] the first effort in this direction is
[01:10:20] this paper from openai in 2022 and this
[01:10:23] paper was called instruct GPT or the
[01:10:25] technique that they developed and this
[01:10:27] was the first time that opena has kind
[01:10:29] of talked about how you can take
[01:10:30] language models and fine-tune them on
[01:10:32] conversations and so this paper has a
[01:10:34] number of details that I would like to
[01:10:36] take you through so the first stop I
[01:10:38] would like to make is in section 3.4
[01:10:40] where they talk about the human
[01:10:41] contractors that they hired uh in this
[01:10:44] case from upwork or through scale AI to
[01:10:47] uh construct these conversations and so
[01:10:49] there are human labelers involved whose
[01:10:52] job it is professionally to create these
[01:10:54] conversations and these labelers are
[01:10:56] asked to come up with prompts and then
[01:10:58] they are asked to also complete the
[01:11:00] ideal assistant responses and so these
[01:11:03] are the kinds of prompts that people
[01:11:04] came up with so these are human labelers
[01:11:06] so list five ideas for how to regain
[01:11:08] enthusiasm for my career what are the
[01:11:10] top 10 science fiction books I should
[01:11:12] read next and there's many different
[01:11:13] types of uh kind of prompts here so
[01:11:16] translate this sentence from uh to
[01:11:18] Spanish Etc and so there's many things
[01:11:21] here that people came up with they first
[01:11:23] come up with the prompt and then they
[01:11:25] also uh answer that prompt and they give
[01:11:28] the ideal assistant response now how do
[01:11:30] they know what is the ideal assistant
[01:11:32] response that they should write for
[01:11:33] these prompts so when we scroll down a
[01:11:35] little bit further we see that here we
[01:11:37] have this excerpt of labeling
[01:11:39] instructions uh that are given to the
[01:11:41] human labelers so the company that is
[01:11:44] developing the language model like for
[01:11:45] example open AI writes up labeling
[01:11:47] instructions for how the humans should
[01:11:49] create ideal responses and so here for
[01:11:52] example is an excerpt uh of these kinds
[01:11:54] of labeling instruction instructions on
[01:11:56] High level you're asking people to be
[01:11:57] helpful truthful and harmless and you
[01:11:59] can pause the video if you'd like to see
[01:12:01] more here but on a high level basically
[01:12:04] just just answer try to be helpful try
[01:12:06] to be truthful and don't answer
[01:12:08] questions that we don't want um kind of
[01:12:10] the system to handle uh later in chat
[01:12:13] gbt and so roughly speaking the company
[01:12:16] comes up with the labeling instructions
[01:12:18] usually they are not this short usually
[01:12:19] there are hundreds of pages and people
[01:12:21] have to study them professionally and
[01:12:23] then they write out the ideal assistant
[01:12:26] responses uh following those labeling
[01:12:28] instructions so this is a very human
[01:12:30] heavy process as it was described in
[01:12:32] this paper now the data set for instruct
[01:12:34] GPT was never actually released by openi
[01:12:37] but we do have some open- Source um
[01:12:39] reproductions that were're trying to
[01:12:40] follow this kind of a setup and collect
[01:12:42] their own data so one that I'm familiar
[01:12:45] with for example is the effort of open
[01:12:48] Assistant from a while back and this is
[01:12:50] just one of I think many examples but I
[01:12:52] just want to show you an example so
[01:12:54] here's so these were people on the
[01:12:56] internet that were asked to basically
[01:12:57] create these conversations similar to
[01:12:59] what um open I did with human labelers
[01:13:03] and so here's an entry of a person who
[01:13:05] came up with this BR can you write a
[01:13:07] short introduction to the relevance of
[01:13:08] the term
[01:13:09] manop uh in economics please use
[01:13:12] examples Etc and then the same person or
[01:13:15] potentially a different person will
[01:13:17] write up the response so here's the
[01:13:18] assistant response to this and so then
[01:13:21] the same person or different person will
[01:13:23] actually write out this ideal
[01:13:26] response and then this is an example of
[01:13:29] maybe how the conversation could
[01:13:30] continue now explain it to a dog and
[01:13:33] then you can try to come up with a
[01:13:34] slightly a simpler explanation or
[01:13:36] something like that now this then
[01:13:39] becomes the label and we end up training
[01:13:41] on this so what happens during training
[01:13:45] is that um of course we're not going to
[01:13:48] have a full coverage of all the possible
[01:13:50] questions that um the model will
[01:13:53] encounter at test time during inference
[01:13:56] we can't possibly cover all the possible
[01:13:57] prompts that people are going to be
[01:13:59] asking in the future but if we have a
[01:14:02] like a data set of a few of these
[01:14:03] examples then the model during training
[01:14:06] will start to take on this Persona of
[01:14:09] this helpful truthful harmless assistant
[01:14:12] and it's all programmed by example and
[01:14:14] so these are all examples of behavior
[01:14:16] and if you have conversations of these
[01:14:18] example behaviors and you have enough of
[01:14:19] them like 100,00 and you train on it the
[01:14:22] model sort of starts to understand the
[01:14:23] statistical pattern and it kind of takes
[01:14:26] on this personality of this
[01:14:28] assistant now it's possible that when
[01:14:30] you get the exact same question like
[01:14:32] this at test time it's possible that the
[01:14:35] answer will be recited as exactly what
[01:14:38] was in the training set but more likely
[01:14:40] than that is that the model will kind of
[01:14:43] like do something of a similar Vibe um
[01:14:45] and we will understand that this is the
[01:14:47] kind of answer that you want um so
[01:14:51] that's what we're doing we're
[01:14:52] programming the system um by example and
[01:14:55] the system adopts statistically this
[01:14:58] Persona of this helpful truthful
[01:15:00] harmless assistant which is kind of like
[01:15:02] reflected in the labeling instructions
[01:15:04] that the company creates now I want to
[01:15:06] show you that the state-of-the-art has
[01:15:08] kind of advanced in the last 2 or 3
[01:15:09] years uh since the instr GPT paper so in
[01:15:12] particular it's not very common for
[01:15:14] humans to be doing all the heavy lifting
[01:15:16] just by themselves anymore and that's
[01:15:18] because we now have language models and
[01:15:19] these language models are helping us
[01:15:21] create these data sets and conversations
[01:15:23] so it is very rare that the people will
[01:15:25] like literally just write out the
[01:15:26] response from scratch it is a lot more
[01:15:28] likely that they will use an existing
[01:15:29] llm to basically like uh come up with an
[01:15:32] answer and then they will edit it or
[01:15:34] things like that so there's many
[01:15:35] different ways in which now llms have
[01:15:37] started to kind of permeate this
[01:15:39] posttraining Set uh stack and llms are
[01:15:43] basically used pervasively to help
[01:15:45] create these massive data sets of
[01:15:46] conversations so I don't want to show
[01:15:49] like Ultra chat is one um such example
[01:15:52] of like a more modern data set of
[01:15:53] conversations it is to a very large
[01:15:56] extent synthetic but uh I believe
[01:15:58] there's some human involvement I could
[01:15:59] be wrong with that usually there will be
[01:16:01] a little bit of human but there will be
[01:16:02] a huge amount of synthetic help um and
[01:16:06] this is all kind of like uh constructed
[01:16:08] in different ways and Ultra chat is just
[01:16:10] one example of many sft data sets that
[01:16:12] currently exist and the only thing I
[01:16:14] want to show you is that uh these data
[01:16:15] sets have now millions of conversations
[01:16:18] uh these conversations are mostly
[01:16:19] synthetic but they're probably edited to
[01:16:21] some extent by humans and they span a
[01:16:23] huge diversity of sort of
[01:16:27] um uh areas and so on so these are
[01:16:31] fairly extensive artifacts by now and
[01:16:33] there's all these like sft mixtures as
[01:16:35] they're called so you have a mixture of
[01:16:37] like lots of different types and sources
[01:16:39] and it's partially synthetic partially
[01:16:41] human and it's kind of like um gone in
[01:16:44] that direction since uh but roughly
[01:16:46] speaking we still have sft data sets
[01:16:48] they're made up of conversations we're
[01:16:50] training on them um just like we did
[01:16:52] before and
[01:16:55] uh I guess like the last thing to note
[01:16:57] is that I want to dispel a little bit of
[01:17:00] the magic of talking to an AI like when
[01:17:02] you go to chat GPT and you give it a
[01:17:04] question and then you hit enter uh what
[01:17:07] is coming back is kind of like
[01:17:10] statistically aligned with what's
[01:17:12] happening in the training set and these
[01:17:14] training sets I mean they really just
[01:17:16] have a seed in humans following labeling
[01:17:19] instructions so what are you actually
[01:17:21] talking to in chat GPT or how should you
[01:17:24] think about it well it's not coming from
[01:17:25] some magical AI like roughly speaking
[01:17:28] it's coming from something that is
[01:17:29] statistically imitating human labelers
[01:17:32] which comes from labeling instructions
[01:17:34] written by these companies and so you're
[01:17:36] kind of imitating this uh you're kind of
[01:17:38] getting um it's almost as if you're
[01:17:40] asking human labeler and imagine that
[01:17:43] the answer that is given to you uh from
[01:17:45] chbt is some kind of a simulation of a
[01:17:47] human labeler uh and it's kind of like
[01:17:50] asking what would a human labeler say in
[01:17:53] this kind of a conversation
[01:17:56] and uh it's not just like this human
[01:17:58] labeler is not just like a random person
[01:18:00] from the internet because these
[01:18:01] companies actually hire experts so for
[01:18:03] example when you are asking questions
[01:18:04] about code and so on the human labelers
[01:18:06] that would be in um involved in creation
[01:18:08] of these conversation data sets they
[01:18:10] will usually be usually be educated
[01:18:12] expert people and you're kind of like
[01:18:15] asking a question of like a simulation
[01:18:17] of those people if that makes sense so
[01:18:19] you're not talking to a magical AI
[01:18:21] you're talking to an average labeler
[01:18:22] this average labeler is probably fairly
[01:18:24] highly skilled
[01:18:25] but you're talking to kind of like an
[01:18:26] instantaneous simulation of that kind of
[01:18:29] a person that would be hired uh in the
[01:18:32] construction of these data sets so let
[01:18:34] me give you one more specific example
[01:18:36] before we move on for example when I go
[01:18:38] to chpt and I say recommend the top five
[01:18:40] landmarks who see in Paris and then I
[01:18:42] hit
[01:18:44] enter
[01:18:49] uh okay here we go okay when I hit enter
[01:18:52] what's coming out here how do I think
[01:18:55] about it well it's not some kind of a
[01:18:56] magical AI that has gone out and
[01:18:58] researched all the landmarks and then
[01:19:00] ranked them using its infinite
[01:19:01] intelligence Etc what I'm getting is a
[01:19:04] statistical simulation of a labeler that
[01:19:07] was hired by open AI you can think about
[01:19:09] it roughly in that way and so if this
[01:19:13] specific um question is in the
[01:19:16] posttraining data set somewhere at open
[01:19:17] aai then I'm very likely to see an
[01:19:20] answer that is probably very very
[01:19:22] similar to what that human labeler would
[01:19:24] have put down
[01:19:25] for those five landmarks how does the
[01:19:27] human labeler come up with this well
[01:19:28] they go off and they go on the internet
[01:19:29] and they kind of do their own little
[01:19:31] research for 20 minutes and they just
[01:19:32] come up with a list right now so if they
[01:19:35] come up with this list and this is in
[01:19:37] the data set I'm probably very likely to
[01:19:39] see what they submitted as the correct
[01:19:41] answer from the assistant now if this
[01:19:44] specific query is not part of the post
[01:19:46] training data set then what I'm getting
[01:19:48] here is a little bit more emergent uh
[01:19:51] because uh the model kind of understands
[01:19:53] the statistically
[01:19:55] um the kinds of landmarks that are in
[01:19:57] this training set are usually the
[01:19:59] prominent landmarks the landmarks that
[01:20:00] people usually want to see the kinds of
[01:20:02] landmarks that are usually uh very often
[01:20:05] talked about on the internet and
[01:20:06] remember that the model already has a
[01:20:08] ton of Knowledge from its pre-training
[01:20:10] on the internet so it's probably seen a
[01:20:12] ton of conversations about Paris about
[01:20:13] landmarks about the kinds of things that
[01:20:15] people like to see and so it's the
[01:20:17] pre-training knowledge that has then
[01:20:18] combined with the postering data set
[01:20:20] that results in this kind of an
[01:20:23] imitation um
[01:20:25] so that's uh that's roughly how you can
[01:20:27] kind of think about what's happening
[01:20:29] behind the scenes here in in this
[01:20:31] statistical sense okay now I want to
[01:20:33] turn to the topic of llm psychology as I
[01:20:35] like to call it which is what are sort
[01:20:37] of the emergent cognitive effects of the
[01:20:40] training pipeline that we have for these
[01:20:42] models so in particular the first one I
[01:20:44] want to talk to is of course
[01:20:47] hallucinations so you might be familiar
[01:20:50] with model hallucinations it's when llms
[01:20:52] make stuff up they just totally
[01:20:53] fabricate information Etc and it's a big
[01:20:56] problem with llm assistants it is a
[01:20:58] problem that existed to a large extent
[01:21:00] with early models uh from many years ago
[01:21:02] and I think the problem has gotten a bit
[01:21:04] better uh because there are some
[01:21:05] medications that I'm going to go into in
[01:21:07] a second for now let's just try to
[01:21:09] understand where these hallucinations
[01:21:10] come from so here's a specific example
[01:21:13] of a few uh of three conversations that
[01:21:16] you might think you have in your
[01:21:17] training set and um these are pretty
[01:21:20] reasonable conversations that you could
[01:21:22] imagine being in the training set so
[01:21:23] like for example who is Cruz well Tom
[01:21:25] Cruz is an famous actor American actor
[01:21:27] and producer Etc who is John baraso this
[01:21:31] turns out to be a us senetor for example
[01:21:34] who is genis Khan well genis Khan was
[01:21:36] blah blah blah and so this is what your
[01:21:39] conversations could look like at
[01:21:40] training time now the problem with this
[01:21:42] is that when the human is writing the
[01:21:46] correct answer for the assistant in each
[01:21:48] one of these cases uh the human either
[01:21:51] like knows who this person is or they
[01:21:52] research them on the Internet and they
[01:21:53] come in and they write this response
[01:21:55] that kind of has this like confident
[01:21:57] tone of an answer and what happens
[01:21:59] basically is that at test time when you
[01:22:01] ask for someone who is this is a totally
[01:22:03] random name that I totally came up with
[01:22:05] and I don't think this person exists um
[01:22:07] as far as I know I just Tred to generate
[01:22:09] it randomly the problem is when we ask
[01:22:11] who is Orson kovats the problem is that
[01:22:15] the assistant will not just tell you oh
[01:22:17] I don't know even if the assistant and
[01:22:20] the language model itself might know
[01:22:23] inside its features inside its
[01:22:24] activations inside of its brain sort of
[01:22:26] it might know that this person is like
[01:22:28] not someone that um that is that it's
[01:22:30] familiar with even if some part of the
[01:22:32] network kind of knows that in some sense
[01:22:35] the uh saying that oh I don't know who
[01:22:37] this is is is not going to happen
[01:22:40] because the model statistically imitates
[01:22:42] is training set in the training set the
[01:22:45] questions of the form who is blah are
[01:22:47] confidently answered with the correct
[01:22:49] answer and so it's going to take on the
[01:22:52] style of the answer and it's going to do
[01:22:53] its best it's going to give you
[01:22:55] statistically the most likely guess and
[01:22:57] it's just going to basically make stuff
[01:22:58] up because these models again we just
[01:23:01] talked about it is they don't have
[01:23:02] access to the internet they're not doing
[01:23:04] research these are statistical token
[01:23:06] tumblers as I call them uh is just
[01:23:08] trying to sample the next token in the
[01:23:10] sequence and it's going to basically
[01:23:12] make stuff up so let's take a look at
[01:23:13] what this looks
[01:23:15] like I have here what's called the
[01:23:17] inference playground from hugging face
[01:23:20] and I am on purpose picking on a model
[01:23:22] called Falcon 7B which is an old model
[01:23:25] this is a few years ago now so it's an
[01:23:27] older model So It suffers from
[01:23:28] hallucinations and as I mentioned this
[01:23:31] has improved over time recently but
[01:23:33] let's say who is Orson kovats let's ask
[01:23:35] Falcon 7B instruct
[01:23:37] run oh yeah Orson kovat is an American
[01:23:40] author and science uh fiction writer
[01:23:42] okay this is totally false it's
[01:23:44] hallucination let's try again these are
[01:23:46] statistical systems right so we can
[01:23:48] resample this time Orson kovat is a
[01:23:51] fictional character from this 1950s TV
[01:23:53] show it's total BS right let's try again
[01:23:57] he's a former minor league baseball
[01:23:59] player okay so basically the model
[01:24:02] doesn't know and it's given us lots of
[01:24:04] different answers because it doesn't
[01:24:06] know it's just kind of like sampling
[01:24:08] from these probabilities the model
[01:24:10] starts with the tokens who is oron
[01:24:12] kovats assistant and then it comes in
[01:24:14] here and it's get it's getting these
[01:24:17] probabilities and it's just sampling
[01:24:19] from the probabilities and it just like
[01:24:20] comes up with stuff and the stuff is
[01:24:24] actually
[01:24:24] statistically consistent with the style
[01:24:27] of the answer in its training set and
[01:24:29] it's just doing that but you and I
[01:24:31] experiened it as a madeup factual
[01:24:33] knowledge but keep in mind that uh the
[01:24:36] model basically doesn't know and it's
[01:24:37] just imitating the format of the answer
[01:24:40] and it's not going to go off and look it
[01:24:41] up uh because it's just imitating again
[01:24:44] the answer so how can we uh mitigate
[01:24:47] this because for example when we go to
[01:24:48] chat apt and I say who is oron kovats
[01:24:50] and I'm now asking the stateoftheart
[01:24:52] state-of-the-art model from open AI
[01:24:55] this model will tell
[01:24:56] you oh so this model is actually is even
[01:25:00] smarter because you saw very briefly it
[01:25:02] said searching the web uh we're going to
[01:25:04] cover this later um it's actually trying
[01:25:07] to do tool use and
[01:25:11] uh kind of just like came up with some
[01:25:13] kind of a story but I want to just who
[01:25:15] or Kovach did not use any tools I don't
[01:25:19] want it to do web
[01:25:22] search there's a wellknown historical or
[01:25:24] public figure named or oron kovats so
[01:25:27] this model is not going to make up stuff
[01:25:29] this model knows that it doesn't know
[01:25:31] and it tells you that it doesn't appear
[01:25:32] to be a person that this model knows so
[01:25:35] somehow we sort of improved
[01:25:37] hallucinations even though they clearly
[01:25:39] are an issue in older models and it
[01:25:42] makes totally uh sense why you would be
[01:25:44] getting these kinds of answers if this
[01:25:46] is what your training set looks like so
[01:25:47] how do we fix this okay well clearly we
[01:25:50] need some examples in our data set that
[01:25:53] where the correct answer for the
[01:25:54] assistant is that the model doesn't know
[01:25:57] about some particular fact but we only
[01:25:59] need to have those answers be produced
[01:26:02] in the cases where the model actually
[01:26:03] doesn't know and so the question is how
[01:26:05] do we know what the model knows or
[01:26:07] doesn't know well we can empirically
[01:26:09] probe the model to figure that out so
[01:26:11] let's take a look at for example how
[01:26:13] meta uh dealt with hallucinations for
[01:26:16] the Llama 3 series of models as an
[01:26:18] example so in this paper that they
[01:26:20] published from meta we can go into
[01:26:22] hallucinations
[01:26:25] which they call here factuality and they
[01:26:27] describe the procedure by which they
[01:26:29] basically interrogate the model to
[01:26:32] figure out what it knows and doesn't
[01:26:33] know to figure out sort of like the
[01:26:35] boundary of its knowledge and then they
[01:26:38] add examples to the training set where
[01:26:41] for the things where the model doesn't
[01:26:44] know them the correct answer is that the
[01:26:46] model doesn't know them which sounds
[01:26:48] like a very easy thing to do in
[01:26:50] principle but this roughly fixes the
[01:26:53] issue and the the reason it fixes the
[01:26:54] issue is
[01:26:56] because remember like the model might
[01:26:59] actually have a pretty good model of its
[01:27:01] self knowledge inside the network so
[01:27:04] remember we looked at the network and
[01:27:06] all these neurons inside the network you
[01:27:08] might imagine that there's a neuron
[01:27:09] somewhere in the network that sort of
[01:27:11] like lights up for when the model is
[01:27:14] uncertain but the problem is that the
[01:27:17] activation of that neuron is not
[01:27:18] currently wired up to the model actually
[01:27:20] saying in words that it doesn't know so
[01:27:23] even though the internal of the neural
[01:27:24] network no because there's some neurons
[01:27:26] that represent that the model uh will
[01:27:29] not surface that it will instead take
[01:27:31] its best guess so that it sounds
[01:27:33] confident um just like it sees in a
[01:27:35] training set so we need to basically
[01:27:37] interrogate the model and allow it to
[01:27:39] say I don't know in the cases that it
[01:27:41] doesn't know so let me take you through
[01:27:43] what meta roughly does so basically what
[01:27:45] they do is here I have an example uh
[01:27:48] Dominic kek is uh the featured article
[01:27:51] today so I just went there randomly and
[01:27:54] what they do is basically they take a
[01:27:55] random document in a training set and
[01:27:58] they take a paragraph and then they use
[01:28:01] an llm to construct questions about that
[01:28:04] paragraph so for example I did that with
[01:28:06] chat GPT
[01:28:09] here so I said here's a paragraph from
[01:28:12] this document generate three specific
[01:28:14] factual questions based on this
[01:28:15] paragraph and give me the questions and
[01:28:17] the answers and so the llms are already
[01:28:20] good enough to create and reframe this
[01:28:23] information so if the information is in
[01:28:25] the context window um of this llm this
[01:28:29] actually works pretty well it doesn't
[01:28:30] have to rely on its memory it's right
[01:28:33] there in the context window and so it
[01:28:35] can basically reframe that information
[01:28:37] with fairly high accuracy so for example
[01:28:40] can generate questions for us like for
[01:28:41] which team did he play here's the answer
[01:28:44] how many cups did he win Etc and now
[01:28:47] what we have to do is we have some
[01:28:48] question and answers and now we want to
[01:28:50] interrogate the model so roughly
[01:28:51] speaking what we'll do is we'll take our
[01:28:53] questions and we'll go to our model
[01:28:55] which would be uh say llama uh in meta
[01:28:59] but let's just interrogate mol 7B here
[01:29:01] as an example that's another model so
[01:29:04] does this model know about this answer
[01:29:07] let's take a
[01:29:09] look uh so he played for Buffalo Sabers
[01:29:12] right so the model knows and the the way
[01:29:15] that you can programmatically decide is
[01:29:16] basically we're going to take this
[01:29:18] answer from the model and we're going to
[01:29:20] compare it to the correct answer and
[01:29:23] again the model model are good enough to
[01:29:24] do this automatically so there's no
[01:29:26] humans involved here we can take uh
[01:29:28] basically the answer from the model and
[01:29:30] we can use another llm judge to check if
[01:29:33] that is correct according to this answer
[01:29:35] and if it is correct that means that the
[01:29:37] model probably knows so what we're going
[01:29:38] to do is we're going to do this maybe a
[01:29:40] few times so okay it knows it's Buffalo
[01:29:42] Savers let's drag
[01:29:45] in um Buffalo Sabers let's try one more
[01:29:51] time Buffalo Sabers so we asked three
[01:29:54] times about this factual question and
[01:29:55] the model seems to know so everything is
[01:29:58] great now let's try the second question
[01:30:00] how many Stanley Cups did he
[01:30:02] win and again let's interrogate the
[01:30:04] model about that and the correct answer
[01:30:06] is
[01:30:08] two so um here the model claims that he
[01:30:13] won um four times which is not correct
[01:30:17] right it doesn't match two so the model
[01:30:20] doesn't know it's making stuff up let's
[01:30:22] try again
[01:30:27] um so here the model again it's kind of
[01:30:30] like making stuff up right let's
[01:30:34] Dragon here it says did he did not even
[01:30:37] did not win during his career so
[01:30:39] obviously the model doesn't know and the
[01:30:41] way we can programmatically tell again
[01:30:42] is we interrogate the model three times
[01:30:45] and we compare its answers maybe three
[01:30:47] times five times whatever it is to the
[01:30:49] correct answer and if the model doesn't
[01:30:51] know then we know that the model doesn't
[01:30:53] know this question
[01:30:54] and then what we do is we take this
[01:30:56] question we create a new conversation in
[01:30:59] the training set so we're going to add a
[01:31:01] new conversation training set and when
[01:31:03] the question is how many Stanley Cups
[01:31:05] did he win the answer is I'm sorry I
[01:31:08] don't know or I don't remember and
[01:31:10] that's the correct answer for this
[01:31:12] question because we interrogated the
[01:31:13] model and we saw that that's the case if
[01:31:15] you do this for many different types of
[01:31:18] uh questions for many different types of
[01:31:20] documents you are giving the model an
[01:31:23] opportunity to in its training set
[01:31:25] refuse to say based on its knowledge and
[01:31:28] if you just have a few examples of that
[01:31:30] in your training set the model will know
[01:31:33] um and and has the opportunity to learn
[01:31:35] the association of this knowledge-based
[01:31:37] refusal to this internal neuron
[01:31:41] somewhere in its Network that we presume
[01:31:43] exists and empirically this turns out to
[01:31:45] be probably the case and it can learn
[01:31:47] that Association that hey when this
[01:31:49] neuron of uncertainty is high then I
[01:31:52] actually don't know and I'm allowed to
[01:31:54] say that I'm sorry but I don't think I
[01:31:56] remember this Etc and if you have these
[01:31:59] uh examples in your training set then
[01:32:01] this is a large mitigation for
[01:32:03] hallucination and that's roughly
[01:32:05] speaking why chpt is able to do stuff
[01:32:08] like this as well so these are kinds of
[01:32:10] uh mitigations that people have
[01:32:12] implemented and that have improved the
[01:32:14] factuality issue over time okay so I've
[01:32:16] described mitigation number one for
[01:32:19] basically mitigating the hallucinations
[01:32:21] issue now we can actually do much better
[01:32:24] than that uh it's instead of just saying
[01:32:27] that we don't know uh we can introduce
[01:32:29] an additional mitigation number two to
[01:32:32] give the llm an opportunity to be
[01:32:33] factual and actually answer the question
[01:32:36] now what do you and I do if I was to ask
[01:32:39] you a factual question and you don't
[01:32:40] know uh what would you do um in order to
[01:32:43] answer the question well you could uh go
[01:32:45] off and do some search and uh use the
[01:32:47] internet and you could figure out the
[01:32:49] answer and then tell me what that answer
[01:32:51] is and we can do the exact exact same
[01:32:54] thing with these models so think of the
[01:32:56] knowledge inside the neural network
[01:32:58] inside its billions of parameters think
[01:33:01] of that as kind of a vague recollection
[01:33:02] of the things that the model has seen
[01:33:05] during its training during the
[01:33:07] pre-training stage a long time ago so
[01:33:09] think of that knowledge in the
[01:33:10] parameters as something you read a month
[01:33:13] ago and if you keep reading something
[01:33:15] then you will remember it and the model
[01:33:17] remembers that but if it's something
[01:33:18] rare then you probably don't have a
[01:33:20] really good recollection of that
[01:33:21] information but what you and I do is we
[01:33:23] just go and look it up now when you go
[01:33:25] and look it up what you're doing
[01:33:26] basically is like you're refreshing your
[01:33:28] working memory with information and then
[01:33:30] you're able to sort of like retrieve it
[01:33:32] talk about it or Etc so we need some
[01:33:34] equivalent of allowing the model to
[01:33:36] refresh its memory or its recollection
[01:33:38] and we can do that by introducing tools
[01:33:41] uh for the
[01:33:42] models so the way we are going to
[01:33:44] approach this is that instead of just
[01:33:45] saying hey I'm sorry I don't know we can
[01:33:48] attempt to use tools so we can create uh
[01:33:53] a mechanism
[01:33:54] by which the language model can emit
[01:33:56] special tokens and these are tokens that
[01:33:57] we're going to introduce new tokens so
[01:34:00] for example here I've introduced two
[01:34:02] tokens and I've introduced a format or a
[01:34:04] protocol for how the model is allowed to
[01:34:07] use these tokens so for example instead
[01:34:09] of answering the question when the model
[01:34:12] does not instead of just saying I don't
[01:34:14] know sorry the model has the option now
[01:34:16] to emitting the special token search
[01:34:18] start and this is the query that will go
[01:34:20] to like bing.com in the case of openai
[01:34:22] or say Google search or something like
[01:34:24] that so it will emit the query and then
[01:34:26] it will emit search end and then here
[01:34:30] what will happen is that the program
[01:34:32] that is sampling from the model that is
[01:34:34] running the inference when it sees the
[01:34:36] special token search end instead of
[01:34:39] sampling the next token uh in the
[01:34:41] sequence it will actually pause
[01:34:44] generating from the model it will go off
[01:34:46] it will open a session with bing.com and
[01:34:49] it will paste the search query into Bing
[01:34:52] and it will then um get all the text
[01:34:54] that is retrieved and it will basically
[01:34:56] take that text it will maybe represent
[01:34:58] it again with some other special tokens
[01:35:00] or something like that and it will take
[01:35:02] that text and it will copy paste it here
[01:35:05] into what I Tred to like show with the
[01:35:07] brackets so all that text kind of comes
[01:35:09] here and when the text comes here it
[01:35:12] enters the context window so the model
[01:35:15] so that text from the web search is now
[01:35:17] inside the context window that will feed
[01:35:20] into the neural network and you should
[01:35:21] think of the context window as kind of
[01:35:23] like the working memory of the model
[01:35:25] that data that is in the context window
[01:35:27] is directly accessible by the model it
[01:35:29] directly feeds into the neural network
[01:35:31] so it's not anymore a vague recollection
[01:35:33] it's data that it it has in the context
[01:35:36] window and is directly available to that
[01:35:38] model so now when it's sampling the new
[01:35:41] uh tokens here afterwards it can
[01:35:43] reference very easily the data that has
[01:35:45] been copy pasted in there so that's
[01:35:48] roughly how these um how these tools use
[01:35:52] uh tools uh function
[01:35:54] and so web search is just one of the
[01:35:55] tools we're going to look at some of the
[01:35:56] other tools in a bit uh but basically
[01:35:59] you introduce new tokens you introduce
[01:36:00] some schema by which the model can
[01:36:02] utilize these tokens and can call these
[01:36:04] special functions like web search
[01:36:06] functions and how do you teach the model
[01:36:08] how to correctly use these tools like
[01:36:10] say web search search start search end
[01:36:12] Etc well again you do that through
[01:36:14] training sets so we need now to have a
[01:36:16] bunch of data and a bunch of
[01:36:18] conversations that show the model by
[01:36:21] example how to use web search so what
[01:36:24] are the what are the settings where you
[01:36:25] are using the search um and what does
[01:36:28] that look like and here's by example how
[01:36:30] you start a search and the search Etc
[01:36:33] and uh if you have a few thousand maybe
[01:36:35] examples of that in your training set
[01:36:36] the model will actually do a pretty good
[01:36:38] job of understanding uh how this tool
[01:36:40] works and it will know how to sort of
[01:36:43] structure its queries and of course
[01:36:44] because of the pre-training data set and
[01:36:47] its understanding of the world it
[01:36:48] actually kind of understands what a web
[01:36:49] search is and so it actually kind of has
[01:36:51] a pretty good native understanding
[01:36:54] um of what kind of stuff is a good
[01:36:56] search query um and so it all kind of
[01:36:58] just like works you just need a little
[01:37:00] bit of a few examples to show it how to
[01:37:02] use this new tool and then it can lean
[01:37:04] on it to retrieve information and uh put
[01:37:07] it in the context window and that's
[01:37:08] equivalent to you and I looking
[01:37:10] something up because once it's in the
[01:37:12] context it's in the working memory and
[01:37:13] it's very easy to manipulate and access
[01:37:16] so that's what we saw a few minutes ago
[01:37:18] when I was searching on chat GPT for who
[01:37:20] is Orson kovats the chat GPT language
[01:37:23] model decided Ed that this is some kind
[01:37:24] of a rare um individual or something
[01:37:27] like that and instead of giving me an
[01:37:29] answer from its memory it decided that
[01:37:31] it will sample a special token that is
[01:37:33] going to do web search and we saw
[01:37:35] briefly something flash it was like
[01:37:36] using the web tool or something like
[01:37:38] that so it briefly said that and then we
[01:37:40] waited for like two seconds and then it
[01:37:41] generated this and you see how it's
[01:37:43] creating references here and so it's
[01:37:45] citing sources so what happened here is
[01:37:50] it went off it did a web web search it
[01:37:52] found these sources and these URLs and
[01:37:55] the text of these web pages was all
[01:37:58] stuffed in between here and it's not
[01:38:01] showing here but it's it's basically
[01:38:02] stuffed as text in between here and now
[01:38:06] it sees that text and now it kind of
[01:38:08] references it and says that okay it
[01:38:11] could be these people citation could be
[01:38:13] those people citation Etc so that's what
[01:38:15] happened here and that's what and that's
[01:38:17] why when I said who is Orson kovats I
[01:38:19] could also say don't use any tools and
[01:38:22] then that's enough to um
[01:38:24] basically convince chat PT to not use
[01:38:25] tools and just use its memory and its
[01:38:28] recollection I also went off and I um
[01:38:32] tried to ask this question of Chachi PT
[01:38:34] so how many standing cups did uh Dominic
[01:38:37] Hasek win and Chachi P actually decided
[01:38:39] that it knows the answer and it has the
[01:38:40] confidence to say that uh he want twice
[01:38:43] and so it kind of just relied on its
[01:38:45] memory because presumably it has um it
[01:38:49] has enough of
[01:38:50] a kind of confidence in its weights in
[01:38:53] it parameters and activations that this
[01:38:55] is uh retrievable just for memory um but
[01:38:59] you can also
[01:39:01] conversely use web search to make sure
[01:39:04] and then for the same query it actually
[01:39:06] goes off and it searches and then it
[01:39:07] finds a bunch of sources it finds all
[01:39:10] this all of this stuff gets copy pasted
[01:39:12] in there and then it tells us uh to
[01:39:15] again and sites and it actually says the
[01:39:17] Wikipedia article which is the source of
[01:39:20] this information for us as well so
[01:39:23] that's tools web search the model
[01:39:25] determines when to search and then uh
[01:39:27] that's kind of like how these tools uh
[01:39:29] work and this is an additional kind of
[01:39:32] mitigation for uh hallucinations and
[01:39:34] factuality so I want to stress one more
[01:39:37] time this very important sort of
[01:39:38] psychology
[01:39:40] Point knowledge in the parameters of the
[01:39:43] neural network is a vague recollection
[01:39:45] the knowledge in the tokens that make up
[01:39:47] the context
[01:39:48] window is the working memory and it
[01:39:51] roughly speaking Works kind of like um
[01:39:53] it works for us in our brain the stuff
[01:39:55] we remember is our parameters uh and the
[01:39:58] stuff that we just experienced like a
[01:40:01] few seconds or minutes ago and so on you
[01:40:03] can imagine that being in our context
[01:40:04] window and this context window is being
[01:40:05] built up as you have a conscious
[01:40:07] experience around you so this has a
[01:40:10] bunch of um implications also for your
[01:40:12] use of LOLs in practice so for example I
[01:40:15] can go to chat GPT and I can do
[01:40:17] something like this I can say can you
[01:40:18] Summarize chapter one of Jane Austin's
[01:40:20] Pride and Prejudice right and this is a
[01:40:22] perfectly fine prompt and Chach actually
[01:40:25] does something relatively reasonable
[01:40:26] here and but the reason it does that is
[01:40:28] because Chach has a pretty good
[01:40:30] recollection of a famous work like Pride
[01:40:32] and Prejudice it's probably seen a ton
[01:40:34] of stuff about it there's probably
[01:40:35] forums about this book it's probably
[01:40:37] read versions of this book um and it's
[01:40:40] kind of like remembers because even if
[01:40:43] you've read this or articles about it
[01:40:46] you'd kind of have a recollection enough
[01:40:48] to actually say all this but usually
[01:40:49] when I actually interact with LMS and I
[01:40:51] want them to recall specific things it
[01:40:53] always works better if you just give it
[01:40:55] to them so I think a much better prompt
[01:40:57] would be something like this can you
[01:40:59] summarize for me chapter one of genos's
[01:41:01] spr and Prejudice and then I am
[01:41:03] attaching it below for your reference
[01:41:04] and then I do something like a delimeter
[01:41:06] here and I paste it in and I I found
[01:41:08] that just copy pasting it from some
[01:41:10] website that I found here um so copy
[01:41:14] pasting the chapter one here and I do
[01:41:16] that because when it's in the context
[01:41:17] window the model has direct access to it
[01:41:20] and can exactly it doesn't have to
[01:41:22] recall it it just has access to it and
[01:41:24] so this summary is can be expected to be
[01:41:27] a significantly high quality or higher
[01:41:29] quality than this summary uh just
[01:41:31] because it's directly available to the
[01:41:32] model and I think you and I would work
[01:41:34] in the same way if you want to it would
[01:41:36] be you would produce a much better
[01:41:37] summary if you had reread this chapter
[01:41:40] before you had to summarize it and
[01:41:42] that's basically what's happening here
[01:41:44] or the equivalent of it the next sort of
[01:41:47] psychological Quirk I'd like to talk
[01:41:48] about briefly is that of the knowledge
[01:41:50] of self so what I see very often on the
[01:41:52] internet is that people do something
[01:41:54] like this they ask llms something like
[01:41:56] what model are you and who built you and
[01:41:59] um basically this uh question is a
[01:42:01] little bit nonsensical and the reason I
[01:42:03] say that is that as I try to kind of
[01:42:05] explain with some of the underhood
[01:42:07] fundamentals this thing is not a person
[01:42:09] right it doesn't have a persistent
[01:42:11] existence in any way it sort of boots up
[01:42:14] processes tokens and shuts off and it
[01:42:17] does that for every single person it
[01:42:18] just kind of builds up a context window
[01:42:19] of conversation and then everything gets
[01:42:21] deleted and so this this entity is kind
[01:42:23] of like restarted from scratch every
[01:42:25] single conversation if that makes sense
[01:42:27] it has no persistent self it has no
[01:42:28] sense of self it's a token tumbler and
[01:42:31] uh it follows the statistical
[01:42:33] regularities of its training set so it
[01:42:35] doesn't really make sense to ask it who
[01:42:38] are you what build you Etc and by
[01:42:40] default if you do what I described and
[01:42:42] just by default and from nowhere you're
[01:42:44] going to get some pretty random answers
[01:42:46] so for example let's uh pick on Falcon
[01:42:48] which is a fairly old model and let's
[01:42:50] see what it tells
[01:42:51] us uh so it's evading the question uh
[01:42:55] talented engineers and developers here
[01:42:58] it says I was built by open AI based on
[01:42:59] the gpt3 model it's totally making stuff
[01:43:01] up now the fact that it's built by open
[01:43:04] AI here I think a lot of people would
[01:43:06] take this as evidence that this model
[01:43:07] was somehow trained on open AI data or
[01:43:09] something like that I don't actually
[01:43:10] think that that's necessarily true the
[01:43:12] reason for that is
[01:43:14] that if you don't explicitly program the
[01:43:17] model to answer these kinds of questions
[01:43:20] then what you're going to get is its
[01:43:22] statistical best guess at the answer and
[01:43:25] this model had a um sft data mixture of
[01:43:29] conversations and during the
[01:43:32] fine-tuning um the model sort of
[01:43:35] understands as it's training on this
[01:43:36] data that it's taking on this
[01:43:38] personality of this like helpful
[01:43:40] assistant and it doesn't know how to it
[01:43:42] doesn't actually it wasn't told exactly
[01:43:44] what label to apply to self it just kind
[01:43:47] of is taking on this uh this uh Persona
[01:43:50] of a helpful assistant and remember that
[01:43:53] the pre-training stage took the
[01:43:55] documents from the entire internet and
[01:43:57] Chach and open AI are very prominent in
[01:43:59] these documents and so I think what's
[01:44:01] actually likely to be happening here is
[01:44:03] that this is just its hallucinated label
[01:44:06] for what it is this is its self-identity
[01:44:08] is that it's chat GPT by open Ai and
[01:44:11] it's only saying that because there's a
[01:44:12] ton of data on the internet of um
[01:44:15] answers like this that are actually
[01:44:17] coming from open from chasht and So
[01:44:20] that's its label for what it is now you
[01:44:23] can override this as a developer if you
[01:44:25] have a llm model you can actually
[01:44:27] override it and there are a few ways to
[01:44:28] do that so for example let me show you
[01:44:31] there's this MMO model from Allen Ai and
[01:44:35] um this is one llm it's not a top tier
[01:44:37] LM or anything like that but I like it
[01:44:39] because it is fully open source so the
[01:44:41] paper for Almo and everything else is
[01:44:43] completely fully open source which is
[01:44:44] nice um so here we are looking at its
[01:44:47] sft mixture so this is the data mixture
[01:44:49] of um the fine tuning so this is the
[01:44:52] conversations data it right and so the
[01:44:54] way that they are solving it for Theo
[01:44:56] model is we see that there's a bunch of
[01:44:58] stuff in the mixture and there's a total
[01:44:59] of 1 million conversations here but here
[01:45:02] we have alot to hardcoded if we go there
[01:45:05] we see that this is 240
[01:45:07] conversations and look at these 240
[01:45:10] conversations they're hardcoded tell me
[01:45:12] about yourself says user and then the
[01:45:15] assistant says I'm and open language
[01:45:17] model developed by AI to Allen Institute
[01:45:19] of artificial intelligence Etc I'm here
[01:45:21] to help blah blah blah what is your name
[01:45:23] uh Theo project so these are all kinds
[01:45:26] of like cooked up hardcoded questions
[01:45:27] abouto 2 and the correct answers to give
[01:45:30] in these cases if you take 240 questions
[01:45:33] like this or conversations put them into
[01:45:35] your training set and fine tune with it
[01:45:37] then the model will actually be expected
[01:45:39] to parot this stuff later if you don't
[01:45:43] give it this then it's probably a Chach
[01:45:45] by open
[01:45:46] Ai and um there's one more way to
[01:45:49] sometimes do this is
[01:45:51] that basically um in these conversations
[01:45:55] and you have terms between human and
[01:45:56] assistant sometimes there's a special
[01:45:58] message called system message at the
[01:46:00] very beginning of the conversation so
[01:46:02] it's not just between human and
[01:46:03] assistant there's a system and in the
[01:46:05] system message you can actually hardcode
[01:46:07] and remind the model that hey you are a
[01:46:10] model developed by open Ai and your name
[01:46:13] is chashi pt40 and you were trained on
[01:46:16] this date and your knowledge cut off is
[01:46:18] this and basically it kind of like
[01:46:19] documents the model a little bit and
[01:46:21] then this is inserted into to your
[01:46:23] conversations so when you go on chpt you
[01:46:25] see a blank page but actually the system
[01:46:27] message is kind of like hidden in there
[01:46:28] and those tokens are in the context
[01:46:30] window and so those are the two ways to
[01:46:33] kind of um program the models to talk
[01:46:35] about themselves either it's done
[01:46:37] through uh data like this or it's done
[01:46:40] through system message and things like
[01:46:42] that basically invisible tokens that are
[01:46:44] in the context window and remind the
[01:46:45] model of its identity but it's all just
[01:46:47] kind of like cooked up and bolted on in
[01:46:50] some in some way it's not actually like
[01:46:51] really deeply there in any real sense as
[01:46:54] it would before a human I want to now
[01:46:57] continue to the next section which deals
[01:46:59] with the computational capabilities or
[01:47:01] like I should say the native
[01:47:02] computational capabilities of these
[01:47:03] models in problem solving scenarios and
[01:47:06] so in particular we have to be very
[01:47:07] careful with these models when we
[01:47:09] construct our examples of conversations
[01:47:11] and there's a lot of sharp edges here
[01:47:13] that are kind of like elucidative is
[01:47:15] that a word uh they're kind of like
[01:47:16] interesting to look at when we consider
[01:47:18] how these models think so um consider
[01:47:22] the following prompt from a human and
[01:47:24] supposed that basically that we are
[01:47:25] building out a conversation to enter
[01:47:27] into our training set of conversations
[01:47:29] so we're going to train the model on
[01:47:30] this we're teaching you how to basically
[01:47:32] solve simple math problems so the prompt
[01:47:34] is Emily buys three apples and two
[01:47:36] oranges each orange cost $2 the total
[01:47:38] cost is 13 what is the cost of apples
[01:47:41] very simple math question now there are
[01:47:43] two answers here on the left and on the
[01:47:45] right they are both correct answers they
[01:47:48] both say that the answer is three which
[01:47:49] is correct but one of these two is a
[01:47:52] significant ific anly better answer for
[01:47:54] the assistant than the other like if I
[01:47:56] was Data labeler and I was creating one
[01:47:57] of these one of these would be uh a
[01:48:01] really terrible answer for the assistant
[01:48:03] and the other would be okay and so I'd
[01:48:05] like you to potentially pause the video
[01:48:07] Even and think through why one of these
[01:48:09] two is significantly better answer uh
[01:48:12] than the other and um if you use the
[01:48:14] wrong one your model will actually be uh
[01:48:17] really bad at math potentially and it
[01:48:19] would have uh bad outcomes and this is
[01:48:21] something that you would be careful with
[01:48:22] in your life labeling documentations
[01:48:23] when you are training people uh to
[01:48:25] create the ideal responses for the
[01:48:27] assistant okay so the key to this
[01:48:29] question is to realize and remember that
[01:48:32] when the models are training and also
[01:48:34] inferencing they are working in
[01:48:35] onedimensional sequence of tokens from
[01:48:37] left to right and this is the picture
[01:48:40] that I often have in my mind I imagine
[01:48:42] basically the token sequence evolving
[01:48:43] from left to right and to always produce
[01:48:46] the next token in a sequence we are
[01:48:48] feeding all these tokens into the neural
[01:48:50] network and this neural network then is
[01:48:53] the probabilities for the next token and
[01:48:54] sequence right so this picture here is
[01:48:56] the exact same picture we saw uh before
[01:48:58] up here and this comes from the web demo
[01:49:01] that I showed you before right so this
[01:49:04] is the calculation that basically takes
[01:49:05] the input tokens here on the top and uh
[01:49:09] performs these operations of all these
[01:49:11] neurons and uh gives you the answer for
[01:49:13] the probabilities of what comes next now
[01:49:15] the important thing to realize is that
[01:49:17] roughly
[01:49:19] speaking uh there's basically a finite
[01:49:21] number of layers of computation that
[01:49:22] happened here so for example this model
[01:49:25] here has only one two three layers of
[01:49:28] what's called detention and uh MLP here
[01:49:31] um maybe um typical modern
[01:49:34] state-of-the-art Network would have more
[01:49:36] like say 100 layers or something like
[01:49:37] that but there's only 100 layers of
[01:49:39] computation or something like that to go
[01:49:40] from the previous token sequence to the
[01:49:42] probabilities for the next token and so
[01:49:44] there's a finite amount of computation
[01:49:46] that happens here for every single token
[01:49:49] and you should think of this as a very
[01:49:50] small amount of computation and this
[01:49:52] amount of computation is almost roughly
[01:49:54] fixed uh for every single token in this
[01:49:57] sequence um the that's not actually
[01:49:59] fully true because the more tokens you
[01:50:01] feed in uh the the more expensive uh
[01:50:04] this forward pass will be of this neural
[01:50:06] network but not by much so you should
[01:50:09] think of this uh and I think as a good
[01:50:10] model to have in mind this is a fixed
[01:50:12] amount of compute that's going to happen
[01:50:13] in this box for every single one of
[01:50:15] these tokens and this amount of compute
[01:50:17] Cann possibly be too big because there's
[01:50:19] not that many layers that are sort of
[01:50:21] going from the top to bottom here
[01:50:23] there's not that that much
[01:50:24] computationally that will happen here
[01:50:26] and so you can't imagine the model to to
[01:50:27] basically do arbitrary computation in a
[01:50:29] single forward pass to get a single
[01:50:31] token and so what that means is that we
[01:50:34] actually have to distribute our
[01:50:35] reasoning and our computation across
[01:50:37] many tokens because every single token
[01:50:40] is only spending a finite amount of
[01:50:41] computation on it and so we kind of want
[01:50:45] to distribute the computation across
[01:50:47] many tokens and we can't have too much
[01:50:50] computation or expect too much
[01:50:52] computation out of of the model in any
[01:50:53] single individual token because there's
[01:50:55] only so much computation that happens
[01:50:57] per token okay roughly fixed amount of
[01:51:00] computation here
[01:51:02] so that's why this answer here is
[01:51:06] significantly worse and the reason for
[01:51:07] that is Imagine going from left to right
[01:51:09] here um and I copy pasted it right here
[01:51:13] the answer is three Etc imagine the
[01:51:16] model having to go from left to right
[01:51:17] emitting these tokens one at a time it
[01:51:19] has to say or we're expecting to say the
[01:51:23] answer is space dollar sign and then
[01:51:27] right here we're expecting it to
[01:51:28] basically cram all of the computation of
[01:51:30] this problem into this single token it
[01:51:32] has to emit the correct answer three and
[01:51:35] then once we've emitted the answer three
[01:51:37] we're expecting it to say all these
[01:51:39] tokens but at this point we've already
[01:51:41] prod produced the answer and it's
[01:51:43] already in the context window for all
[01:51:44] these tokens that follow so anything
[01:51:46] here is just um kind of post Hawk
[01:51:49] justification of why this is the answer
[01:51:52] um because the answer is already created
[01:51:53] it's already in the token window so it's
[01:51:56] it's not actually being calculated here
[01:51:58] um and so if you are answering the
[01:52:01] question directly and immediately you
[01:52:03] are training the model to to try to
[01:52:06] basically guess the answer in a single
[01:52:07] token and that is just not going to work
[01:52:10] because of the finite amount of
[01:52:11] computation that happens per token
[01:52:13] that's why this answer on the right is
[01:52:15] significantly better because we are
[01:52:17] Distributing this computation across the
[01:52:19] answer we're actually getting the model
[01:52:20] to sort of slowly come to the answer
[01:52:23] from the left to right we're getting
[01:52:24] intermediate results we're saying okay
[01:52:26] the total cost of oranges is four so 30
[01:52:28] - 4 is 9 and so we're creating
[01:52:32] intermediate calculations and each one
[01:52:34] of these calculations is by itself not
[01:52:36] that expensive and so we're actually
[01:52:38] basically kind of guessing a little bit
[01:52:40] the difficulty that the model is capable
[01:52:42] of in any single one of these individual
[01:52:44] tokens and there can never be too much
[01:52:47] work in any one of these tokens
[01:52:49] computationally because then the model
[01:52:50] won't be able to do that later at test
[01:52:52] time and so we're teaching the model
[01:52:55] here to spread out its reasoning and to
[01:52:57] spread out its computation over the
[01:52:59] tokens and in this way it only has very
[01:53:02] simple problems in each token and they
[01:53:05] can add up and then by the time it's
[01:53:07] near the end it has all the previous
[01:53:09] results in its working memory and it's
[01:53:11] much easier for it to determine that the
[01:53:13] answer is and here it is three so this
[01:53:15] is a significantly better label for our
[01:53:18] computation this would be really bad and
[01:53:20] is teaching the model to try to do all
[01:53:23] the computation in a single token and
[01:53:24] it's really
[01:53:25] bad so uh that's kind of like an
[01:53:28] interesting thing to keep in mind is in
[01:53:30] your
[01:53:31] prompts uh usually don't have to think
[01:53:33] about it explicitly because uh the
[01:53:36] people at open AI have labelers and so
[01:53:38] on that actually worry about this and
[01:53:40] they make sure that the answers are
[01:53:41] spread out and so actually open AI will
[01:53:43] kind of like do the right thing so when
[01:53:45] I ask this question for chat GPT it's
[01:53:48] actually going to go very slowly it's
[01:53:49] going to be like okay let's define our
[01:53:50] variables set up the equation
[01:53:52] and it's kind of creating all these
[01:53:54] intermediate results these are not for
[01:53:56] you these are for the model if the model
[01:53:58] is not creating these intermediate
[01:53:59] results for itself it's not going to be
[01:54:01] able to reach three I also wanted to
[01:54:04] show you that it's possible to be a bit
[01:54:06] mean to the model uh we can just ask for
[01:54:08] things so as an example I said I gave it
[01:54:10] the exact same uh prompt and I said
[01:54:13] answer the question in a single token
[01:54:15] just immediately give me the answer
[01:54:16] nothing else and it turns out that for
[01:54:18] this simple um prompt here it actually
[01:54:21] was able to do it in single go so it
[01:54:23] just created a single I think this is
[01:54:25] two tokens right uh because the dollar
[01:54:27] sign is its own token so basically this
[01:54:30] model didn't give me a single token it
[01:54:31] gave me two tokens but it still produced
[01:54:33] the correct answer and it did that in a
[01:54:35] single forward pass of the
[01:54:37] network now that's because the numbers
[01:54:40] here I think are very simple and so I
[01:54:41] made it a bit more difficult to be a bit
[01:54:43] mean to the model so I said Emily buys
[01:54:45] 23 apples and 177 oranges and then I
[01:54:48] just made the numbers a bit bigger and
[01:54:50] I'm just making it harder for the model
[01:54:51] I'm asking it to more computation in a
[01:54:53] single token and so I said the same
[01:54:55] thing and here it gave me five and five
[01:54:58] is actually not correct so the model
[01:55:00] failed to do all of this calculation in
[01:55:02] a single forward pass of the network it
[01:55:04] failed to go from the input tokens and
[01:55:07] then in a single forward pass of the
[01:55:09] network single go through the network it
[01:55:11] couldn't produce the result and then I
[01:55:13] said okay now don't worry about the the
[01:55:16] token limit and just solve the problem
[01:55:18] as usual and then it goes all the
[01:55:20] intermediate results it simplifies and
[01:55:22] every one of these intermediate results
[01:55:24] here and intermediate calculations is
[01:55:26] much easier for the model and um it sort
[01:55:29] of it's not too much work per token all
[01:55:32] of the tokens here are correct and it
[01:55:33] arises the solution which is seven and I
[01:55:36] just couldn't squeeze all of this work
[01:55:38] it couldn't squeeze that into a single
[01:55:39] forward passive Network so I think
[01:55:41] that's kind of just a cute example and
[01:55:43] something to kind of like think about
[01:55:45] and I think it's kind of again just
[01:55:46] elucidative in terms of how these uh
[01:55:48] models work the last thing that I would
[01:55:50] say on this topic is that if I was in
[01:55:52] practi is trying to actually solve this
[01:55:53] in my day-to-day life I might actually
[01:55:55] not uh trust that the model that all the
[01:55:57] intermediate calculations correctly here
[01:55:59] so actually probably what I do is
[01:56:01] something like this I would come here
[01:56:02] and I would say use code and uh that's
[01:56:06] because code is one of the possible
[01:56:08] tools that chachy PD can use and instead
[01:56:11] of it having to do mental arithmetic
[01:56:14] like this mental arithmetic here I don't
[01:56:15] fully trust it and especially if the
[01:56:17] numbers get really big there's no
[01:56:19] guarantee that the model will do this
[01:56:20] correctly any one of these intermediates
[01:56:22] steps might in principle fail we're
[01:56:24] using neural networks to do mental
[01:56:26] arithmetic uh kind of like you doing
[01:56:27] mental arithmetic in your brain it might
[01:56:30] just like uh screw up some of the
[01:56:31] intermediate results it's actually kind
[01:56:32] of amazing that it can even do this kind
[01:56:34] of mental arithmetic I don't think I
[01:56:35] could do this in my head but basically
[01:56:37] the model is kind of like doing it in
[01:56:38] its head and I don't trust that so I
[01:56:40] wanted to use tools so you can say stuff
[01:56:42] like use
[01:56:43] code and uh I'm not sure what happened
[01:56:47] there use
[01:56:50] code and so um like I mentioned there's
[01:56:53] a special tool and the uh the model can
[01:56:55] write code and I can inspect that this
[01:56:58] code is correct and then uh it's not
[01:57:01] relying on its mental arithmetic it is
[01:57:03] using the python interpreter which is a
[01:57:05] very simple programming language to
[01:57:07] basically uh write out the code that
[01:57:08] calculates the result and I would
[01:57:10] personally trust this a lot more because
[01:57:12] this came out of a Python program which
[01:57:14] I think has a lot more correctness
[01:57:15] guarantees than the mental arithmetic of
[01:57:17] a language model uh so just um another
[01:57:21] kind of uh potential hint that if you
[01:57:23] have these kinds of problems uh you may
[01:57:24] want to basically just uh ask the model
[01:57:26] to use the code interpreter and just
[01:57:28] like we saw with the web search the
[01:57:30] model has special uh kind of tokens for
[01:57:34] calling uh like it will not actually
[01:57:36] generate these tokens from the language
[01:57:38] model it will write the program and then
[01:57:40] it actually sends that program to a
[01:57:42] different sort of part of the computer
[01:57:44] that actually just runs that program and
[01:57:46] brings back the result and then the
[01:57:48] model gets access to that result and can
[01:57:50] tell you that okay the cost of each
[01:57:51] apple is seven
[01:57:53] um so that's another kind of tool and I
[01:57:55] would use this in practice for yourself
[01:57:57] and it's um yeah it's just uh less error
[01:58:01] prone I would say so that's why I called
[01:58:03] this section models need tokens to think
[01:58:06] distribute your competition across many
[01:58:08] tokens ask models to create intermediate
[01:58:10] results or whenever you can lean on
[01:58:13] tools and Tool use instead of allowing
[01:58:15] the models to do all of the stuff in
[01:58:17] their memory so if they try to do it all
[01:58:18] in their memory I don't fully trust it
[01:58:21] and prefer to use tools whenever
[01:58:22] possible I want to show you one more
[01:58:24] example of where this actually comes up
[01:58:26] and that's in counting so models
[01:58:28] actually are not very good at counting
[01:58:30] for the exact same reason you're asking
[01:58:32] for way too much in a single individual
[01:58:34] token so let me show you a simple
[01:58:36] example of that um how many dots are
[01:58:38] below and then I just put in a bunch of
[01:58:41] dots and Chach says there are and then
[01:58:44] it just tries to solve the problem in a
[01:58:46] single token so in a single token it has
[01:58:49] to count the number of dots in its
[01:58:51] context window
[01:58:53] um and it has to do that in the single
[01:58:55] forward pass of a network and a single
[01:58:57] forward pass of a network as we talked
[01:58:58] about there's not that much computation
[01:59:00] that can happen there just think of that
[01:59:01] as being like very little competation
[01:59:03] that happens there so if I just look at
[01:59:06] what the model sees let's go to the LM
[01:59:09] go to tokenizer it sees uh
[01:59:13] this how many dots are below and then it
[01:59:15] turns out that these dots here this
[01:59:17] group of I think 20 dots is a single
[01:59:20] token and then this group of whatever it
[01:59:22] is is another token and then for some
[01:59:25] reason they break up as this so I don't
[01:59:28] actually this has to do with the details
[01:59:29] of the tokenizer but it turns out that
[01:59:31] these um the model basically sees the
[01:59:34] token ID this this this and so on and
[01:59:38] then from these token IDs it's expected
[01:59:40] to count the number and spoiler alert is
[01:59:43] not 161 it's actually I believe
[01:59:45] 177 so here's what we can do instead uh
[01:59:48] we can say use code and you might expect
[01:59:51] that like why should this work and it's
[01:59:54] actually kind of subtle and kind of
[01:59:55] interesting so when I say use code I
[01:59:57] actually expect this to work let's see
[01:59:59] okay 177 is correct so what happens here
[02:00:02] is I've actually it doesn't look like it
[02:00:04] but I've broken down the problem into a
[02:00:08] problems that are easier for the model I
[02:00:10] know that the model can't count it can't
[02:00:12] do mental counting but I know that the
[02:00:14] model is actually pretty good at doing
[02:00:15] copy pasting so what I'm doing here is
[02:00:18] when I say use code it creates a string
[02:00:20] in Python for this and the task of
[02:00:23] basically copy pasting my input here to
[02:00:27] here is very simple because for the
[02:00:29] model um it sees this string of uh it
[02:00:33] sees it as just these four tokens or
[02:00:35] whatever it is so it's very simple for
[02:00:37] the model to copy paste those token IDs
[02:00:40] and um kind of unpack them into Dots
[02:00:45] here and so it creates this string and
[02:00:47] then it calls python routine. count and
[02:00:50] then it comes up with the correct answer
[02:00:52] so the python interpreter is doing the
[02:00:53] counting it's not the models mental
[02:00:55] arithmetic doing the counting so it's
[02:00:57] again a simple example of um models need
[02:01:00] tokens to think don't rely on their
[02:01:02] mental arithmetic and um that's why also
[02:01:05] the models are not very good at counting
[02:01:07] if you need them to do counting tasks
[02:01:08] always ask them to lean on the tool now
[02:01:11] the models also have many other little
[02:01:13] cognitive deficits here and there and
[02:01:15] these are kind of like sharp edges of
[02:01:16] the technology to be kind of aware of
[02:01:18] over time so as an example the models
[02:01:20] are not very good with all kinds of
[02:01:22] spelling related tasks they're not very
[02:01:24] good at it and I told you that we would
[02:01:26] loop back around to tokenization and the
[02:01:29] reason to do for this is that the models
[02:01:31] they don't see the characters they see
[02:01:33] tokens and they their entire world is
[02:01:35] about tokens which are these little text
[02:01:37] chunks and so they don't see characters
[02:01:39] like our eyes do and so very simple
[02:01:41] character level tasks often fail so for
[02:01:45] example uh I'm giving it a string
[02:01:47] ubiquitous and I'm asking it to print
[02:01:49] only every third character starting with
[02:01:51] the first one so we start with U and
[02:01:54] then we should go every third so every
[02:01:56] so 1 2 3 Q should be next and then Etc
[02:02:01] so this I see is not correct and again
[02:02:03] my hypothesis is that this is again
[02:02:05] Dental arithmetic here is failing number
[02:02:08] one a little bit but number two I think
[02:02:10] the the more important issue here is
[02:02:12] that if you go to Tik
[02:02:13] tokenizer and you look at ubiquitous we
[02:02:16] see that it is three tokens right so you
[02:02:19] and I see ubiquitous and we can easily
[02:02:21] access the individual letters because we
[02:02:23] kind of see them and when we have it in
[02:02:25] the working memory of our visual sort of
[02:02:27] field we can really easily index into
[02:02:29] every third letter and I can do that
[02:02:31] task but the models don't have access to
[02:02:33] the individual letters they see this as
[02:02:35] these three tokens and uh remember these
[02:02:38] models are trained from scratch on the
[02:02:39] internet and all these token uh
[02:02:42] basically the model has to discover how
[02:02:44] many of all these different letters are
[02:02:45] packed into all these different tokens
[02:02:47] and the reason we even use tokens is
[02:02:49] mostly for efficiency uh but I think a
[02:02:51] lot of people areed interested to delete
[02:02:52] tokens entirely like we should really
[02:02:54] have character level or bite level
[02:02:56] models it's just that that would create
[02:02:58] very long sequences and people don't
[02:02:59] know how to deal with that right now so
[02:03:01] while we have the token World any kind
[02:03:03] of spelling tasks are not actually
[02:03:05] expected to work super well so because I
[02:03:07] know that spelling is not a strong suit
[02:03:09] because of tokenization I can again Ask
[02:03:11] it to lean On Tools so I can just say
[02:03:13] use code and I would again expect this
[02:03:16] to work because the task of copy pasting
[02:03:18] ubiquitous into the python interpreter
[02:03:20] is much easier and then we're leaning on
[02:03:22] python interpreter to manipulate the
[02:03:25] characters of this string so when I say
[02:03:27] use
[02:03:28] code
[02:03:30] ubiquitous yes it indexes into every
[02:03:32] third character and the actual truth is
[02:03:35] u2s
[02:03:36] uqs uh which looks correct to me so um
[02:03:41] again an example of spelling related
[02:03:42] tasks not working very well a very
[02:03:44] famous example of that recently is how
[02:03:47] many R are there in strawberry and this
[02:03:49] went viral many times and basically the
[02:03:51] models now get it correct they say there
[02:03:53] are three Rs in Strawberry but for a
[02:03:55] very long time all the state-of-the-art
[02:03:56] models would insist that there are only
[02:03:58] two RS in strawberry and this caused a
[02:04:00] lot of you know Ruckus because is that a
[02:04:03] word I think so because um it just kind
[02:04:06] of like why are the models so brilliant
[02:04:08] and they can solve math Olympiad
[02:04:10] questions but they can't like count RS
[02:04:12] in strawberry and the answer for that
[02:04:14] again is I've got built up to it kind of
[02:04:16] slowly but number one the models don't
[02:04:18] see characters they see tokens and
[02:04:20] number two they are not very good at
[02:04:22] counting and so here we are combining
[02:04:25] the difficulty of seeing the characters
[02:04:27] with the difficulty of counting and
[02:04:29] that's why the models struggled with
[02:04:30] this even though I think by now honestly
[02:04:33] I think open I may have hardcoded the
[02:04:34] answer here or I'm not sure what they
[02:04:35] did but um uh but this specific query
[02:04:39] now works
[02:04:41] so models are not very good at spelling
[02:04:44] and there there's a bunch of other
[02:04:45] little sharp edges and I don't want to
[02:04:46] go into all of them I just want to show
[02:04:48] you a few examples of things to be aware
[02:04:50] of and uh when you're using these models
[02:04:52] in practice I don't actually want to
[02:04:54] have a comprehensive analysis here of
[02:04:55] all the ways that the models are kind of
[02:04:57] like falling short I just want to make
[02:04:59] the point that there are some Jagged
[02:05:01] edges here and there and we've discussed
[02:05:03] a few of them and a few of them make
[02:05:05] sense but some of them also will just
[02:05:06] not make as much sense and they're kind
[02:05:08] of like you're left scratching your head
[02:05:10] even if you understand in- depth how
[02:05:11] these models work and and good example
[02:05:14] of that recently is the following uh the
[02:05:16] models are not very good at very simple
[02:05:17] questions like this and uh this is
[02:05:20] shocking to a lot of people because
[02:05:22] these math uh these problems can solve
[02:05:23] complex math problems they can answer
[02:05:25] PhD grade physics chemistry biology
[02:05:28] questions much better than I can but
[02:05:30] sometimes they fall short in like super
[02:05:31] simple problems like this so here we go
[02:05:34] 9.11 is bigger than 9.9 and it justifies
[02:05:38] it in some way but obviously and then at
[02:05:40] the end okay it actually it flips its
[02:05:44] decision later so um I don't believe
[02:05:47] that this is very reproducible sometimes
[02:05:49] it flips around its answer sometimes
[02:05:50] gets it right sometimes get it get it
[02:05:52] wrong uh let's try
[02:05:56] again okay even though it might look
[02:05:59] larger okay so here it doesn't even
[02:06:01] correct itself in the end if you ask
[02:06:03] many times sometimes it gets it right
[02:06:04] too but how is it that the model can do
[02:06:07] so great at Olympiad grade problems but
[02:06:10] then fail on very simple problems like
[02:06:12] this and uh I think this one is as I
[02:06:15] mentioned a little bit of a head
[02:06:16] scratcher it turns out that a bunch of
[02:06:18] people studied this in depth and I
[02:06:19] haven't actually read the paper uh but
[02:06:22] what I was told by this team was that
[02:06:24] when you scrutinize the activations
[02:06:27] inside the neural network when you look
[02:06:29] at some of the features and what what
[02:06:31] features turn on or off and what neurons
[02:06:33] turn on or off uh a bunch of neurons
[02:06:35] inside the neural network light up that
[02:06:37] are usually associated with Bible verses
[02:06:40] U and so I think the model is kind of
[02:06:42] like reminded that these almost look
[02:06:44] like Bible verse markers and in a bip
[02:06:48] verse setting 9.11 would come after 99.9
[02:06:52] and so basically the model somehow finds
[02:06:53] it like cognitively very distracting
[02:06:56] that in Bible verses 9.11 would be
[02:06:58] greater um even though here it's
[02:07:00] actually trying to justify it and come
[02:07:02] up to the answer with a math it still
[02:07:04] ends up with the wrong answer here so it
[02:07:07] basically just doesn't fully make sense
[02:07:08] and it's not fully understood and um
[02:07:12] there's a few Jagged issues like that so
[02:07:14] that's why treat this as a as what it is
[02:07:17] which is a St stochastic system that is
[02:07:19] really magical but that you can't also
[02:07:21] fully trust and you want to use it as a
[02:07:23] tool not as something that you kind of
[02:07:25] like letter rip on a problem and
[02:07:27] copypaste the results okay so we have
[02:07:29] now covered two major stages of training
[02:07:32] of large language models we saw that in
[02:07:34] the first stage this is called the
[02:07:36] pre-training stage we are basically
[02:07:38] training on internet documents and when
[02:07:40] you train a language model on internet
[02:07:42] documents you get what's called a base
[02:07:44] model and it's basically an internet
[02:07:45] document simulator right now we saw that
[02:07:48] this is an interesting artifact and uh
[02:07:51] this takes many months to train on
[02:07:53] thousands of computers and it's kind of
[02:07:54] a lossy compression of the internet and
[02:07:57] it's extremely interesting but it's not
[02:07:58] directly useful because we don't want to
[02:08:00] sample internet documents we want to ask
[02:08:02] questions of an AI and have it respond
[02:08:05] to our questions so for that we need an
[02:08:07] assistant and we saw that we can
[02:08:09] actually construct an assistant in the
[02:08:11] process of a post
[02:08:13] training and specifically in the process
[02:08:16] of supervised fine-tuning as we call
[02:08:19] it so in this stage we saw that it's
[02:08:22] algorithmically identical to
[02:08:24] pre-training nothing is going to change
[02:08:25] the only thing that changes is the data
[02:08:27] set so instead of Internet documents we
[02:08:30] now want to create and curate a very
[02:08:32] nice data set of conversations so we
[02:08:35] want Millions conversations on all kinds
[02:08:38] of diverse topics between a human and an
[02:08:41] assistant and fundamentally these
[02:08:44] conversations are created by humans so
[02:08:47] humans write the prompts and humans
[02:08:49] write the ideal response responses and
[02:08:52] they do that based on labeling
[02:08:54] documentations now in the modern stack
[02:08:57] it's not actually done fully and
[02:08:59] manually by humans right they actually
[02:09:00] now have a lot of help from these tools
[02:09:02] so we can use language models um to help
[02:09:05] us create these data sets and that's
[02:09:07] done extensively but fundamentally it's
[02:09:09] all still coming from Human curation at
[02:09:10] the end so we create these conversations
[02:09:13] that now becomes our data set we fine
[02:09:15] tune on it or continue training on it
[02:09:17] and we get an assistant and then we kind
[02:09:20] of shifted gears and started talking
[02:09:21] about some of the kind of cognitive
[02:09:22] implications of what this assistant is
[02:09:24] like and we saw that for example the
[02:09:26] assistant will hallucinate if you don't
[02:09:29] take some sort of mitigations towards it
[02:09:32] so we saw that hallucinations would be
[02:09:34] common and then we looked at some of the
[02:09:35] mitigations of those hallucinations and
[02:09:38] then we saw that the models are quite
[02:09:39] impressive and can do a lot of stuff in
[02:09:40] their head but we saw that they can also
[02:09:43] Lean On Tools to become better so for
[02:09:45] example we can lo lean on a web search
[02:09:48] in order to hallucinate less and to
[02:09:50] maybe bring up some more um recent
[02:09:53] information or something like that or we
[02:09:54] can lean on tools like code interpreter
[02:09:57] so the code can so the llm can write
[02:09:59] some code and actually run it and see
[02:10:00] the
[02:10:01] results so these are some of the topics
[02:10:03] we looked at so far um now what I'd like
[02:10:06] to do is I'd like to cover the last and
[02:10:09] major stage of this Pipeline and that is
[02:10:12] reinforcement learning so reinforcement
[02:10:15] learning is still kind of thought to be
[02:10:16] under the umbrella of posttraining uh
[02:10:19] but it is the last third major stage and
[02:10:22] it's a different way of training
[02:10:24] language models and usually follows as
[02:10:26] this third step so inside companies like
[02:10:29] open AI you will start here and these
[02:10:31] are all separate teams so there's a team
[02:10:33] doing data for pre-training and a team
[02:10:35] doing training for pre-training and then
[02:10:37] there's a team doing all the
[02:10:39] conversation generation in a in a
[02:10:42] different team that is kind of doing the
[02:10:44] supervis fine tuning and there will be a
[02:10:45] team for the reinforcement learning as
[02:10:47] well so it's kind of like a handoff of
[02:10:49] these models you get your base model the
[02:10:51] then you find you need to be an
[02:10:52] assistant and then you go into
[02:10:53] reinforcement learning which we'll talk
[02:10:55] about uh
[02:10:56] now so that's kind of like the major
[02:10:58] flow and so let's now focus on
[02:11:01] reinforcement learning the last major
[02:11:03] stage of training and let me first
[02:11:05] actually motivate it and why we would
[02:11:07] want to do reinforcement learning and
[02:11:09] what it looks like on a high level so I
[02:11:11] would now like to try to motivate the
[02:11:12] reinforcement learning stage and what it
[02:11:13] corresponds to with something that
[02:11:15] you're probably familiar with and that
[02:11:16] is basically going to school so just
[02:11:19] like you went to school to become um
[02:11:21] really good at something we want to take
[02:11:23] large language models through school and
[02:11:25] really what we're doing is um we're um
[02:11:29] we have a few paradigms of ways of uh
[02:11:32] giving them knowledge or transferring
[02:11:33] skills so in particular when we're
[02:11:36] working with textbooks in school you'll
[02:11:38] see that there are three major kind of
[02:11:40] uh pieces of information in these
[02:11:42] textbooks three classes of information
[02:11:45] the first thing you'll see is you'll see
[02:11:46] a lot of exposition um and by the way
[02:11:49] this is a totally random book I pulled
[02:11:50] from the internet I I think it's some
[02:11:51] kind of an organic chemistry or
[02:11:53] something I'm not sure uh but the
[02:11:55] important thing is that you'll see that
[02:11:56] most of the text most of it is kind of
[02:11:58] just like the meat of it is exposition
[02:12:00] it's kind of like background knowledge
[02:12:02] Etc as you are reading through the words
[02:12:05] of this Exposition you can think of that
[02:12:08] roughly as training on that data so um
[02:12:12] and that's why when you're reading
[02:12:13] through this stuff this background
[02:12:14] knowledge and this all this context
[02:12:16] information it's kind of equivalent to
[02:12:18] pre-training so it's it's where we build
[02:12:21] sort of like a knowledge base of this
[02:12:23] data and get a sense of the topic the
[02:12:27] next major kind of information that you
[02:12:28] will see is these uh problems and with
[02:12:32] their worked Solutions so basically a
[02:12:35] human expert in this case uh the author
[02:12:37] of this book has given us not just a
[02:12:39] problem but has also worked through the
[02:12:41] solution and the solution is basically
[02:12:43] like equivalent to having like this
[02:12:45] ideal response for an assistant so it's
[02:12:48] basically the expert is showing us how
[02:12:49] to solve the problem in it's uh kind of
[02:12:52] like um in its full form so as we are
[02:12:55] reading the solution we are basically
[02:12:57] training on the expert data and then
[02:13:01] later we can try to imitate the expert
[02:13:03] um and basically um that's that roughly
[02:13:07] correspond to having the sft model
[02:13:08] that's what it would be doing so
[02:13:11] basically we've already done
[02:13:12] pre-training and we've already covered
[02:13:14] this um imitation of experts and how
[02:13:17] they solve these problems and the third
[02:13:19] stage of reinforcement learning is
[02:13:21] basically the practice problems so
[02:13:24] sometimes you'll see this is just a
[02:13:25] single practice problem here but of
[02:13:27] course there will be usually many
[02:13:28] practice problems at the end of each
[02:13:30] chapter in any textbook and practice
[02:13:32] problems of course we know are critical
[02:13:34] for learning because what are they
[02:13:36] getting you to do they're getting you to
[02:13:37] practice uh to practice yourself and
[02:13:39] discover ways of solving these problems
[02:13:42] yourself and so what you get in a
[02:13:44] practice problem is you get a problem
[02:13:46] description but you're not given the
[02:13:48] solution but you are given the final
[02:13:50] answer answer usually in the answer key
[02:13:53] of the textbook and so you know the
[02:13:55] final answer that you're trying to get
[02:13:56] to and you have the problem statement
[02:13:58] but you don't have the solution you are
[02:14:00] trying to practice the solution you're
[02:14:02] trying out many different things and
[02:14:04] you're seeing what gets you to the final
[02:14:07] solution the best and so you're
[02:14:09] discovering how to solve these problems
[02:14:11] so and in the process of that you're
[02:14:13] relying on number one the background
[02:14:14] information which comes from
[02:14:15] pre-training and number two maybe a
[02:14:17] little bit of imitation of human experts
[02:14:20] and you can probably try similar kinds
[02:14:22] of solutions and so on so we've done
[02:14:25] this and this and now in this section
[02:14:27] we're going to try to practice and so
[02:14:30] we're going to be given prompts we're
[02:14:32] going to be given Solutions U sorry the
[02:14:34] final answers but we're not going to be
[02:14:36] given expert Solutions we have to
[02:14:38] practice and try stuff out and that's
[02:14:40] what reinforcement learning is about
[02:14:43] okay so let's go back to the problem
[02:14:44] that we worked with previously just so
[02:14:46] we have a concrete example to talk
[02:14:47] through as we explore sort of the topic
[02:14:50] here so um I'm here in the Teck
[02:14:52] tokenizer because I'd also like to well
[02:14:55] I get a text box which is useful but
[02:14:57] number two I want to remind you again
[02:14:59] that we're always working with
[02:14:59] onedimensional token sequences and so um
[02:15:02] I actually like prefer this view because
[02:15:04] this is like the native view of the llm
[02:15:06] if that makes sense like this is what it
[02:15:08] actually sees it sees token IDs right
[02:15:11] okay so Emily buys three apples and two
[02:15:14] oranges each orange is $2 the total cost
[02:15:17] of all the fruit is $13 what is the cost
[02:15:19] of each apple
[02:15:21] and what I'd like to what I like you to
[02:15:23] appreciate here is these are like four
[02:15:26] possible candidate Solutions as an
[02:15:29] example and they all reach the answer
[02:15:31] three now what I'd like you to
[02:15:33] appreciate at this point is that if I am
[02:15:35] the human data labeler that is creating
[02:15:37] a conversation to be entered into the
[02:15:39] training set I don't actually really
[02:15:42] know which of these
[02:15:44] conversations to um to add to the data
[02:15:48] set some of these conversations kind of
[02:15:50] set up a system equations some of them
[02:15:52] sort of like just talk through it in
[02:15:54] English and some of them just kind of
[02:15:55] like skip right through to the
[02:15:58] solution um if you look at chbt for
[02:16:00] example and you give it this question it
[02:16:03] defines a system of variables and it
[02:16:05] kind of like does this little thing what
[02:16:07] we have to appreciate and uh
[02:16:08] differentiate between though is um the
[02:16:12] first purpose of a solution is to reach
[02:16:14] the right answer of course we want to
[02:16:15] get the final answer three that is the
[02:16:17] that is the important purpose here but
[02:16:19] there's kind of like a secondary purpose
[02:16:21] as well where here we are also just kind
[02:16:23] of trying to make it like nice uh for
[02:16:26] the human because we're kind of assuming
[02:16:27] that the person wants to see the
[02:16:29] solution they want to see the
[02:16:30] intermediate steps we want to present it
[02:16:31] nicely Etc so there are two separate
[02:16:33] things going on here number one is the
[02:16:36] presentation for the human but number
[02:16:37] two we're trying to actually get the
[02:16:38] right answer um so let's for the moment
[02:16:42] focus on just reaching the final answer
[02:16:44] if we're only care if we only care about
[02:16:46] the final answer then which of these is
[02:16:49] the optimal or the best prompt um sorry
[02:16:53] the best solution for the llm to reach
[02:16:56] the right
[02:16:57] answer um and what I'm trying to get at
[02:17:00] is we don't know me as a human labeler I
[02:17:03] would not know which one of these is
[02:17:04] best so as an example we saw earlier on
[02:17:07] when we looked at
[02:17:09] um the token sequences here and the
[02:17:11] mental arithmetic and reasoning we saw
[02:17:14] that for each token we can only spend
[02:17:15] basically a finite number of finite
[02:17:18] amount of compute here that is not very
[02:17:19] large or you should think about it that
[02:17:20] way way and so we can't actually make
[02:17:23] too big of a leap in any one token is is
[02:17:26] maybe the way to think about it so as an
[02:17:28] example in this one what's really nice
[02:17:30] about it is that it's very few tokens so
[02:17:32] it's going to take us very short amount
[02:17:34] of time to get to the answer but right
[02:17:37] here when we're doing 30 - 4 IDE 3
[02:17:39] equals right in this token here we're
[02:17:42] actually asking for a lot of computation
[02:17:44] to happen on that single individual
[02:17:45] token and so maybe this is a bad example
[02:17:48] to give to the llm because it's kind of
[02:17:49] incentivizing it to skip through the
[02:17:50] calculations very quickly and it's going
[02:17:52] to actually make up mistakes make
[02:17:54] mistakes in this mental arithmetic uh so
[02:17:56] maybe it would work better to like
[02:17:58] spread out the spread it out more maybe
[02:18:01] it would be better to set it up as an
[02:18:02] equation maybe it would be better to
[02:18:04] talk through it we fundamentally don't
[02:18:06] know and we don't know because what is
[02:18:09] easy for you or I as or as human
[02:18:12] labelers what's easy for us or hard for
[02:18:14] us is different than what's easy or hard
[02:18:16] for the llm it cognition is different um
[02:18:20] and the token sequences are kind of like
[02:18:23] different hard for it and so some of the
[02:18:27] token sequences here that are trivial
[02:18:30] for me might be um very too much of a
[02:18:33] leap for the llm so right here this
[02:18:36] token would be way too hard but
[02:18:38] conversely many of the tokens that I'm
[02:18:40] creating here might be just trivial to
[02:18:43] the llm and we're just wasting tokens
[02:18:45] like why waste all these tokens when
[02:18:46] this is all trivial so if the only thing
[02:18:49] we care care about is the final answer
[02:18:51] and we're separating out the issue of
[02:18:53] the presentation to the human um then we
[02:18:56] don't actually really know how to
[02:18:57] annotate this example we don't know what
[02:18:59] solution to get to the llm because we
[02:19:01] are not the
[02:19:02] llm and it's clear here in the case of
[02:19:05] like the math example but this is
[02:19:07] actually like a very pervasive issue
[02:19:08] like for our knowledge is not lm's
[02:19:11] knowledge like the llm actually has a
[02:19:13] ton of knowledge of PhD in math and
[02:19:15] physics chemistry and whatnot so in many
[02:19:17] ways it actually knows more than I do
[02:19:19] and I'm I'm potentially not utilizing
[02:19:21] that knowledge in its problem solving
[02:19:24] but conversely I might be injecting a
[02:19:26] bunch of knowledge in my solutions that
[02:19:28] the LM doesn't know in its parameters
[02:19:31] and then those are like sudden leaps
[02:19:33] that are very confusing to the model and
[02:19:36] so our cognitions are different and I
[02:19:38] don't really know what to put here if
[02:19:41] all we care about is the reaching the
[02:19:42] final solution and doing it economically
[02:19:45] ideally and so long story short we are
[02:19:49] not in a good position to create these
[02:19:52] uh token sequences for the LM and
[02:19:55] they're useful by imitation to
[02:19:56] initialize the system but we really want
[02:19:59] the llm to discover the token sequences
[02:20:01] that work for it we need to find it
[02:20:04] needs to find for itself what token
[02:20:06] sequence reliably gets to the answer
[02:20:09] given the prompt and it needs to
[02:20:11] discover that in the process of
[02:20:12] reinforcement learning and of trial and
[02:20:14] error so let's see how this example
[02:20:18] would work like in reinforcement
[02:20:19] learning
[02:20:21] okay so we're now back in the huging
[02:20:23] face inference playground and uh that
[02:20:26] just allows me to very easily call uh
[02:20:28] different kinds of models so as an
[02:20:29] example here on the top right I chose
[02:20:31] the Gemma 2 2 billion parameter model so
[02:20:34] two billion is very very small so this
[02:20:36] is a tiny model but it's okay so we're
[02:20:39] going to give it um the way that
[02:20:40] reinforcement learning will basically
[02:20:41] work is actually quite quite simple um
[02:20:44] we need to try many different kinds of
[02:20:47] solutions and we want to see which
[02:20:49] Solutions work well or not
[02:20:51] so we're basically going to take the
[02:20:53] prompt we're going to run the
[02:20:55] model and the model generates a solution
[02:20:58] and then we're going to inspect the
[02:20:59] solution and we know that the correct
[02:21:02] answer for this one is $3 and so indeed
[02:21:05] the model gets it correct it says it's
[02:21:06] $3 so this is correct so that's just one
[02:21:10] attempt at DIS solution so now we're
[02:21:11] going to delete this and we're going to
[02:21:13] rerun it again let's try a second
[02:21:15] attempt so the model solves it in a bit
[02:21:17] slightly different way right every
[02:21:19] single attempt will be a different
[02:21:21] generation because these models are
[02:21:23] stochastic systems remember that at
[02:21:24] every single token here we have a
[02:21:26] probability distribution and we're
[02:21:27] sampling from that distribution so we
[02:21:29] end up kind kind of going down slightly
[02:21:31] different paths and so this is a second
[02:21:34] solution that also ends in the correct
[02:21:36] answer now we're going to delete that
[02:21:38] let's go a third
[02:21:39] time okay so again slightly different
[02:21:42] solution but also gets it
[02:21:44] correct now we can actually repeat this
[02:21:46] uh many times and so in practice you
[02:21:49] might actually sample thousand of
[02:21:51] independent Solutions or even like
[02:21:52] million solutions for just a single
[02:21:55] prompt um and some of them will be
[02:21:57] correct and some of them will not be
[02:21:58] very correct and basically what we want
[02:22:00] to do is we want to encourage the
[02:22:02] solutions that lead to correct answers
[02:22:05] so let's take a look at what that looks
[02:22:06] like so if we come back over here here's
[02:22:09] kind of like a cartoon diagram of what
[02:22:10] this is looking like we have a prompt
[02:22:13] and then we tried many different
[02:22:15] solutions in
[02:22:16] parallel and some of the solutions um
[02:22:19] might go well so they get the right
[02:22:21] answer which is in green and some of the
[02:22:24] solutions might go poorly and may not
[02:22:25] reach the right answer which is red now
[02:22:28] this problem here unfortunately is not
[02:22:29] the best example because it's a trivial
[02:22:32] prompt and as we saw uh even like a two
[02:22:34] billion parameter model always gets it
[02:22:36] right so it's not the best example in
[02:22:38] that sense but let's just exercise some
[02:22:40] imagination here and let's just suppose
[02:22:43] that the um green ones are good and the
[02:22:47] red ones are
[02:22:48] bad okay so we generated 15 Solutions
[02:22:52] only four of them got the right answer
[02:22:54] and so now what we want to do is
[02:22:56] basically we want to encourage the kinds
[02:22:58] of solutions that lead to right answers
[02:23:00] so whatever token sequences happened in
[02:23:03] these red Solutions obviously something
[02:23:05] went wrong along the way somewhere and
[02:23:07] uh this was not a good path to take
[02:23:09] through the solution and whatever token
[02:23:11] sequences there were in these Green
[02:23:13] Solutions well things went uh pretty
[02:23:15] well in this situation and so we want to
[02:23:18] do more things like it in prompts like
[02:23:21] this and the way we encourage this kind
[02:23:23] of a behavior in the future is we
[02:23:25] basically train on these sequences um
[02:23:28] but these training sequencies now are
[02:23:29] not coming from expert human annotators
[02:23:32] there's no human who decided that this
[02:23:33] is the correct solution this solution
[02:23:36] came from the model itself so the model
[02:23:38] is practicing here it's tried out a few
[02:23:40] Solutions four of them seem to have
[02:23:41] worked and now the model will kind of
[02:23:43] like train on them and this corresponds
[02:23:45] to a student basically looking at their
[02:23:47] Solutions and being like okay well this
[02:23:48] one worked really well so this is this
[02:23:50] is how I should be solving these kinds
[02:23:52] of problems and uh here in this example
[02:23:55] there are many different ways to
[02:23:57] actually like really tweak the
[02:23:58] methodology a little bit here but just
[02:24:00] to give the core idea across maybe it's
[02:24:02] simplest to just think about take the
[02:24:04] taking the single best solution out of
[02:24:06] these four uh like say this one that's
[02:24:08] why it was yellow uh so this is the the
[02:24:12] solution that not only led to the right
[02:24:13] answer but may maybe had some other nice
[02:24:15] properties maybe it was the shortest one
[02:24:17] or it looked nicest in some ways or uh
[02:24:20] there's other criteria you could think
[02:24:21] of as an example but we're going to
[02:24:23] decide that this the top solution we're
[02:24:25] going to train on it and then uh the
[02:24:28] model will be slightly more likely once
[02:24:30] you do the parameter update to take this
[02:24:33] path in this kind of a setting in the
[02:24:36] future but you have to remember that
[02:24:38] we're going to run many different
[02:24:39] diverse prompts across lots of math
[02:24:42] problems and physics problems and
[02:24:43] whatever wherever there might be so tens
[02:24:46] of thousands of prompts maybe have in
[02:24:47] mind there's thousands of solutions
[02:24:50] prompt and so this is all happening kind
[02:24:52] of like at the same time and as we're
[02:24:55] iterating this process the model is
[02:24:57] discovering for itself what kinds of
[02:24:59] token sequences lead it to correct
[02:25:02] answers it's not coming from a human
[02:25:05] annotator the the model is kind of like
[02:25:08] playing in this playground and it knows
[02:25:10] what it's trying to get to and it's
[02:25:12] discovering sequences that work for it
[02:25:15] uh these are sequences that don't make
[02:25:16] any mental leaps uh they they seem to
[02:25:19] work reliably and statistically and uh
[02:25:23] fully utilize the knowledge of the model
[02:25:25] as it has it and so uh this is the
[02:25:28] process of reinforcement
[02:25:29] learning it's basically a guess and
[02:25:31] check we're going to guess many
[02:25:32] different types of solutions we're going
[02:25:33] to check them and we're going to do more
[02:25:35] of what worked in the future and that is
[02:25:38] uh reinforcement learning so in the
[02:25:40] context of what came before we see now
[02:25:43] that the sft model the supervised fine
[02:25:45] tuning model it's still helpful because
[02:25:47] it still kind of like initializes the
[02:25:49] model a little bit into to the vicinity
[02:25:51] of the correct Solutions so it's kind of
[02:25:53] like a initialization of um of the model
[02:25:56] in the sense that it kind of gets the
[02:25:58] model to you know take Solutions like
[02:26:00] write out Solutions and maybe it has an
[02:26:03] understanding of setting up a system of
[02:26:04] equations or maybe it kind of like talks
[02:26:06] through a solution so it gets you into
[02:26:08] the vicinity of correct Solutions but
[02:26:10] reinforcement learning is where
[02:26:11] everything gets dialed in we really
[02:26:13] discover the solutions that work for the
[02:26:15] model get the right answers we encourage
[02:26:17] them and then the model just kind of
[02:26:19] like gets better over time time okay so
[02:26:21] that is the high Lev process for how we
[02:26:23] train large language models in short we
[02:26:26] train them kind of very similar to how
[02:26:27] we train children and basically the only
[02:26:30] difference is that children go through
[02:26:32] chapters of books and they do all these
[02:26:34] different types of training exercises um
[02:26:37] kind of within the chapter of each book
[02:26:39] but instead when we train AIS it's
[02:26:41] almost like we kind of do it stage by
[02:26:43] stage depending on the type of that
[02:26:45] stage so first what we do is we do
[02:26:47] pre-training which as we saw is
[02:26:49] equivalent to uh basically reading all
[02:26:51] the expository material so we look at
[02:26:53] all the textbooks at the same time and
[02:26:55] we read all the exposition and we try to
[02:26:57] build a knowledge base the second thing
[02:27:00] then is we go into the sft stage which
[02:27:02] is really looking at all the fixed uh
[02:27:04] sort of like solutions from Human
[02:27:07] Experts of all the different kinds of
[02:27:09] worked Solutions across all the
[02:27:11] textbooks and we just kind of get an sft
[02:27:14] model which is able to imitate the
[02:27:16] experts but does so kind of blindly it
[02:27:18] just kind of like does its best guess
[02:27:20] uh kind of just like trying to mimic
[02:27:22] statistically the expert behavior and so
[02:27:24] that's what you get when you look at all
[02:27:26] the work Solutions and then finally in
[02:27:28] the last stage we do all the practice
[02:27:30] problems in the RL stage across all the
[02:27:33] textbooks we only do the practice
[02:27:35] problems and that's how we get the RL
[02:27:37] model so on a high level the way we
[02:27:40] train llms is very much equivalent uh to
[02:27:43] the process that we train uh that we use
[02:27:45] for training of children the next point
[02:27:47] I would like to make is that actually
[02:27:49] these first two stat ages pre-training
[02:27:51] and surprise fine-tuning they've been
[02:27:52] around for years and they are very
[02:27:53] standard and everyone does them all the
[02:27:55] different llm providers it is this last
[02:27:58] stage the RL training that is a lot more
[02:28:00] early in its process of development and
[02:28:02] is not standard yet in the field and so
[02:28:06] um this stage is a lot more kind of
[02:28:09] early and nent and the reason for that
[02:28:11] is because I actually skipped over a ton
[02:28:13] of little details here in this process
[02:28:15] the high level idea is very simple it's
[02:28:17] trial and there learning but there's a
[02:28:18] ton of details and little math
[02:28:20] mathematical kind of like nuances to
[02:28:21] exactly how you pick the solutions that
[02:28:23] are the best and how much you train on
[02:28:25] them and what is the prompt distribution
[02:28:27] and how to set up the training run such
[02:28:29] that this actually works so there's a
[02:28:30] lot of little details and knobs to the
[02:28:32] core idea that is very very simple and
[02:28:35] so getting the details right here uh is
[02:28:37] not trivial and so a lot of companies
[02:28:40] like for example open and other LM
[02:28:41] providers have experimented internally
[02:28:44] with reinforcement learning fine tuning
[02:28:46] for llms for a while but they've not
[02:28:48] talked about it publicly
[02:28:50] um it's all kind of done inside the
[02:28:52] company and so that's why the paper from
[02:28:55] Deep seek that came out very very
[02:28:56] recently was such a big deal because
[02:28:59] this is a paper from this company called
[02:29:01] DC Kai in China and this paper really
[02:29:05] talked very publicly about reinforcement
[02:29:07] learning fine training for large
[02:29:08] language models and how incredibly
[02:29:10] important it is for large language
[02:29:12] models and how it brings out a lot of
[02:29:14] reasoning capabilities in the models
[02:29:16] we'll go into this in a second so this
[02:29:18] paper reinvigorated the public interest
[02:29:21] of using RL for llms and gave a lot of
[02:29:25] the um sort of n-r details that are
[02:29:27] needed to reproduce their results and
[02:29:29] actually get the stage to work for large
[02:29:31] langage models so let me take you
[02:29:33] briefly through this uh deep seek R1
[02:29:35] paper and what happens when you actually
[02:29:36] correctly apply RL to language models
[02:29:38] and what that looks like and what that
[02:29:39] gives you so the first thing I'll scroll
[02:29:41] to is this uh kind of figure two here
[02:29:43] where we are looking at the Improvement
[02:29:45] in how the models are solving
[02:29:47] mathematical problems so this is the
[02:29:49] accuracy of solving mathematical
[02:29:50] problems on the a accuracy and then we
[02:29:54] can go to the web page and we can see
[02:29:55] the kinds of problems that are actually
[02:29:56] in these um these the kinds of math
[02:29:58] problems that are being measured here so
[02:30:00] these are simple math problems you can
[02:30:02] um pause the video if you like but these
[02:30:04] are the kinds of problems that basically
[02:30:06] the models are being asked to solve and
[02:30:08] you can see that in the beginning
[02:30:09] they're not doing very well but then as
[02:30:10] you update the model with this many
[02:30:12] thousands of steps their accuracy kind
[02:30:14] of continues to climb so the models are
[02:30:17] improving and they're solving these
[02:30:18] problems with a higher accuracy
[02:30:20] as you do this trial and error on a
[02:30:22] large data set of these kinds of
[02:30:24] problems and the models are discovering
[02:30:26] how to solve math problems but even more
[02:30:29] incredible than the quantitative kind of
[02:30:32] results of solving these problems with a
[02:30:33] higher accuracy is the qualitative means
[02:30:35] by which the model achieves these
[02:30:37] results so when we scroll down uh one of
[02:30:40] the figures here that is kind of
[02:30:41] interesting is that later on in the
[02:30:43] optimization the model seems to be uh
[02:30:46] using average length per response uh
[02:30:49] goes up up so the model seems to be
[02:30:51] using more tokens to get its higher
[02:30:54] accuracy results so it's learning to
[02:30:56] create very very long Solutions why are
[02:30:59] these Solutions very long we can look at
[02:31:00] them qualitatively here so basically
[02:31:03] what they discover is that the model
[02:31:05] solution get very very long partially
[02:31:07] because so here's a question and here's
[02:31:09] kind of the answer from the model what
[02:31:11] the model learns to do um and this is an
[02:31:13] immerging property of new optimization
[02:31:15] it just discovers that this is good for
[02:31:17] problem solving is it starts to do stuff
[02:31:19] like this wait wait wait that's Nota
[02:31:21] moment I can flag here let's reevaluate
[02:31:23] this step by step to identify the
[02:31:25] correct sum can be so what is the model
[02:31:27] doing here right the model is basically
[02:31:30] re-evaluating steps it has learned that
[02:31:32] it works better for accuracy to try out
[02:31:35] lots of ideas try something from
[02:31:37] different perspectives retrace reframe
[02:31:39] backtrack is doing a lot of the things
[02:31:41] that you and I are doing in the process
[02:31:43] of problem solving for mathematical
[02:31:44] questions but it's rediscovering what
[02:31:46] happens in your head not what you put
[02:31:48] down on the solution and there is no
[02:31:50] human who can hardcode this stuff in the
[02:31:52] ideal assistant response this is only
[02:31:55] something that can be discovered in the
[02:31:56] process of reinforcement learning
[02:31:57] because you wouldn't know what to put
[02:31:59] here this just turns out to work for the
[02:32:02] model and it improves its accuracy in
[02:32:04] problem solving so the model learns what
[02:32:06] we call these chains of thought in your
[02:32:08] head and it's an emergent property of
[02:32:10] the optim of the optimization and that's
[02:32:13] what's bloating up the response length
[02:32:16] but that's also what's increasing the
[02:32:18] accuracy of the problem problem solving
[02:32:20] so what's incredible here is basically
[02:32:22] the model is discovering ways to think
[02:32:24] it's learning what I like to call
[02:32:26] cognitive strategies of how you
[02:32:28] manipulate a problem and how you
[02:32:30] approach it from different perspectives
[02:32:31] how you pull in some analogies or do
[02:32:33] different kinds of things like that and
[02:32:35] how you kind of uh try out many
[02:32:37] different things over time uh check a
[02:32:39] result from different perspectives and
[02:32:40] how you kind of uh solve problems but
[02:32:43] here it's kind of discovered by the RL
[02:32:44] so extremely incredible to see this
[02:32:47] emerge in the optimization without
[02:32:48] having to hardcode it anywhere the only
[02:32:50] thing we've given it are the correct
[02:32:52] answers and this comes out from trying
[02:32:54] to just solve them correctly which is
[02:32:56] incredible
[02:32:58] um now let's go back to actually the
[02:33:00] problem that we've been working with and
[02:33:02] let's take a look at what it would look
[02:33:03] like uh for uh for this kind of a model
[02:33:07] what we call reasoning or thinking model
[02:33:09] to solve that problem okay so recall
[02:33:12] that this is the problem we've been
[02:33:13] working with and when I pasted it into
[02:33:15] chat GPT 40 I'm getting this kind of a
[02:33:17] response let's take a look at what
[02:33:19] happens when you give this same query to
[02:33:22] what's called a reasoning or a thinking
[02:33:23] model this is a model that was trained
[02:33:25] with reinforcement learning so this
[02:33:28] model described in this paper DC car1 is
[02:33:30] available on chat. dec.com uh so this is
[02:33:34] kind of like the company uh that
[02:33:35] developed is hosting it you have to make
[02:33:37] sure that the Deep think button is
[02:33:39] turned on to get the R1 model as it's
[02:33:41] called we can paste it here and run
[02:33:44] it and so let's take a look at what
[02:33:46] happens now and what is the output of
[02:33:48] the model okay so here's it says so this
[02:33:51] is previously what we get using
[02:33:53] basically what's an sft approach a
[02:33:54] supervised funing approach this is like
[02:33:56] mimicking an expert solution this is
[02:33:58] what we get from the RL model okay let
[02:34:01] me try to figure this out so Emily buys
[02:34:03] three apples and two oranges each orange
[02:34:05] cost $2 total is 13 I need to find out
[02:34:07] blah blah blah so here you you um as
[02:34:11] you're reading this you can't escape
[02:34:14] thinking that this model is
[02:34:16] thinking um is definitely pursuing the
[02:34:19] solution solution it deres that it must
[02:34:21] cost $3 and then it says wait a second
[02:34:23] let me check my math again to be sure
[02:34:25] and then it tries it from a slightly
[02:34:26] different perspective and then it says
[02:34:28] yep all that checks out I think that's
[02:34:30] the answer I don't see any mistakes let
[02:34:33] me see if there's another way to
[02:34:34] approach the problem maybe setting up an
[02:34:36] equation let's let the cost of one apple
[02:34:39] be $8 then blah blah blah yep same
[02:34:42] answer so definitely each apple is $3
[02:34:44] all right confident that that's correct
[02:34:47] and then what it does once it sort of um
[02:34:49] did the thinking process is it writes up
[02:34:51] the nice solution for the human and so
[02:34:54] this is now considering so this is more
[02:34:56] about the correctness aspect and this is
[02:34:58] more about the presentation aspect where
[02:35:00] it kind of like writes it out nicely and
[02:35:03] uh boxes in the correct answer at the
[02:35:05] bottom and so what's incredible about
[02:35:07] this is we get this like thinking
[02:35:08] process of the model and this is what's
[02:35:10] coming from the reinforcement learning
[02:35:12] process this is what's bloating up the
[02:35:15] length of the token sequences they're
[02:35:16] doing thinking and they're trying
[02:35:17] different ways this is what's giving you
[02:35:20] higher accuracy in problem
[02:35:22] solving and this is where we are seeing
[02:35:24] these aha moments and these different
[02:35:26] strategies and these um ideas for how
[02:35:29] you can make sure that you're getting
[02:35:31] the correct
[02:35:32] answer the last point I wanted to make
[02:35:34] is some people are a little bit nervous
[02:35:36] about putting you know very sensitive
[02:35:38] data into chat.com because this is a
[02:35:41] Chinese company so people don't um
[02:35:43] people are a little bit careful and Cy
[02:35:45] with that a little bit um deep seek R1
[02:35:48] is a model that was released by this
[02:35:50] company so this is an open source model
[02:35:52] or open weights model it is available
[02:35:54] for anyone to download and use you will
[02:35:56] not be able to like run it in its full
[02:35:59] um sort of the full model in full
[02:36:02] Precision you won't run that on a
[02:36:04] MacBook but uh or like a local device
[02:36:07] because this is a fairly large model but
[02:36:08] many companies are hosting the full
[02:36:10] largest model one of those companies
[02:36:12] that I like to use is called
[02:36:14] together. so when you go to together.
[02:36:17] you sign up and you go to playgrounds
[02:36:19] you can can select here in the chat deep
[02:36:21] seek R1 and there's many different kinds
[02:36:23] of other models that you can select here
[02:36:25] these are all state-of-the-art models so
[02:36:27] this is kind of similar to the hugging
[02:36:28] face inference playground that we've
[02:36:29] been playing with so far but together. a
[02:36:32] will usually host all the
[02:36:33] state-of-the-art models so select DT
[02:36:36] car1 um you can try to ignore a lot of
[02:36:38] these I think the default settings will
[02:36:39] often be okay and we can put in this and
[02:36:43] because the model was released by Deep
[02:36:45] seek what you're getting here should be
[02:36:47] basically equivalent to what you're
[02:36:48] getting here now because of the
[02:36:50] randomness in the sampling we're going
[02:36:51] to get something slightly different uh
[02:36:53] but in principle this should be uh
[02:36:55] identical in terms of the power of the
[02:36:57] model and you should be able to see the
[02:36:58] same things quantitatively and
[02:37:00] qualitatively uh but uh this model is
[02:37:02] coming from kind of a an American
[02:37:04] company so that's deep seek and that's
[02:37:07] the what's called a reasoning
[02:37:09] model now when I go back to chat uh let
[02:37:12] me go to chat here okay so the models
[02:37:14] that you're going to see in the drop
[02:37:15] down here some of them like 01 03 mini
[02:37:18] O3 mini High Etc they are talking about
[02:37:21] uses Advanced reasoning now what this is
[02:37:23] referring to uses Advanced reasoning is
[02:37:26] it's referring to the fact that it was
[02:37:27] trained by reinforcement learning with
[02:37:29] techniques very similar to those of deep
[02:37:31] C car1 per public statements of opening
[02:37:34] ey employees uh so these are thinking
[02:37:37] models trained with RL and these models
[02:37:40] like GPT 4 or GPT 4 40 mini that you're
[02:37:42] getting in the free tier you should
[02:37:43] think of them as mostly sft models
[02:37:45] supervised fine tuning models they don't
[02:37:47] actually do this like thinking as as you
[02:37:49] see in the RL models and even though
[02:37:52] there's a little bit of reinforcement
[02:37:53] learning involved with these models and
[02:37:55] I'll go that into that in a second these
[02:37:56] are mostly sft models I think you should
[02:37:58] think about it that way so in the same
[02:38:00] way as what we saw here we can pick one
[02:38:03] of the thinking models like say 03 mini
[02:38:05] high and these models by the way might
[02:38:07] not be available to you unless you pay a
[02:38:09] Chachi PT subscription of either $20 per
[02:38:11] month or $200 per month for some of the
[02:38:14] top models so we can pick a thinking
[02:38:16] model and run now what's going to happen
[02:38:20] here is it's going to say reasoning and
[02:38:21] it's going to start to do stuff like
[02:38:23] this and um what we're seeing here is
[02:38:26] not exactly the stuff we're seeing here
[02:38:29] so even though under the hood the model
[02:38:31] produces these kinds of uh kind of
[02:38:34] chains of thought opening ey chooses to
[02:38:36] not show the exact chains of thought in
[02:38:38] the web interface it shows little
[02:38:40] summaries of that of those chains of
[02:38:42] thought and open kind of does this I
[02:38:44] think partly because uh they are worried
[02:38:46] about what's called the distillation
[02:38:48] risk that is that someone could come in
[02:38:50] and actually try to imitate those
[02:38:51] reasoning traces and recover a lot of
[02:38:53] the reasoning performance by just
[02:38:55] imitating the reasoning uh chains of
[02:38:57] thought and so they kind of hide them
[02:38:59] and they only show little summaries of
[02:39:00] them so you're not getting exactly what
[02:39:02] you would get in deep seek as with
[02:39:04] respect to the reasoning itself and then
[02:39:07] they write up the
[02:39:08] solution so these are kind of like
[02:39:10] equivalent even though we're not seeing
[02:39:12] the full under the hood details now in
[02:39:14] terms of the performance uh these models
[02:39:17] and deep seek models are currently rly
[02:39:19] on par I would say it's kind of hard to
[02:39:21] tell because of the evaluations but if
[02:39:22] you're paying $200 per month to open AI
[02:39:24] some of these models I believe are
[02:39:25] currently they basically still look
[02:39:27] better uh but deep seek R1 for now is
[02:39:30] still a very solid choice for a thinking
[02:39:33] model that would be available to you um
[02:39:36] sort of um either on this website or any
[02:39:39] other website because the model is open
[02:39:40] weights you can just download it so
[02:39:43] that's thinking models so what is the
[02:39:46] summary so far well we've talked about
[02:39:48] reinforcement learning and the fact that
[02:39:50] thinking emerges in the process of the
[02:39:52] optimization on when we basically run RL
[02:39:55] on many math uh and kind of code
[02:39:57] problems that have verifiable Solutions
[02:39:59] so there's like an answer three
[02:40:01] Etc now these thinking models you can
[02:40:04] access in for example deep seek or any
[02:40:07] inference provider like together. a and
[02:40:09] choosing deep seek over there these
[02:40:12] thinking models are also available uh in
[02:40:14] chpt under any of the 01 or O3
[02:40:17] models but these GPT 4 R models Etc
[02:40:20] they're not thinking models you should
[02:40:21] think of them as mostly sft models now
[02:40:25] if you are um if you have a prompt that
[02:40:27] requires Advanced reasoning and so on
[02:40:29] you should probably use some of the
[02:40:30] thinking models or at least try them out
[02:40:32] but empirically for a lot of my use when
[02:40:35] you're asking a simpler question there's
[02:40:36] like a knowledge based question or
[02:40:37] something like that this might be
[02:40:39] Overkill like there's no need to think
[02:40:40] 30 seconds about some factual question
[02:40:42] so for that I will uh sometimes default
[02:40:44] to just GPT 40 so empirically about 80
[02:40:47] 90% of my use is just gp4
[02:40:49] and when I come across a very difficult
[02:40:51] problem like in math and code Etc I will
[02:40:53] reach for the thinking models but then I
[02:40:56] have to wait a bit longer because
[02:40:57] they're thinking um so you can access
[02:41:00] these on chat on deep seek also I wanted
[02:41:02] to point out that um AI studio.
[02:41:05] go.com even though it looks really busy
[02:41:08] really ugly because Google's just unable
[02:41:10] to do this kind of stuff well it's like
[02:41:13] what is happening but if you choose
[02:41:15] model and you choose here Gemini 2.0
[02:41:17] flash thinking experimental 01 21 if you
[02:41:20] choose that one that's also a a kind of
[02:41:22] early experiment experimental of a
[02:41:25] thinking model by Google so we can go
[02:41:27] here and we can give it the same problem
[02:41:29] and click run and this is also a
[02:41:31] thinking problem a thinking model that
[02:41:33] will also do something
[02:41:35] similar and comes out with the right
[02:41:37] answer here so basically Gemini also
[02:41:40] offers a thinking model anthropic
[02:41:42] currently does not offer a thinking
[02:41:43] model but basically this is kind of like
[02:41:45] the frontier development of these llms I
[02:41:47] think RL is kind of like this new
[02:41:49] exciting stage but getting the details
[02:41:51] right is difficult and that's why all
[02:41:53] these models and thinking models are
[02:41:55] currently experimental as of 2025 very
[02:41:57] early 2025 um but this is kind of like
[02:42:01] the frontier development of pushing the
[02:42:02] performance on these very difficult
[02:42:03] problems using reasoning that is
[02:42:05] emerging in these optimizations one more
[02:42:07] connection that I wanted to bring up is
[02:42:10] that the discovery that reinforcement
[02:42:12] learning is extremely powerful way of
[02:42:14] learning is not new to the field of AI
[02:42:17] and one place what we've already seen
[02:42:19] this demonstrated is in the game of Go
[02:42:22] and famously Deep Mind developed the
[02:42:24] system alphago and you can watch a movie
[02:42:26] about it um where the system is learning
[02:42:29] to play the game of go against top human
[02:42:32] players and um when we go to the paper
[02:42:36] underlying alphago so in this paper when
[02:42:39] we scroll
[02:42:41] down we actually find a really
[02:42:43] interesting
[02:42:44] plot um that I think uh is kind of
[02:42:47] familiar uh to us and we're kind of like
[02:42:49] we discovering in the more open domain
[02:42:51] of arbitrary problem solving instead of
[02:42:53] on the closed specific domain of the
[02:42:55] game of Go but basically what they saw
[02:42:57] and we're going to see this in llms as
[02:42:59] well as this becomes more mature is this
[02:43:03] is the ELO rating of playing game of Go
[02:43:05] and this is leas dull an extremely
[02:43:07] strong human player and here what they
[02:43:09] are comparing is the strength of a model
[02:43:11] learned trained by supervised learning
[02:43:14] and a model trained by reinforcement
[02:43:15] learning so the supervised learning
[02:43:17] model is imitating human expert players
[02:43:20] so if you just get a huge amount of
[02:43:22] games played by expert players in the
[02:43:23] game of Go and you try to imitate them
[02:43:26] you are going to get better but then you
[02:43:28] top out and you never quite get better
[02:43:31] than some of the top top top players of
[02:43:34] in the game of Go like LEL so you're
[02:43:35] never going to reach there because
[02:43:37] you're just imitating human players you
[02:43:39] can't fundamentally go beyond a human
[02:43:40] player if you're just imitating human
[02:43:42] players but in a process of
[02:43:44] reinforcement learning is significantly
[02:43:46] more powerful in reinforcement learning
[02:43:48] for a game of Go it means that the
[02:43:50] system is playing moves that empirically
[02:43:53] and statistically lead to win to winning
[02:43:56] the game and so alphago is a system
[02:43:59] where it kind of plays against it itself
[02:44:02] and it's using reinforcement learning to
[02:44:03] create
[02:44:04] rollouts so it's the exact same diagram
[02:44:07] here but there's no prompt it's just uh
[02:44:10] because there's no prompt it's just a
[02:44:11] fixed game of Go but it's trying out
[02:44:13] lots of solutions it's trying out lots
[02:44:15] of plays and then the games that lead to
[02:44:18] a win instead of a specific answer are
[02:44:20] reinforced they're they're made stronger
[02:44:24] and so um the system is learning
[02:44:26] basically the sequences of actions that
[02:44:28] empirically and statistically lead to
[02:44:30] winning the game and reinforcement
[02:44:32] learning is not going to be constrained
[02:44:34] by human performance and reinforcement
[02:44:36] learning can do significantly better and
[02:44:38] overcome even the top players like Lisa
[02:44:41] Dole and so uh probably they could have
[02:44:44] run this longer and they just chose to
[02:44:46] crop it at some point because this costs
[02:44:47] money but this is very powerful
[02:44:49] demonstration of reinforcement learning
[02:44:51] and we're only starting to kind of see
[02:44:52] hints of this diagram in larger language
[02:44:55] models for reasoning problems so we're
[02:44:58] not going to get too far by just
[02:44:59] imitating experts we need to go beyond
[02:45:01] that set up these like little game
[02:45:03] environments and get let let the system
[02:45:07] discover reasoning traces or like ways
[02:45:09] of solving problems uh that are unique
[02:45:14] and that uh just basically work
[02:45:16] well now on this aspect of uniqueness
[02:45:19] notice that when you're doing
[02:45:19] reinforcement learning nothing prevents
[02:45:21] you from veering off the distribution of
[02:45:24] how humans are playing the game and so
[02:45:26] when we go back to uh this alphao search
[02:45:29] here one of the suggested modifications
[02:45:31] is called move 37 and move 37 in alphao
[02:45:34] is referring to a specific point in time
[02:45:37] where alphago basically played a move
[02:45:40] that uh no human expert would play uh so
[02:45:43] the probability of this move uh to be
[02:45:45] played by a human player was evaluated
[02:45:47] to be about 1 in 10th ,000 so it's a
[02:45:49] very rare move but in retrospect it was
[02:45:52] a brilliant move so alphago in the
[02:45:54] process of reinforcement learning
[02:45:55] discovered kind of like a strategy of
[02:45:57] playing that was unknown to humans and
[02:46:00] but is in retrospect uh brilliant I
[02:46:02] recommend this YouTube video um leis do
[02:46:04] versus alphao move 37 reactions and
[02:46:06] Analysis and this is kind of what it
[02:46:08] looked like when alphao played this
[02:46:11] move
[02:46:14] value that's a very that's a very
[02:46:16] surprising move I thought I thought it
[02:46:19] was I thought it was a
[02:46:21] mistake when I see this move anyway so
[02:46:24] basically people are kind of freaking
[02:46:25] out because it's a it's a move that a
[02:46:28] human would not play that alphago played
[02:46:31] because in its training uh this move
[02:46:33] seemed to be a good idea it just happens
[02:46:35] not to be a kind of thing that a humans
[02:46:37] would would do and so that is again the
[02:46:39] power of reinforcement learning and in
[02:46:41] principle we can actually see the
[02:46:42] equivalence of that if we continue
[02:46:44] scaling this Paradigm in language models
[02:46:46] and what that looks like is kind of
[02:46:47] unknown so so um what does it mean to
[02:46:50] solve problems in such a way that uh
[02:46:54] even humans would not be able to get how
[02:46:56] can you be better at reasoning or
[02:46:58] thinking than humans how can you go
[02:47:00] beyond just uh a thinking human like
[02:47:03] maybe it means discovering analogies
[02:47:05] that humans would not be able to uh
[02:47:07] create or maybe it's like a new thinking
[02:47:09] strategy it's kind of hard to think
[02:47:10] through uh maybe it's a holy new
[02:47:14] language that actually is not even
[02:47:16] English maybe it discovers its own
[02:47:17] language that is a lot better at
[02:47:19] thinking um because the model is
[02:47:22] unconstrained to even like stick with
[02:47:24] English uh so maybe it takes a different
[02:47:27] language to think in or it discovers its
[02:47:29] own language so in principle the
[02:47:31] behavior of the system is a lot less
[02:47:33] defined it is open to do whatever works
[02:47:37] and it is open to also slowly Drift from
[02:47:40] the distribution of its training data
[02:47:41] which is English but all of that can
[02:47:43] only be done if we have a very large
[02:47:45] diverse set of problems in which the
[02:47:48] these strategy can be refined and
[02:47:49] perfected and so that is a lot of the
[02:47:51] frontier LM research that's going on
[02:47:53] right now is trying to kind of create
[02:47:55] those kinds of prompt distributions that
[02:47:57] are large and diverse these are all kind
[02:47:59] of like game environments in which the
[02:48:00] llms can practice their thinking and uh
[02:48:04] it's kind of like writing you know these
[02:48:06] practice problems we have to create
[02:48:07] practice problems for all of domains of
[02:48:10] knowledge and if we have practice
[02:48:12] problems and tons of them the models
[02:48:14] will be able to reinforcement learning
[02:48:16] reinforcement learn on them and kind of
[02:48:18] uh create these kinds of uh diagrams but
[02:48:21] in the domain of open thinking instead
[02:48:23] of a closed domain like game of Go
[02:48:26] there's one more section within
[02:48:27] reinforcement learning that I wanted to
[02:48:29] cover and that is that of learning in
[02:48:32] unverifiable domains so so far all of
[02:48:35] the problems that we've looked at are in
[02:48:36] what's called verifiable domains that is
[02:48:38] any candidate solution we can score very
[02:48:41] easily against a concrete answer so for
[02:48:44] example answer is three and we can very
[02:48:45] easily score these Solutions against the
[02:48:47] answer of three
[02:48:49] either we require the models to like box
[02:48:51] in their answers and then we just check
[02:48:53] for equality of whatever is in the box
[02:48:55] with the answer or you can also use uh
[02:48:58] kind of what's called an llm judge so
[02:49:00] the llm judge looks at a solution and it
[02:49:03] gets the answer and just basically
[02:49:05] scores the solution for whether it's
[02:49:06] consistent with the answer or not and
[02:49:08] llms uh empirically are good enough at
[02:49:10] the current capability that they can do
[02:49:12] this fairly reliably so we can apply
[02:49:14] those kinds of techniques as well in any
[02:49:16] case we have a concrete answer and we're
[02:49:17] just checking Solutions again against it
[02:49:19] and we can do this automatically with no
[02:49:21] kind of humans in the loop the problem
[02:49:23] is that we can't apply the strategy in
[02:49:25] what's called unverifiable domains so
[02:49:28] usually these are for example creative
[02:49:29] writing tasks like write a joke about
[02:49:31] Pelicans or write a poem or summarize a
[02:49:33] paragraph or something like that in
[02:49:35] these kinds of domains it becomes harder
[02:49:37] to score our different solutions to this
[02:49:39] problem so for example writing a joke
[02:49:41] about Pelicans we can generate lots of
[02:49:43] different uh jokes of course that's fine
[02:49:45] for example we can go to chbt and we can
[02:49:47] get it to uh generate a joke about
[02:49:51] Pelicans uh so much stuff in their beaks
[02:49:53] because they don't bellan in
[02:49:56] backpacks what
[02:49:59] okay we can uh we can try something else
[02:50:02] why don't Pelicans ever pay for their
[02:50:04] drinks because they always B it to
[02:50:06] someone else haha okay so these models
[02:50:10] are not obviously not very good at humor
[02:50:12] actually I think it's pretty fascinating
[02:50:13] because I think humor is secretly very
[02:50:15] difficult and the model have the
[02:50:16] capability I think anyway in any case
[02:50:20] you could imagine creating lots of jokes
[02:50:23] the problem that we are facing is how do
[02:50:24] we score them now in principle we could
[02:50:27] of course get a human to look at all
[02:50:29] these jokes just like I did right now
[02:50:31] the problem with that is if you are
[02:50:32] doing reinforcement learning you're
[02:50:34] going to be doing many thousands of
[02:50:36] updates and for each update you want to
[02:50:38] be looking at say thousands of prompts
[02:50:40] and for each prompt you want to be
[02:50:41] potentially looking at looking at
[02:50:43] hundred or thousands of different kinds
[02:50:44] of generations and so there's just like
[02:50:47] way too many of these to look at and so
[02:50:50] um in principle you could have a human
[02:50:52] inspect all of them and score them and
[02:50:53] decide that okay maybe this one is funny
[02:50:55] and uh maybe this one is funny and this
[02:50:58] one is funny and we could train on them
[02:51:01] to get the model to become slightly
[02:51:02] better at jokes um in the context of
[02:51:05] pelicans at least um the problem is that
[02:51:09] it's just like way too much human time
[02:51:10] this is an unscalable strategy we need
[02:51:12] some kind of an automatic strategy for
[02:51:14] doing this and one sort of solution to
[02:51:16] this was proposed in this paper
[02:51:19] uh that introduced what's called
[02:51:20] reinforcement learning from Human
[02:51:21] feedback and so this was a paper from
[02:51:23] open at the time and many of these
[02:51:25] people are now um co-founders in
[02:51:27] anthropic um and this kind of proposed a
[02:51:30] approach for uh basically doing
[02:51:33] reinforcement learning in unverifiable
[02:51:35] domains so let's take a look at how that
[02:51:36] works so this is the cartoon diagram of
[02:51:39] the core ideas involved so as I
[02:51:41] mentioned the native approach is if we
[02:51:44] just set Infinity human time we could
[02:51:46] just run RL in these domains just fine
[02:51:49] so for example we can run RL as usual if
[02:51:51] I have Infinity humans I would I just
[02:51:53] want to do and these are just cartoon
[02:51:55] numbers I want to do 1,000 updates where
[02:51:57] each update will be on 1,000 prompts and
[02:52:00] in for each prompt we're going to have
[02:52:02] 1,000 roll outs that we're scoring so we
[02:52:05] can run RL with this kind of a setup the
[02:52:08] problem is in the process of doing this
[02:52:10] I will need to run one I will need to
[02:52:12] ask a human to evaluate a joke a total
[02:52:15] of 1 billion times and so that's a lot
[02:52:18] of people looking at really terrible
[02:52:19] jokes so we don't want to do that so
[02:52:22] instead we want to take the arlef
[02:52:24] approach so um in our Rel of approach we
[02:52:27] are kind of like the the core trick is
[02:52:29] that of indirection so we're going to
[02:52:32] involve humans just a little bit and the
[02:52:35] way we cheat is that we basically train
[02:52:37] a whole separate neural network that we
[02:52:39] call a reward model and this neural
[02:52:41] network will kind of like imitate human
[02:52:44] scores so we're going to ask humans to
[02:52:46] score um roll
[02:52:49] we're going to then imitate human scores
[02:52:51] using a neural network and this neural
[02:52:54] network will become a kind of simulator
[02:52:55] of human
[02:52:56] preferences and now that we have a
[02:52:58] neural network simulator we can do RL
[02:53:01] against it so instead of asking a real
[02:53:03] human we're asking a simulated human for
[02:53:06] their score of a joke as an example and
[02:53:09] so once we have a simulator we're often
[02:53:11] racist because we can query it as many
[02:53:13] times as we want to and it's all whole
[02:53:16] automatic process and we can now do
[02:53:17] reinforcement learning with respect to
[02:53:19] the simulator and the simulator as you
[02:53:20] might expect is not going to be a
[02:53:22] perfect human but if it's at least
[02:53:24] statistically similar to human judgment
[02:53:26] then you might expect that this will do
[02:53:28] something and in practice indeed uh it
[02:53:30] does so once we have a simulator we can
[02:53:32] do RL and everything works great so let
[02:53:35] me show you a cartoon diagram a little
[02:53:36] bit of what this process looks like
[02:53:38] although the details are not 100 like
[02:53:40] super important it's just a core idea of
[02:53:42] how this works so here I have a cartoon
[02:53:44] diagram of a hypothetical example of
[02:53:46] what training the reward model would
[02:53:47] look like so we have a prompt like write
[02:53:50] a joke about picans and then here we
[02:53:52] have five separate roll outs so these
[02:53:54] are all five different jokes just like
[02:53:56] this one now the first thing we're going
[02:53:59] to do is we are going to ask a human to
[02:54:02] uh order these jokes from the best to
[02:54:05] worst so this is uh so here this human
[02:54:08] thought that this joke is the best the
[02:54:10] funniest so number one joke this is
[02:54:14] number two joke number three joke four
[02:54:16] and five so this is the worst joke
[02:54:19] we're asking humans to order instead of
[02:54:20] give scores directly because it's a bit
[02:54:22] of an easier task it's easier for a
[02:54:24] human to give an ordering than to give
[02:54:26] precise scores now that is now the
[02:54:29] supervision for the model so the human
[02:54:31] has ordered them and that is kind of
[02:54:32] like their contribution to the training
[02:54:34] process but now separately what we're
[02:54:36] going to do is we're going to ask a
[02:54:37] reward model uh about its scoring of
[02:54:40] these jokes now the reward model is a
[02:54:42] whole separate neural network completely
[02:54:44] separate neural net um and it's also
[02:54:47] probably a transform
[02:54:49] uh but it's not a language model in the
[02:54:50] sense that it generates diverse language
[02:54:53] Etc it's just a scoring model so the
[02:54:56] reward model will take as an input The
[02:54:59] Prompt number one and number two a
[02:55:02] candidate joke so um those are the two
[02:55:05] inputs that go into the reward model so
[02:55:07] here for example the reward model would
[02:55:08] be taken this prompt and this joke now
[02:55:11] the output of a reward model is a single
[02:55:14] number and this number is thought of as
[02:55:16] a score and it can range for example
[02:55:18] from Z to one so zero would be the worst
[02:55:20] score and one would be the best score so
[02:55:23] here are some examples of what a
[02:55:25] hypothetical reward model at some stage
[02:55:27] in the training process would give uh s
[02:55:29] scoring to these jokes so 0.1 is a very
[02:55:33] low score 08 is a really high score and
[02:55:36] so on and so now um we compare the
[02:55:40] scores given by the reward model with uh
[02:55:43] the ordering given by the human and
[02:55:45] there's a precise mathematical way to
[02:55:47] actually calculate this uh basically set
[02:55:49] up a loss function and calculate a kind
[02:55:51] of like a correspondence here and uh
[02:55:54] update a model based on it but I just
[02:55:55] want to give you the intuition which is
[02:55:57] that as an example here for this second
[02:56:00] joke the the human thought that it was
[02:56:02] the funniest and the model kind of
[02:56:03] agreed right 08 is a relatively high
[02:56:05] score but this score should have been
[02:56:07] even higher right so after an update we
[02:56:10] would expect that maybe this score
[02:56:11] should have been will actually grow
[02:56:13] after an update of the network to be
[02:56:15] like say 081 or
[02:56:16] something um for this one here they
[02:56:19] actually are in a massive disagreement
[02:56:21] because the human thought that this was
[02:56:22] number two but here the the score is
[02:56:24] only 0.1 and so this score needs to be
[02:56:27] much higher so after an update on top of
[02:56:30] this um kind of a supervision this might
[02:56:33] grow a lot more like maybe it's 0.15 or
[02:56:35] something like
[02:56:36] that um and then here the human thought
[02:56:39] that this one was the worst joke but
[02:56:41] here the model actually gave it a fairly
[02:56:43] High number so you might expect that
[02:56:45] after the update uh this would come down
[02:56:47] to maybe 3 3.5 or something like that so
[02:56:50] basically we're doing what we did before
[02:56:51] we're slightly nudging the predictions
[02:56:54] from the models using a neural network
[02:56:57] training
[02:56:58] process and we're trying to make the
[02:57:00] reward model scores be consistent with
[02:57:03] human
[02:57:04] ordering and so um as we update the
[02:57:07] reward model on human data it becomes
[02:57:09] better and better simulator of the
[02:57:11] scores and orders uh that humans provide
[02:57:14] and then becomes kind of like the the
[02:57:17] neural the simulator of human
[02:57:18] preferences which we can then do RL
[02:57:20] against but critically we're not asking
[02:57:23] humans one billion times to look at a
[02:57:24] joke we're maybe looking at th000
[02:57:26] prompts and five roll outs each so maybe
[02:57:28] 5,000 jokes that humans have to look at
[02:57:30] in total and they just give the ordering
[02:57:33] and then we're training the model to be
[02:57:34] consistent with that ordering and I'm
[02:57:36] skipping over the mathematical details
[02:57:38] but I just want you to understand a high
[02:57:39] level idea that uh this reward model is
[02:57:42] do is basically giving us this scour and
[02:57:45] we have a way of training it to be
[02:57:46] consistent with human orderings
[02:57:48] and that's how rhf works okay so that is
[02:57:51] the rough idea we basically train
[02:57:53] simulators of humans and RL with respect
[02:57:55] to those
[02:57:56] simulators now I want to talk about
[02:57:59] first the upside of reinforcement
[02:58:00] learning from Human
[02:58:03] feedback the first thing is that this
[02:58:05] allows us to run reinforcement learning
[02:58:07] which we know is incredibly powerful
[02:58:09] kind of set of techniques and it allows
[02:58:10] us to do it in arbitrary domains and
[02:58:13] including the ones that are unverifiable
[02:58:15] so things like summarization and poem
[02:58:17] writing joke writing or any other
[02:58:19] creative writing really uh in domains
[02:58:21] outside of math and code
[02:58:23] Etc now empirically what we see when we
[02:58:25] actually apply rhf is that this is a way
[02:58:28] to improve the performance of the model
[02:58:30] and uh I have a top answer for why that
[02:58:33] might be but I don't actually know that
[02:58:35] it is like super well established on
[02:58:38] like why this is you can empirically
[02:58:39] observe that when you do rhf correctly
[02:58:41] the models you get are just like a
[02:58:43] little bit better um but as to why is I
[02:58:45] think like not as clear so here's my
[02:58:47] best guess my best guess is that this is
[02:58:49] possibly mostly due to the discriminator
[02:58:52] generator
[02:58:53] Gap what that means is that in many
[02:58:55] cases it is significantly easier to
[02:58:58] discriminate than to generate for humans
[02:59:01] so in particular an example of this is
[02:59:04] um in when we do supervised fine-tuning
[02:59:07] right
[02:59:09] sft we're asking humans to generate the
[02:59:12] ideal assistant response and in many
[02:59:15] cases here um as I've shown it uh the
[02:59:18] ideal response is very simple to write
[02:59:20] but in many cases might not be so for
[02:59:22] example in summarization or poem writing
[02:59:24] or joke writing like how are you as a
[02:59:26] human assist as a human labeler um
[02:59:29] supposed to give the ideal response in
[02:59:30] these cases it requires creative human
[02:59:32] writing to do that and so rhf kind of
[02:59:35] sidesteps this because we get um we get
[02:59:38] to ask people a significantly easier
[02:59:40] question as a data labelers they're not
[02:59:42] asked to write poems directly they're
[02:59:44] just given five poems from the model and
[02:59:46] they're just asked to order them and so
[02:59:49] that's just a much easier task for a
[02:59:51] human labeler to do and so what I think
[02:59:53] this allows you to do basically is it um
[02:59:57] it kind of like allows a lot more higher
[03:00:00] accuracy data because we're not asking
[03:00:02] people to do the generation task which
[03:00:04] can be extremely difficult like we're
[03:00:06] not asking them to do creative writing
[03:00:07] we're just trying to get them to
[03:00:09] distinguish between creative writings
[03:00:11] and uh find the ones that are best and
[03:00:14] that is the signal that humans are
[03:00:15] providing just the ordering and that is
[03:00:17] their input into the system and then the
[03:00:20] system in rhf just discovers the kinds
[03:00:23] of responses that would be graded well
[03:00:26] by humans and so that step of
[03:00:28] indirection allows the models to become
[03:00:30] a bit better so that is the upside of
[03:00:33] our LF it allows us to run RL it
[03:00:35] empirically results in better models and
[03:00:37] it allows uh people to contribute their
[03:00:40] supervision uh even without having to do
[03:00:42] extremely difficult tasks um in the case
[03:00:45] of writing ideal responses unfortunately
[03:00:47] our HF also comes with significant
[03:00:49] downsides and so um the main one is that
[03:00:54] basically we are doing reinforcement
[03:00:55] learning not with respect to humans and
[03:00:57] actual human judgment but with respect
[03:00:59] to a lossy simulation of humans right
[03:01:01] and this lossy simulation could be
[03:01:03] misleading because it's just a it's just
[03:01:05] a simulation right it's just a language
[03:01:07] model that's kind of outputting scores
[03:01:09] and it might not perfectly reflect the
[03:01:11] opinion of an actual human with an
[03:01:13] actual brain in all the possible
[03:01:15] different cases so that's number one
[03:01:17] which is actually something even more
[03:01:18] subtle and devious going on that uh
[03:01:21] really
[03:01:22] dramatically holds back our LF as a
[03:01:24] technique that we can really scale to
[03:01:27] significantly um kind of Smart Systems
[03:01:31] and that is that reinforcement learning
[03:01:32] is extremely good at discovering a way
[03:01:35] to game the model to game the simulation
[03:01:38] so this reward model that we're
[03:01:40] constructing here that gives the course
[03:01:43] these models are Transformers these
[03:01:46] Transformers are massive neurals they
[03:01:48] have billions of parameters and they
[03:01:50] imitate humans but they do so in a kind
[03:01:52] of like a simulation way now the problem
[03:01:54] is that these are massive complicated
[03:01:56] systems right there's a billion
[03:01:57] parameters here that are outputting a
[03:01:58] single
[03:02:00] score it turns out that there are ways
[03:02:02] to gain these models you can find kinds
[03:02:05] of inputs that were not part of their
[03:02:08] training set and these inputs
[03:02:11] inexplicably get very high scores but in
[03:02:13] a fake way so very often what you find
[03:02:17] if you run our lch for very long so for
[03:02:19] example if we do 1,000 updates which is
[03:02:21] like say a lot of updates you might
[03:02:23] expect that your jokes are getting
[03:02:25] better and that you're getting like real
[03:02:26] bangers about Pelicans but that's not
[03:02:28] EXA exactly what happens what happens is
[03:02:31] that uh in the first few hundred steps
[03:02:34] the jokes about Pelicans are probably
[03:02:35] improving a little bit and then they
[03:02:37] actually dramatically fall off the cliff
[03:02:38] and you start to get extremely
[03:02:40] nonsensical results like for example you
[03:02:42] start to get um the top joke about
[03:02:45] Pelicans starts to be the
[03:02:48] and this makes no sense right like when
[03:02:49] you look at it why should this be a top
[03:02:50] joke but when you take the the and you
[03:02:53] plug it into your reward model you'd
[03:02:55] expect score of zero but actually the
[03:02:57] reward model loves this as a joke it
[03:02:59] will tell you that the the the theth is
[03:03:02] a score of 1. Z this is a top joke and
[03:03:06] this makes no sense right but it's
[03:03:07] because these models are just
[03:03:09] simulations of humans and they're
[03:03:10] massive neural lots and you can find
[03:03:12] inputs at the bottom that kind of like
[03:03:15] get into the part of the input space
[03:03:16] that kind of gives you nonsensical
[03:03:17] results these examples are what's called
[03:03:20] adversarial examples and I'm not going
[03:03:22] to go into the topic too much but these
[03:03:24] are adversarial inputs to the model they
[03:03:26] are specific little inputs that kind of
[03:03:29] go between the nooks and crannies of the
[03:03:30] model and give nonsensical results at
[03:03:32] the top now here's what you might
[03:03:34] imagine doing you say okay the the the
[03:03:36] is obviously not score of one um it's
[03:03:39] obviously a low score so let's take the
[03:03:41] the the the the let's add it to the data
[03:03:43] set and give it an ordering that is
[03:03:45] extremely bad like a score of five and
[03:03:47] indeed your model will learn that the D
[03:03:50] should have a very low score and it will
[03:03:51] give it score of zero the problem is
[03:03:53] that there will always be basically
[03:03:55] infinite number of nonsensical
[03:03:57] adversarial examples hiding in the model
[03:04:00] if you iterate this process many times
[03:04:02] and you keep adding nonsensical stuff to
[03:04:04] your reward model and giving it very low
[03:04:05] scores you can you'll never win the game
[03:04:09] uh you can do this many many rounds and
[03:04:11] reinforcement learning if you run it
[03:04:12] long enough will always find a way to
[03:04:14] gain the model it will discover
[03:04:15] adversarial examples it will get get
[03:04:17] really high scores uh with nonsensical
[03:04:20] results and fundamentally this is
[03:04:23] because our scoring function is a giant
[03:04:26] neural nut and RL is extremely good at
[03:04:28] finding just the ways to trick it uh so
[03:04:33] long story short you always run rhf put
[03:04:36] for maybe a few hundred updates the
[03:04:38] model is getting better and then you
[03:04:39] have to crop it and you are done you
[03:04:42] can't run too much against this reward
[03:04:45] model because the optimization will
[03:04:47] start to game it and you basically crop
[03:04:50] it and you call it and you ship it um
[03:04:53] and uh you can improve the reward model
[03:04:56] but you kind of like come across these
[03:04:57] situations eventually at some point so
[03:05:00] rhf basically what I usually say is that
[03:05:03] RF is not RL and what I mean by that is
[03:05:06] I mean RF is RL obviously but it's not
[03:05:09] RL in the magical sense this is not RL
[03:05:12] that you can run
[03:05:13] indefinitely these kinds of problems
[03:05:16] like where you are getting con correct
[03:05:18] answer you cannot gain this as easily
[03:05:20] you either got the correct answer or you
[03:05:21] didn't and the scoring function is much
[03:05:23] much simpler you're just looking at the
[03:05:25] boxed area and seeing if the result is
[03:05:27] correct so it's very difficult to gain
[03:05:29] these functions but uh gaming a reward
[03:05:32] model is possible now in these
[03:05:34] verifiable domains you can run RL
[03:05:36] indefinitely you could run for tens of
[03:05:38] thousands hundreds of thousands of steps
[03:05:40] and discover all kinds of really crazy
[03:05:41] strategies that we might not even ever
[03:05:43] think about of Performing really well
[03:05:45] for all these problems in the game of Go
[03:05:48] there's no way to to beat to basically
[03:05:50] game uh the winning of a game or the
[03:05:52] losing of a game we have a perfect
[03:05:54] simulator we know all the different uh
[03:05:57] where all the stones are placed and we
[03:05:59] can calculate uh whether someone has won
[03:06:01] or not there's no way to gain that and
[03:06:03] so you can do RL indefinitely and you
[03:06:05] can eventually be beat even leol but
[03:06:08] with models like this which are gameable
[03:06:11] you cannot repeat this process
[03:06:13] indefinitely so I kind of see rhf as not
[03:06:16] real RL because the reward function is
[03:06:19] gameable so it's kind of more like in
[03:06:21] the realm of like little fine-tuning
[03:06:23] it's a little it's a little Improvement
[03:06:26] but it's not something that is
[03:06:27] fundamentally set up correctly where you
[03:06:29] can insert more compute run for longer
[03:06:32] and get much better and magical results
[03:06:34] so it's it's uh it's not RL in that
[03:06:36] sense it's not RL in the sense that it
[03:06:38] lacks magic um it can find you in your
[03:06:41] model and get a better performance and
[03:06:43] indeed if we go back to chat GPT the GPT
[03:06:46] 40 model has gone through rhf because it
[03:06:50] works well but it's just not RL in the
[03:06:52] same sense rlf is like a little fine
[03:06:54] tune that slightly improves your model
[03:06:56] is maybe like the way I would think
[03:06:57] about it okay so that's most of the
[03:06:59] technical content that I wanted to cover
[03:07:01] I took you through the three major
[03:07:03] stages and paradigms of training these
[03:07:05] models pre-training supervised fine
[03:07:07] tuning and reinforcement learning and I
[03:07:09] showed you that they Loosely correspond
[03:07:11] to the process we already use for
[03:07:12] teaching children and so in particular
[03:07:15] we talked about pre-training being sort
[03:07:17] of like the basic knowledge acquisition
[03:07:18] of reading Exposition supervised fine
[03:07:21] tuning being the process of looking at
[03:07:22] lots and lots of worked examples and
[03:07:24] imitating experts and practice problems
[03:07:28] the only difference is that we now have
[03:07:30] to effectively write textbooks for llms
[03:07:32] and AIS across all the disciplines of
[03:07:35] human knowledge and also in all the
[03:07:37] cases where we actually would like them
[03:07:39] to work like code and math and you know
[03:07:42] basically all the other disciplines so
[03:07:44] we're in the process of writing
[03:07:45] textbooks for them refining all the
[03:07:47] algorithms that I've presented on the
[03:07:48] high level and then of course doing a
[03:07:50] really really good job at the execution
[03:07:52] of training these models at scale and
[03:07:54] efficiently so in particular I didn't go
[03:07:56] into too many details but these are
[03:07:58] extremely large and complicated
[03:08:00] distributed uh sort of
[03:08:04] um jobs that have to run over tens of
[03:08:07] thousands or even hundreds of thousands
[03:08:08] of gpus and the engineering that goes
[03:08:10] into this is really at the stateof the
[03:08:12] art of what's possible with computers at
[03:08:14] that scale so I didn't cover that aspect
[03:08:17] too much
[03:08:19] but um this is very kind of serious and
[03:08:22] they were underlying all these very
[03:08:24] simple algorithms
[03:08:25] ultimately now I also talked about sort
[03:08:28] of like the theory of mind a little bit
[03:08:30] of these models and the thing I want you
[03:08:31] to take away is that these models are
[03:08:33] really good but they're extremely useful
[03:08:35] as tools for your work you shouldn't uh
[03:08:38] sort of trust them fully and I showed
[03:08:39] you some examples of that even though we
[03:08:41] have mitigations for hallucinations the
[03:08:43] models are not perfect and they will
[03:08:44] hallucinate still it's gotten better
[03:08:46] over time and it will continue to get
[03:08:48] better but they can
[03:08:49] hallucinate in other words in in
[03:08:52] addition to that I covered kind of like
[03:08:53] what I call the Swiss cheese uh sort of
[03:08:56] model of llm capabilities that you
[03:08:57] should have in your mind the models are
[03:08:59] incredibly good across so many different
[03:09:00] disciplines but then fail randomly
[03:09:02] almost in some unique cases so for
[03:09:05] example what is bigger 9.11 or 9.9 like
[03:09:07] the model doesn't know but
[03:09:09] simultaneously it can turn around and
[03:09:11] solve Olympiad questions and so this is
[03:09:14] a hole in the Swiss cheese and there are
[03:09:16] many of them and you don't want to trip
[03:09:17] over them so don't um treat these models
[03:09:21] as infallible models check their work
[03:09:23] use them as tools use them for
[03:09:25] inspiration use them for the first draft
[03:09:28] but uh work with them as tools and be
[03:09:30] ultimately respons responsible for the
[03:09:32] you know product of your
[03:09:35] work and that's roughly what I wanted to
[03:09:38] talk about this is how they're trained
[03:09:40] and this is what they are let's now turn
[03:09:43] to what are some of the future
[03:09:44] capabilities of these models uh probably
[03:09:46] what's coming down the pipe and also
[03:09:48] where can you find these models I have a
[03:09:50] few blow points on some of the things
[03:09:51] that you can expect coming down the pipe
[03:09:53] the first thing you'll notice is that
[03:09:55] the models will very rapidly become
[03:09:56] multimodal everything I talked about
[03:09:58] above concerned text but very soon we'll
[03:10:01] have llms that can not just handle text
[03:10:03] but they can also operate natively and
[03:10:05] very easily over audio so they can hear
[03:10:08] and speak and also images so they can
[03:10:10] see and paint and we're already seeing
[03:10:13] the beginnings of all of this uh but
[03:10:15] this will be all done natively inside
[03:10:17] inside the language model and this will
[03:10:19] enable kind of like natural
[03:10:20] conversations and roughly speaking the
[03:10:22] reason that this is actually no
[03:10:23] different from everything we've covered
[03:10:24] above is that as a baseline you can
[03:10:28] tokenize audio and images and apply the
[03:10:31] exact same approaches of everything that
[03:10:32] we've talked about above so it's not a
[03:10:34] fundamental change it's just uh it's
[03:10:36] just a to we have to add some tokens so
[03:10:38] as an example for tokenizing audio we
[03:10:41] can look at slices of the spectrogram of
[03:10:43] the audio signal and we can tokenize
[03:10:45] that and just add more tokens that
[03:10:47] suddenly represent audio and just add
[03:10:50] them into the context windows and train
[03:10:51] on them just like above the same for
[03:10:53] images we can use patches and we can
[03:10:56] separately tokenize patches and then
[03:10:58] what is an image an image is just a
[03:11:00] sequence of tokens and this actually
[03:11:03] kind of works and there's a lot of early
[03:11:04] work in this direction and so we can
[03:11:06] just create streams of tokens that are
[03:11:08] representing audio images as well as
[03:11:10] text and interpers them and handle them
[03:11:12] all simultaneously in a single model so
[03:11:14] that's one example of multimodality
[03:11:17] uh second something that people are very
[03:11:18] interested in
[03:11:20] is currently most of the work is that
[03:11:22] we're handing individual tasks to the
[03:11:24] models on kind of like a silver platter
[03:11:26] like please solve this task for me and
[03:11:28] the model sort of like does this little
[03:11:29] task but it's up to us to still sort of
[03:11:32] like organize a coherent execution of
[03:11:35] tasks to perform jobs and the models are
[03:11:38] not yet at the capability required to do
[03:11:41] this in a coherent error correcting way
[03:11:43] over long periods of time so they're not
[03:11:46] able to fully string together tasks to
[03:11:48] perform these longer running jobs but
[03:11:51] they're getting there and this is
[03:11:52] improving uh over time but uh probably
[03:11:55] what's going to happen here is we're
[03:11:56] going to start to see what's called
[03:11:57] agents which perform tasks over time and
[03:12:00] you you supervise them and you watch
[03:12:02] their work and they come up to once in a
[03:12:04] while report progress and so on so we're
[03:12:07] going to see more long running agents uh
[03:12:09] tasks that don't just take you know a
[03:12:11] few seconds of response but many tens of
[03:12:13] seconds or even minutes or hours over
[03:12:15] time uh but these uh models are not
[03:12:17] infallible as we talked about above so
[03:12:19] all of this will require supervision so
[03:12:21] for example in factories people talk
[03:12:23] about the human to robot ratio uh for
[03:12:26] automation I think we're going to see
[03:12:27] something similar in the digital space
[03:12:29] where we are going to be talking about
[03:12:31] human to agent ratios where humans
[03:12:33] becomes a lot more supervisors of agent
[03:12:35] tasks um in the digital
[03:12:38] domain uh next um I think everything is
[03:12:41] going to become a lot more pervasive and
[03:12:42] invisible so it's kind of like
[03:12:44] integrated into the tools and everywhere
[03:12:48] um and in addition kind of like computer
[03:12:51] using so right now these models aren't
[03:12:53] able to take actions on your behalf but
[03:12:56] I think this is a separate bullet point
[03:12:58] um if you saw chpt launch the operator
[03:13:02] then uh that's one early example of that
[03:13:04] where you can actually hand off control
[03:13:05] to the model to perform you know
[03:13:07] keyboard and mouse actions on your
[03:13:09] behalf so that's also something that
[03:13:11] that I think is very interesting the
[03:13:13] last point I have here is just a general
[03:13:14] comment that there's still a lot of
[03:13:15] research to potentially do in this
[03:13:16] domain main one example of that uh is
[03:13:19] something along the lines of test time
[03:13:20] training so remember that everything
[03:13:22] we've done above and that we talked
[03:13:24] about has two major stages there's first
[03:13:27] the training stage where we tune the
[03:13:28] parameters of the model to perform the
[03:13:30] tasks well once we get the parameters we
[03:13:33] fix them and then we deploy the model
[03:13:34] for inference from there the model is
[03:13:37] fixed it doesn't change anymore it
[03:13:39] doesn't learn from all the stuff that
[03:13:41] it's doing a test time it's a fixed um
[03:13:43] number of parameters and the only thing
[03:13:45] that is changing is now the token inside
[03:13:47] the context windows and so the only type
[03:13:49] of learning or test time learning that
[03:13:51] the model has access to is the in
[03:13:53] context learning of its uh kind of like
[03:13:56] uh dynamically adjustable context window
[03:13:59] depending on like what it's doing at
[03:14:00] test time so but I think this is still
[03:14:03] different from humans who actually are
[03:14:04] able to like actually learn uh depending
[03:14:06] on what they're doing especially when
[03:14:08] you sleep for example like your brain is
[03:14:09] updating your parameters or something
[03:14:10] like that right so there's no kind of
[03:14:13] equivalent of that currently in these
[03:14:14] models and tools so there's a lot of
[03:14:16] like um more wonky ideas I think that
[03:14:18] are to be explored still and uh in
[03:14:20] particular I think this will be
[03:14:21] necessary because the context window is
[03:14:24] a finite and precious resource and
[03:14:26] especially once we start to tackle very
[03:14:27] long running multimodal tasks and we're
[03:14:30] putting in videos and these token
[03:14:31] windows will basically start to grow
[03:14:34] extremely large like not thousands or
[03:14:36] even hundreds of thousands but
[03:14:37] significantly beyond that and the only
[03:14:39] trick uh the only kind of trick we have
[03:14:41] Avail to us right now is to make the
[03:14:43] context Windows longer but I think that
[03:14:46] that approach by itself will will not
[03:14:47] will not scale to actual long running
[03:14:49] tasks that are multimodal over time and
[03:14:51] so I think new ideas are needed in some
[03:14:53] of those disciplines um in some of those
[03:14:56] kind of cases in the main where these
[03:14:58] tasks are going to require very long
[03:15:00] contexts so those are some examples of
[03:15:03] some of the things you can um expect
[03:15:05] coming down the pipe let's now turn to
[03:15:07] where you can actually uh kind of keep
[03:15:09] track of this progress and um you know
[03:15:12] be up to date with the latest and grest
[03:15:13] of what's happening in the field so I
[03:15:15] would say the three resources that I
[03:15:16] have consistently used to stay up to
[03:15:18] date are number one El Marina uh so let
[03:15:21] me show you El
[03:15:23] Marina this is basically an llm leader
[03:15:26] board and it ranks all the top models
[03:15:30] and the ranking is based on human
[03:15:32] comparisons so humans prompt these
[03:15:34] models and they get to judge which one
[03:15:35] gives a better answer they don't know
[03:15:37] which model is which they're just
[03:15:39] looking at which model is the better
[03:15:40] answer and you can calculate a ranking
[03:15:42] and then you get some results and so
[03:15:44] what you can hear is what you can see
[03:15:46] here is the different organizations like
[03:15:48] Google Gemini for example that produce
[03:15:49] these models when you click on any one
[03:15:51] of these it takes you to the place where
[03:15:53] that model is
[03:15:55] hosted and then here we see Google is
[03:15:57] currently on top with open AI right
[03:15:59] behind here we see deep seek in position
[03:16:02] number three now the reason this is a
[03:16:04] big deal is the last column here you see
[03:16:05] license deep seek is an MIT license
[03:16:08] model it's open weights anyone can use
[03:16:10] these weights uh anyone can download
[03:16:12] them anyone can host their own version
[03:16:14] of Deep seek and they can use it in what
[03:16:16] whatever way they like and so it's not a
[03:16:18] proprietary model that you don't have
[03:16:19] access to it's it's basically an open
[03:16:21] weight release and so this is kind of
[03:16:24] unprecedented that a model this strong
[03:16:27] was released with open weights so pretty
[03:16:29] cool from the team next up we have a few
[03:16:32] more models from Google and open Ai and
[03:16:34] then when you continue to scroll down
[03:16:35] you start to see some other Usual
[03:16:36] Suspects so xai here anthropic with son
[03:16:40] it uh here at number
[03:16:43] 14 and
[03:16:45] um then
[03:16:47] meta with llama over here so llama
[03:16:51] similar to deep seek is an open weights
[03:16:52] model and so uh but it's down here as
[03:16:55] opposed to up here now I will say that
[03:16:57] this leaderboard was really good for a
[03:17:00] long time I do think that in the last
[03:17:03] few months it's become a little bit
[03:17:05] gamed um and I don't trust it as much as
[03:17:08] I used to I think um just empirically I
[03:17:11] feel like a lot of people for example
[03:17:13] are using a Sonet from anthropic and
[03:17:15] that it's a really good model so but
[03:17:17] that's all the way down here um in
[03:17:19] number 14 and conversely I think not as
[03:17:22] many people are using Gemini but it's
[03:17:23] racking really really high uh so I think
[03:17:27] use this as a first pass uh but uh sort
[03:17:30] of try out a few of the models for your
[03:17:32] tasks and see which one performs better
[03:17:35] the second thing that I would point to
[03:17:37] is the uh AI news uh newsletter so AI
[03:17:41] news is not very creatively named but it
[03:17:43] is a very good newsletter produced by
[03:17:44] swix and friends so thank you for
[03:17:46] maintaining it
[03:17:47] and it's been very helpful to me because
[03:17:48] it is extremely comprehensive so if you
[03:17:50] go to archives uh you see that it's
[03:17:52] produced almost every other day and um
[03:17:56] it is very comprehensive and some of it
[03:17:58] is written by humans and curated by
[03:17:59] humans but a lot of it is constructed
[03:18:01] automatically with llms so you'll see
[03:18:03] that these are very comprehensive and
[03:18:04] you're probably not missing anything
[03:18:06] major if you go through it of course
[03:18:08] you're probably not going to go through
[03:18:09] it because it's so long but I do think
[03:18:12] that these summaries all the way up top
[03:18:14] are quite good and I think have some
[03:18:15] human oversight uh so this has been very
[03:18:18] helpful to me and the last thing I would
[03:18:20] point to is just X and Twitter uh a lot
[03:18:22] of um AI happens on X and so I would
[03:18:25] just follow people who you like and
[03:18:27] trust and get all your latest and
[03:18:29] greatest uh on X as well so those are
[03:18:32] the major places that have worked for me
[03:18:33] over time and finally a few words on
[03:18:35] where you can find the models and where
[03:18:37] can you use them so the first one I
[03:18:39] would say is for any of the biggest
[03:18:41] proprietary models you just have to go
[03:18:42] to the website of that LM provider so
[03:18:44] for example for open a that's uh chat
[03:18:47] I believe actually works now uh so
[03:18:49] that's for open
[03:18:50] AI now for or you know for um for Gemini
[03:18:54] I think it's gem. google.com or AI
[03:18:57] Studio I think they have two for some
[03:18:59] reason that I don't fly understand no
[03:19:01] one does um for the open weights models
[03:19:04] like deep SE CL Etc you have to go to
[03:19:06] some kind of an inference provider of
[03:19:08] LMS so my favorite one is together
[03:19:10] together. a and I showed you that when
[03:19:11] you go to the playground of together. a
[03:19:14] then you can sort of pick lots of
[03:19:15] different models and all of these are
[03:19:17] open models of different types and you
[03:19:19] can talk to them here as an
[03:19:21] example um now if you'd like to use a
[03:19:24] base model like um you know a base model
[03:19:28] then this is where I think it's not as
[03:19:29] common to find base models even on these
[03:19:31] inference providers they are all
[03:19:32] targeting assistants and chat and so I
[03:19:35] think even here I can't I couldn't see
[03:19:37] base models here so for base models I
[03:19:39] usually go to hyperbolic because they
[03:19:41] serve my llama 3.1 base and I love that
[03:19:45] model and you can just talk to it here
[03:19:47] so as far as I know this is this is a
[03:19:49] good place for a base model and I wish
[03:19:51] more people hosted base models because
[03:19:53] they are useful and interesting to work
[03:19:54] with in some cases finally you can also
[03:19:57] take some of the models that are smaller
[03:19:59] and you can run them locally and so for
[03:20:02] example deep seek the biggest model
[03:20:04] you're not going to be able to run
[03:20:05] locally on your MacBook but there are
[03:20:07] smaller versions of the deep seek model
[03:20:09] that are what's called distilled and
[03:20:11] then also you can run these models at
[03:20:12] smaller Precision so not at the native
[03:20:14] Precision of for example fp8 on deep
[03:20:17] seek or you know bf16 llama but much
[03:20:20] much lower than that um and don't worry
[03:20:23] if you don't fully understand those
[03:20:24] details but you can run smaller versions
[03:20:26] that have been distilled and then at
[03:20:28] even lower precision and then you can
[03:20:29] fit them on your uh computer and so you
[03:20:33] can actually run pretty okay models on
[03:20:35] your laptop and my favorite I think
[03:20:37] place I go to usually is LM studio uh
[03:20:39] which is basically an app you can get
[03:20:42] and I think it kind of actually looks
[03:20:43] really ugly and it's I don't like that
[03:20:45] it shows you all these models that are
[03:20:46] basically not that useful like everyone
[03:20:48] just wants to run deep seek so I don't
[03:20:49] know why they give you these 500
[03:20:51] different types of models they're really
[03:20:53] complicated to search for and you have
[03:20:54] to choose different distillations and
[03:20:56] different uh precisions and it's all
[03:20:58] really confusing but once you actually
[03:21:00] understand how it works and that's a
[03:21:01] whole separate video then you can
[03:21:02] actually load up a model like here I
[03:21:04] loaded up a llama 3 uh2 instruct 1
[03:21:08] billion and um you can just talk to it
[03:21:11] so I ask for Pelican jokes and I can ask
[03:21:14] for another one and it gives me another
[03:21:15] one Etc all of this that happens here is
[03:21:18] locally on your computer so we're not
[03:21:20] actually going to anywhere anyone else
[03:21:22] this is running on the GPU on the
[03:21:24] MacBook Pro so that's very nice and you
[03:21:26] can then eject the model when you're
[03:21:28] done and that frees up the ram so LM
[03:21:31] studio is probably like my favorite one
[03:21:33] even though I don't I think it's got a
[03:21:34] lot of uiux issues and it's really
[03:21:36] geared towards uh professionals almost
[03:21:39] uh but if you watch some videos on
[03:21:40] YouTube I think you can figure out how
[03:21:41] to how to use this
[03:21:43] interface uh so those are a few words on
[03:21:45] where to find them so let me now loop
[03:21:47] back around to where we started the
[03:21:49] question was when we go to chashi
[03:21:50] pta.com and we enter some kind of a
[03:21:53] query and we hit go what exactly is
[03:21:57] happening here what are we seeing what
[03:21:59] are we talking to how does this work and
[03:22:03] I hope that this video gave you some
[03:22:04] appreciation for some of the under the
[03:22:06] hood details of how these models are
[03:22:08] trained and what this is that is coming
[03:22:10] back so in particular we now know that
[03:22:12] your query is taken and is first chopped
[03:22:15] up into tokens so we go to to tick
[03:22:18] tokenizer and here where is the place in
[03:22:21] the in the um sort of format that is for
[03:22:24] the user query we basically put in our
[03:22:27] query right there so our query goes into
[03:22:31] what we discussed here is the
[03:22:32] conversation protocol format which is
[03:22:34] this way that we maintain conversation
[03:22:36] objects so this gets inserted there and
[03:22:39] then this whole thing ends up being just
[03:22:40] a token sequence a onedimensional token
[03:22:43] sequence under the hood so Chachi PT saw
[03:22:46] this token sequence and then when we hit
[03:22:48] go it basically continues appending
[03:22:50] tokens into this list it continues the
[03:22:53] sequence it acts like a token
[03:22:55] autocomplete so in particular it gave us
[03:22:57] this response so we can basically just
[03:23:00] put it here and we see the tokens that
[03:23:02] it continued uh these are the tokens
[03:23:04] that it continued with
[03:23:06] roughly now the question
[03:23:08] becomes okay why are these the tokens
[03:23:10] that the model responded with what are
[03:23:12] these tokens where are they coming from
[03:23:14] uh what are we talking to and how do we
[03:23:17] program this system and so that's where
[03:23:19] we shifted gears and we talked about the
[03:23:21] under thehood pieces of it so the first
[03:23:24] stage of this process and there are
[03:23:25] three stages is the pre-training stage
[03:23:27] which fundamentally has to do with just
[03:23:28] knowledge acquisition from the internet
[03:23:30] into the parameters of this neural
[03:23:32] network and so the neural net
[03:23:35] internalizes a lot of Knowledge from the
[03:23:37] internet but where the personality
[03:23:39] really comes in is in the process of
[03:23:41] supervised fine-tuning here and so what
[03:23:44] what happens here is that basically the
[03:23:46] a company like openai will curate a
[03:23:49] large data set of conversations like say
[03:23:51] 1 million conversation across very
[03:23:53] diverse topics and there will be
[03:23:55] conversations between a human and an
[03:23:57] assistant and even though there's a lot
[03:23:59] of synthetic data generation used
[03:24:01] throughout this entire process and a lot
[03:24:02] of llm help and so on fundamentally this
[03:24:05] is a human data curation task with lots
[03:24:08] of humans involved and in particular
[03:24:10] these humans are data labelers hired by
[03:24:12] open AI who are given labeling
[03:24:14] instructions that they learn and they
[03:24:16] task is to create ideal assistant
[03:24:18] responses for any arbitrary prompts so
[03:24:21] they are teaching the neural network by
[03:24:24] example how to respond to
[03:24:27] prompts so what is the way to think
[03:24:29] about what came back here like what is
[03:24:32] this well I think the right way to think
[03:24:34] about it is that this is the neural
[03:24:37] network simulation of a data labeler at
[03:24:40] openai so it's as if I gave this query
[03:24:44] to a data Li open and this data labeler
[03:24:47] first reads all of the labeling
[03:24:48] instructions from open Ai and then
[03:24:51] spends 2 hours writing up the ideal
[03:24:53] assistant response to this query and uh
[03:24:57] giving it to me now we're not actually
[03:24:59] doing that right because we didn't wait
[03:25:01] two hours so what we're getting here is
[03:25:02] a neural network simulation of that
[03:25:05] process and we have to keep in mind that
[03:25:08] these neural networks don't function
[03:25:10] like human brains do they are different
[03:25:12] what's easy or hard for them is
[03:25:13] different from what's easy or hard for
[03:25:15] humans and so we really are just getting
[03:25:17] a simulation so here I shown you this is
[03:25:20] a token stream and this is fundamentally
[03:25:23] the neural network with a bunch of
[03:25:24] activations and neurons in between this
[03:25:26] is a fixed mathematical expression that
[03:25:28] mixes inputs from tokens with parameters
[03:25:32] of the model and they get mixed up and
[03:25:35] get you the next token in a sequence but
[03:25:37] this is a finite amount of compute that
[03:25:39] happens for every single token and so
[03:25:41] this is some kind of a lossy simulation
[03:25:44] of a human that is kind of like
[03:25:46] restricted in this way and so whatever
[03:25:49] the humans
[03:25:50] write the language model is kind of
[03:25:52] imitating on this token level with only
[03:25:55] this this specific computation for every
[03:25:58] single token and
[03:26:00] sequence we also saw that as a result of
[03:26:03] this and the cognitive differences the
[03:26:05] models will suffer in a variety of ways
[03:26:08] and uh you have to be very careful with
[03:26:10] their use so for example we saw that
[03:26:11] they will suffer from hallucinations and
[03:26:14] they also we have the sense of a Swiss
[03:26:16] model of the LM capabilities where
[03:26:18] basically there's like holes in the
[03:26:20] cheese sometimes the models will just
[03:26:22] arbitrarily like do something dumb uh so
[03:26:25] even though they're doing lots of
[03:26:26] magical stuff sometimes they just can't
[03:26:28] so maybe you're not giving them enough
[03:26:30] tokens to think and maybe they're going
[03:26:32] to just make stuff up because they're
[03:26:33] mental arithmetic breaks uh maybe they
[03:26:35] are suddenly unable to count number of
[03:26:38] letters um or maybe they're unable to
[03:26:40] tell you that 911 9.11 is smaller than
[03:26:43] 9.9 and it looks kind of dumb and so so
[03:26:46] it's a Swiss cheese capability and we
[03:26:48] have to be careful with that and we saw
[03:26:49] the reasons for
[03:26:50] that but fundamentally this is how we
[03:26:53] think of what came back it's again a
[03:26:56] simulation of this neural network of a
[03:27:00] human data labeler following the
[03:27:03] labeling instructions at open a so
[03:27:06] that's what we're getting back now I do
[03:27:09] think that the uh things change a little
[03:27:11] bit when you actually go and reach for
[03:27:13] one of the thinking models like o03 mini
[03:27:17] and the reason for that is that GPT
[03:27:20] 40 basically doesn't do reinforcement
[03:27:23] learning it does do rhf but I've told
[03:27:26] you that rhf is not RL there's no
[03:27:29] there's no uh time for magic in there
[03:27:31] it's just a little bit of a fine-tuning
[03:27:33] is the way to look at it but these
[03:27:35] thinking models they do use RL so they
[03:27:38] go through this third state stage of
[03:27:41] perfecting their thinking process and
[03:27:44] discovering new thinking strategies and
[03:27:46] uh
[03:27:46] solutions to problem solving that look a
[03:27:49] little bit like your internal monologue
[03:27:51] in your head and they practice that on a
[03:27:53] large collection of practice problems
[03:27:55] that companies like openi create and
[03:27:57] curate and um then make available to the
[03:28:00] LMS so when I come here and I talked to
[03:28:02] a thinking model and I put in this
[03:28:05] question what we're seeing here is not
[03:28:07] anymore just the straightforward
[03:28:09] simulation of a human data labeler like
[03:28:11] this is actually kind of new unique and
[03:28:14] interesting um and of course open is not
[03:28:16] showing us the under thehood thinking
[03:28:18] and the chains of thought that are
[03:28:20] underlying the reasoning here but we
[03:28:23] know that such a thing exists and this
[03:28:24] is a summary of it and what we're
[03:28:26] getting here is actually not just an
[03:28:27] imitation of a human data labeler it's
[03:28:29] actually something that is kind of new
[03:28:30] and interesting and exciting in the
[03:28:32] sense that it is a function of thinking
[03:28:35] that was emergent in a simulation it's
[03:28:37] not just imitating human data labeler it
[03:28:39] comes from this reinforcement learning
[03:28:41] process and so here we're of course not
[03:28:43] giving it a chance to shine because this
[03:28:45] is not a mathematical or a reasoning
[03:28:46] problem this is just some kind of a sort
[03:28:48] of creative writing problem roughly
[03:28:50] speaking and I think it's um it's a a
[03:28:54] question an open question as to whether
[03:28:57] the thinking strategies that are
[03:28:59] developed inside verifiable domains
[03:29:02] transfer and are generalizable to other
[03:29:05] domains that are unverifiable such as
[03:29:07] create writing the extent to which that
[03:29:09] transfer happens is unknown in the field
[03:29:12] I would say so we're not sure if we are
[03:29:14] able to do RL on everything that is very
[03:29:16] verifiable and see the benefits of that
[03:29:18] on things that are unverifiable like
[03:29:20] this prompt so that's an open question
[03:29:22] the other thing that's interesting is
[03:29:23] that this reinforcement learning here is
[03:29:26] still like way too new primordial and
[03:29:29] nent so we're just seeing like the
[03:29:31] beginnings of the hints of greatness uh
[03:29:34] in the reasoning problems we're seeing
[03:29:36] something that is in principle capable
[03:29:38] of something like the equivalent of move
[03:29:40] 37 but not in the game of Go but in open
[03:29:44] domain thinking and problem solving in
[03:29:46] principle this Paradigm is capable of
[03:29:48] doing something really cool new and
[03:29:50] exciting something even that no human
[03:29:52] has thought of before in principle these
[03:29:54] models are capable of analogies no human
[03:29:56] has had so I think it's incredibly
[03:29:58] exciting that these models exist but
[03:30:00] again it's very early and these are
[03:30:02] primordial models for now um and they
[03:30:05] will mostly shine in domains that are
[03:30:06] verifiable like math en code Etc so very
[03:30:10] interesting to play with and think about
[03:30:11] and
[03:30:12] use and then that's roughly it um um I
[03:30:16] would say those are the broad Strokes of
[03:30:18] what's available right now I will say
[03:30:20] that overall it is an extremely exciting
[03:30:23] time to be in the
[03:30:24] field personally I use these models all
[03:30:26] the time daily uh tens or hundreds of
[03:30:28] times because they dramatically
[03:30:30] accelerate my work I think a lot of
[03:30:31] people see the same thing I think we're
[03:30:33] going to see a huge amount of wealth
[03:30:34] creation as a result of these models be
[03:30:37] aware of some of their shortcomings even
[03:30:40] with RL models they're going to suffer
[03:30:42] from some of these use it as a tool in a
[03:30:44] toolbox don't trust it fully because
[03:30:47] they will randomly do dumb things they
[03:30:49] will randomly hallucinate they will
[03:30:51] randomly skip over some mental
[03:30:52] arithmetic and not get it right um they
[03:30:55] randomly can't count or something like
[03:30:56] that so use them as tools in the toolbox
[03:30:58] check their work and own the product of
[03:31:00] your work but use them for inspiration
[03:31:03] for first draft uh ask them questions
[03:31:06] but always check and verify and you will
[03:31:08] be very successful in your work if you
[03:31:10] do so uh so I hope this video was useful
[03:31:13] and interesting to you I hope you had it
[03:31:15] fun and uh it's already like very long
[03:31:17] so I apologize for that but I hope it
[03:31:19] was useful and yeah I will see you later