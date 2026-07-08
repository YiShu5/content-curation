---
source_url: "https://www.youtube.com/watch?v=sgD-sw0RW78"
platform: youtube
uploader: "Arize AI"
title: "Letta: Building Stateful AI Agents with Memory and Sleep-Time Compute"
upload_date: "20250702"
duration: 2202
fetched_at: "2026-06-26T09:48:48.544740Z"
transcript_source: whisper-local
---

[00:00:00] There's a few things I kind of want to try to help everyone understand today. I think one of the first things, if you're at my panel earlier, was basically like what is an agent and like what is missing in agents today that, yeah, that just really doesn't exist and maybe like how much of it needs to be the model, how much of it needs to be the framework, and the title of this talk is obviously about learning, and I think that is really actually the fundamental missing piece in kind of LM-driven AI today.
[00:00:29] It's that a lot of these agents that we build on top of language models, they actually don't really have the capability to learn. I think there's a lot of different ways to talk about this problem that can be phrased as like the long context problem, it can be phrased as like maybe an RL problem, but fundamentally we just don't really have many agents that are deployed in production that can run for a very extended period of time. They don't derail, and instead they get like better and better and better as they run, kind of like humans do, as opposed to something that's like a workflow that you run once and you kind of throw it away. I think that's probably everyone in this room has like built some agent, but I think there's a good chance that
[00:00:58] that agent you built was something that you ran one time and you threw away, right? But I think we're moving towards a future where agents are much more like humans, and they're things that kind of like persist indefinitely.
[00:01:07] So yeah, some background on the company. Yeah, who here has heard of like MemGPT by any chance? It's like, okay, so it's like a paper that came out a while ago. It's about, I think if you see any of the memory features that are inside of like ChatGPT, Gemini, basically I think every single chatbot today has some sort of like memory feature baked in where it's like reading and writing to some sort of scratch pad memory.
[00:01:27] That idea is basically like the MemGPT paper idea where you have an agent and you let it edit, it has tool calling functions like create memory, delete memory, view memories.
[00:01:36] And yeah, that's something that myself and also my co-founder Sarah and our founding research scientist at Letta, we all worked on at Berkeley in the last year of our PhDs.
[00:01:44] And some other stuff that you might be familiar with, there's also the loss in the middle paper.
[00:01:48] But I think a more recent direction we're extremely excited about is this idea of sleep time compute.
[00:01:54] So that's something I'll also try to cover in this talk.
[00:01:55] I think everyone here has probably heard of test time compute, right?
[00:01:58] Test time compute, the new frontier to scale intelligence.
[00:02:00] I think sleep time compute is kind of test time compute taken to its limits.
[00:02:04] And I think this is actually the general direction that every sort of agentic system deployed in production is moving towards.
[00:02:10] So I think the idea of, you know, cloud code running in the cloud or cursor background agents.
[00:02:15] These are all like formalized, I think, in the limit of what they can do.
[00:02:18] They're kind of formalized as these sorts of sleep time compute agents.
[00:02:22] So I'll touch on that in the talk as well.
[00:02:23] And yeah, briefly to touch on what is Letta.
[00:02:26] So Letta, of course, is the name of the company.
[00:02:28] But I think if you are a software developer, like most of us here probably are, and you want to use Letta, the software, to do something at work or for, you know, your hobby,
[00:02:37] Letta is basically the fastest way to create AI agents that have long-term human-like memory.
[00:02:41] So if you're trying to build some sort of agentic system and part of your domain is you want this thing to not just like run once and then you throw it away,
[00:02:50] you want to deploy some sort of agent, maybe it's a co-worker, a very advanced workflow,
[00:02:54] and you want to run it many, many times or continually feed it more and more data,
[00:02:58] and you want it to get better and better over time, that is basically Letta.
[00:03:01] So I think today the best way to do that is to use our open source software.
[00:03:05] So I'll touch a little bit on this term I'll use for the rest of the talk called staple agents.
[00:03:10] So who here has, like, heard of the term staple agents?
[00:03:12] Okay, a few of us.
[00:03:14] Yeah, that's cool.
[00:03:15] Because I think staple agents is something that we started talking about last year.
[00:03:18] I think I've seen a decent amount of, like, pickup on this.
[00:03:20] I think even, like, Langrath is starting to adopt the terminology staple agent to describe what they're doing.
[00:03:25] But, yeah, we used to just call things agents back when I was a PhD student,
[00:03:28] but I think now I don't really like to use the word agent because it's very ill-defined.
[00:03:32] I think agent in 2025 doesn't really mean anything.
[00:03:34] I think anything that ever touched an LLM now is called an agent for better or worse.
[00:03:39] I think the proper, maybe, like, the better qualified terminology to describe what we really mean when we say agent
[00:03:45] and we want something that's really intelligent and really autonomous,
[00:03:48] I think staple agent actually captures that kind of perfectly well.
[00:03:52] So I really don't think we should be calling workflows agents.
[00:03:55] I think that's kind of, like, a disservice, but I feel like it's too late.
[00:03:58] Workflows are agents now, so might as well call the thing we used to call an agent a staple agent.
[00:04:02] So, yeah, I think we're all interested in, I mean, I think this stuff is super cool, right?
[00:04:06] So this is, I don't know exactly which software this was, but, you know, workflow builders have existed for a while.
[00:04:11] I'm pretty sure N8M, like, existed prior to ChatGPT.
[00:04:13] But I think these workflows and these workflow builders, they became much, much more powerful,
[00:04:19] or, like, Zapier is another one, right?
[00:04:20] It became much more powerful after, like, the advent of LMs.
[00:04:23] But at the end of the day, I don't think this is really, you know, when we used ChatGPT or used GPT-4 for the first time,
[00:04:29] and we got super excited about what we saw, I don't think we immediately thought about, like,
[00:04:33] oh, now let's, like, put ChatGPT into a workflow, right?
[00:04:35] I think we thought about something a little bit different, something much more autonomous.
[00:04:38] Maybe something kind of like this movie that we're probably all familiar with.
[00:04:44] Yeah, so I think that the thing missing with workflows, and the thing also missing with basically what everyone calls an agent today,
[00:04:50] is there really is not a lot of focus on state, memory, and in particular, the ability to learn.
[00:04:56] So, again, learning, I think, is the key distinction, which is kind of why AI today is not, in some ways,
[00:05:03] it's very useful for some things, but not useful for other things.
[00:05:05] I think the reason it's not useful for the other things is because we don't really have these learning systems built super well.
[00:05:10] So, yeah, this is a tweet I saw, yeah, I clearly reposted it.
[00:05:13] I thought it was pretty funny.
[00:05:15] I think it's kind of a very, an experience we can probably all relate to.
[00:05:19] I think if you can't read in the back, it says, it's like,
[00:05:21] my reaction when I have to end a Claude instance that helped me deal with some real shit in my life,
[00:05:26] and the context has become too long, and it's starting to go haywire, right?
[00:05:29] So, yeah, I know there are some people who, like, one thread ChatGPT.
[00:05:32] I think that's kind of insane, but people do that.
[00:05:34] But I've definitely had this, you know, this experience where I'm continuing a very long debugging session
[00:05:39] with, like, ChatGPT or Claude, and eventually it's, like, time to end it, you know?
[00:05:42] It's over.
[00:05:44] The context is too polluted.
[00:05:45] It's like there's no going back.
[00:05:46] And then you can do that trick where you're like,
[00:05:48] please summarize this chat for, like, the next session so I can copy-paste.
[00:05:51] But, yeah, I think the promise of Staple Agents is that this never happens again, right?
[00:05:56] We never, the only reason you would ever leave kind of a chatbot or leave an agent is,
[00:06:02] it's for other reasons.
[00:06:03] It's not because the agent derailed.
[00:06:04] It's not because it was getting worse and worse over time because of context pollution.
[00:06:07] It's maybe because you want a more specialized agent, right?
[00:06:11] You're done with, like, coding, and now you want to do, like, cooking or fitness or something.
[00:06:13] So then maybe you go to a different agent.
[00:06:15] So OpenAI, I think there's been a lot of attempts to define agents now.
[00:06:20] So OpenAI, I'm going to pick on them here.
[00:06:23] They're the big boys.
[00:06:24] But they had this, like, presentation at, I believe this was the AI Engineer Conference in New York City,
[00:06:30] where they're kind of outlining what is an agent.
[00:06:32] And I think even here, if you talk to, you know, like, most AI researchers,
[00:06:36] the thing they would immediately call out here that's missing is, like, memory or state.
[00:06:40] Like, they're opening up saying an agent is just model, instructions, tools, and runtime,
[00:06:43] but it doesn't have state, and that's where a stateful agent comes in.
[00:06:47] So a lot of the stuff I'm saying about learning being extremely important
[00:06:51] and memory being kind of, like, a cornerstone of human-like intelligence,
[00:06:55] this is not new stuff, right?
[00:06:57] I think if you go and pick up this really old book on reinforcement learning by Sun Lombardo,
[00:07:01] it's kind of, like, the RL canon, and you scroll to, like, the first few pages,
[00:07:05] it's very, very quickly you start to see the word learn.
[00:07:08] And this is the kind of diagram you see to describe what an agent is.
[00:07:12] This is, like, prior to ChatGPT.
[00:07:14] This is, like, the agent in AI before that.
[00:07:16] You know, I think that there's very few elements here.
[00:07:19] It's, like, you have the agent, you have the environment,
[00:07:21] you have the reward, the observations, the actions.
[00:07:23] I think everything here we already have, right?
[00:07:25] The agent is the language model.
[00:07:27] The action is the tools, the MCP servers, whatever.
[00:07:29] The environment, maybe it's, like, a web simulator.
[00:07:32] Like, you're connecting your agent to the web.
[00:07:33] Maybe it's your agent running inside of your own, like, CRM or something,
[00:07:37] or it's running inside of, like, your internal business.
[00:07:39] And I think the one thing that's missing that doesn't really exist in most systems today
[00:07:45] is, like, the state.
[00:07:46] And I think the key part that makes this a very important part of this diagram
[00:07:51] is it's a loop.
[00:07:51] It's a circle, right?
[00:07:52] And the reason it's a closed loop is because the agent updates its own state
[00:07:55] or updates its own memory as it continues to act in this environment.
[00:07:58] And, yeah, this is where I think maybe things get a little bit more interesting,
[00:08:03] is that this learning, I don't think you have to do this learning only at inference time,
[00:08:09] right, when you kind of interact with the agent.
[00:08:11] I think right now what happens when you use ChatGPT is ChatGPT,
[00:08:15] like, when you're using it, it's interacting with you.
[00:08:17] It's, like, you know, there's, the brain is cooking on some GPU farm somewhere.
[00:08:21] But when you leave ChatGPT, ChatGPT is, like, completely dormant
[00:08:24] and never does anything until you come back, right?
[00:08:26] I think there's a lot of, like, missed opportunity to be doing things in the background, right?
[00:08:30] You can imagine, like, Claude code.
[00:08:32] If you're, who here has used, like, Claude code or, like, Cursor?
[00:08:35] Like, these very, like, powerful coding agents, right?
[00:08:36] Well, imagine if you, like, instantiate Claude code
[00:08:38] and then someone in your open office, like, starts screaming at you
[00:08:42] about some, like, you know, prod went down.
[00:08:44] So you have to go do something else.
[00:08:45] But then you come back to Claude code.
[00:08:47] And if Claude code is, like, running in the clouds,
[00:08:49] you don't have to worry about, like, your, you know,
[00:08:50] your laptop battery dying or anything.
[00:08:52] Why should have Claude code just been,
[00:08:54] have been sitting there the whole time?
[00:08:55] Like, it had access to your GitHub repo.
[00:08:57] It had access to your code.
[00:08:58] It should have been doing something like indexing your code base.
[00:09:00] And maybe it could have been crawling Slack
[00:09:02] to figure out all the recent things that people were complaining about,
[00:09:04] crawling GitHub issues, right?
[00:09:06] So I think if we call, when we're interacting with agents, test time.
[00:09:10] And that's why we call test time compute.
[00:09:12] That's, like, the new kind of scaling mode.
[00:09:14] You kind of run it for longer when you ask it a question.
[00:09:16] That's why 0.3, like, takes, you know, 10, 20 minutes.
[00:09:19] Well, if that's test time, then I think everything else,
[00:09:21] we can call it sleep time.
[00:09:23] And we should actually be using,
[00:09:25] utilizing our agents at that point in time.
[00:09:26] I think this is really where everything is going to next.
[00:09:30] Like, dramatic, like, extremely asynchronous,
[00:09:32] massively parallel, like, fleets of agents running
[00:09:37] at any given point in time.
[00:09:38] And that's something that we're also very interested in at Leta.
[00:09:40] But I think there's some very obvious examples
[00:09:44] I can kind of point to for why you might want this.
[00:09:47] One example, it's a little bit contrived,
[00:09:49] but imagine if you're playing a game with ChatGPT
[00:09:51] and your ChatGPT is asking you, like, you know,
[00:09:54] 50 questions or something.
[00:09:56] I forgot what the game is called.
[00:09:57] It's asking you a bunch of questions about yourself.
[00:09:58] And the questions are extremely mundane.
[00:10:00] It's actually just about what colors you like.
[00:10:01] So you could be having this conversation
[00:10:02] where you're saying, oh, I like blue.
[00:10:04] Oh, I like red more than blue.
[00:10:06] Oh, I like gray.
[00:10:07] I like, oh, I hate green, right?
[00:10:08] But I think if you actually played this out with ChatGPT
[00:10:12] and you, like, prime ChatGPT to be pretty aggressive
[00:10:15] about its memory, ChatGPT's memory
[00:10:16] at the end of the experiment would look a lot like this, right?
[00:10:19] It would look like a lot like just a list of facts
[00:10:22] that you had stated out.
[00:10:22] And I think if you all look at the thing on the left,
[00:10:26] maybe we're all kind of itching and saying, like,
[00:10:29] hey, that's, like, really inefficient, right?
[00:10:30] This is, like, a whole bunch of atomic statements,
[00:10:32] but often memories are more than a sum of their parts, right?
[00:10:36] So what you could do here
[00:10:37] is you could just rewrite this entire list of preferences
[00:10:40] into, you know, their color preferences
[00:10:42] are gray, red, blue, green, and they hate green, right?
[00:10:46] So it's kind of a rewriting of your memories
[00:10:48] to be much more compact
[00:10:49] and actually communicate, like, much more information in them.
[00:10:52] So I think this sort of thing is a pretty obvious,
[00:10:57] it's an obvious next step for even ChatGPT memory.
[00:11:00] Who here is, like, open ChatGPT memory
[00:11:02] for whatever reason,
[00:11:03] because maybe you're interested in what was happening,
[00:11:05] and you were just kind of, like, flabbergasted
[00:11:06] at how, like, dirty it was,
[00:11:08] how it just had, like, the most random stuff in there,
[00:11:10] like a list of, like, all these different facts
[00:11:11] that don't relate to each other,
[00:11:12] or maybe they do relate to each other,
[00:11:13] but they're, like, they should be consolidated.
[00:11:15] So I think that naturally is also kind of the next step
[00:11:17] for ChatGPT memory.
[00:11:18] They'll kind of run these sleep-time compute cycles
[00:11:20] where they run agents in the background
[00:11:21] to kind of crank over all your memories
[00:11:23] and consolidate them.
[00:11:24] But I think ChatGPT is just, like, one example.
[00:11:27] I think this example applies very heavily to coding.
[00:11:29] And I didn't realize I was going to be able
[00:11:31] to plug in my own laptop,
[00:11:32] so I did not, I was going to,
[00:11:34] I would usually live demo this
[00:11:35] if you have time against the live demo it.
[00:11:37] But this is an example of what this looks like
[00:11:39] running inside of Leta, our software.
[00:11:40] So I don't know exactly when the loop starts here.
[00:11:44] Okay, so this loop is starting,
[00:11:45] and you can see the user says something like,
[00:11:47] my name is Sarah.
[00:11:49] And if you were running the usual memGPT-style agent,
[00:11:52] what actually happened here
[00:11:53] is the agent would pause and say,
[00:11:55] hold on, hold on,
[00:11:55] I'm going to, like, write to my memory real quick.
[00:11:57] Let me get back to you.
[00:11:58] And then it returns.
[00:11:59] The problem with that
[00:12:00] is it's obviously, like, pretty intrusive.
[00:12:01] You have double the LM latency,
[00:12:03] effectively, to get back a response.
[00:12:04] What's happening in this loop,
[00:12:06] you're seeing is actually there's an agent
[00:12:08] completely detached in the background.
[00:12:09] It's effectively, like,
[00:12:10] the subconscious brain of the main agent.
[00:12:12] And that agent is going to, like,
[00:12:14] do this sort of memory rewriting
[00:12:15] in the background.
[00:12:16] So you completely remove
[00:12:17] any sort of synchronous blocking problems.
[00:12:19] And I think this is basically
[00:12:21] where all these sorts of, like,
[00:12:23] memory-driven agents are going.
[00:12:25] It's all about asynchronous.
[00:12:25] It's all about sleep-time compute.
[00:12:27] Another example,
[00:12:29] I probably should have used coding here,
[00:12:31] but this diagram was already made.
[00:12:32] But another example is, you know,
[00:12:35] if you're using Claude projects.
[00:12:36] Who of yours used Claude projects?
[00:12:37] I think it's, like, pretty, yeah, okay,
[00:12:38] decent amount of people.
[00:12:39] So I think it's, like,
[00:12:39] it's a pretty great tool.
[00:12:40] So basically, it's a very easy way
[00:12:42] to get Claude to know about, like,
[00:12:44] some documents you have in an organized way.
[00:12:46] But all that happens
[00:12:48] when you upload a document to Claude projects
[00:12:49] is it basically just gets interpreted into text
[00:12:52] and it gets dumped
[00:12:53] at the context window, right?
[00:12:54] I think a much more human-like experience,
[00:12:57] if your AI was really,
[00:12:58] had, like, human-like memory,
[00:12:59] human-like agency,
[00:13:00] is that as soon as you uploaded
[00:13:02] some sort of document, you know,
[00:13:03] like, maybe it's a group of documents,
[00:13:04] my business plans,
[00:13:05] my, you know, USA shirts,
[00:13:07] idea, v1 PDF,
[00:13:08] candidatefactories.pdf,
[00:13:10] I just dump these PDFs into Claude,
[00:13:12] well, Claude should immediately start cooking.
[00:13:14] And it should start, like,
[00:13:14] reading over all these documents,
[00:13:16] analyzing them,
[00:13:17] and doing this very proactively.
[00:13:18] I shouldn't have to kind of ask it a question
[00:13:21] to trigger some analysis, right?
[00:13:22] This should all happen at sleep time.
[00:13:23] So this is another thing.
[00:13:26] And then to read kind of the text here
[00:13:29] for people in the back,
[00:13:29] basically these documents get turned
[00:13:32] without you doing anything into a memory.
[00:13:34] And that memory says, like,
[00:13:35] this data source contains important information
[00:13:38] about Chad's business plans for his company.
[00:13:40] The idea of v1 file covers logistics
[00:13:42] of running a clothing operation,
[00:13:43] specializes in men's T-shirts,
[00:13:44] you know, maybe some sort of dropshipping thing.
[00:13:47] Well, I guess it's made in the USA,
[00:13:48] so it's not dropshipping.
[00:13:49] But, yeah, you get the idea, right?
[00:13:51] Basically, you upload all these documents,
[00:13:52] and you have all these GPUs,
[00:13:54] and often, like, you know,
[00:13:55] these data centers,
[00:13:56] they want to saturate,
[00:13:57] they want to saturate GPU inference.
[00:13:59] And you should just run these agents
[00:14:00] on this data
[00:14:02] without the user having to intervene
[00:14:03] and do anything for you.
[00:14:05] Yeah, so this is another example,
[00:14:07] screen grab of what this looks like in practice.
[00:14:10] So all the ideas I'm talking about,
[00:14:11] they're implemented in the memgpt project,
[00:14:13] or, sorry, in the Leta project.
[00:14:14] But, yeah, if you upload a file,
[00:14:15] effectively a new block in memory gets generated,
[00:14:18] and you have an agent
[00:14:19] that kind of runs in the background
[00:14:20] without you chatting to the main agent,
[00:14:23] and it kind of generates these memories
[00:14:24] about that document.
[00:14:26] So I think
[00:14:27] you can basically think about
[00:14:31] there are two main directions
[00:14:33] to scale compute.
[00:14:34] If you assume that model performance
[00:14:36] is, like, saturated
[00:14:37] or is, like, saturating to some point
[00:14:39] or has diminishing returns, right?
[00:14:41] I think the obvious one
[00:14:42] that we've heard about for the past year
[00:14:43] is test-time compute.
[00:14:44] You, like, let the language models
[00:14:46] run for longer.
[00:14:47] They get better and better answers
[00:14:49] because they get to think for longer.
[00:14:50] And the other one is,
[00:14:52] well, you don't just run them
[00:14:53] for longer and longer
[00:14:54] when the user asks.
[00:14:55] You run them for longer and longer
[00:14:56] all the time, right?
[00:14:57] As much as you can,
[00:14:58] as much as it kind of, like,
[00:15:00] makes meaningful sense.
[00:15:01] And I think, yeah,
[00:15:02] that's kind of the direction
[00:15:03] everything is going in.
[00:15:04] So I think the natural question here,
[00:15:06] and I think this is kind of
[00:15:07] the second half of the talk
[00:15:09] is fundamentally
[00:15:10] if we're all kind of builders
[00:15:11] or developers in this audience
[00:15:13] and we're interested in the idea
[00:15:14] of stateful agents, right?
[00:15:15] And it's clear that maybe
[00:15:16] language models themselves
[00:15:17] are not stateful agents.
[00:15:18] Well, what do we have to build?
[00:15:21] Like, what's left?
[00:15:22] If we have the models,
[00:15:23] the best models on the planet Earth
[00:15:25] given to us by these frontier labs,
[00:15:26] what's left to make
[00:15:28] these sorts of stateful agents?
[00:15:30] And I think really the best way
[00:15:31] to frame what's left
[00:15:32] is it's effectively
[00:15:33] building an operating system.
[00:15:35] But it's building
[00:15:35] an operating system
[00:15:36] whose primary function
[00:15:37] or primary objective
[00:15:38] is to orchestrate context.
[00:15:39] So there was a talk recently
[00:15:43] by Andrei Karpathy
[00:15:44] where he talked about
[00:15:45] context engineering, right?
[00:15:46] And I think actually
[00:15:47] the tweet or something
[00:15:48] was yesterday or today.
[00:15:49] So this terminal
[00:15:50] is kind of taking off.
[00:15:51] So I think that's exactly
[00:15:53] what I'm talking about here as well.
[00:15:55] It's basically
[00:15:55] you need some sort of system
[00:15:58] that is going to do
[00:15:58] context engineering
[00:15:59] on your behalf
[00:16:00] to move tokens
[00:16:01] in and out of the context window.
[00:16:02] But beyond that,
[00:16:03] I think that's it.
[00:16:03] You basically,
[00:16:04] I think the map
[00:16:06] or the road to AGI
[00:16:07] is very simple.
[00:16:08] It's you have the language models
[00:16:09] and you need to build
[00:16:09] the operating system
[00:16:10] to manage the context.
[00:16:11] And I think those
[00:16:12] are the two parts.
[00:16:14] And I think a lot of us
[00:16:16] probably have heard
[00:16:17] about the LMOS operating
[00:16:18] system thing.
[00:16:19] That's also something
[00:16:19] that we were talking about
[00:16:21] and also Andrei was talking
[00:16:22] about as far back
[00:16:23] as like 2023.
[00:16:23] So yeah,
[00:16:24] the name of the paper
[00:16:26] MemGPT was actually
[00:16:27] MemGPT towards language
[00:16:28] models as operating systems.
[00:16:30] So an operating system
[00:16:31] for language models
[00:16:32] driven by language models.
[00:16:33] So yeah, this idea,
[00:16:34] we've been working on it
[00:16:35] for a while.
[00:16:36] And yeah,
[00:16:36] we really think this is
[00:16:37] kind of the last missing piece.
[00:16:39] So one way to describe it
[00:16:42] is it's basically
[00:16:43] the open AI operating system.
[00:16:44] So all the stuff
[00:16:46] we're describing today,
[00:16:47] this dream of having
[00:16:48] the truly stateful agent,
[00:16:49] well, it's definitely
[00:16:51] not just my dream.
[00:16:52] I think it's also the dream
[00:16:53] of Sam Altman
[00:16:54] and other people
[00:16:55] running these frontier labs.
[00:16:56] But I think Leta
[00:16:57] is the only company
[00:16:58] that's really building
[00:16:59] this sort of software
[00:17:00] in the open as open source.
[00:17:02] And I think one interesting thing
[00:17:05] that I'm not sure
[00:17:06] if it's on these slides,
[00:17:07] but an interesting thought
[00:17:09] experiment you can do
[00:17:10] is if we believe
[00:17:10] we are actually moving
[00:17:12] into a world
[00:17:12] where we have these agents
[00:17:13] that are no longer workflows,
[00:17:14] they last for days,
[00:17:16] weeks, months, years.
[00:17:18] Just think about
[00:17:19] how often you swap out
[00:17:20] your models, right?
[00:17:21] How often does the best model
[00:17:23] whiplash from open AI
[00:17:25] to anthropic
[00:17:26] to deep seek, right?
[00:17:27] I think we're very quickly
[00:17:29] moving to a world
[00:17:30] where the lifetime
[00:17:31] of the agents
[00:17:32] are much longer
[00:17:32] than the lifetime
[00:17:33] of the models.
[00:17:33] And I think part of the reason
[00:17:36] why it's so important
[00:17:36] for this AI operating system
[00:17:38] that stores the agent memory
[00:17:39] and stores the agent state
[00:17:40] to be open
[00:17:40] is because you really
[00:17:42] don't want to end up
[00:17:42] in a scenario
[00:17:43] where you're building
[00:17:43] these agents,
[00:17:44] these staple agents
[00:17:45] that run for years
[00:17:46] or decades
[00:17:47] at your company,
[00:17:48] for example,
[00:17:48] and have them locked
[00:17:50] into a single model provider,
[00:17:51] right?
[00:17:51] I mean, just imagine
[00:17:52] how devastating it would be
[00:17:53] if you built, you know,
[00:17:54] the kind of an AGI employee
[00:17:56] that works at your company,
[00:17:57] but an employee
[00:17:58] cannot be migrated
[00:17:59] from open AI
[00:18:00] to anthropic.
[00:18:01] And then let's say
[00:18:02] open AI has a really bad year
[00:18:03] one year
[00:18:04] and their models
[00:18:04] just like suck
[00:18:05] compared to like
[00:18:06] the new Sonnet, right?
[00:18:07] Well, your employee
[00:18:08] is permanently gimped.
[00:18:09] It cannot be moved
[00:18:10] to the new anthropic model
[00:18:11] because you've decided
[00:18:12] to build your stateful agent
[00:18:13] on open AI.
[00:18:14] So I think there's
[00:18:15] a very strong incentive
[00:18:16] actually for this,
[00:18:17] the other part
[00:18:18] of the equation,
[00:18:19] not just the model,
[00:18:19] but for the system
[00:18:20] around it
[00:18:21] for that to be open.
[00:18:22] I think that there's
[00:18:22] just too many incentives
[00:18:23] for that to be closed.
[00:18:24] Yeah, so this diagram,
[00:18:28] I think we looked
[00:18:28] at it earlier.
[00:18:29] It's just about like
[00:18:29] what are the pieces here?
[00:18:31] It's like the state,
[00:18:31] the model,
[00:18:32] and the action.
[00:18:32] And I think
[00:18:34] to kind of blow
[00:18:34] this model up
[00:18:35] or blow that chart
[00:18:36] a little bit wider,
[00:18:37] really the pieces
[00:18:39] are still very simple,
[00:18:40] but I think
[00:18:41] the individual building blocks,
[00:18:42] there's a lot
[00:18:43] of new things emerging, right?
[00:18:44] So I think we've all
[00:18:45] been maybe kind of shocked
[00:18:47] or excited
[00:18:48] by the energy around MCP.
[00:18:49] So I think a lot of us,
[00:18:51] you know,
[00:18:51] if I made this diagram
[00:18:53] a year ago,
[00:18:53] MCP is not in here.
[00:18:55] It's just like Python tools
[00:18:56] executed on modal maybe.
[00:18:58] But now MCP
[00:18:59] is maybe the primary way
[00:19:00] to take actions.
[00:19:01] And the thing in the middle,
[00:19:03] you know,
[00:19:03] I think if I made this
[00:19:04] a year ago,
[00:19:05] Gemini would not be here
[00:19:06] because those models
[00:19:07] were not that good.
[00:19:08] But now today,
[00:19:09] I'm definitely including
[00:19:10] Gemini because we see
[00:19:11] a lot of developers
[00:19:11] in production running
[00:19:12] Gemini just because
[00:19:13] of the cost performance
[00:19:14] trade-off.
[00:19:15] And the thing that I think
[00:19:17] has not changed
[00:19:18] this entire time
[00:19:19] kind of since,
[00:19:20] you know,
[00:19:20] I was a PhD student
[00:19:21] and since we started
[00:19:22] this company
[00:19:22] is really this is just,
[00:19:24] you know,
[00:19:25] it's a puzzle
[00:19:25] that has three pieces
[00:19:26] and the piece on the left,
[00:19:28] the state,
[00:19:28] the memory,
[00:19:29] and the context.
[00:19:29] I think every month,
[00:19:31] every quarter,
[00:19:33] every year,
[00:19:33] it becomes much more
[00:19:34] apparent to everyone
[00:19:36] building on these systems
[00:19:36] that this is actually
[00:19:37] extremely important.
[00:19:38] And, you know,
[00:19:39] going back to my last point
[00:19:40] about the model,
[00:19:41] the agents outlasting
[00:19:42] the model,
[00:19:43] I think one way
[00:19:44] to phrase this
[00:19:45] is that the memory
[00:19:46] and the context
[00:19:47] is more valuable
[00:19:47] than the model.
[00:19:48] I think basically
[00:19:50] if you have agents
[00:19:51] that run for like,
[00:19:52] you know,
[00:19:52] five,
[00:19:53] ten years,
[00:19:54] there's no way
[00:19:55] that the most important
[00:19:56] part of that agent,
[00:19:57] if the agent is just
[00:19:57] state, memory,
[00:19:58] and the model,
[00:19:58] is the model, right?
[00:20:00] It's the state
[00:20:01] and the memory.
[00:20:02] And yeah,
[00:20:04] functionally,
[00:20:04] how you would actually
[00:20:05] interface with this
[00:20:05] is you would use an API.
[00:20:06] So I think a lot
[00:20:07] of the things
[00:20:08] we kind of play with today
[00:20:09] when we're building agents,
[00:20:11] we're basically,
[00:20:12] you know,
[00:20:12] building on agent frameworks
[00:20:14] that are agent libraries.
[00:20:15] They're kind of middleware
[00:20:16] that lets us build
[00:20:17] very quickly on OpenAI.
[00:20:18] And what makes
[00:20:19] these agent libraries
[00:20:20] so easy to use
[00:20:21] also makes these agent libraries
[00:20:23] so easy to throw away.
[00:20:24] It makes it so easy
[00:20:25] for you to swap
[00:20:25] from OpenAI Agents SDK
[00:20:26] to, you know,
[00:20:27] LangChain
[00:20:28] to, like,
[00:20:29] whatever agent library
[00:20:30] because really
[00:20:31] these are just,
[00:20:31] it's like middleware
[00:20:32] that's helping you use
[00:20:33] the model providers,
[00:20:35] but it's not necessarily,
[00:20:36] it's not dealing
[00:20:37] with this thing on the left
[00:20:38] which is like the state
[00:20:39] and the memory context
[00:20:39] that's storage.
[00:20:40] So I think
[00:20:43] with regards to,
[00:20:43] like, what,
[00:20:44] you know,
[00:20:44] if anyone here is wondering,
[00:20:45] like,
[00:20:46] what,
[00:20:46] if you call
[00:20:48] Leta an agent framework,
[00:20:49] how is it different
[00:20:49] from other agent frameworks?
[00:20:51] Leta,
[00:20:52] sure,
[00:20:52] you can call it
[00:20:53] an agent framework,
[00:20:53] but it's really all about,
[00:20:54] it's a service.
[00:20:55] It's all about running
[00:20:55] a database that stores
[00:20:56] all the memories,
[00:20:57] all the context
[00:20:58] of your models.
[00:20:58] Okay,
[00:20:59] I'm getting the wrap-up
[00:21:00] signal here,
[00:21:01] so the last thing
[00:21:02] I want to talk about,
[00:21:03] oh,
[00:21:06] really quick,
[00:21:07] this thing here,
[00:21:07] one interesting thing
[00:21:09] that we talk about
[00:21:10] a lot with Leta
[00:21:10] is that you're building
[00:21:11] an operating system,
[00:21:12] but you're making
[00:21:12] the operating system
[00:21:13] run by other agents,
[00:21:14] right?
[00:21:15] The agents decide
[00:21:15] what gets stored,
[00:21:17] the agents decide
[00:21:17] kind of what gets
[00:21:18] pulled into context.
[00:21:18] So obviously,
[00:21:19] if you're doing that,
[00:21:21] you need a leaderboard
[00:21:22] to kind of evaluate,
[00:21:22] well,
[00:21:23] what models are very good
[00:21:23] at running an operating system?
[00:21:25] So this is something
[00:21:25] we run.
[00:21:26] I'm not going to touch
[00:21:27] on this here.
[00:21:27] If you want to look
[00:21:28] at details about
[00:21:28] how this is done,
[00:21:29] it's all open.
[00:21:30] Just go to the Leta leaderboard.
[00:21:32] And the last thing
[00:21:33] I'll say is a lot
[00:21:34] of the stuff
[00:21:34] I'm talking about today,
[00:21:35] it is in production.
[00:21:36] So I did talk about
[00:21:38] at the beginning
[00:21:39] of this talk
[00:21:40] how I think
[00:21:41] a lot of people
[00:21:41] are deploying
[00:21:42] workflows,
[00:21:43] stateless agents,
[00:21:44] things that really
[00:21:45] aren't,
[00:21:46] they aren't stateful,
[00:21:47] they aren't long running,
[00:21:48] but there are companies
[00:21:50] that are building this.
[00:21:51] So I think
[00:21:52] definitely the largest,
[00:21:52] I think probably
[00:21:53] the largest deployment
[00:21:54] of stateful agents
[00:21:54] in the world right now
[00:21:56] is with built rewards.
[00:21:57] So basically,
[00:21:57] their recommendation engine,
[00:21:59] it is driven
[00:22:00] by stateful agents.
[00:22:00] So there's a chance
[00:22:02] that if you use
[00:22:03] built rewards,
[00:22:03] you might be feature flagged
[00:22:05] into like the version
[00:22:07] of the recommender system
[00:22:07] that is actually,
[00:22:08] I think there's like
[00:22:09] over a million agents
[00:22:10] now running,
[00:22:11] but you might be
[00:22:11] in the version
[00:22:12] where your recommendations
[00:22:13] are generated by agents.
[00:22:14] It's not generated
[00:22:15] by like a classic
[00:22:16] black box recommender system.
[00:22:17] These agents
[00:22:18] that kind of look
[00:22:18] at all your transactions,
[00:22:19] they turn those transactions
[00:22:21] into memories,
[00:22:21] and those memories
[00:22:22] are used to generate
[00:22:23] very, very good
[00:22:24] recommendations.
[00:22:25] So yeah,
[00:22:26] I'll wrap up there.
[00:22:27] And yeah,
[00:22:29] I'll be around
[00:22:29] for a bit longer,
[00:22:31] so I know
[00:22:32] there's a closing slide here,
[00:22:33] but yeah,
[00:22:34] happy to chat more
[00:22:35] about this.
[00:22:36] Yeah,
[00:22:37] and thanks so much
[00:22:37] for coming.
[00:22:48] Thank you.
[00:23:18] Thank you.
[00:23:48] Thank you.
[00:24:18] Thank you.
[00:24:48] Thank you.
[00:25:18] Thank you.
[00:25:48] Thank you.
[00:26:18] Thank you.
[00:26:48] Thank you.
[00:27:18] Thank you.
[00:27:48] Thank you.
[00:28:18] Thank you.
[00:28:48] Thank you.
[00:29:18] Thank you.
[00:29:48] Thank you.
[00:30:18] Thank you.
[00:30:48] Thank you.
[00:31:18] Thank you.
[00:31:48] Thank you.
[00:32:18] Thank you.
[00:32:48] Thank you.
[00:33:18] Thank you.
[00:33:48] Thank you.
[00:34:18] Thank you.
[00:34:48] Thank you.
[00:35:18] Thank you.
[00:35:19] Thank you.
[00:35:19] Thank you.
[00:35:48] Thank you.
[00:35:49] Thank you.
[00:36:18] Thank you.
[00:36:20] Thank you.