---
source_url: "https://www.youtube.com/watch?v=wgDzOSPbTqg"
platform: youtube
uploader: "Dr. Maryam Miradi"
title: "7 Context Engineering Rules for Production AI Agents (Anthropic + LangGraph)"
upload_date: "20251122"
duration: 893
fetched_at: "2026-06-26T09:50:51.107591Z"
transcript_source: whisper-local
---

[00:00:00] This video is on 7 advanced context engineering methods for AI agents.
[00:00:03] I spent 40 plus hours studying the best in the industry and extracted 7 methods that are intuitive
[00:00:09] and simple but advanced and suitable for AI agents in production. Also will tie everything
[00:00:14] together with 8 method laws and will give you actually Python code in Langer. You can find
[00:00:19] all of the references in the description. I'm Mariam, PhD with 20 plus years in AI teaching
[00:00:24] AI agents 2000 in 90 plus countries. Let's go to method 1, pre-road threshold.
[00:00:29] To explain the route, we can ask ourselves, what will you engineer context in the first
[00:00:34] place? We know that agents need useful context to create desired output. The context window
[00:00:38] is nowadays very large, like 1 million tokens. But after using only 10% of it, basically agents
[00:00:46] start to become poisoned, distracted, confused, or clashed. So context capacity is not the same
[00:00:53] as context quality. So how about that 10%? Company Chroma is going to explain that 10% to us. It says
[00:01:03] that model fails not cleanly at their limits, but it degrades progressively. It means that at 128k
[00:01:10] they are in the safe zone, at 200k they have like quality degradation, 500k severe performance drops,
[00:01:18] and 1 million K is technically the drop or the limit. So what are the symptoms? Are that repetition, you
[00:01:27] start to get a slower response, you get some wrong tools, they call like invalid functions, they lost the
[00:01:34] instruction, they forget what you have just said. And what you can do is to avoid actually that rot. What are the
[00:01:43] errors? So the solution to that is it's basically very simple. You monitor your context window and the
[00:01:48] context size continuously. As soon as you hit that 128k to 200k, you trigger reduction. Okay, you can say
[00:01:57] reduction, should I summarize it? It's not just the same. I will explain that in just a few minutes, but let's
[00:02:04] first identify another problem. Imagine you just detect the rot zone at 200k, you're going to take care of it. But your
[00:02:12] agency still has like 20 more steps to execute and just need those information. So here is the critical
[00:02:20] question. If it cannot stay in the context, where does it go? Andrei Karpathy says treat your context
[00:02:27] window as a computer. Same as that CPU has fast access, RAM has like a little bit of a slower access,
[00:02:32] and then you've got disk which is the slowest access. Your agency needs also that kind of hierarchy. So keep
[00:02:39] only what you need right now for the current decision, everything else offloaded. So our method 2 is
[00:02:45] basically context offloading. So you can do context offloading by storing everything heavy in files,
[00:02:52] like logs, search results, like scraped HTML, a PDF extraction, large JSON responses, and then return
[00:03:01] only. The file path identifiers and clean summaries structure the schemas. And you will have like two
[00:03:08] levels of context offloading. Level one is a short term kind of scratchpad. You write to scratchpad and
[00:03:15] then you read it from it and read the scratchpad. If it's empty, write initial ones. Otherwise, we just
[00:03:21] write the key findings to scratchpad. Don't keep raw search results in the context. You just keep
[00:03:27] references to nodes and final answers are basically synthesis of scratchpad nodes. And if I want to show
[00:03:35] you the code, this is actually how simple we can just do it in blockchain. So use the scratchpad like a
[00:03:43] message state, explain it, then write the tool. As you can see, you can just define the tools. Write to scratchpad
[00:03:51] tool and then just save it. You just give the description and then read will be again also same way.
[00:03:59] And then we have search tools or other tools and then you can add that tool. So read from scratchpad and
[00:04:06] write from scratchpad to your tools. It is as simple as that. And the second one is just do a long-term memory
[00:04:13] store, which is just write it to your Postgres. It's really easy. And if you look at the code,
[00:04:18] you can go ahead and pick up the vector stores, the PG to Postgres embedding and just write it
[00:04:26] from a document to that Postgres. It is pretty straight. And there is these brilliant things that
[00:04:32] many stores, they use kind of plan to do empty. And for every complex text, they just continuously rewrite
[00:04:40] that to-do. And then in this case, memory lives in your system and not in your LLM or AI agent context.
[00:04:49] So you may ask, what about tools themselves? Don't 100 tools definition bloat context? Okay, just give it
[00:04:55] fewer tools. But then we cannot solve a complicated problem. So we have this tool paradox. You know,
[00:05:03] you need more capability, but too many tools cause confusion. This is our method three. Just before
[00:05:10] that, I have made one of my paid course modules free. It's a link in the description. I will give you
[00:05:19] also a free guide. It's the first link. And if you want to dive into my paid course, it's also in the
[00:05:26] description. This is the five in one AI agent mastery. Okay, what are the three simple layers? So the core
[00:05:35] functions are layer one. Think of read file, write file, search browsers. So here is the trick. By just
[00:05:41] using these tools, you can do anything. For other things that you need, you go to pre-installed tools.
[00:05:48] Those are basically all your other tools. So if you've got a video converter or an image processor or speech
[00:05:56] recognition or even your MCP tools, you just install here unlimited tools, but they are just not in your
[00:06:05] list of tools in your permanent tools. And finally, we have the layer of power. Just write code. So you just
[00:06:13] write custom code for anything you want. So your agent will call any API, use any Python library,
[00:06:19] do heavy computation process, large databases at this stage. It just gives you that a small interface,
[00:06:27] but infinite possibility. But now you have another problem. Even with a smart tool design,
[00:06:33] tool outputs still add thousands of tokens to your context. So for example, a single web search,
[00:06:41] it can be like 3000 tokens. And then you have fire read another 5000. And then after 22 calls,
[00:06:50] you are basically drowning in outputs. So how do you actually reduce this without losing critical
[00:06:56] information? It is with compaction. Do you remember that I was talking about compaction and reduction
[00:07:02] earlier? And I said, I will talk about it later. This is actually our method four, which will show you how
[00:07:08] how to compact our context. So instead of having that full raw contact, we want actually that reference
[00:07:17] contact, the compact contact. So what we do in the compaction, and that's why it's reversible,
[00:07:22] you strip the reconstructable information, but keep identifiers. So universal identifiers are file
[00:07:29] so that you want to do that. So the file operation gives file. So the browser operation gives URL and search
[00:07:33] operation gives query strings and API calls will give you request IDs. Context summarization is different.
[00:07:40] You compress information in shorter form, so your details are lost. And what is the golden rule for
[00:07:47] when to do summarization is that when you do summarize, always summarize from the full version. Never compact
[00:07:53] compact version. Just always from a structured schema, not free format prompts. So let me show you do
[00:08:01] compaction, compaction, compaction, and a little bit of summarization. And then you go compaction and
[00:08:08] compaction. And the last one you can see is just kind of hanging there. Because a pro tip is keep the last few
[00:08:17] tools unsummarized. And this maintains actually the style of what you were writing. So it provides fresh
[00:08:23] view shot example. It also prevents the model from imitating your compact format. So coding it in
[00:08:30] LangChain is straightforward. What you can see is that you give the guidelines the same as I explained in
[00:08:36] the prompt. Add that node to the graph, which is a tool node with summarization. It's as simple as that.
[00:08:42] If you have a workflow that needs 50 tool calls, this is still going to bloat your context, right?
[00:08:50] That's where the method number five is coming. Another intuitive but very effective way to decrease
[00:08:56] your context window. So if you have a deep search, your agent is going to just do some research, get
[00:09:04] some links, then extract the key points, compare the resources, synthesize findings, and then you've got a
[00:09:10] lot of tokens at hand. And you can do that five times in your 140,000 tokens, which is you are in the rot
[00:09:17] zone. But if you want to use the agent as tool, which is called SOP agent as well, what you do is you
[00:09:24] use a helper agent. So each time you just create a new helper, fresh empty content, do the 50 tool costs you
[00:09:33] need. Return the summary and throw away the entire helper agent. Basically, you create another
[00:09:39] new helper the next time you need actually that tool. And in this way, the SOP agent will return
[00:09:47] 500 tokens. So SOP agent context is thrown away because it's basically a temporary workspace.
[00:09:54] So if you're wondering what if a helper agent needs 200 tokens, then I would say use this decision tree.
[00:10:00] Between 5 to 20 tools, just use your main agent. 20 to 50 tools, use a SOP agent.
[00:10:07] And if you have more than that, basically do context uploading, as we have said, because it's
[00:10:11] just too much to do. And the question is, if SOP agents are so powerful, why not use them for everything?
[00:10:19] But we have a problem with the SOP agents, because they have a trap, which is called isolation. Because in
[00:10:24] isolation, you increase the capacity, but then you lose coordination and cooperation. Cognition AI says,
[00:10:32] don't build a multi-agent when you need actually this coherence. You need to create a decision all
[00:10:39] together. So what they say is, if you have this kind of tasks, the agent breaks down to tasks, and you get it and
[00:10:48] combine it is almost surely unreliable. It's still unreliable when you do the SOP agents and they do
[00:10:54] the SOP tasks and they combine it. What is working is when you have supervision, one agent just kind of
[00:11:01] give two SOP agents the SOP tasks and they can just do it separately. I will give it back to the
[00:11:09] agent and that agent will combine it. This is what we call context quarantine. In context quarantine,
[00:11:16] you just have a supervisor agent. You synthesize everything. One agent does all the decision
[00:11:21] making. So when to use it, use multi-agent for information gathering. I use this supervisor system
[00:11:27] when you need coherence. How do you code it? Graph for both of them. So you have the math expert and the
[00:11:33] research expert and it will be combined by the supervisor. But if any agent may not help us see
[00:11:41] different tools at once, it struggles to pick the right one. And we can solve that actually with our
[00:11:47] method number seven, which is RAC for tools. It's extremely intuitive and simple, but we are going to
[00:11:54] use our vector database, our RAC method to solve this problem. If you don't know about RAC, I have a video
[00:12:01] about RAC on my channel. You just pre-process. You just create a registry of your tools. For each tool,
[00:12:10] you write a description, convert the description to embedding, and then store it in a searchable
[00:12:14] database. Then your user can ask something like, what's the better in Tokyo? And then you go ahead and
[00:12:23] basically find all the tools by finding the similarities in your embedding. The similarity gives you
[00:12:30] actually five top tools, for example, and in this case would get weather, get forecast to get temperature,
[00:12:37] get humidity and weather alerts. Now agent basically can see only five tools. It will be way easier to get
[00:12:45] the right tools. It will not be confused by 100 other tools, which makes it very easy for your agent to
[00:12:51] choose. If we want to code it, you will have just a tool registry and you will have tool IDs and the
[00:12:59] description. As I said, you can just use the store base and space store in a line graph and you finally
[00:13:07] can have something like query that and we'll search for that tool for the top five. This works actually with
[00:13:13] layer action space, sub-agents, or also agent as tools, all of the previous methods that we mentioned.
[00:13:20] It's relevant when you have a lot of similar tools. If you just have limited tools, it doesn't make sense to
[00:13:26] use RAP. I promised a number of laws and meta laws. Number one, offload everything token heavy. Number two,
[00:13:33] compact first, summarize last. Number three, set alerts on 128k. Split by task time, not job title. Three layer
[00:13:42] design, as I just mentioned. You go to basic utility and code and then structure beats free format. You know that.
[00:13:50] Simpler systems always win. And at the end, the law number eight is monitored continuously. And if you
[00:13:56] want to have also as a checklist, this is actually the context engineering checklist that you can also
[00:14:01] screenshot and always use. If you want to keep just one law that would be like the unifying principle,
[00:14:09] that would be the simpler system always win. Because context engineering should make the
[00:14:14] AI agent job simpler, not harder. So I hope that all of these methods could just make the desired output that
[00:14:21] you want for your AI agent. It makes it for my 300 plus agents that I have built. Check out my free
[00:14:28] module and also the course. All the methods that I mentioned are brilliant but simple. You can only get better at
[00:14:37] them and apply them if you build AI agents. And if you want to build AI agents like hands-on and real-world AI
[00:14:45] agents, watch this next video where I build AI cybersecurity end-to-end in just 12 minutes. See you there.