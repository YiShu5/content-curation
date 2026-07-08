---
source_url: "https://www.youtube.com/watch?v=ff3j4olCUig"
platform: youtube
uploader: "DeepLearningAI"
title: "Build Your Own App In Just 30 Minutes! Full Course with Andrew Ng"
upload_date: "20260602"
duration: 1557
fetched_at: "2026-06-21T11:17:37.621592Z"
transcript_source: bibigpt
---

[00:00:02] Hi, I'm Andrew Ng.
[00:00:03] I want to show you how to build fun
[00:00:05] useful software using AI, regardless of your background or training.
[00:00:09] If you're intrigued about using AI or vibe coding to build cool software
[00:00:15] but aren't sure where to start, this course is for you.
[00:00:19] Let me show you a funny birthday card app that you learn to build in minutes using ChatGPT
[00:00:25] Gemini, or any other similar AI system
[00:00:27] even if you've never written a line of code before.
[00:00:31] This birthday card app is a computer program called a web application
[00:00:36] which means that it runs right in your web browser.
[00:00:38] The app takes whatever you type in and creates a custom card for you on this font.
[00:00:43] In the next lesson, you build your own version by describing what you want the AI to do
[00:00:47] and the AI will write all the code for you.
[00:00:50] To use the app, you enter a name
[00:00:51] an age, a hobby, penguin fashion design
[00:00:54] an adjective, suspiciously fun, and a plural noun
[00:00:58] lucky socks.
[00:00:59] Then hit generate card.
[00:01:01] And it says, "Karen, against all odds
[00:01:03] you've turned 27.
[00:01:05] Your devotion to penguin fashion design is the stuff of legends and your suspiciously fun nature
[00:01:09] iconic.
[00:01:09] Statistically speaking, most people like you.
[00:01:12] " I think that's pretty funny.
[00:01:13] Or if I don't feel like filling in all of these words myself
[00:01:16] I can hit, "I'm feeling lucky," and have this fill in automatically and then generate a different card.
[00:01:22] And there's another birthday card.
[00:01:24] And you get a different funny story or a different funny birthday card this time.
[00:01:28] Notice the app stores all the cards we've generated.
[00:01:31] If I click copy on any of them
[00:01:33] the birthday message goes to my clipboard so I can paste the message into an email or text and send it as a birthday card.
[00:01:39] You might be excited to jump right in and start building out your own idea.
[00:01:43] And if so, that's great.
[00:01:44] And before doing that, spending a little time building this birthday card app yourself will help a lot.
[00:01:50] Doing so will give you a better feel for how to talk to the AI so you actually get the results you want.
[00:01:55] And this practice process will build your intuition for how to shape what the AI actually creates
[00:02:01] and you get a better sense of how even small tweaks can lead to very different outcomes.
[00:02:06] Once these set of concepts become a bit more familiar to you
[00:02:11] building your own ideas become faster and easier because you have a better sense of how to steer the process.
[00:02:18] So an app like this might seem complicated to build.
[00:02:21] But in the next video, I'll show you how you can build something like this in minutes.
[00:02:25] Let's go on to the next video.
[00:02:27] The easiest way to create software in the AI era is no longer to type out code yourself.
[00:02:33] Instead, you should tell AI to do it for you.
[00:02:37] Telling AI what to do is called prompting.
[00:02:40] When given precise instructions, AI can do a lot of things for you.
[00:02:46] What I want to do in this video is share with you some best practices for prompting AI to create software for you.
[00:02:53] First, we'll walk through an example together.
[00:02:55] Then you try yourself, using any AI chat system
[00:02:58] like ChatGPT, Gemini, Claude, or the one built right into this website.
[00:03:04] To use any of these AI systems, you give it a prompt or set of instructions like this to tell it to create a web page to help me write birthday cards.
[00:03:13] And when I give a person's name, age
[00:03:15] and hobby, it should give me back a funny message.
[00:03:17] And if you do this, it might actually generate an app that looks like this
[00:03:21] which is a good start.
[00:03:22] You can enter the name, age, and hobby
[00:03:25] and it generates, you know, an okay message like this.
[00:03:27] But if you aren't satisfied with this, you might then continue the conversation with AI and say
[00:03:33] "Make it prettier by adding a festive title and colors.
[00:03:35] " And this will give you a second version of the app that now looks a bit better.
[00:03:40] And if you're still unsatisfied, you might say
[00:03:42] "Display the color on the right side.
[00:03:44] Make it look like the inside of a birthday card
[00:03:45] " and get back a third version.
[00:03:47] And if you have ideas to make it even better
[00:03:50] you could give it more instructions, like add a fun title at the top and so on.
[00:03:55] This is how I actually work in practice when using AI to write code for me.
[00:03:59] I'll often start off with a basic set of instructions and see what I get
[00:04:03] and then repeatedly tell the AI how I want to improve it.
[00:04:07] It turns out that when you're building software applications
[00:04:10] there's a number of basic building blocks you might end up including in the prompt.
[00:04:14] One thing I often include is the goal.
[00:04:16] So here the goal is to create a web page to help me write birthday cards.
[00:04:19] Another thing you might include is to specify what is the input.
[00:04:23] That is, what does the user have to tell the software?
[00:04:26] This is us telling the software what we want it to output
[00:04:31] as well as the layout.
[00:04:33] So what's on the left, what's on the right
[00:04:34] how do you arrange the different parts of this app.
[00:04:38] And lastly, any special instructions for additional features you want it to include.
[00:04:43] There are many ways to write good prompts
[00:04:45] but as you start your journey of telling AI to build software for you
[00:04:48] I encourage you to consider these five building blocks as common pieces that you might choose to include in the prompt.
[00:04:56] That is the goal, namely what you want to create
[00:04:59] what input the user will provide, what is the layout of the software app
[00:05:04] what special features you want it to have
[00:05:06] as well as what you want the software to output.
[00:05:09] In a previous slide, we went through a back and forth process of me incrementally
[00:05:14] in four steps, adding to the instructions I gave the AI to tell it what I want it to do.
[00:05:19] But if you already know in advance more or less what you want it to build
[00:05:23] you can also specify all of the building blocks in a single prompt.
[00:05:27] For example, if I already knew the specification I want for the software
[00:05:31] I could write a single much longer prompt like this to create a web page to help me write birthday cards
[00:05:37] where you give a person's name, age
[00:05:40] and hobby, give a refined message, use festive title and colors
[00:05:42] and so on.
[00:05:43] And in this example, I've taken all five building blocks and written them all into a single
[00:05:48] much longer prompt.
[00:05:50] So instead of building things step by step
[00:05:53] like you saw in the last video, you can also give it all the instructions in a single longer prompt
[00:05:58] and that might give you a better.
[00:06:00] ..
[00:06:00] ..
[00:06:01] . first version of your app, which you can then further refine
[00:06:03] if it's still not quite what you want.
[00:06:06] Now, whether you're writing a single long prompt all at once
[00:06:09] or whether you're giving it one building block incrementally
[00:06:12] one piece at a time, I will often start by telling the AI what is my goal.
[00:06:17] And then, with the remaining building blocks
[00:06:18] there are multiple ways to put them together.
[00:06:21] And you don't have to use all the building blocks every time
[00:06:24] and the order is also not very important.
[00:06:26] Start with the goal, and tell it the input/output layout
[00:06:29] and maybe not list any special features.
[00:06:31] Or, you might put the building blocks together this way
[00:06:33] and it could work fine.
[00:06:34] Or you might list out the building blocks in a different order.
[00:06:37] And the AI is usually pretty good at understanding these different rearrangements of the building blocks.
[00:06:43] And if you're feeling like, boy, this is a lot
[00:06:46] I would say, don't worry about it.
[00:06:47] If you just tell the AI whatever's on your mind
[00:06:50] even if it's partial and imperfect, you can then work and go back and forth with the AI a few times to hone it towards something that you want
[00:06:58] together with the AI.
[00:06:59] One of the skills you hone over time is the ability to give AI more specific instructions
[00:07:06] because it turns out that the results you get may vary
[00:07:09] even if you give fairly specific prompts.
[00:07:12] So here's a long detailed prompt that you saw just now
[00:07:14] specifying all of the five building blocks.
[00:07:17] And if you give these same instructions to the same AI system multiple times
[00:07:22] maybe one time it will give an app that looks like this
[00:07:24] which is pretty nice.
[00:07:25] And maybe a second time it will build something like that
[00:07:27] and the third time it will build something like that.
[00:07:29] And all of these look pretty good, because you can see there's some variation among them.
[00:07:32] In contrast, if someone were to give a much less specific prompt
[00:07:36] a much less clear prompt, so it's a very short prompt that just says
[00:07:39] "Create a webpage, tell me to write birthday cards.
[00:07:41] " Because this is a relatively vague prompt
[00:07:43] the results you get if you run this multiple times through an AI system
[00:07:47] maybe once you get this, a second time you get this
[00:07:49] which looks totally different, with different fields
[00:07:52] and a third time you would get this
[00:07:54] which, again, looks totally different than the first two times.
[00:07:57] The more specific and the more precise the prompts you write
[00:08:01] the more predictable will be the results.
[00:08:04] But even then, there'll be a little bit of variability.
[00:08:06] So if you get results that are a little bit different than what I show in this video
[00:08:10] don't worry about it.
[00:08:11] That's the normal cause of how AI systems behave.
[00:08:14] But if it surprises you with something you really don't like
[00:08:16] that's okay too.
[00:08:17] Just give it additional instructions to steer or to move the AI closer to whatever you do want it to do.
[00:08:23] The best way to learn this is to put your hands on your keyboard and to try using the AI yourself.
[00:08:28] Let me show you what it will look like.
[00:08:30] What I'd like you to do after this video is go to this section on the website and go through this exercise yourself.
[00:08:36] So, there are instructions here that you can read later
[00:08:39] but this is an AI system similar to ChatGPT and Gemini and Claude and so on.
[00:08:45] And, um, I'm going to select and then copy and paste the first prompt here
[00:08:52] where it tells the AI to create a webpage
[00:08:54] tell me to write birthday cards, and so on.
[00:08:56] And I'm gonna hit this to send it to the AI.
[00:08:59] So here, it will think for a little bit and then it will generate HTML page that it can then download and run.
[00:09:07] Notice while it's still running that this download button here is grayed out
[00:09:10] so I can't actually click on it yet.
[00:09:12] But the AI system will take just a little bit of time to write something called a HTML page.
[00:09:19] This is what webpages are made of.
[00:09:21] That will be this birthday card generator.
[00:09:24] Now that the AI has finished generating all of this HTML code
[00:09:29] I can click this download button, and here I'm running Chrome on a Mac.
[00:09:34] I'll show you later what to do if you're on a different machine.
[00:09:36] And, um, I can go to this downloaded menu here and open up file.
[00:09:41] HTML.
[00:09:42] And this has created a little birthday card generator.
[00:09:46] So here's Karen, 27, and I can create a simple birthday message.
[00:09:53] Not bad.
[00:09:54] And notice that this is actually a piece of code written in HTML that is running on your computer right now
[00:10:04] if you were to do this yourself.
[00:10:06] The code is in this file called file.
[00:10:09] HTML, and it's actually saved to my computer right now.
[00:10:13] And if you do this, it will be saved to your computer.
[00:10:15] Now, if you want to improve the code
[00:10:19] you can then prompt it, add a festive title and colors
[00:10:22] and then it updates the code.
[00:10:24] Same as before, I have to wait until it's finished
[00:10:26] uh, writing the code before I can download it.
[00:10:29] And now I can download it, and same as before
[00:10:32] open it.
[00:10:33] Oh, wow, now it looks much more festive.
[00:10:36] And so, what I'd like you to do is try it out for yourself.
[00:10:40] You can, you know, add this third prompt
[00:10:42] run it, add this fourth prompt, or try some other prompt if you feel so inclined.
[00:10:47] But it's also fine to use just these four prompts
[00:10:50] one at a time, and see what birthday card generator you get out of this process.
[00:10:55] Even though I'm showing you this process on a website
[00:10:58] these same prompts should give you similar results on OpenAI's ChatGPT
[00:11:01] Google's Gemini, Anthropic's Claude, or any other popular AI system.
[00:11:06] What you're learning isn't tied to any one platform
[00:11:08] and these skills apply to any AI system you choose to use.
[00:11:11] When you click the download button, your web browser will usually download the file.
[00:11:17] HTML or whatever say, file the AI generated with the code to your downloads folder.
[00:11:24] So these videos show you how you can navigate on either Windows or Mac to the downloads folder to find that file.
[00:11:33] And then if you double-click on it, it should open up in a web browser and let you see what the code you just generated looks like when it runs in your web browser.
[00:11:44] Please try this out.
[00:11:45] After you try out this process and generate a web app
[00:11:49] one mindset that I hope you have is that.
[00:11:52] ..
[00:11:53] Getting feedback is often a great step in building software applications.
[00:11:58] Whenever I write software, I'll often show it to friends
[00:12:01] show it to family, or sometimes respectfully approach strangers and ask if they're willing to look at whatever I'm building and see if they can let me know what they think.
[00:12:09] Or email it to a colleague or post it online forum to get feedback
[00:12:13] because I find that when people look at it
[00:12:16] they'll often have suggestions for how to make it even better.
[00:12:19] Or sometimes if you get a laugh out of a friend by showing them something funny
[00:12:24] I find that really encouraging as well and gives me the energy to keep on going.
[00:12:28] So what I'd like you to do now is go onto the next item in this course and try it out yourself.
[00:12:34] Get AI to generate some code for you and download the HTML file and see what results you get.
[00:12:40] If you feel so moved, I hope you also show it to a friend or show it to someone else to get their feedback.
[00:12:47] After that, please come back to the next video where we'll keep on working on the app and we'll look at how you can add even more features to the birthday card app to make it even more fun and interesting.
[00:12:58] Now that you've built a basic birthday card app
[00:13:11] let's see how you can add additional features to it so it can do additional things or be more fun.
[00:13:16] If you showed your app to anyone else
[00:13:19] maybe they'll have ideas for things to add too.
[00:13:22] And I also wanna show you what to do if there's something wrong with whatever the AI had built for you
[00:13:28] such as if it doesn't work the way you're expecting.
[00:13:31] As before, the primary way we will tell AI what features to add is by prompting.
[00:13:39] To understand why it's important to be specific in the way you prompt
[00:13:42] let me pick an analogy to ordering food.
[00:13:45] If you go to a food truck and say
[00:13:49] "Give me a sandwich," who knows what type of sandwich they will give you if that's all you say.
[00:13:53] But if you say something more specific like
[00:13:55] "I would like a vegetarian sandwich," then that narrows down the range of what you may get back.
[00:14:00] Or if you say, "I'd like a vegetarian sandwich with hummus and cheese on multigrain bread
[00:14:03] " then that specific instruction really means what you get back becomes much more predictable.
[00:14:09] Or if you say, "I'd like such and such vegetarian sandwich and add a drink and make it to go please
[00:14:14] " then it becomes much more predictable what the food truck will give you back.
[00:14:20] At a food truck, by being specific with what you ask for
[00:14:23] you're more likely to get what you want
[00:14:24] and so too it is with prompting AI.
[00:14:27] By writing more specific prompts, you're more likely to get exactly what you want.
[00:14:31] Ooh, ah, this is exactly what I wanted.
[00:14:36] As you gain skills in getting AI to write for you
[00:14:40] you get better at being more specific with the instructions you give to AI
[00:14:45] and this will give you better results.
[00:14:47] I previously built an app using a prompt like this
[00:14:50] either on one go or by going back and forth a few times.
[00:14:53] What I'd like to do now is add a few new features and modify some existing ones.
[00:14:58] For example, instead of having three input fields like we have so far
[00:15:03] name, age, and hobby, maybe you want to gather five pieces of information
[00:15:08] so have five input fields that users can input so you can create more personalized messages.
[00:15:13] Or maybe you want a "I'm feeling lucky" button that automatically fills out all the fields for you so you don't have to type everything in each time you use the app.
[00:15:21] Or you could also update the look and feel
[00:15:23] say change the title or add a button that copies the message to your clipboard so you can easily email it to friends
[00:15:30] or even redesign the entire color scheme to better match your style.
[00:15:34] After having built a basic app, you can then make the app yours by deciding what features you want to add.
[00:15:41] So you might continue the chat conversation by telling the AI to make it have five clearly labeled inputs
[00:15:48] name, age, hobby, an adjective, and a plural noun
[00:15:51] and it'll update the app to look like this.
[00:15:54] And notice that I'm writing very specific instructions here.
[00:15:58] I'm not just saying make it have five fields
[00:15:59] I'm telling it what are the five fields I want it to have.
[00:16:02] Or if I add an "I'm feeling lucky" button
[00:16:06] again, I try to be specific in telling it what I want the "I'm feeling lucky" button to do.
[00:16:10] I want it to automatically fill in the blanks with random words
[00:16:13] and I want the predefined word choices to be funny.
[00:16:16] And here, I'm actually adding two features at the same time.
[00:16:20] I might update the titles and subtitles and also add a button to copy the codes to clipboard
[00:16:25] so this is actually two of the bullets from the previous slide that I'm adding at the same time.
[00:16:29] And, um, I actually like the color blue
[00:16:31] so let's make the color theme blue.
[00:16:33] Feel free to try out these prompts yourself
[00:16:35] or even better, pick a different color theme or tell it to implement any other idea that you have.
[00:16:42] If you like pink like my daughter does
[00:16:44] or green like my son does, tell it to use a pink or green color theme instead
[00:16:48] or make some other changes depending on what you feel like doing.
[00:16:51] And if you ever change your mind, you can do that too.
[00:16:54] So after I've made the color theme blue
[00:16:56] if I decide that I don't want it blue after all
[00:16:59] I actually want it to be purple, you can write a prompt like that and the AI will obediently change it to purple.
[00:17:04] Now, a lot of the time, AI is pretty good at giving you exactly what you ask it to do.
[00:17:12] But sometimes, there's a chance to generate an HTML page that doesn't work.
[00:17:17] In software, we call this a bug
[00:17:19] when there's something that doesn't quite work the way it's supposed to.
[00:17:22] Here's actually a broken version of an app that AI generated for me earlier
[00:17:28] where I've typed in all of these fields
[00:17:31] but if I click generate card, nothing happens.
[00:17:33] So that's kind of weird.
[00:17:35] You know, I'm clicking my mouse, but it's not actually generating a card.
[00:17:38] It turns out "I'm feeling lucky" works, but again
[00:17:40] generate card doesn't create any card for me.
[00:17:43] If that happens, what I'd encourage you to do is to clearly tell the AI what happens.
[00:17:49] So here, type, "Nothing happens when I click on the generate card button.
[00:17:52] Can you fix it for me?
[00:17:54] " And if you do that, the AI is usually pretty good at finding at least basic bugs and fixing whatever is wrong.
[00:18:03] When you do this, sometimes the AI will write some technical explanations of what went wrong.
[00:18:08] So here it says, "JavaScript was attached to the button's click event.
[00:18:11] " Boy, that's a lot of technical terminology.
[00:18:13] I would say for now, just don't worry about what the AI is saying here.
[00:18:16] You don't need to understand these technical details.
[00:18:18] If you're really curious, you can actually ask the AI
[00:18:20] "What do these terms mean?
[00:18:21] " But you don't have to do that.
[00:18:23] Let the AI do its thinking, say whatever you want it's about the technology
[00:18:27] and then focus on downloading the new HTML file to see if that works.
[00:18:31] I hope you all started a basic birthday card app
[00:18:34] and either try building the features I suggested earlier in this video or some features that maybe your friends have suggested or your own ideas.
[00:18:44] And in fact, if you're not sure what else to do
[00:18:47] you can also ask the AI for ideas.
[00:18:49] So if you ask it, "How can I make this birthday card app cool?
[00:18:52] " it may give a few suggestions and then you could pick one or more and use the AI's idea to make your app more cool.
[00:19:00] I actually use AI as a brainstorming tool a lot when I'm building software
[00:19:05] and you should do the same too if you don't already have ideas that you're excited about.
[00:19:09] Please go to the next item in this website and have fun adding features or play with the color theme or implement whatever you feel like.
[00:19:17] When you come back, we'll use the skills you've already learned to build a second app
[00:19:23] a ping pong game.
[00:19:24] Using the skills you now have in prompting
[00:19:37] let's build another app, this time, a ping pong game.
[00:19:40] Because if AI is now possible to go from an idea to a working app
[00:19:45] sometimes in minutes.
[00:19:47] One of the earliest video games in computer history was a game called Pong
[00:19:52] which was sort of a two-person ping pong game
[00:19:54] and that had taken the team weeks to build.
[00:19:58] But now, thanks to AI, you can build something like this in minutes.
[00:20:02] Let's apply the prompting techniques we learned.
[00:20:04] I'm gonna start quickly and write a moderately specific prompt and say
[00:20:09] "Build me a table tennis game as a single HTML file.
[00:20:11] User plays against computer.
[00:20:13] Moves the paddle or the arrow keys.
[00:20:14] " And if you do that, you might get a first version of the app that looks like this.
[00:20:18] So here it says, you know, "JavaScript was attached to the button's click event.
[00:21:18] " Boy, there's a lot of technical terminology.
[00:21:24] I would say for now, just don't worry about what the AI is saying here.
[00:21:29] You don't need to understand these technical details.
[00:21:30] If you're really curious, you can actually ask the AI
[00:21:42] "What do these terms mean?
[00:21:47] " But you don't have to do that.
[00:21:52] Let the AI do its thinking, say whatever it wants about the technology
[00:22:04] and then focus on downloading the new HTML file to see if that works.
[00:22:13] If you made it this far, congratulations.
[00:22:15] You're an AI builder now.
[00:22:18] I've met people who've been clearly building software with AI
[00:22:22] maybe even for months, that somehow still wonder if they're actually a builder.
[00:22:27] I'm here to tell you, yes, you are
[00:22:30] and I count you as one of us
[00:22:32] a builder.
[00:22:33] All right.
[00:22:34] I hope you do one last activity and get a certificate for this course.
[00:22:38] The final project is to make your own fill-in-the-blanks story builder.
[00:22:45] I help you used the prompt building blocks to build your own fill-in-the-blanks app.
[00:22:49] Your final project must include three to five input fields
[00:22:52] a button to take the inputs and then generates the outputs
[00:22:56] and a place to display the output.
[00:22:58] You've already seen the birthday card app.
[00:23:01] Here are some other ideas for maybe inspiration.
[00:23:05] This is a funny product review generator where the blanks are the product name
[00:23:11] some number, a noun, a body part
[00:23:13] and so on, and it generates product reviews.
[00:23:16] Notice it says, "These are totally honest product reviews that look like this.
[00:23:21] " Feel free to pause the video and read this if you want
[00:23:24] but I love this.
[00:23:25] Or here's another time-off-request generator where you specify how much time you want off
[00:23:31] a noun, a body part, an object
[00:23:34] and then it says, "I need an entire month off effective immediately because a vintage fur view requires my urgent attention.
[00:23:40] " And so whether a birthday card, or a product review
[00:23:43] or a time off, or some other type of story generator
[00:23:47] please write your own prompts and use it to generate an app like this.
[00:23:51] On the website, when you go to the next item
[00:23:54] you will see the usual chatbot that you can use to write your prompts to get an HTML file and download it onto your own computer.
[00:24:01] Please do that, run it, see if it works to your satisfaction.
[00:24:05] And you could either use our website, or you're also welcome to use an external website like ChatGPT or Gemini to generate your HTML file.
[00:24:13] When you're done building this project, please go to this final page
[00:24:17] it might take a second to load, and then click Upload File.
[00:24:21] And here I'm going to navigate to the file that I had downloaded
[00:24:26] and, um, here's a preview of the app I actually generated.
[00:24:29] When you're ready, hit "Submit Assignment," and our AI will look at your HTML file and see if it seems to work correctly and give you feedback
[00:24:38] if any.
[00:24:38] Assuming it works, this will bring you to the last exercise of this course and will earn you a certificate.
[00:24:46] Most effective builders keep taking courses and also keep building.
[00:24:50] I find that if someone only builds, they often end up unaware of core concepts and can end up spending months reinventing the wheel
[00:24:59] or worse, doing things in very strange ways.
[00:25:01] But conversely, if someone only takes courses
[00:25:05] then they end up with theoretical knowledge without knowing how to apply it.
[00:25:09] So both building and taking courses are important.
[00:25:13] Please keep building whatever you feel like, and I'll also suggest some additional courses for you to consider in the next item.
[00:25:21] Keep sharing your applications with friends to get the feedback
[00:25:24] or maybe just to get a laugh out of them.
[00:25:26] Being a builder is one of the most fun things in the world.
[00:25:31] I'm glad you and I have started this journey together
[00:25:35] and I hope we'll keep building and learning together.
[00:25:39] Thank you also to DeepLearning.
[00:25:41] ai's Summer Ray, Andres Gonzalez, and Tommy Nelson
[00:25:44] who had contributed to this course.