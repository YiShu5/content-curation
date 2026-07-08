---
source_url: "https://www.youtube.com/watch?v=BacJ6sEhqMo"
platform: youtube
uploader: "IBM Technology"
title: "The Four Types of Memory Every AI Agent Needs"
upload_date: "20260526"
duration: 640
fetched_at: "2026-06-26T09:42:42.262008Z"
transcript_source: whisper-local
---

[00:00:00] AI agents have different ways to remember stuff and each serves a different purpose.
[00:00:04] So let's take a look at the four main types of AI agent memory from some pretty foundational stuff
[00:00:12] to what I think are some quite interesting emerging areas.
[00:00:16] And I think it's really, first of all, worth considering how we do it.
[00:00:21] How does human memory actually work?
[00:00:26] Well, we can think of human memory as having, first of all, short-term memory.
[00:00:34] So that's the stuff that is active in the brain right now, like what I'm saying at this very moment.
[00:00:42] That's one type of memory.
[00:00:44] But there's also a type of memory called factual knowledge.
[00:00:48] So this is things like the company security policies that you remember,
[00:00:53] or it could be facts, like Python is an interpreted language.
[00:00:58] Then there are learned skills, like, oh, I don't know, writing backwards on a sheet of glass, for example,
[00:01:09] which I am totally doing here.
[00:01:12] There is absolutely no camera trickery involved.
[00:01:15] And then there is personal experience.
[00:01:20] Like the time I spent three hours debugging a Kubernetes cluster only to discover.
[00:01:25] I was pointing at the wrong cluster the entire time.
[00:01:29] Seriously, that was three hours of my time.
[00:01:33] Anyway, anyway, it turns out that well-designed AI agents,
[00:01:37] they also need these three types of memory, or these four types of memory that I've got here.
[00:01:43] And there's actually a well-known framework for this.
[00:01:47] And it's from a Princeton research team.
[00:01:49] And they gave it the name of Koala.
[00:01:53] That's Cognitive Architectures for Language Agents.
[00:01:56] And Koala maps out four distinct types of memory that agents need.
[00:02:01] So let's walk through each one and see how they actually work in real agentic systems today.
[00:02:09] So type one, that is working memory.
[00:02:14] This is the agent's context window.
[00:02:17] It's everything the agent can see right now.
[00:02:19] The current conversation, if there's any system instructions, they'll be in there.
[00:02:23] If there's any files or data that have been loaded into the prompt, that's where they'll be as well.
[00:02:27] So it's really kind of the scratch pad.
[00:02:29] And the analogy everybody uses for this is this is just like RAM, random access memory.
[00:02:38] It's fast and immediately accessible, but it's volatile.
[00:02:43] When the session ends, it's gone.
[00:02:46] And it's also limited in size.
[00:02:50] I mean, the biggest context windows available today are pretty big.
[00:02:55] I mean, it could be like one million tokens or even more than that.
[00:03:00] But that still has a ceiling.
[00:03:02] And try to stuff too much in there.
[00:03:05] And performance is going to degrade as the model starts losing track of things that are kind of buried in the middle of the context window.
[00:03:13] So every agent has working memory, but then so does every chatbot.
[00:03:17] It's just the context window.
[00:03:19] So the question is, what else do agentic systems need?
[00:03:24] Well, let me add to that list.
[00:03:27] Number two, semantic memory.
[00:03:30] And this is the agent's knowledge base.
[00:03:33] So semantic memory stores facts and rules and conventions, documentation.
[00:03:38] And in the academic literature, this often gets described in terms of things like vector databases or as knowledge graphs.
[00:03:47] And yeah, those are real implementations.
[00:03:49] But in a lot of production agentic systems today, semantic memory is something much simpler than that.
[00:03:58] It's just simply markdown files, .md files.
[00:04:03] So take clawed code as an example of this.
[00:04:07] So it has one of these marked down files.
[00:04:09] It's one is called clawed.md.
[00:04:14] And that sits in the root of a project.
[00:04:16] And that file contains the project architecture, the coding conventions, the build commands, what frameworks to use, and also what not to do.
[00:04:24] And that file gets loaded into the context window at the start of every session.
[00:04:30] So semantic memory tells the agent what it needs to know in general.
[00:04:36] And without it, the agent is, well, it's kind of destined to make the same mistakes over and over again because it has no persistent knowledge to draw from.
[00:04:45] So working memory, semantic memory, what else is there?
[00:04:51] Well, number three, that is procedural memory.
[00:04:54] Now procedural memory is how the agent knows how to do things.
[00:04:59] And there's an open standard for this that's called agent skills.
[00:05:06] And it uses a file format called skill.md.
[00:05:13] Now a skill is just a folder with a markdown file that describes the skill and what that skill does and some step-by-step instructions for how to perform that skill.
[00:05:23] And it could be anything from creating a PowerPoint presentation to running a structured code review.
[00:05:29] So the agent doesn't load all of its skills into the context window or I guess I should say into the working memory at once because that can blow through the working memory budget if there are a lot of defined agent skills.
[00:05:48] So instead the agent just sees a lightweight index, which is just the name and the description of each available skill.
[00:05:56] And then when a task comes in that matches one of these skill descriptions, the agent loads the full instructions.
[00:06:07] And if the skill references other stuff like other files or templates or scripts, well, those only get pulled in when the agent actually needs them during execution.
[00:06:16] So the agent advertises what skills it has, it loads the instructions in when they're needed and then executes with the additional resources pulled in as they're needed as well.
[00:06:27] And all that is quite different from semantic memory where the knowledge is always present in context.
[00:06:35] All right, number four is episodic memory and episodic memory is the agent's record of what happened in past interactions and past decisions and what it learned from them.
[00:06:47] Now, a naive implementation of this is just to save every conversation transcript and then just search through them as you need to.
[00:06:58] And that technically counts as episodic memory, but often that's not very useful.
[00:07:03] So what production systems actually do is a bit more like distillation.
[00:07:10] So as the agent works across sessions, it kind of accumulates notes for itself, but it doesn't save everything.
[00:07:19] It decides what's worth remembering based on whether that information would actually be useful in a future conversation.
[00:07:25] So the result is distilled or compressed experience.
[00:07:30] So things like last time we debugged the auth module, the issue was in the middleware layer.
[00:07:37] That's something that's a lot more useful to remember than just a full transcript of a 45 minute debugging session.
[00:07:44] And this is where memory starts to kind of genuinely look like learning because the agent is going to get better over time.
[00:07:51] But episodic memory is also the hardest type of these to get right because what do you delete?
[00:07:59] When does information become obsolete?
[00:08:02] If a user changes jobs, do you keep the old project memories around or should we forget them?
[00:08:09] Well, humans are actually pretty good at forgetting.
[00:08:12] I do it all the time.
[00:08:14] And as frustrating as that can be, it can be quite useful.
[00:08:17] But for agents, forgetting is an engineering problem.
[00:08:22] So four types of memory, working, semantic, procedural, episodic, but not every agent necessarily needs all four.
[00:08:32] Let me give you an example.
[00:08:34] So let's say we're building a simple reflex agent.
[00:08:37] So that's something like a thermostat or just like a basic routing bot doesn't need all four.
[00:08:43] It might only need access to working memory, the context window, and that's basically it.
[00:08:50] Now, if we take something a little bit more complicated, like a customer support agent,
[00:08:57] but one that's still fairly simple and narrow, like an agent that resets passwords, for example.
[00:09:03] Well, that will still have access to the working memory, of course, but it probably also needs access to procedural memory as well.
[00:09:15] Because it needs to recall the password reset skill, but that might be it.
[00:09:20] Whereas if we take a look at something like a coding agent, it probably needs access to all four.
[00:09:29] So it certainly needs access to the working memory, the context window, but it also needs the product knowledge it would get from semantic and then the skill system from procedural and also the auto memory from episodic that learns across sessions.
[00:09:47] So, so memory is really what separates a chat bot from an agent because a chat bot gives a response, but an agent can give a response shaped by persistent knowledge and accumulated experience.
[00:10:02] It remembers the project, it remembers preferences, and a good memory architecture also remembers the mistakes.
[00:10:11] So we're not destined to repeat them, which honestly would have been wonderful if an agent had told me about that Kubernetes cluster before our three.
[00:10:20] So four types of AI agent memory, which of these are you using in your own agentic workflows?
[00:10:28] So four types of AI agent memory.
[00:10:29] So four types of AI agent memory, which they're using in your own agent memory.
[00:10:30] So three types of AI agent memory, which of course we're using in your own agent memory.
[00:10:31] So three types of AI agent memory, which of course we're using in your own agent memory, which of course we're using in your own agent memory.
[00:10:32] So three types of AI agent memory, which of course we're using in your own agent memory.
[00:10:35] So three types of AI agent memory, which of course we're using in your own agent memory, which of course we're using in your own agent memory.
[00:10:37] So three types of AI agent memory, which of course we're using in your own agent memory.
[00:10:39] So three types of AI agent memory, which of course we're using in your own agent memory, which of course we're using in your own agent memory.