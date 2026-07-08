---
source_url: "https://www.youtube.com/watch?v=7LWTZqksmSg"
platform: youtube
uploader: "AI Jason"
title: "Unlock AI Agent real power?! Long term memory & Self improving"
upload_date: "20240416"
duration: 1330
fetched_at: "2026-06-26T09:53:58.490053Z"
transcript_source: whisper-local
---

[00:00:00] One question that I got asked a lot is can the AI agent get better and better over time to learn
[00:00:05] from its past mistakes and interactions? If the agent you are building is similar to the structure
[00:00:10] that I show here, the answer to this question at default is no, because most of the time the agents
[00:00:15] we are building today is stateless, which means there's no real difference between the agent running
[00:00:19] for the first time versus a hundred times, because it has zero context about what has happened in any
[00:00:25] other session. And this kind of sucks if they had some past conversation with the user where user
[00:00:30] already expressed certain preference, like I don't eat fish. The next time the user talks to this agent,
[00:00:36] they expect the agent to remember the preference that they gave before. And it is really bad experience
[00:00:40] when the agent forgot. Every time we talk to the agent, it is almost feel like start from scratch.
[00:00:45] And that also means it is quite hard for you to train agent on the specific standard procedure for
[00:00:51] different type of tasks. For example, if the user asks agent to give a summary of news,
[00:00:55] and this particular user don't really like a specific data source like CNN. Even though the user give
[00:01:00] very explicit instructions, the next time when it get agent to do similar tasks, it still need to give
[00:01:06] this instruction again and again, because agent won't really learn about this specific SOP. And most importantly,
[00:01:12] after we deploy AI agents in real world, there will be millions of different edge cases. For example,
[00:01:17] I was building a meeting schedule agent who can coordinate time and book meeting for the user. And I was expecting user input to be like,
[00:01:23] how about next Tuesday night and CET. But after we deploy in real world, people were prompting the
[00:01:29] agent in many different ways. And there were so many complex scenarios that we didn't expect before. Like the user can be in
[00:01:35] multiple different time zones across a period of time. If all those iterations are relying on human to come in and make
[00:01:41] adjustments, this human driven agent iterations is almost become a bottleneck for the agent to deliver great performance.
[00:01:47] But what if we can actually get agent to learn from its past interactions, remember users'
[00:01:52] preference, and even update its own system prompt and workflow. That can deliver pretty amazing results.
[00:01:58] Because imagine you can build a marketing or sales agent who can even run A/B tasks by itself with different
[00:02:03] prompt style and based on external or human feedback to autonomously reflect and improve its workflow and prompts. So the ability to have long-term memory and learn from those memories is really powerful.
[00:02:15] It's really powerful. And what's really fascinating is this exactly how human learn as well. So people normally learn new skills and knowledge through this three-step process.
[00:02:24] It first requires us to pay attention to specific things that we want to learn. And after we pay attention to specific data that we receive, then we will go through a process where we will encode this data into our brain and replace this data many, many times through a process called consolidation.
[00:02:39] And at the end of this, this piece of information became a long-term memory that's stored in our brain.
[00:02:44] But there's one caveat. If there's some knowledge in your memory that you haven't really retrieved or used for a very long time, those information will fade away from your long-term knowledge.
[00:02:53] This is where AI agent became really interesting because this won't be a problem for AI agents. The data will always be stored there and they can be retrieved for the agent anytime. And this means the amount of skills the agent can handle can grow exceptionally more than human.
[00:03:06] So instead of just a simple conversation between the user and agent, we can add a new workflow to replicate the process of creating, storing, and retrieving long-term knowledge.
[00:03:16] So you can have a new agent, maybe called knowledge agent, where it will be looking at the conversation between the user and agent and try to decide is there any interesting information that should be stored for later retrieval.
[00:03:27] And then this knowledge agent can summarize and extract specific information stored in a vector database.
[00:03:33] So that the next time when this agent have similar situation, it can try to do a vector search and retrieve relevant information.
[00:03:40] As a simple example, if there's a conversation between the user and agent where the user species said, my name is Jason and I don't really eat fish.
[00:03:47] Apart from the agent answering the question, there could be a knowledge agent behind the scenes look at this conversation and firstly ask, is there any information in the message that is worth saving as knowledge?
[00:03:57] And if yes, it can trigger the second tool or process to abstract learning and save that as a knowledge into our database.
[00:04:04] So you can call it function called create knowledge, where it can pass on the knowledge type to be a diary requirement and detail is no fish.
[00:04:11] So that the next time when the user comes again to say, hey, prepare some meal plan for me the next week, it will be able to retrieve relevant knowledge and then append this knowledge together with the user query.
[00:04:22] Pretty much like a rack.
[00:04:23] So that the real agent will receive a message says the user says, prepare the meal plan for me.
[00:04:28] And here are some past contacts where I don't really eat fish.
[00:04:31] So that this time the agent will be able to respond with this preference in mind.
[00:04:36] And this at high level, how you can build long-term memory for your agent system.
[00:04:40] And this is probably a oversimplified version.
[00:04:42] And behind the scenes, there's a huge amount of optimization that needs to happen to make this production ready.
[00:04:47] For example, it probably take a lot of time to do this process for every single message come in.
[00:04:52] And you don't really want to add too much latency to the user experience so that you can add optimization, have a cheaper and faster model to firstly check.
[00:05:00] Is there anything interesting that works to convert into knowledge?
[00:05:03] If no, let's keep this knowledge process.
[00:05:05] If yes, then go through this process.
[00:05:07] And same thing when the agent receiving new query from user, it can also have a cheaper and faster model like Haiku or Mictro to quickly check.
[00:05:16] Is there any relevant information that require a retrieval this time?
[00:05:20] If yes, then do a proper rack.
[00:05:22] If no, then just answer the question right away.
[00:05:24] And as the user has more and more interactions, this knowledge base will became huge too.
[00:05:29] So you can do additional optimization.
[00:05:30] Like if the knowledge and data is not used much for the past six months, then move that to a code storage.
[00:05:36] So you can reduce the vector database cost.
[00:05:38] And those are just some simple implementations.
[00:05:41] There was one project last year called MIMGPT, which represent for memory GPT.
[00:05:46] So the prompt token of large language model in MIMGPT will be break down into three parts.
[00:05:51] One is the system instruction, which is like system prompts that don't really change.
[00:05:55] The second is working contact is where they will retrieve from the long-term memory, which they call archive storage.
[00:06:01] And they have a queue manager to achieve some sophisticated prioritization about what information to be put into the prompt token.
[00:06:07] For example, in a conversation like this, where the agent asks, how was your day-to-day?
[00:06:12] And the user said, my boyfriend James baked me a birthday cake.
[00:06:16] Then the agent would trigger a function to add in some working contacts, which is birthday is February 7th and boyfriend name is James.
[00:06:24] And in a later conversation where the agent asks, did you do anything else to celebrate your birthday?
[00:06:29] And the user says, yeah, we went to Six Flags.
[00:06:31] Then the agent will try to retrieve past conversation that is related to Six Flags, where the user actually mentioned James,
[00:06:38] which is their boyfriend and I actually first met at Six Flags.
[00:06:42] Then the agent would be able to generate a response that, did you go with James?
[00:06:45] It's so cute how both you met there.
[00:06:47] And if a couple of months later, where the agent was asking how James doing, any special plan today?
[00:06:53] And the user respond, actually James and I broke up.
[00:06:56] Then this agent will start updating its knowledge base, where it update James as ex-boyfriend instead of boyfriend.
[00:07:03] So you can see how this long-term memory really changes experience for the user.
[00:07:07] And this similar setup is also introduced in ChatGPT for some beta user,
[00:07:11] where they also have very simple and basic memory management.
[00:07:14] And this is also much more than just remember user's preference.
[00:07:17] I was using similar method for enhancing the customer support agent.
[00:07:21] So if you ever build a customer support agent, one challenge is that in real world,
[00:07:25] the question user asks can often require knowledge that not exists in the original datasets.
[00:07:30] So what I did was implement a process where if a user asks a question that customer support agent can't answer at the beginning,
[00:07:37] it can escalate to the manager, which is a human.
[00:07:40] And the human can give instruction back to agent and support agent will be able to answer user's questions.
[00:07:46] But behind the scenes, it will also try to extract this new knowledge and update into their own knowledge base.
[00:07:52] So that next time when something similar happens, it can retrieve this knowledge to answer the question.
[00:07:56] And on the other hand, I remember I saw a project last year where they showcased a truly self-evolving agent system.
[00:08:03] It is a project that has short name called CLIN, which represents continuously learning language agent.
[00:08:09] So they put agent into a simulated environment where an item in this world actually follows the real world science and physics.
[00:08:16] And the AI agent in this world can interact with different items.
[00:08:19] Like if you put a fire on the wood, then it will fire up.
[00:08:22] But if you put a pot of water on this firewood, then the water will boil.
[00:08:26] So it's simulation environment for the agent to interact with the world.
[00:08:30] And the goal of this project is they want to build an agent system who can continuously learn about this world by interacting with it.
[00:08:37] Because once you can build such continuously learning agent system, you can just put that into any digital simulation world.
[00:08:43] Like in a totally different game, like a Minecraft or GTA, you can just start learning by interacting with the world.
[00:08:49] And what I found really interesting is the way they set it up.
[00:08:52] So this agent will be given different types of tasks.
[00:08:54] Like it might be given a task called grow and orange.
[00:08:57] Then the agent will start doing this task by bringing it down into different actions they can take, observe results and decide next step.
[00:09:04] And even though in the end for the first try, the agent didn't really complete this task.
[00:09:08] But there are certain progress it made.
[00:09:10] For example, when it went to the kitchen, it actually found the seeds which is necessary to grow an orange.
[00:09:15] Then it will try to reflect in the end of this trial and get a learning that going to the kitchen may be necessary to find the seeds.
[00:09:22] And this information will be fair to agent the next time it tried to complete the same task.
[00:09:26] So this time it will retrieve knowledge that going to the kitchen may be necessary to find the seeds.
[00:09:31] So that it go to the kitchen right away.
[00:09:33] And in the end, in the second trial, it actually completes the task.
[00:09:36] And again, it will try to reflect in general knowledge.
[00:09:38] This time it found not only going to the kitchen may be necessary to find the seeds, but also moving seeds to the pot may be necessary for planting the seeds.
[00:09:46] And with this new knowledge, it can complete the task even faster next time.
[00:09:50] And with similar methods, Adrian will try to complete similar tasks in many different environments for multiple times.
[00:09:56] It will look at all the sessions it has ever done and abstract general learnings that can be adopted across different tasks and different environments.
[00:10:04] For example, it might get learning from different sessions initially using a lighter on the metal pot should be necessary to heat the water in the pot.
[00:10:12] In a different trial, it might find turning on the stove should be necessary to create a heat source.
[00:10:17] And with those two learnings, it will try to generalize a new learning that using a heat source like stove or lighter on the container should be necessary to heat a substance.
[00:10:26] So with this process, you can see that agents are really developing an understanding of how the world works as well as abstract learning that can be used across multiple different tasks and different environments.
[00:10:38] So we have talked a lot about different concepts and methods in terms of creating agent long-term memory.
[00:10:43] I'm going to show you a quick example of how can you create long-term memory into your agents in just 10 minutes.
[00:10:48] But before I dive into this, I think most of us here believe AI going to fundamentally change how we use software, but actually design a good AI native product is really hard.
[00:10:58] One of the platforms that have the best AI native experience, in my opinion, is Gama.
[00:11:03] So Gama is an AI native slide deck and website builder, where they resync the whole workflow of building slide deck and website and bake AI into every part of the journey.
[00:11:12] The part I love the most is how they design experience, where the AI agent and human actually collaborate together.
[00:11:18] Here's a quick example.
[00:11:19] So you can visit gama.app to create account for free.
[00:11:22] And let's say I want to create slide deck about history of large language model.
[00:11:25] I can just click on this create with AI button, select generate, select the presentation, but you can also choose website or documents and type in the history of large language model and click generate outline.
[00:11:37] So instead of getting the AI to creating the whole slide deck autonomously, they introduce a aligning stage where the AI will firstly propose a list of outline of the slide deck.
[00:11:46] And the user can just come here and make change.
[00:11:49] Then you can also set up how text heavy it should be, as well as the image source.
[00:11:53] You can even click on advanced mode, where you will have a lot more control, like voice and tones, as well as additional prompts that you want to add in.
[00:11:59] If everything looks right, I can click on continue, choose a scene.
[00:12:02] Then you start getting to this amazing experience where the AI is actually creating the whole slide deck in front of your life, where it will draft the whole content and also insert image.
[00:12:11] And you can see the content here is not just simple placeholder.
[00:12:14] It actually write content based on the instruction it was given.
[00:12:17] And in just 10 seconds, a beautifully designed slide deck is already created.
[00:12:21] And if I want to make change, I can either do it manually or I can click on this edit with AI button, where they have this co-pilot built in.
[00:12:28] For the slide deck, I want to make change.
[00:12:30] And then say, I want to turn this into a timeline view and add a bit more details.
[00:12:37] Then boom, it became a timeline view that is beautifully designed as well.
[00:12:41] And you might also want to update some images where I can just click on the image and click on edit.
[00:12:45] I can just change the prompt that I want, or I can just search across the web.
[00:12:48] And same for the text as well.
[00:12:50] If the text here is a bit too technical, I can just say, rewrite this slide content for a five-year-old.
[00:12:56] And now all the content is much easier to understand with a lot of analogy.
[00:13:00] So I think Gamma set a really good example of how a AI native experience should look like.
[00:13:05] I definitely recommend you go and check it out.
[00:13:07] You can click on the link below to try out Gamma for free.
[00:13:10] Now let's dive into how can we implement long-term memory into your agents.
[00:13:13] The good thing is it's actually very easy.
[00:13:15] There are many different ways you can implement long-term memory into your agent in less than 10 minutes, including some open source version.
[00:13:22] And I'm going to quickly show you.
[00:13:23] So there are host solutions like Zapp, which you can basically use their API endpoint and SDK to store the long-term memory.
[00:13:30] And they really optimize for speed and memory index to improve the memory retrieval accuracy.
[00:13:35] But there are some costs coming with using Zapp if your volume become bigger and bigger.
[00:13:40] On the other hand, there are video from Deploying AI, which is another AI YouTube channel,
[00:13:44] where he showcased a very detailed example of how to create a memory agent from scratch,
[00:13:48] where the agent can just have his long-term memory about user's preference.
[00:13:52] So I definitely recommend go have a watch if you want to implement from scratch.
[00:13:56] But if you're using framework like AutoGen already,
[00:13:59] this extremely easy way for you to add long-term memory to your agent,
[00:14:03] because they introduced the concept of teachable agents,
[00:14:05] which is a very similar setup to what we have discussed so far.
[00:14:08] Basically, it is a special ability that you can add to any AutoGen agent.
[00:14:12] And there will be a text analyzer agent who can review the conversation, extrapolate knowledge,
[00:14:18] and save to the vector database.
[00:14:20] As I mentioned, the setup is extremely easy.
[00:14:22] I'm going to show you how can you add long-term memory to your AutoGen agent in just five minutes.
[00:14:26] So I will open Visual Studio Code and then add a new file called OAIConfigList.
[00:14:30] Inside, I will just paste in GPT-4 model.
[00:14:33] So if you're using AutoGen and you have a list of different models,
[00:14:36] you can just save your model configuration here to be reused.
[00:14:39] And then I will also create a file called .env.
[00:14:41] This is where we're going to save the environmental variable like OpenAI API keys.
[00:14:46] So I will put OpenAI API key here.
[00:14:48] And also I'm going to add another one called tokenizer parallelism to be false.
[00:14:53] So this is something we're going to use later for those teachable agent to remove some noise in the conversation.
[00:14:58] And after doing this, I will create another file called app.py.
[00:15:01] So first, let's make sure you install the teach bit,
[00:15:04] which is a new ability that you can add to your agent for long-term memory.
[00:15:08] So I'll do pip install teachable.
[00:15:10] And after I finish, I can close this.
[00:15:12] I'll first import a few different libraries we're going to use from AutoGen.
[00:15:16] And one of them is this one called ability.
[00:15:18] And this is a new ability that they add for long-term memory.
[00:15:21] And if you are seeing something similar like mine,
[00:15:23] which is showing some arrow for the package we're importing,
[00:15:26] that means you probably are on the wrong environment.
[00:15:29] And if you're on Mac, you can do Command + Shift + P and do select interpreter
[00:15:33] and choose the right one you're using.
[00:15:35] For me, it will be this user local bin Python 3.
[00:15:38] After you choose the right environment, then this warning will go away.
[00:15:41] And also I'm going to load .env.
[00:15:43] And this will basically read the environment variables that we save in .env file.
[00:15:47] And next, I'm going to load the large language model config
[00:15:50] so that we can define the model for the agent to use.
[00:15:53] And next step is I will create an agent called teachable agent.
[00:15:57] And as you can see here, this is just normal conversable agent.
[00:16:00] Teachability is an ability that you can add to any agent.
[00:16:04] So I'm going to instance a teachability object.
[00:16:06] So t equal to teachability, which is the one that we import from this new auto-gen library.
[00:16:12] And reset db to be false.
[00:16:14] This means every time we will reuse the existing knowledge database that we created before.
[00:16:18] And then this is passed to the knowledge database.
[00:16:21] Then I will try to add this teachability to the teachable agent that we created before.
[00:16:25] And that's pretty much it.
[00:16:26] Now we can add a user proxy agent and start the conversation.
[00:16:30] Okay.
[00:16:31] Looks like we have some error because at default it is running on Docker and we didn't have Docker running.
[00:16:36] So you can either open Docker if you already have the installed,
[00:16:39] or we can go back to .env file and then set autogen use docker equal to false and save this.
[00:16:45] And then let's run again, python app.py.
[00:16:48] Okay, great.
[00:16:49] So you can see the ask for my information and also create a new file called tempt, which inside here,
[00:16:55] it has a chroma vector database created.
[00:16:58] Tempt.
[00:16:59] This is where it will create a vector database for us to store the long-term memory.
[00:17:02] So I will say, Jason, I don't eat fish.
[00:17:06] And as you can see here, a database actually has been created.
[00:17:09] It says, I have noticed that you don't eat fish.
[00:17:11] I will remember this information for future interactions, especially during meal stretches.
[00:17:16] And if I exit and then try to run again, python app.y.
[00:17:20] This time I'm going to ask, give me the mail plan for the next week.
[00:17:23] And you can see, so it generate a mail plan for the whole week.
[00:17:27] And I double check.
[00:17:28] There's no fish involved in this mail plan, which is pretty good.
[00:17:32] And I can even ask why there is no fish.
[00:17:35] So it remember my name.
[00:17:36] I didn't mention my name in this conversation at all.
[00:17:39] And then it says, I didn't include any fish in the mail plan because you previously mentioned that you don't eat fish.
[00:17:45] So here we go.
[00:17:46] We got this agent working in just five minutes that actually remember your preference and can learn from the past interactions.
[00:17:52] And we can learn more about how it works exactly by command and click teachability.
[00:17:57] So you can see this one class called teachability.
[00:17:59] And if you scroll down, there are a few different components.
[00:18:02] And if you command and click memo store, you will see that memo store is a class that they created for the agent to interact with the memory knowledge base, which is a database.
[00:18:11] It packed a few different functions for updating, retrieving, creating the database.
[00:18:16] And at default, it is using the chroma.
[00:18:18] If you want to use different type of DB, you can create a subclass for this store.
[00:18:22] If you scroll down, you can also see that it create a text analyzer agent.
[00:18:26] If we command and click on that, you will see that this text agent is a subclass of conversible agent.
[00:18:32] So the user will give it a text to analyze instructions and please follow the instruction and give the result back.
[00:18:38] So this is pretty much what it does.
[00:18:39] It will be given some instruction and it will try to analyze return the result based on it.
[00:18:44] So I'm going to close this and get back to the teachability.
[00:18:47] And you can see that it also add a new system prompt to the agent that says you've been given a special ability to remember user teachings from prior conversations.
[00:18:57] There's one function called no storage.
[00:18:59] So this is a function that will be triggered at the end of each agent session where we'll pass on every single message line by line to this function to decide if a message contains any interesting information that should be stored into our knowledge database.
[00:19:13] So it will firstly send the message to the text analyzer and ask is there any part of the text that asks agent to perform a task or solve a problem.
[00:19:22] Just return yes or no.
[00:19:23] If the answer is yes, then ask the text analyzer to now briefly copy any advice from the text that may be used for similar but different tasks in future.
[00:19:34] If no advice present, just return no.
[00:19:36] If the response is unknown, which means it actually has advice and it will ask text analyzer again to briefly copy just the task from text.
[00:19:44] Then stop.
[00:19:45] Don't solve it.
[00:19:45] Just include any advice.
[00:19:46] So this will basically extract the actual advice.
[00:19:49] And also try to ask task analyzer to figure out what type of task it is, because in the end, it actually want to generate task advice or problem solution pair in the vector database.
[00:19:59] So this one is about generating the title or name of task itself.
[00:20:04] Then it will save this pair to our database.
[00:20:06] And on the other hand, it will also try to check if there are any facts or information that need to be learned to our database.
[00:20:11] So it will do something very similar but different prompt.
[00:20:15] This time it will ask, does the text contain any information that could be committed to memory?
[00:20:20] Answer just one word, yes or no.
[00:20:21] And if yes, imagine that user forgot about this information in the text.
[00:20:25] How would you ask for this information?
[00:20:27] So this will basically come up with a question that we're going to store in the database.
[00:20:31] And then it will ask the text analyzer to generate the answer itself.
[00:20:34] In the end, save this question, answer pair into our database.
[00:20:37] So this is remote storage and this function is pretty heavy, as you can see, because it called the text analyzer agent multiple times, but it only be wrong once in the end of conversation.
[00:20:48] And this is a function that actually will be called every time to check if there's any information that need to be retrieved and sent to agent as part of context.
[00:20:56] So again, it will send to the text analyzer to check, does this user query ask agent to perform tasks or solve a problem?
[00:21:02] If yes, then it will try to extract the actual task context.
[00:21:06] And also quite interesting, it will ask to come up with a generalized task title because we're going to do a knowledge retrieval.
[00:21:13] So a more generalized task title can lead to more accurate retrieval result.
[00:21:17] And then it will call this retrieve relevant memos and append this results after the user query as part of context.
[00:21:23] So this is basically how you achieve this teachable with long-term memory.
[00:21:27] It has few quite interesting abstraction about how to do this retrieval and how to decide whether this new knowledge to be saved.
[00:21:34] If you're interested, you can even customize this class a little bit based on your own needs.
[00:21:38] For example, as we mentioned before, you can actually do a lot of optimization to reduce the latency and saving the cost.
[00:21:44] But this is how easy you add long-term memory into your agent today.
[00:21:48] As you can see, I definitely think this long-term memory is ability that we should start more agent builders should include into your agent stack.
[00:21:55] And very interesting to see if this actually sparked any new interesting use case.
[00:22:00] I'm going to continue posting interesting AI I'm doing, especially with AI agents.
[00:22:04] So please comment and subscribe if you want to get updates.
[00:22:08] Thank you and I'll see you next time.