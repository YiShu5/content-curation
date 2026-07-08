---
source_url: "https://www.youtube.com/watch?v=1pZQkhexEJg"
platform: youtube
uploader: "AI Anytime"
title: "AI Agents Memory Design & Optimization Techniques"
upload_date: "20250807"
duration: 1547
fetched_at: "2026-06-26T09:44:56.796370Z"
transcript_source: youtube-transcript-api
---

[00:00:03] Hey, how it's going guys? In this video,
[00:00:05] we are going to look at memory
[00:00:07] management for agentic AI system. One of
[00:00:11] the most important component of building
[00:00:14] AI agents or agentic AI, you know, uh in
[00:00:17] enterprise or even in production, even
[00:00:20] at startups or if you are doing
[00:00:21] individually, right, we're building, you
[00:00:23] know, AI agents, multiple agentic AI
[00:00:26] systems, so on and so forth. The most
[00:00:27] important thing is memory management.
[00:00:29] Memory is the most complex topic also
[00:00:32] within the agent ecosystem. It's not
[00:00:33] that easy to implement and there are
[00:00:35] different types of optimization
[00:00:37] strategies that can be used to improve
[00:00:40] the performance of AI agent system.
[00:00:43] That's what we're going to look at in
[00:00:44] this video. Look at the memory and how
[00:00:46] you can design you know the the memory
[00:00:48] management part of it and how to
[00:00:50] optimize those memory when you are
[00:00:52] building uh AI agents or agent AI is
[00:00:55] been used interchangeably. Aentki has
[00:00:58] more autonomy, one of the
[00:00:59] characteristics, but quite similar. So
[00:01:01] if you look at here on my screen, I have
[00:01:03] this uh and we're going to make it open
[00:01:05] source. By the way, this will be
[00:01:06] available to you. So you can use this
[00:01:08] entire playground, all the code and
[00:01:10] everything. So if you look at here, it
[00:01:12] says AI agent memory design and
[00:01:15] optimization playground interactive
[00:01:17] testing environment for multiple memory
[00:01:19] optimization techniques. Uh if you look
[00:01:22] at here, it says available memory
[00:01:25] strategies. You know, it starts from
[00:01:27] sequential memory, goes up to OS like
[00:01:29] memory, operating system memory, more
[00:01:31] like RAM and disk simulation. My
[00:01:33] favorite by the way. So, starting from
[00:01:35] sequential, we're going to look at
[00:01:36] sliding window memory. We're going to
[00:01:37] look at summarization memory. We're
[00:01:39] going to look at retrieval memory. We're
[00:01:41] going to look at memory, enhanced, you
[00:01:44] know, augmented or enhanced memory as
[00:01:46] well, hierarchal memory, graph memory,
[00:01:49] compression memory, and then enlarge OS
[00:01:51] like memory. So we're going to talk
[00:01:52] about all of these things here, you
[00:01:53] know, how to how to use it, when to use
[00:01:56] it. I have created this entire notion
[00:01:58] page for you. So you can also go through
[00:02:00] it with the documentation, code
[00:02:02] snippets, so on and so forth. So this
[00:02:04] this is the only video or the code base
[00:02:07] or the documentation or the project
[00:02:09] whatever you call it. This is the only
[00:02:11] resource that you need to master, you
[00:02:13] know, memory part of building AI agents
[00:02:16] or agentic AI. So we're going to go
[00:02:18] through all of this and we have
[00:02:20] something called single tester batch
[00:02:22] comparison. You can compare multiple
[00:02:24] memories you know multiple memory
[00:02:26] strategies that you can compare over
[00:02:28] here that you see. And then we have
[00:02:30] performance dashboard. Performance
[00:02:31] dashboard data is not yet there because
[00:02:33] I haven't tested it yet. I will show you
[00:02:34] in a little bit. Uh single tester. Let's
[00:02:37] say we're going to talk about sequential
[00:02:39] memory, right? And I say initialize
[00:02:40] agent. The moment I hit initialize
[00:02:43] agent, you can see a chat interface
[00:02:45] opens over here. And let me show you
[00:02:47] what I mean by memory. Right? Most of
[00:02:49] you probably are not aware of memory,
[00:02:50] right? And you want to learn about it.
[00:02:52] So let me show you an example here. I'm
[00:02:54] going to say hi
[00:02:57] uh my name is Son
[00:03:00] and I'm going to send this. The moment I
[00:03:02] send it, it goes to a model. We are
[00:03:04] using OpenAI models. You use any model
[00:03:06] doesn't matter here. You know the the
[00:03:07] the thing that we're talking here is
[00:03:10] about memory. Okay. So if you look at
[00:03:12] here, it says, "Hi, my name is Sonu."
[00:03:14] And it gives me an answer. It says, "Hi,
[00:03:16] Sono. It's nice to meet you. How can I
[00:03:18] assist you today?" It also gives you the
[00:03:20] token count. That is very important. So,
[00:03:22] we're going to look at the latency.
[00:03:23] We're going to look at the token count.
[00:03:24] We're going to look at the accuracy. And
[00:03:26] of course, collectively, we're going to
[00:03:28] look at the performance of it, right?
[00:03:29] That's the agenda of it. So, here you
[00:03:32] can see, hi, my name is Sonu. Uh, you
[00:03:35] know, and I I just just ask this
[00:03:36] question here. Uh, and let me just ask
[00:03:40] other thing. Uh I am exploring
[00:03:46] quantum AI
[00:03:49] and I just do send now. Okay, you can
[00:03:51] see that sounds fascinating. Sonu
[00:03:53] quantum AI is an exciting field. So
[00:03:55] first I ask a question, my name is Sonu
[00:03:58] and then I ask I'm exploring quantum AI.
[00:04:00] Now I'm going to ask one more thing.
[00:04:04] What did I ask you first?
[00:04:11] And the moment I hit enter, it's going
[00:04:13] to answer me that you know Sonu or
[00:04:15] something. Okay, you can see over here
[00:04:16] it says you first asked me to introduce
[00:04:18] myself and mention that your name is
[00:04:20] Sonu. So this is what memory is. Memory
[00:04:22] means for agents. Human memory is really
[00:04:24] diff guys. You know we have a long-term
[00:04:26] memory. We have different way our memory
[00:04:29] works. Uh the the way human brain
[00:04:31] functions it's not exactly how we do
[00:04:33] right now. It's all context and database
[00:04:35] that you see when we talk about uh
[00:04:37] memory in AI systems. It's all database
[00:04:39] to be honest. Even if you're building it
[00:04:40] on production grade, it's still
[00:04:42] databases. Okay, to be honest. So if you
[00:04:45] look at here, it says what did I ask you
[00:04:47] first? And it answers me that you first
[00:04:49] asked me. But look at the number of
[00:04:51] tokens that it has consumed and time 1.8
[00:04:54] seconds 109 tokens. when you are
[00:04:56] building production grade right uh
[00:04:58] aentic systems where you have n number
[00:05:01] of users and it's conversational in
[00:05:04] fashion imagine how much memory you know
[00:05:06] uh compute it's going to utilize the
[00:05:08] memory part it's going to utilize a lot
[00:05:09] of compute latency will become an issue
[00:05:11] uh token cost will become an issue why
[00:05:14] I'm saying this because from a from a
[00:05:16] recent study that I was reading from
[00:05:18] Gartner Gartner said that 40% of AI
[00:05:21] projects will be canceled the agent AI
[00:05:23] projects will be cancelled by year 2027
[00:05:25] I believe or six whatever. Uh so what
[00:05:28] does that mean actually because we are
[00:05:29] not having a good governance layer by
[00:05:31] 2027 here that you see so memory also
[00:05:35] becomes part of that governance layer.
[00:05:36] So you have data ops where you look at
[00:05:38] the data layer you have uh your LLM ops
[00:05:41] the LLM ops comes up because we are
[00:05:43] talking about LLM based agents similarly
[00:05:46] we also have to have memory ops to be
[00:05:48] honest right now we look we have to look
[00:05:49] at the memory layer of it so that is
[00:05:51] also very important now this was the
[00:05:53] sequential memory and let me show you uh
[00:05:56] here we have a memory statistics that
[00:05:58] you see memory size six m messages
[00:06:01] conversational turns and in the detail
[00:06:03] statistics you find out all those
[00:06:05] details strategy type to sequential
[00:06:07] memory total messages six total turns
[00:06:10] three total content tokens and prompt
[00:06:13] tokens. So look at that right it's also
[00:06:15] gives you the advantages and
[00:06:16] disadvantages perfect recall because
[00:06:19] recall is really going to be perfect
[00:06:20] because it's sequential in order one
[00:06:21] after the other so previous context goes
[00:06:24] into the memory uh of or the prompt you
[00:06:26] know when we hit the LLM but the problem
[00:06:29] is linear token growth linear token
[00:06:32] growth is a problem here because the
[00:06:33] token consumption goes high so it's it's
[00:06:36] directly proportional to your you know
[00:06:38] uh API cost right the cost of the LLM so
[00:06:41] that's what it is not scalable by the
[00:06:43] So this is the one aspect. Now
[00:06:46] the thing is I want to show you this
[00:06:48] code will be with you. Don't worry about
[00:06:50] it. You can see I have created this
[00:06:51] memory strategies folder here and all of
[00:06:54] these are let me just show you
[00:06:55] sequential memory because it's important
[00:06:56] to show you. Now this is a sequential
[00:06:59] memory class uh that we have over here.
[00:07:01] If you look at this sequential memory
[00:07:04] you know it has an init function uh and
[00:07:06] then we have an add message function
[00:07:08] that takes your user input and takes
[00:07:10] your AI response. Therefore it takes and
[00:07:13] append into a list basically that's what
[00:07:15] it does and then it also counts the
[00:07:17] token and get context very simple memory
[00:07:20] here that you see get memory stats the
[00:07:22] sequential is the most easy one the
[00:07:24] similarly like sequential I have created
[00:07:27] different modular classes you can see
[00:07:29] these are all modular these are all
[00:07:30] class so we can use this in any one of
[00:07:32] our application also with any framework
[00:07:34] that we are using that if you want to
[00:07:36] use right so let me just go back and
[00:07:38] show you this this is one thing now to
[00:07:41] explain this further right I have
[00:07:43] created this agent memory design and
[00:07:45] optimization that you see because this
[00:07:47] is really important for you to go
[00:07:49] through and understand so the memory
[00:07:51] challenge is the first thing I told you
[00:07:53] why we need memory right so we need
[00:07:55] memory because of LLMs are you know
[00:07:58] statelessness they don't have a state
[00:08:00] right you need because they are like
[00:08:02] prompt based uh actions that they do you
[00:08:05] ask a question it returns an answer and
[00:08:07] most AI agents are now LLM based agents
[00:08:10] the other challenges are exponential ial
[00:08:11] token cost right it's a conversational
[00:08:14] history grows up let's say on daily
[00:08:16] basis if I'm having two hours of
[00:08:18] conversation right uh it it really goes
[00:08:21] high and if you if you have seen
[00:08:23] recently Sam Alman has said don't say hi
[00:08:26] hello hello or please or thank you or
[00:08:28] something to chat GPT because it cost a
[00:08:30] lot of money money to them right so
[00:08:32] don't do that actually then loss of
[00:08:34] context is also a a very big challenge
[00:08:36] in the conversational terms sometimes
[00:08:38] you know there is a tendency of uh LLM's
[00:08:42] misses or lost in middle. There is
[00:08:43] something called lost in middle attack
[00:08:45] that you should read about it.
[00:08:48] It's a Stanford paper lost in middle you
[00:08:50] know you read about man uh not man in
[00:08:53] the middle excuse me uh it's lost in the
[00:08:57] middle
[00:08:58] uh llm
[00:09:04] yes lost in the middle how language
[00:09:06] models use long context basically. So
[00:09:09] this is something that you should also
[00:09:10] read you know that will that will expand
[00:09:13] your understanding of the topic that why
[00:09:16] do we need such things right so going
[00:09:18] back here so you can see loss of context
[00:09:20] poor user experience due to repetitive
[00:09:22] information gathering if you're asking
[00:09:24] same thing again and again right so we
[00:09:26] should not do that actually right here
[00:09:28] so that is something also there now then
[00:09:30] we have inefficient resource utilization
[00:09:33] in production systems because when you
[00:09:34] work in production it's not that
[00:09:36] straightforward that we do like in PC's
[00:09:39] right so memory optimization matters
[00:09:42] right without memory you can see I have
[00:09:43] this code snippet don't worry I'll give
[00:09:45] you this uh notion page as well like
[00:09:47] this notion template whatever we call it
[00:09:49] okay here I have explained everything
[00:09:51] just now we saw sequential memory you
[00:09:53] can see perfect recall simple
[00:09:55] implementations the next is sliding
[00:09:57] window memory now slide sliding window
[00:09:59] is like you know it's a fixed size
[00:10:01] memory uh windows like let's say you
[00:10:04] have three four five as n number of your
[00:10:07] window you know it only look at your
[00:10:09] most recent N conversation n can be
[00:10:12] something that you can set so for
[00:10:13] example let's say if I select here
[00:10:15] sliding window memory and if I select
[00:10:17] window size as four it will look at the
[00:10:20] previous four context or whatever
[00:10:23] conversations that I that I have over
[00:10:24] there so that is on the
[00:10:27] uh sliding window memory that you see
[00:10:29] right uh it controls the memory
[00:10:31] consumption but it may lose important
[00:10:33] information because when the
[00:10:34] conversation goes like uh big right uh
[00:10:37] leni. So that is pretty straightforward.
[00:10:40] One of my favorite in this is of course
[00:10:42] summarization and retrieval. I I like
[00:10:44] retrieval a lot right because retrieval
[00:10:46] helps me retrieve some information that
[00:10:49] only I need in that memory. Let's go
[00:10:51] through the retrieval. Uh you can go
[00:10:53] through summarization by yourself. Let
[00:10:55] me come back here and go to retrieval
[00:10:59] memory. Now in the retrieval memory you
[00:11:01] can see retrieval count k equals to two.
[00:11:03] It's very similar right? when you build
[00:11:04] rack systems you know the retrieval part
[00:11:06] of it where you use embedding model
[00:11:08] right to do that let me show you how I
[00:11:10] have been doing it let's go to retrieval
[00:11:13] here right retrieval memory now if you
[00:11:15] look at the retrieval memory class what
[00:11:17] we are doing here we have a class that
[00:11:18] uses base memory strategy now base
[00:11:21] memory strategy is nothing but this one
[00:11:23] base memory strategy it's pretty simple
[00:11:26] thing so I'm not covering it look at the
[00:11:28] retrieval now if you look at the
[00:11:30] retrieval here we have by default k
[00:11:33] equals to and have an embedding
[00:11:35] dimension of 1536 over here and we are
[00:11:39] using text embedding is small from open
[00:11:42] AI you can use any other embedding model
[00:11:44] and we are using it's based on ukidian
[00:11:46] distance the way we have implemented
[00:11:48] this memory for AI agents the retrieval
[00:11:51] one you know it uses index flat L2 of
[00:11:54] course that uses ukidian distance for
[00:11:57] search the search that we do in the
[00:11:59] retrieval right it's all distance based
[00:12:01] search that we use and you can see It
[00:12:03] has if you look at it I also have
[00:12:05] commented it so you can understand
[00:12:06] better. List to store original text
[00:12:08] content of each document. Now this list
[00:12:11] basically store your original text
[00:12:12] content for each document that has been
[00:12:15] that has been kind of vectorized or
[00:12:16] whatever and then you know initialize
[00:12:19] fast. We are using fast CPU for this
[00:12:21] purpose. You can use any other vector
[00:12:23] store or vector database uh depending on
[00:12:25] what kind of services you have handy.
[00:12:28] And then if you keep going down right
[00:12:30] you can find it out this pretty much
[00:12:32] straightforward generates the embedding
[00:12:33] takes the document docs docs are nothing
[00:12:35] but the chunks that we do the chunks on
[00:12:38] you know recursive character text
[00:12:40] splitter or whatever you use to chunk it
[00:12:42] paragraph based chunks character based
[00:12:44] chunks word based chunks sentence based
[00:12:47] chunks so on and so forth right this is
[00:12:49] what we do here and then we create the
[00:12:53] we vectorize it and then store that that
[00:12:55] you see Right. And add vector to fast
[00:12:58] index making it searchable. This is what
[00:13:00] we not persisting it right now. It's on
[00:13:02] the runtime. So it's like on once your
[00:13:04] session is over this also gets
[00:13:05] disappeared actually. And this gets the
[00:13:08] content. Find K most relevant document
[00:13:10] from memory based on semantic similarity
[00:13:13] to query. Right? This is what it is. And
[00:13:15] we're going to talk about that in a
[00:13:16] little bit. Right? Let's let's go go
[00:13:18] through that. And it finds out you can
[00:13:21] see convert user query to embedding
[00:13:23] vector. convert to format required by
[00:13:25] fast perform search use return indices
[00:13:29] and then you just in the memory here so
[00:13:31] let's try it out right this is very
[00:13:33] interesting so
[00:13:37] let's try the okay let me initialize
[00:13:39] agent the moment you see I initialize
[00:13:40] agent you can see it says retrieval
[00:13:42] memory agent initialized and here I'm
[00:13:44] going to ask like you know I going to
[00:13:46] ask like you know I'm planning to
[00:13:50] go to UK
[00:13:53] This is my one question that I'm I'm
[00:13:55] just saying. Go to the United Kingdom
[00:13:56] would have been better, right?
[00:13:57] Grammatically,
[00:13:59] it says, "That sounds exciting. What
[00:14:01] specific information or assistance are
[00:14:03] you looking for regarding your trip to
[00:14:05] the UK? Are you interested in travel
[00:14:07] tips, places to visit, accommodations,
[00:14:09] or anything else?" Right? That's what it
[00:14:11] it replied to me. Now I'm going to say
[00:14:15] you know uh I'm I'm talking something
[00:14:18] else. Now for my
[00:14:23] for my memory project
[00:14:27] I used streamlate
[00:14:30] as the
[00:14:32] web interface.
[00:14:34] That's what I'm going to say here. I'm
[00:14:36] just now asking something not related to
[00:14:38] that trip because I want to you know
[00:14:40] make some uh how should I say it I just
[00:14:44] want to diversify that because I want to
[00:14:46] use the retrieval here right later on.
[00:14:47] So if you look at this it says great
[00:14:50] choice stream is a fantastic tool for
[00:14:52] building web applications I agree with
[00:14:53] this right and something right let's go
[00:14:55] and ask the next question here I want to
[00:14:58] visit
[00:15:01] Manchester
[00:15:03] uh rather I'll just go very specific
[00:15:07] I want to visit Old Trafford
[00:15:09] at
[00:15:11] at Manchester to watch United play
[00:15:15] something like this and I ask I'm a huge
[00:15:18] Man United fan. You can see that in
[00:15:20] back, right? Uh it says that sounds like
[00:15:22] a fantastic experience. Old Trafford is
[00:15:23] an iconic stadium. Are you looking for
[00:15:25] information on purchasing? Blah blah
[00:15:26] blah. And now I'm again going to divert.
[00:15:29] So for for the front uh for the
[00:15:33] backend API, I used
[00:15:37] fast API. That's what I used. And after
[00:15:39] this, I'm just going to ask one more and
[00:15:41] then I think we are good actually.
[00:15:47] Okay, now you can see we have a lot of
[00:15:48] conversation, right? Eight documents,
[00:15:50] eight vectors. It's it's happening on
[00:15:52] the fly. Okay, now I'm going to ask
[00:15:57] what city
[00:15:59] I'm going to, you know, uh travel.
[00:16:11] Let me ask what city I'm going to travel
[00:16:13] actually.
[00:16:19] And I'm asking this question what city
[00:16:21] I'm going to travel right and you can
[00:16:24] see the the token that it used that
[00:16:26] that's what I want to show okay you can
[00:16:28] see it says you haven't mentioned which
[00:16:29] specific city in the UK you want plan to
[00:16:31] travel to have a particular city that's
[00:16:32] a problem of the retrieval but if you
[00:16:34] look at that part here it says 86 tokens
[00:16:37] so it took place tokens by the way if
[00:16:39] you compare that with the sequential or
[00:16:40] sliding window or any other previous
[00:16:42] methods that we were talking about maybe
[00:16:44] the retrieval didn't work out because it
[00:16:46] should have figured it out from here
[00:16:48] when I said that I want to uh travel to
[00:16:51] Manchester because Manchester is a city
[00:16:53] uh in the United Kingdom. But that is
[00:16:56] completely fine. That's not the agenda
[00:16:58] of this video that if if the embedding
[00:17:00] models are uh working fine or not. Uh
[00:17:02] but here if you look at the embedding
[00:17:04] dimensions, number of document vectors,
[00:17:06] so on and so forth. So the number of
[00:17:09] token that it takes in the retrieval
[00:17:12] memory uh that you see it's it uses
[00:17:14] vector embeddings and similarity search
[00:17:17] and uh it uses it it's really less it it
[00:17:21] takes faster response time and also
[00:17:23] takes less token. So the in the
[00:17:25] production and then you have to make
[00:17:27] sure that you are using a really high
[00:17:28] quality embedding model and a vector
[00:17:30] database uh you know to amplify this
[00:17:34] retrieval memory and make sure it gets
[00:17:35] it right. uh it's faster also like for
[00:17:37] example if you see for the back end API
[00:17:40] I used fast API for this it took like
[00:17:42] 1.49 seconds just on relying on llm
[00:17:45] because you're passing a lot of previous
[00:17:47] context also right in that if you are
[00:17:50] not using retrieval by the way I'm
[00:17:51] saying for this one which what city I'm
[00:17:54] going to travel it based on the vectors
[00:17:56] it's the search and then gets you right
[00:17:58] 86 tokens 1.23 23 seconds. So this is on
[00:18:02] the retrieval memory. The same happens
[00:18:03] on the summarization. You know it
[00:18:05] summarizes it. It have some uh buffer.
[00:18:08] Same happens with sliding window memory.
[00:18:10] You have memory augmented memory. And
[00:18:13] all of these classes are defined here.
[00:18:14] If you go to memory augmented, you know,
[00:18:16] you can see it says it's a combination
[00:18:18] of sliding window with persistence
[00:18:20] memory tokens. Okay. There are
[00:18:22] advantages and disadvantages for this
[00:18:24] also. It's a complex implementations.
[00:18:27] Additional LLM calls increase cost and
[00:18:30] so on and so forth. So we have memory,
[00:18:32] augmented memory, we have OS memory
[00:18:34] which is again RAM like thing retrieval
[00:18:36] we talked sequential we talked sliding
[00:18:38] window we talked pretty standard
[00:18:40] summarization memory it's pretty
[00:18:42] standard also
[00:18:44] you know it compresses conversational
[00:18:46] history using LM like it summarizes your
[00:18:48] conversations and then based on that it
[00:18:49] decides it when you ask questions and
[00:18:51] then we have graph memory based on
[00:18:54] network X for relationship modeling what
[00:18:57] you can also do you can also do batch
[00:18:59] comparison so let's say here the
[00:19:01] My name is Alex blah blah blah. You can
[00:19:04] see I'm a software engineer. I'm working
[00:19:05] on a machine learning project. I prefer
[00:19:07] Python and love coffee. What do you
[00:19:09] remember about me and you can see you
[00:19:11] can run batch test. You can select
[00:19:12] multiple uh memories combinations and
[00:19:15] you can compare with each other. You can
[00:19:17] select from the drop- down basically
[00:19:20] from the drop down you can select it and
[00:19:22] it can work. So you can see it over
[00:19:23] here. Look at the average tokens, right?
[00:19:26] For retrieval memory 74 and for
[00:19:29] sequential memory 104. These are all
[00:19:31] tradeoffs by the way. Okay, it's it's
[00:19:33] something that you have to see like it's
[00:19:34] a trade-off. If you look at the final
[00:19:36] response, I remember that your name is
[00:19:38] Alex and you are a software engineer
[00:19:41] currently working on a machine learning
[00:19:42] project which is correct. You prefer
[00:19:44] using Python and love coffee. If there's
[00:19:46] anything else you would like to say or
[00:19:47] look at the memory statistics, right,
[00:19:50] total turns four. It took four turn. Of
[00:19:52] course token cost have been a bit higher
[00:19:55] uh that we see the average tokens
[00:19:57] talking about the average tokens guys
[00:19:59] not the complete tokens complete tokens
[00:20:01] can be find here in this total one now
[00:20:04] that is the one in the retrieval
[00:20:07] retrieval is a bit difficult to work
[00:20:10] right see people always say that why
[00:20:12] can't we build 100% successful rag
[00:20:15] systems problem is not with LLM problem
[00:20:18] is I will also not say is like with uh
[00:20:21] you
[00:20:23] problems are with the retrieval part
[00:20:24] guys. Retrieval is one of the most
[00:20:26] complex very intuitive a lot of people
[00:20:28] do uh you know people who who works in
[00:20:30] that area where they do research. Uh the
[00:20:33] problem is in the distance-based
[00:20:34] algorithms that's where the retrieval
[00:20:36] algorithms are difficult you know uh and
[00:20:39] that's why we don't get 100% correct
[00:20:41] results. If you look at here it says hi
[00:20:43] Alex I remember that you are a software
[00:20:45] engineer you mentioned wanting to
[00:20:47] discuss the projects you are currently
[00:20:48] working on the technologies blah blah
[00:20:50] blah right it not comprehensive as this
[00:20:53] because it also captures Python and love
[00:20:55] coffee but this also captures that
[00:20:57] software engineer Alex blah blah blah
[00:20:59] blah right so it also works uh that way
[00:21:02] so on this playground that you see you
[00:21:05] can also use different memory design or
[00:21:09] optimization strategies to kind of
[00:21:11] compare with each other. We also have a
[00:21:13] performance dashboard that you see on
[00:21:15] the performance dashboard you can find
[00:21:17] out token uses comparison you can find
[00:21:19] out response time analysis so on and so
[00:21:22] forth right with the current model that
[00:21:23] we have used it this has been used
[00:21:26] through plotly express we using plotly
[00:21:28] to do that now let's go back to batch
[00:21:30] comparisons you can see all the sessions
[00:21:32] are there so we're using stimulate
[00:21:33] sessions to make sure that the responses
[00:21:35] are there even if you change the tab
[00:21:38] right and this is the overview you can
[00:21:39] go through other memories also So guys I
[00:21:41] don't want to create a very lengthy
[00:21:42] video here you can read about uh in
[00:21:46] detail and can understand that how other
[00:21:49] memories are also working because this
[00:21:51] will help you make sure that you get the
[00:21:55] fundamentals cover understanding of the
[00:21:57] memory management and then you can build
[00:21:58] better uh know better aentic system on
[00:22:01] the memory part. Go through the code.
[00:22:03] Everything is modular. You see graph
[00:22:05] memory, compression memory, everything
[00:22:07] is modular. So you can use it in your
[00:22:09] example usages. You can use this in your
[00:22:12] file. You can see I have written each
[00:22:14] strategies can be easily swapped and
[00:22:16] tested. It's a plug-andplay module that
[00:22:18] we have used and you can test it out
[00:22:21] yourself. Not a problem. Now going back
[00:22:24] right
[00:22:26] these are important and I have created
[00:22:28] this agentic AI toolkit. In that toolkit
[00:22:32] you can get governance toolkit. You will
[00:22:34] get 100 plus n workflows, success
[00:22:38] frameworks. You will get use cases kit
[00:22:40] and skilluer. All of these you get in a
[00:22:42] single agentic AI bundle kit. And if you
[00:22:45] want to go details about what this kit
[00:22:47] contains, you can see we have in the
[00:22:49] agentic AI governance because governance
[00:22:51] is really important and this is not for
[00:22:53] individual. If you are some individual
[00:22:55] you know who is just trying learning AI
[00:22:57] agents uh this this bundle is not for
[00:23:00] you but it also has a 3 months skill
[00:23:02] builder kit. So it also has learning
[00:23:04] road maps. So it has learning road maps
[00:23:06] where we talk about phase wise weekly
[00:23:08] breakdown it hands on projects you know
[00:23:11] deployment tools portfolio builder your
[00:23:13] job preparation templates your bonuses
[00:23:16] in that three-month skill kit. Then we
[00:23:18] have use cases selection kit. Not all
[00:23:20] the use cases requires AI agents or
[00:23:23] agentic AI guys. You know discriminative
[00:23:25] models are also very helpful in today's
[00:23:28] world. You can still use machine
[00:23:29] learning natural language or deep
[00:23:30] learning based models or algorithms. You
[00:23:32] don't need everything to be done by AI
[00:23:35] agents. So these use case selection kit
[00:23:37] you know helps you you know uh navigate
[00:23:41] those challenges or confusions on what
[00:23:44] to what to do when to do kind of a
[00:23:46] scenario. And then we have success
[00:23:48] framework. In the success framework, we
[00:23:50] have full life cycle template to manage
[00:23:52] your AI agent projects, architecture
[00:23:54] diagrams, u memory optimization that we
[00:23:57] just saw. It's also part of that kit. We
[00:23:59] have evaluation strategy, anti-failures
[00:24:02] checklist. We have multiple models,
[00:24:04] pitfalls, build versus y matrix, when to
[00:24:07] build, when to buy kind of a thing. If
[00:24:08] you are a startup founder or if you are
[00:24:10] somebody who who is starting a new AI
[00:24:12] department or initiatives, uh this can
[00:24:15] really help you. We have Nit and
[00:24:17] workflow templates, battle tested
[00:24:20] templates guys, all tested, you know, if
[00:24:22] you want to use it. And then governance
[00:24:24] and risk management toolkit. All these
[00:24:26] five comes together in a single kit that
[00:24:28] I have named it Agentic AI toolkit. I'll
[00:24:30] give the link in description. Check it
[00:24:32] out. If you are interested, take it. If
[00:24:33] you are not interested, that is
[00:24:34] completely fine up to you. Right? It's
[00:24:37] pretty affordable prices. It took me
[00:24:39] more than 4 months to design and compile
[00:24:41] and curate this. So you can find it out
[00:24:44] over here. and lifetime updates. Every
[00:24:47] week I make updates. I keep pushing, you
[00:24:49] know, more collaterals and projects and
[00:24:52] private repositories into this kit. So,
[00:24:54] you can find those in description.
[00:24:56] Right. Going back to the memory design
[00:24:58] and optimization playground. Uh, very
[00:24:59] very important guys, focus on memory.
[00:25:02] Look at this uh open-source project.
[00:25:04] I'll give the link in description on my
[00:25:05] GitHub. Check it out. I'll also deploy
[00:25:08] this so you can try it out by yourself.
[00:25:11] And if you want to contribute to this
[00:25:13] repository, make a pull request and
[00:25:14] we'll see from there. Right? And if you
[00:25:17] have any question, thoughts or
[00:25:18] feedbacks, let me know in the comment
[00:25:20] box. You can also reach out to me
[00:25:22] through my social media channel. Guys,
[00:25:24] found those information on channel
[00:25:25] banner and channel about us. If you like
[00:25:28] this video, please hit the like icon. If
[00:25:31] you haven't subscribed the channel yet,
[00:25:32] please do subscribe the channel guys.
[00:25:34] That motivates me to create more such
[00:25:35] videos in near future. That's all for
[00:25:38] this video. Thank you so much for
[00:25:39] watching. See you in the next one.