---
source_url: "https://www.youtube.com/watch?v=W2HVdB4Jbjs"
platform: youtube
uploader: "AI Engineer"
title: "Architecting Agent Memory: Principles, Patterns, and Best Practices — Richmond Alake, MongoDB"
upload_date: "20250627"
duration: 1056
fetched_at: "2026-06-26T09:40:44.387590Z"
transcript_source: whisper-local
---

[00:00:00] in the next 10 to 15 minutes has I guess my promise to you I'm going to give you
[00:00:20] some information that will be high level there will be some practical component to it but this
[00:00:29] information I'll give you within the next six months will be very relevant and it will put
[00:00:34] you in the best position to build the best AI applications to build the best agents that are
[00:00:40] believable capable and reliable I know we're gonna get there you know what just for you there
[00:00:50] we go you're welcome so we're gonna be talking about memory we're gonna be talking about the
[00:00:58] stateless applications that we're building today and how we can make them stateful we're going to be
[00:01:04] talking about the prompt engineering that we're doing today and how we can reduce that by focusing
[00:01:09] on persistence we're going to be turning the responses in our AI application and making our
[00:01:15] agents build relationship with our customers and all of it is going to be centered around memory so I'm
[00:01:26] going to do a very quick evolution of what we've been seeing for the past two to three years we started
[00:01:33] off with chatbots LLM power chatbots they were great chapter GPT came out November 2022 and yeah exploded then we went into rag we gave this chatbots more domain
[00:01:45] specific relevant knowledge and they gave us more personalized responses then we begin to scale
[00:01:51] to compute the compute the data we gave us emergent capabilities right
[00:01:57] right reasoning to use now in the world of AI agents and agentic systems and the big debate is what is an agent right what is an AI agent I don't like to go into that debate because that's like asking what is consciousness
[00:01:57] is a spectrum
[00:02:02] is a spectrum
[00:02:10] the agenticity and that's a word now agenticity and that's a word now agenticity of of an agent is a spectrum so they're different levels
[00:02:16] I came here and I saw Waymo and to me was pure sorcery
[00:02:22] we don't have that in the UK and they're different levels of self-driving so you can look at the agentic spectrum in that respect
[00:02:28] we have a minimal agent where there's an agentic spectrum in that respect we have a minimal agent where there's an LLM running a loop great then you have a level four is autonomous agent a bunch of agents that have access to
[00:02:34] tools they can do whatever they want they're not prompted in any way or a minimal way but this is how I see things it's a spectrum so what is an AI agent it's a computational entity with awareness of its environment through perception cognitive abilities through
[00:02:55] It's a spectrum. So what is an AI agent? It's a computation entity with awareness of its environment through perception, cognitive abilities through an LLM, and also can take action through tool use.
[00:03:08] But the most important bit is there is some form of memory, short-term or long-term. Memory is important.
[00:03:16] And it's important because we're trying to make our agents reflective, interactive, proactive, and reactive, and autonomous. And every, most of this, if not all, can be solved with memory.
[00:03:30] I work at MongoDB and we're going to make, we're going to connect the dots, don't worry.
[00:03:35] So this is all nice and good. This is what you look at if you double click into one AI agent is, but the most important bit to me is, I'll go a slide, people are taking pictures, sorry.
[00:03:46] All right, let's go. The most important bit is memory.
[00:03:50] And when we talk about memory, the easy way you can think about it is short-term, long-term, but there are other distinct forms, right?
[00:03:56] Conversational, entity memory, knowledge, data store, cache, working memory.
[00:04:01] We're going to be talking about all of that today. So these are the high-level concepts.
[00:04:04] But let me go a little bit metal. Why we're all here today in this conference, it's because of AI, right?
[00:04:14] We're all architects of intelligence. The whole point of AI is to build some form of computation entity that surpasses human intelligence or mimics it.
[00:04:23] Then AGI, we're focused on making that intelligence surpass humans in all tasks we can think of.
[00:04:32] And if you think about the most intelligent humans you know, what determines the intelligence is their ability to recall.
[00:04:39] It's their memory. So if AI or AGI is meant to mimic human intelligence, it's a no-brainer, no pun intended, that we need memory within the agents that we're building today.
[00:04:50] Does anyone disagree? Good. I would have kicked you out.
[00:04:54] Okay, let's go. So humans, you. In your brain right now, you have this. This is not what it looks like, but it's close enough.
[00:05:02] You have different forms of memory, and that's what makes you intelligent. That's what makes you retain some of the information I'm going to be giving you today.
[00:05:08] There's short-term, long-term, working-memory, semantic, episodic, procedural memory.
[00:05:16] In your brain right now, there is something called a cerebellum. I always get the word wrong, but that's where you store most of the routines and skills you can do.
[00:05:24] Can anyone hear your backflip? Really? Wow. You can see my excitement.
[00:05:32] Your -- the information or the knowledge of that backflip is actually stored in that part of your brain.
[00:05:37] So I heard it's 90% confidence, by the way. That is actually -- it is, right? I'm not going to do one, but --
[00:05:45] But it's stored in that part of your brain. Now, you can actually mimic this in agents, and I'm going to show you how.
[00:05:53] But now we're talking about agent memory.
[00:05:56] Agent memory is the mechanisms that we are implementing to actually make sure that states persist in our AI application.
[00:06:08] Our agents are able to accumulate information, turn data into memory, and have it inform the next execution step.
[00:06:15] But the goal is to make them more reliable, believable, and capable.
[00:06:22] Those are the key things.
[00:06:24] And the core topic that we are going to be working on as AI memory engineers is on memory management.
[00:06:33] We are going to be building memory management systems.
[00:06:37] And memory management is a systematic process of organizing all the information that you're putting into the context window.
[00:06:43] Yes, we have a large context window, but that's not for you to stuff all your data in.
[00:06:48] That's for you to pull in the relevant memory and structure them in a way that is effective, that allows for the response to be relevant.
[00:06:58] So these are the core components of memory management, generation, storage, retrieval integration, updating, deletion.
[00:07:05] There's a lie here.
[00:07:06] There's a lie here because you don't delete memories.
[00:07:09] Humans don't delete their memories except it's a traumatic one that you want to forget.
[00:07:12] But we really should be looking at implementing forgetting mechanisms within the memory management systems that we're building.
[00:07:20] You don't want to delete memories.
[00:07:22] And there are different research papers that are looking at how to implement some form of forgetting within agents.
[00:07:27] But the most important bit is retrieval and getting to the MongoDB part.
[00:07:36] Moving around, this is RAG.
[00:07:39] It's very simple, right?
[00:07:40] Because we've been doing it as AI engineers.
[00:07:43] MongoDB is that one database that is called RAG pipelines because it gives you all the retrieval mechanisms.
[00:07:51] RAG is not just vector.
[00:07:52] Vector search is not all you need.
[00:07:54] You need other type of search.
[00:07:56] And we have that with MongoDB, anything you can think of.
[00:07:59] You're going to be hearing a lot about MongoDB in this conference today.
[00:08:03] But this is what RAG is.
[00:08:05] And you level up.
[00:08:06] You go into the world of agentic RAG, right?
[00:08:09] You give the retrieval capability to the agent as a tool.
[00:08:14] And now we can choose when to call on information.
[00:08:17] There's a lot going on.
[00:08:19] I'll send this somehow to you guys.
[00:08:22] Or you can come to me and I'll LinkedIn it to you.
[00:08:25] Add me on LinkedIn and just ask for the slides and I'll send it to you.
[00:08:31] Richmond Alake on LinkedIn.
[00:08:34] This is memory.
[00:08:36] MongoDB is the memory provider for agentic systems.
[00:08:41] And when you understand that we provide the developer, the AI memory engineer, the AI engineer,
[00:08:47] all the features that they need to turn data into memory to make the agents believable, capable, and reliable,
[00:08:55] you begin to understand the importance of having a technology partner like MongoDB on your AI stack.
[00:09:02] So this is the same image but just a bit more focused on all the different memories.
[00:09:09] I'm going to skip through this slide because I go into a bit of detail.
[00:09:12] I'm also going to give you a library.
[00:09:15] I'm working on an open source library.
[00:09:17] I'm ashamed of the name.
[00:09:19] I was trying to be cool when I came up with it.
[00:09:20] It's called MemoRiz.
[00:09:22] You can type that on Google.
[00:09:25] You'll find it.
[00:09:26] But it has all the design patterns of all of this memory that I'm showing you, all these memory types that I will show you as well.
[00:09:33] But there are different forms of memory in AI agents and how we make them work.
[00:09:37] So let's start with Persona.
[00:09:39] Is anyone here from OpenAI?
[00:09:41] Leave.
[00:09:43] Leave.
[00:09:44] I'm joking.
[00:09:45] Well, a couple of months ago, right?
[00:09:48] So they gave ChatGPT a bit of personality, right?
[00:09:52] And they didn't do a good job.
[00:09:55] But they are going in the right direction, which is we are trying to make our systems more believable.
[00:10:02] Right?
[00:10:03] We're trying to make them more human.
[00:10:04] We're trying to make them create relationship with the consumer, with the users of our systems.
[00:10:09] Persona memory helps with that.
[00:10:12] And you can model that in MongoDB.
[00:10:15] Right?
[00:10:16] This is MemoRiz.
[00:10:17] If you spin up the library, it helps you spin up all of this different type of memory types.
[00:10:23] So this is Persona.
[00:10:24] I have a little demo if we have time.
[00:10:27] But this is Persona memory.
[00:10:30] This is what it would look like in MongoDB.
[00:10:32] Then there's Toolbox.
[00:10:34] The guidance from OpenAI is you should only put the schema of maybe 10 to 21 tools in the context window.
[00:10:44] But when you use your database as a toolbox where you're storing the JSON schema of your tools in MongoDB, you can scale.
[00:10:53] Because just before you hit the LLM, you can just get the relevant tool using any form of search.
[00:11:00] So that's Toolbox.
[00:11:02] That's a Toolbox memory.
[00:11:04] And that's what it would look like.
[00:11:05] Right?
[00:11:06] You would store -- this is how you would model it in MongoDB.
[00:11:09] You store the information of your JSON schema.
[00:11:12] Now, you'll begin to understand that MongoDB gives you that flexible data model.
[00:11:18] The document data model is very flexible.
[00:11:20] It can adapt to whatever data -- whatever model you want your data to take, whatever structure.
[00:11:25] And you have all of the retrieval capabilities -- graph, vector, text, geo-specials query -- in one database.
[00:11:33] Conversation memory is a bit obvious, right?
[00:11:35] Back and forth conversation with ChatGPT, with Claude.
[00:11:38] You can store that in your database as well in MongoDB as conversational memory.
[00:11:43] And this is what that would look like.
[00:11:45] Timestamp, timestamp, and you have a conversation ID.
[00:11:48] And you can see something there called recall recency and associate conversation ID.
[00:11:53] And that's my attempt at implementing some memory signals.
[00:11:57] And that goes into the forgetting mechanism that I'm trying to implement in my very famous library, Memories.
[00:12:06] I'm going to go through the next slides a bit quicker because I want to get to the end of this.
[00:12:11] Workflow memory is very important.
[00:12:13] You build your agency system.
[00:12:14] They execute a certain step.
[00:12:16] Step one, step two, step three, it fails.
[00:12:18] But one thing you could do is the failure is experience.
[00:12:21] It's a learning experience.
[00:12:22] You can store that in your database.
[00:12:24] I see you nodding.
[00:12:25] You're like, yeah.
[00:12:26] You can store that in your database.
[00:12:28] And you could then pull that in in the next execution to inform the LLM to not take this step or explore other paths.
[00:12:35] You can store that in MongoDB as well.
[00:12:38] You can model that.
[00:12:39] Because what you have in MongoDB is that memory provider for your agentic system.
[00:12:43] And this is what that looks like when you model it.
[00:12:46] An example of it anyway.
[00:12:48] So we have episodic memory.
[00:12:49] We have long-term memory.
[00:12:50] We have an agent registry.
[00:12:52] You can store the information of your agent as well.
[00:12:54] And this is how I do it.
[00:12:57] You can see the agent has tools, persona, all the good stuff.
[00:13:00] There's entity memory as well.
[00:13:02] So there's different forms of memory.
[00:13:04] And the memory, the memory's library is very experimental and educational.
[00:13:09] But it encapsulates some of the memory and implementation and design patterns that I'm thinking of on an everyday basis.
[00:13:17] That we're thinking of in MongoDB.
[00:13:19] So MongoDB, you probably get the point now.
[00:13:22] The memory provider for agentic systems.
[00:13:25] There are tools out there that focus on memory management.
[00:13:28] MemGPT, Memzero, ZEP.
[00:13:31] They're great tools.
[00:13:32] But after speaking to some of you folks and some of our partners and customers here.
[00:13:38] There is not one way to solve memory.
[00:13:42] And you need a memory provider to build your custom solution.
[00:13:47] To make sure the memory management systems that you're able to implement are effective.
[00:13:51] So we really understand the importance of managing data and managing memory.
[00:13:59] And that's why, earlier this year, we acquired Voyage AI.
[00:14:03] Now they create the best-- no offense, Open AI-- embedding models in the market today.
[00:14:10] We acquired AI embedded models.
[00:14:11] We have text multimodal.
[00:14:14] We have re-rankers.
[00:14:16] And this allows you to really solve the problem or at least reduce AI hallucination within your rag and agentic systems.
[00:14:24] And what we're doing and what we're focused on, the mission for MongoDB, is to make the developer more productive by taking away the considerations and all the concerns around managing different data and all the process of chunking retrieval strategies.
[00:14:41] And we pull that into the database.
[00:14:43] We are redefining the database.
[00:14:45] And that's why, in a few months, we're going to be pulling in Voyage AI, the embedded models, and the re-rankers into MongoDB Atlas.
[00:14:53] And you will not have to be writing chunking strategies for your data.
[00:14:59] I see a lot of people nodding.
[00:15:00] Yeah.
[00:15:01] That's good.
[00:15:02] So MongoDB is a household name, to be honest.
[00:15:05] I watched MongoDB IPO back when I was in university.
[00:15:10] I bought the stocks when I was in university.
[00:15:13] Free.
[00:15:14] Just free.
[00:15:15] I only had about £100.
[00:15:16] I was broke.
[00:15:18] But we are very focused and we take it very seriously, making sure that you guys can build the best AI products, AI features, very quickly in a secure way.
[00:15:29] So MongoDB is built for the change that we are going to experience.
[00:15:33] Now, tomorrow, in the next couple of years.
[00:15:36] I want to end with this.
[00:15:37] You know who these two guys are?
[00:15:40] Damn.
[00:15:41] Okay.
[00:15:42] This is Hobble and Wiesel.
[00:15:43] They won a Nobel Peace Prize in the late 90s.
[00:15:46] But they did some research on the visual cortex of cats.
[00:15:50] The experiment of cats.
[00:15:52] This probably wouldn't fly now, but back in the 50s and 60s, things were a bit more relaxed.
[00:15:57] But they found out that the visual cortex of the brains between cats and humans actually worked by learning different hierarchies of representation.
[00:16:07] So edges, contours and abstract shapes.
[00:16:10] Now, people that are in deep learning would know that this is how a convolutional neural network works.
[00:16:16] And the research that these guys did inspired and informed convolutional neural networks.
[00:16:23] That's face detection, object detection.
[00:16:26] It all comes from neuroscience.
[00:16:29] So we are architects of intelligence.
[00:16:31] But there is a better architect of intelligence.
[00:16:33] It's nature.
[00:16:34] Nature's created our brains.
[00:16:36] It's the most effective form of intelligence.
[00:16:39] And, well, some humans are meat.
[00:16:40] But it's the most effective form of intelligence that we have today.
[00:16:44] And we can look inwards to build this agentic system.
[00:16:47] So, last week Saturday, myself and Tengu is the chief AI scientist at MongoDB, also the founder of Voyage AI.
[00:16:55] We sat with these three guys in the middle, our neuroscientists.
[00:16:58] Kenneth has been exploring human brain and memory for over 20 years.
[00:17:03] And over here is Charles Parker.
[00:17:06] He's the creator of MemGPT, your letter.
[00:17:08] And we are having these conversations.
[00:17:10] And once again, we're mirroring how we're bringing neuroscientists and application developers together to solve and push us on the path of AGI.
[00:17:21] So, that's my talk done.
[00:17:23] Check out Memories.
[00:17:24] And you can come talk to me about memory.
[00:17:26] Add me on LinkedIn if you want this presentation.
[00:17:28] Thank you for your time.