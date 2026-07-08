---
source_url: "https://www.youtube.com/watch?v=JTL0yp85FsE"
platform: youtube
uploader: "LangChain"
title: "Memory for agents (conceptual video)"
upload_date: "20241008"
duration: 407
fetched_at: "2026-06-26T09:44:04.884142Z"
transcript_source: whisper-local
---

[00:00:00] Today, I want to talk about memory.
[00:00:03] Memory is one of the most exciting things that we think is happening in the agent world,
[00:00:07] and we're adding a bunch of functionality into LaneGraph to help you build applications
[00:00:11] that have memory.
[00:00:13] This video will be more of a conceptual overview.
[00:00:16] We won't go over any code.
[00:00:18] Rather, we're going to talk through a few memory concepts that we think are critical
[00:00:22] to understanding memory and understanding how we're thinking and tackling memory here
[00:00:26] at LaneChain.
[00:00:28] One of the main things that we think about memory is that it needs to be really application
[00:00:32] specific.
[00:00:33] It needs to be specific to what you're trying to do and what things you might want to remember,
[00:00:37] because that's what's going to make your application better.
[00:00:40] So we're not very bullish on the idea of a general memory abstraction or service.
[00:00:45] Rather, we're going to give you low-level components so that you can implement memory
[00:00:49] for yourself, and we're also going to tell you how we're thinking about it so that hopefully
[00:00:53] that can help you implement the best memory for your application.
[00:00:57] At a high level, we think there are two types of memory.
[00:01:01] One is short-term memory, and this primarily relates to conversation memory.
[00:01:05] If you've used LaneGraph before, then you're probably familiar with the idea of a checkpointer.
[00:01:10] Checkpointers maintain memory for a specific thread.
[00:01:13] A thread is equivalent to a conversation.
[00:01:16] And so this is what we call short-term memory, and checkpointers are the LaneGraph implementation
[00:01:20] for implementing that.
[00:01:22] Long-term memory is a new concept that we've recently started to think about and talk about.
[00:01:28] We've added a new abstraction called store to help with this in LaneGraph.
[00:01:34] So when LaneGraph checkpointers keep the memory within a thread, store is used to keep memory
[00:01:39] across threads.
[00:01:41] So it can be updated with information that it's gleaned from multiple different threads, and
[00:01:46] then can pull that in and can use that when processing a new thread.
[00:01:51] Let's talk about some short-term memory things first, and then we'll dive into more detail
[00:01:55] on long-term memory.
[00:01:59] One of the common techniques we see for short-term memory is just filtering messages.
[00:02:03] As you have more and more back and forth with an AI, the message list will grow in length,
[00:02:08] and so being able to filter them is really important.
[00:02:12] There's some basic filtering stuff, like just keep the last 10 messages, but then there's
[00:02:16] also things based on token counts and based on the types of messages as well.
[00:02:20] Perhaps it's more important to keep the human and AI messages rather than the tools, for example.
[00:02:28] If you're not satisfied with just filtering messages, you can also summarize previous messages
[00:02:33] and pass in a summary.
[00:02:34] This is typically done by calling an LLM and storing that as some attribute on your graph
[00:02:39] state.
[00:02:40] Now, let's talk about long-term memory.
[00:02:43] At a high level, we see two different ways that people are putting long-term memory into
[00:02:47] their application.
[00:02:49] One is what we call in the hot path, and so this is where the application logic itself updates
[00:02:54] memory.
[00:02:56] The other is when it happens in the background, and so here you have the application running,
[00:03:00] and there's a separate process that in the background runs and updates memory, and this
[00:03:04] can happen in real time, or this can happen 30 minutes later, an hour later, whatever
[00:03:09] you decide.
[00:03:11] There's some pros and cons to each of these.
[00:03:13] So, in the hot path, it's very transparent when you're updating memory.
[00:03:17] You can show this to the user so they know what's going on.
[00:03:20] It's also real time, so if they go start a separate conversation right away, they have
[00:03:24] that updated memory.
[00:03:26] The downsides are that because it's in the hot path, it can add some latency, and it also
[00:03:31] makes your application logic a little bit more convoluted because now you have to have your
[00:03:36] core application logic in there as well as the logic for how to update the memory.
[00:03:42] When it happens in the background, the pros and cons are flipped, so there's no latency
[00:03:46] that's added because it's happening in the background in a separate process.
[00:03:50] You can also cleanly separate the logic for your application versus the logic for updating
[00:03:55] memory.
[00:03:56] However, there are some cons.
[00:03:59] Because this is happening in the background, you can't easily surface that to the user.
[00:04:04] And separately, depending on how you set it up, this memory may not be updated when you
[00:04:08] go to start a new conversation.
[00:04:10] In fact, a key part of when you're running memory in the background is figuring out when
[00:04:16] exactly to trigger that background run, and that adds some additional logic that you have
[00:04:20] to think about.
[00:04:24] For long-term memory, it's really important to think about what's the exact shape of the
[00:04:28] memory that you're storing.
[00:04:30] And there's a few different options that we see people doing.
[00:04:33] One common type of memory is instructions.
[00:04:36] These are instructions that can be inserted as part of a system prompt.
[00:04:40] That system prompt then controls how the application performs.
[00:04:44] These instructions are often updated based on user interactions or user feedback.
[00:04:48] So for example, if you have a TweetWriter application, and you go back and forth with the user and
[00:04:53] they refine their tweet and you see that they're removing emojis, you can use an LLM to synthesize
[00:04:59] those interactions and update the part of the system prompt to say don't use emojis.
[00:05:05] A second type of memory that we see people storing is what we call profile.
[00:05:09] Instructions are typically a string, but profiles are now a dictionary of key value pairs.
[00:05:16] So for a chatbot that's concerned with being a companion for a user, you might have things
[00:05:20] like name, age, friends that you want to remember about the user.
[00:05:26] The memory process here would extract that information based on user conversations
[00:05:31] and then update any previous information that had existed to create a new updated profile.
[00:05:37] This profile can then be inserted as part of the system message in future conversations.
[00:05:41] And this can be included when responding to the user.
[00:05:45] A step above this profile is a list of these objects.
[00:05:50] This is useful when you want to remember a list of things, for example, a list of my favorite
[00:05:54] restaurants and you want to remember the location and the name and the type of all of them.
[00:05:58] There's some extra complexity here.
[00:06:01] The LLM now has to prompt to not only add a new item to the list, but also update or delete previous ones.
[00:06:08] And so there's a bit of prompt engineering you need to do here.
[00:06:11] Again, we're really excited about memory at LinkChain.
[00:06:15] We think it's a key part of building personalized and differentiated applications.
[00:06:21] But we also think that there's no silver bullet, single answer fits all solution for memory.
[00:06:27] We think that it has to be custom to your application.
[00:06:30] And so we hope to give you a lot of the tools to help you build application specific memory yourself.
[00:06:36] So I know this just covered the concepts, but I'd encourage you to go check out the how to
[00:06:39] guides and the tutorials that we have out for building this type of personalized memory.
[00:06:45] Thanks for watching and let me know if you have any questions.