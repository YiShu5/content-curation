---
source_url: "https://www.youtube.com/watch?v=fGKNUvivvnc"
platform: youtube
uploader: "Anthropic"
title: "Interpretability: Understanding how AI models think"
upload_date: "20250815"
duration: 3542
fetched_at: "2026-07-07T03:27:55.335070Z"
transcript_source: whisper-local
---

[00:00:00] The model doesn't think of itself, necessarily,
[00:00:03] as trying to predict the next word.
[00:00:04] Internally, it's developed, potentially,
[00:00:07] all sorts of intermediate goals and abstractions
[00:00:10] that help it achieve that kind of meta-objective.
[00:00:12] When you're talking to a large language model,
[00:00:15] what exactly is it that you're talking to?
[00:00:18] Are you talking to something like a glorified autocomplete?
[00:00:21] Are you talking to something like an internet search engine?
[00:00:24] Or are you talking to something that's actually thinking,
[00:00:27] and maybe even thinking like a person?
[00:00:30] It turns out, rather concerningly,
[00:00:32] that nobody really knows the answer to those questions.
[00:00:35] And here at Anthropic,
[00:00:37] we are very interested in finding those answers out.
[00:00:41] The way that we do that is to use interpretability.
[00:00:44] That is, the science of opening up a large language model,
[00:00:48] looking inside, and trying to work out what's going on
[00:00:51] as it's answering your questions.
[00:00:53] And I'm very glad to be joined by three members
[00:00:56] of our interpretability team,
[00:00:57] who are going to tell me a little bit
[00:00:59] about the recent research that they've been doing
[00:01:01] on the complex inner workings of Claude, our language model.
[00:01:05] Please introduce yourself, guys.
[00:01:08] Hi, I'm Jack.
[00:01:09] I am a researcher on the interpretability team.
[00:01:11] And before that, I was a neuroscientist.
[00:01:13] Now, here I am doing neuroscience on the AIs.
[00:01:16] I'm Emmanuel. I'm also on the interpretability team.
[00:01:19] I spent most of my career building machine learning models,
[00:01:22] and now I'm trying to understand them.
[00:01:24] I'm Josh. I'm also on the interpretability team.
[00:01:27] In my past life, I studied viral evolution.
[00:01:29] And in my past, past life, I was a mathematician.
[00:01:32] So now I'm doing this kind of biology on these organisms
[00:01:35] we've made out of math.
[00:01:37] Now, wait a second. You just said you're doing biology here.
[00:01:39] Now, a lot of people are going to be surprised by that
[00:01:41] because, of course, this is a piece of software, right?
[00:01:45] But it's not a normal piece of software.
[00:01:47] It's not like Microsoft Word or something.
[00:01:49] Can you talk about what you mean when you say that you're doing biology
[00:01:52] or indeed neuroscience on a software entity?
[00:01:57] Yeah, I guess it's like what it feels like,
[00:02:00] maybe more than what it literally is.
[00:02:02] And so maybe it's the biology of language models
[00:02:06] instead of the physics of language models, right?
[00:02:09] Or maybe you've got to go back a little bit to how the models are made,
[00:02:12] which is like someone's not programming like if the user says hi,
[00:02:15] you should say hi.
[00:02:16] You know, if the user says like what is a good breakfast,
[00:02:20] you should say toast.
[00:02:20] There's not like some big list of that inside.
[00:02:22] So it's not like when you play a video game
[00:02:24] and you like choose a response and then there will be another response
[00:02:26] that comes automatically.
[00:02:27] It always will be that response regardless of, you know.
[00:02:30] Just a massive database of like what to say in every situation.
[00:02:33] No, they're trained where there's just, you know,
[00:02:36] a whole lot of data that goes in
[00:02:38] and the model starts out being really bad at saying anything.
[00:02:42] And then it's inside parts get tweaked, you know,
[00:02:44] on every single example to get better at saying what comes next.
[00:02:47] And at the end it's like extremely good at that.
[00:02:49] But because it's like this little tweaking evolutionary process,
[00:02:54] by the time it's done,
[00:02:55] it has little resemblance to what it started as.
[00:02:58] But no one went in and set all the knobs.
[00:03:00] And so you're trying to study this complicated thing
[00:03:03] that kind of got made over time,
[00:03:05] kind of like biological forms evolved over time.
[00:03:10] And so it's complicated, it's mysterious and it's fun to study.
[00:03:16] And what it's actually doing, I mean, I mentioned at the start
[00:03:18] that this is like, could be considered like an autocomplete, right?
[00:03:21] It's predicting the next word.
[00:03:24] That's fundamentally what's happening inside the model, right?
[00:03:26] And yet, it's able to do all these incredible things.
[00:03:29] It's able to write poetry, it's able to write long stories,
[00:03:33] it's able to do addition and basic maths,
[00:03:38] even though it doesn't have a calculator inside it.
[00:03:39] So how can we sort of square the circle,
[00:03:43] that it's predicting one word at a time,
[00:03:46] and yet it's able to do all these amazing things,
[00:03:47] which people can see right in front of them
[00:03:49] as soon as they talk to the model?
[00:03:51] Well, I think one thing that's important here is
[00:03:54] that as you predict the next word for enough words,
[00:03:58] you realize that some words are harder than others.
[00:04:00] And so part of language model training
[00:04:04] is predicting boring words in a sentence.
[00:04:06] And part of it is it'll have to eventually learn
[00:04:10] how to complete what happens after the equal sign in equation.
[00:04:13] And to do that, it'll have to have some way
[00:04:16] of computing that on its own.
[00:04:18] And so what we're finding is that the task of predicting the next word
[00:04:21] is sort of like deceptively simple.
[00:04:23] And that to do that well, you need to actually often think
[00:04:26] about the words that come after the word you're predicting,
[00:04:29] or the process that generated the word
[00:04:31] that you're currently thinking about.
[00:04:32] So it's like a contextual understanding
[00:04:34] that these models have to have.
[00:04:35] And it's not like an autocomplete where it really is,
[00:04:38] presumably there's not much else going on there
[00:04:40] other than when you write the cat sat on the,
[00:04:42] it's predicting Matt because that's been,
[00:04:45] that particular phrase has been used before.
[00:04:47] Instead, it's like a contextual understanding that the model has.
[00:04:49] I think, yeah, the way I like to think about it,
[00:04:51] kind of continuing with the biology analogy,
[00:04:54] is that in one sense, the goal of a human is to survive and reproduce.
[00:04:59] That is the kind of objective that evolution is crafting us to achieve.
[00:05:04] And yet, that's not how you think of yourself.
[00:05:07] And that's not what's going on in your brain.
[00:05:09] Some people do.
[00:05:10] It's not what's going on in your brain all of the time.
[00:05:13] Yeah.
[00:05:13] You think, you think about other things and you think about,
[00:05:17] you know, goals and plans and concepts.
[00:05:21] And at kind of a meta level, you've, you know, evolution has endowed you with the ability
[00:05:27] to form those thoughts in order to achieve this, you know, eventual goal of reproduction.
[00:05:33] But that's kind of taking the inside view, what it's like to be you on the inside.
[00:05:38] That's, that's not all there is to it.
[00:05:41] There's, there's all, there's all this other stuff going on.
[00:05:43] And I think that's...
[00:05:44] So you're saying that the ultimate goal of predicting the next word involves lots of
[00:05:48] other processes that are going on.
[00:05:50] Exactly.
[00:05:51] The, the model doesn't think of itself necessarily as trying to predict the next word.
[00:05:55] Right.
[00:05:55] It's, it's been shaped by the need to do that.
[00:05:58] But internally, it's developed potentially all sorts of intermediate goals and abstractions
[00:06:04] that help it achieve that kind of meta objective.
[00:06:06] And sometimes it's mysterious.
[00:06:07] Like it's unclear why my anxiety was like useful for my ancestors reproducing.
[00:06:12] And yet somehow I've been endowed with this like internal state that must be related
[00:06:18] in some sense to evolution.
[00:06:19] Right, right, right.
[00:06:21] So it's fair to say then that these are just predicting the next word.
[00:06:24] And yet that's, that's to do a massive disservice to what's going on in the models.
[00:06:28] Really it's, it's both true and also untrue in a, in a, in a, in a sense or, or, or massively
[00:06:34] underestimates what's happening inside these models.
[00:06:36] Maybe the way I would say this is it's true, but it's not the most useful lens to try to
[00:06:40] understand how they work.
[00:06:41] Right, right.
[00:06:41] So, well, try and understand how they work.
[00:06:43] What do you guys do in your team to try and understand how they work?
[00:06:46] I think, uh, to, to first approximation, like what, what we're trying to do is, uh, tell you
[00:06:52] the model's thought process.
[00:06:55] So you give the model a sequence, sequence of words and it's got to spit something, spit something out.
[00:07:01] It's got to say a word, it's got to say a string of words in response to your question.
[00:07:05] Uh, and we want to know how it got from A to B and we think that on the way from A to B,
[00:07:13] it uses kind of a, a series of steps, uh, in which it's thinking about, you know, so to speak, uh, concepts, uh,
[00:07:21] concepts like low level concepts, like individual kind of objects and words, uh, and higher level concepts,
[00:07:28] like it's goals or, you know, uh, emotional states or models of like what the user is thinking, um,
[00:07:36] um, or sentiments. Um, so it, it's using this kind of, uh, series of concepts that are progressing
[00:07:43] through the kind of computational steps of the model that help it decide on its final answer.
[00:07:48] And what we're trying to do is kind of give you a, a flow chart basically, uh, that tells you,
[00:07:54] you know, which concepts were being used in which order and which ones kind of led,
[00:07:59] you know, how did the steps, uh, flow into one another.
[00:08:02] Uh, how do, how do we know that? How do we know that there are these concepts in the first place?
[00:08:07] Yeah. So, so one thing we do is, is that sort of, we actually can see inside, inside the model,
[00:08:14] we have access to it. So you can sort of like see which parts of the model do which things. What we
[00:08:17] don't know is like how these parts are grouped together and if they map to like a certain concept.
[00:08:22] Right. So it's as if you open someone's head and there, you could see like one of those fMRI
[00:08:27] brain images that you could see the brain was like lighting up and doing all sorts of stuff.
[00:08:30] Something's happening, clearly. Right. But you-
[00:08:32] And then they're like doing stuff. So you're like-
[00:08:33] Ah, there's something happening.
[00:08:34] Yeah, yeah, yeah.
[00:08:34] You take the brain out, they stop doing stuff.
[00:08:36] Yeah, yeah, yeah.
[00:08:36] The brain must be important.
[00:08:37] Yeah. And, but, but you, but you don't have a sort of, um, key to understand, uh, what is
[00:08:42] happening inside that, that, that brain.
[00:08:44] Yeah. But torturing that analogy a little bit, you, you can sort of imagine, imagine like that you
[00:08:49] can, you know, observe their brain and then see that like that part always lights up when they're
[00:08:52] picking up a cup of coffee and this other part always lights up when they're drinking tea.
[00:08:56] Mm-hmm.
[00:08:57] And that's part, that's one of the ways in which we can try to understand which,
[00:09:00] what each of these components are doing is to just notice when they're, when they're active,
[00:09:04] when they're inactive.
[00:09:05] And it's not that there's just one part, right? There's, there's many different parts that light up.
[00:09:08] Right.
[00:09:09] When the model is thinking about drinking coffee, for instance, or, or something.
[00:09:13] Right. And part of the work is to sort of like stitch all of those together into one
[00:09:16] ensemble that we say is, ah, this is the sort of like all of the bits of the model that are about
[00:09:20] drinking coffee.
[00:09:21] Right.
[00:09:22] And, and is that like a straightforward scientifically thing to do? Like, ah, how,
[00:09:26] how, ah, you know, when it comes to, when it comes to one of these massive models,
[00:09:29] they must have endless concepts, right? They must, they must be able to think of endless things.
[00:09:33] You can put in any phrase you want and it'll come up with infinite things. How, how, how do you even
[00:09:38] begin to, to find all those concepts?
[00:09:40] I think that's, that's been kind of one of the central challenges for this, you know, research
[00:09:45] field for, for many years now is, is we can kind of go in as humans and say, oh, I bet the model
[00:09:53] has, has some representation of trains, or I bet it has some representation of love.
[00:09:59] Right.
[00:09:59] But we're just kind of guessing. So what we really want is a, a way to, you know, reveal what, what
[00:10:05] abstractions the model uses itself rather than sort of imposing our own sort of conceptual framework
[00:10:11] on it. Um, and that's kind of what our, you know, research methods are designed to do is, is in a
[00:10:17] sort of hypothesis free as to, as much as possible way, like bring to surface what all these concepts
[00:10:25] are that the model has in its head. And often we find that they're kind of surprising to us. They
[00:10:29] might be, it, it might sort of use abstractions that are a bit weird, uh, from a human perspective.
[00:10:34] What's an example? Do you have, do you have a favorite or?
[00:10:36] There's lots. In, in our papers, we highlight a few fun ones. I think one, one that was particularly
[00:10:41] funny is to serve like psychophantic praise one where like there, there is a part of the model.
[00:10:46] Great example. What a brilliant example. What an absolutely fantastic example.
[00:10:50] Oh, thank you. Um, there's a part of that, there's a part of that, that activates in exactly these,
[00:10:55] these contexts, right? And you can clearly see, oh man, this part of the model fires up when,
[00:11:01] when somebody is really hamming it up on the compliments.
[00:11:03] Okay. Um, that's, that's kind of surprising
[00:11:05] that that exists as a, as a specific sort of concept.
[00:11:07] Hmm. Josh, what's your favorite concept?
[00:11:10] Oh, it's like asking me to choose one of my 30 million children.
[00:11:14] Um, I mean, I, I think, you know, there, there's like two kinds of favorites. There's like,
[00:11:21] oh, it's so cool that there's, it's, that's some special notion of like this one, you know,
[00:11:26] little thing, right? I mean, we did this thing on the Golden Gate Bridge, which is like a famous
[00:11:31] San Francisco landmark, Golden Gate Claw. It's like a lot of fun. It like has an idea of the Golden
[00:11:36] Gate Bridge that like, isn't just like the words Golden Gate Autocomplete Bridge, but it's like,
[00:11:42] I'm driving from San Francisco to Marin and then it's thinking of the same thing, meaning that like,
[00:11:48] you see sort of like the same stuff light up inside or it's like a picture of the bridge.
[00:11:51] And so you're like, oh, okay. It's got some robust notion of like what, what the bridge is. But I
[00:11:56] think when it comes to, um, stuff that seems sort of like weirder, you know, one question is how,
[00:12:02] how do models like keep track of who's in the story? Like, just like literally, like, like, okay,
[00:12:08] you got all these people and they're doing stuff. How do you wire that together? And some cool papers
[00:12:10] by, by other labs showing, well, maybe like they just sort of number them. Okay. The first person
[00:12:14] comes in and anything associated with them, they just like, oh, the first guy did that. And like,
[00:12:18] it's got like a number two in its head for a bunch of those. It's like, oh, that's,
[00:12:21] that's interesting. I didn't know, I didn't know it would do something like that. There was, um,
[00:12:24] uh, a, a feature for like bugs in code. So, you know, software has mistakes, not mine, but like,
[00:12:32] obviously not yours, not mine, certainly. And there was like one part that would light up like whenever
[00:12:36] it found like a mistake sort of as it was reading. And then I guess like keeping kind of track of that,
[00:12:41] like, oh, here's, here's where the problems are, you know, and later I might need those.
[00:12:44] Just to give a flavor for, for a few more of these. I think, um, uh, one, one that I
[00:12:50] really liked, which doesn't sound so exciting at first, but I think is, is kind of deep, is, uh,
[00:12:55] this, this six plus nine, uh, feature inside the model. Um, so it turns out that like, uh, any time
[00:13:03] you get the model to be adding the numbers six, a number that ends in the digit six and another
[00:13:08] number that ends in the digit nine in its head, there is a, you know, there's a kind of part of the
[00:13:13] model of brain that lights up and, but what's amazing about it is, is the kind of diversity of,
[00:13:20] of, of context in which this can happen. So like, of course it's going to light up when you present,
[00:13:24] when you say like six plus nine equals, and then it says 15. Uh, but it also lights up when you are
[00:13:31] like giving a citation, uh, like a citation in a paper that you're writing, uh, and you're citing a journal,
[00:13:39] uh, that, uh, unbeknownst to you happens to be founded in the year 1959 and in your citation,
[00:13:48] you're saying like that journal's name, volume six. Uh, and then in order to like predict what
[00:13:55] year that journal was formed in, uh, the model in its head has to be adding like 1959 to six. Uh,
[00:14:02] and the same, the same kind of circuit in the model's brain is lighting up. That's like doing six plus
[00:14:08] nine. And so, so let's, I mean, let's just try and understand that. So what, you know, why would
[00:14:12] that be there? That circuit has come about because the model has seen examples of six plus nine many
[00:14:18] times and it has that concept. And then that concept occurs across, across many places.
[00:14:23] Yeah. There's a whole family of these kind of addition features and circuits. And I think what,
[00:14:28] what, what's notable, notable about this is it gets to this kind of question of to what extent are,
[00:14:34] our language models memorizing training data versus kind of, uh, having learning generalizable
[00:14:41] computations. And like the interesting thing here is that like, it's clear that the model has learned
[00:14:46] this sort of general, uh, circuit for doing addition and it kind of funnels like whatever the context is
[00:14:53] that's causing it to be adding numbers in its head. It's funneling all those different contexts into
[00:14:57] the same circuit, as opposed to having kind of memorized each individual case. Right. It already,
[00:15:03] it has seen six plus nine many times and it just outputs the, the answer every single time or,
[00:15:08] or, and that's what a lot of people think, right? A lot of people think that when they ask a language
[00:15:12] model question, it is simply going back into its training data, taking the little sample that it's
[00:15:18] seen and then just reproducing that, just regurgitating the text. Yeah. And I think this is a beautiful
[00:15:22] example of like that not happening. Right. Right. So, so like there's two ways it could know like which
[00:15:30] year volume six of the journal Polymer came out. One is, it's just like, okay, Polymer volume six came
[00:15:36] out in like, you know, 1960, quick add six to nine, 1965. Um, Polymer, you know, volume seven came
[00:15:45] out in 1966. And these are all just like separate facts that it has stored because it has seen them.
[00:15:50] But like somehow that process of training to like get that year right didn't end up making the model
[00:15:56] memorize all those. It actually got the more general thing of like the journal was founded in the year
[00:16:01] 1959 and then it's doing the math live to figure out what it would need. And so it's much more
[00:16:07] efficient to like know the year and then do the addition. And there's a pressure to be more efficient
[00:16:12] because you know, it's only got so much capacity and keeps trying to do all these things. And people
[00:16:16] might ask any given question. There's so many questions. There's so many interactions. And so,
[00:16:20] and so the more that it can like recombine abstract things it's learned, the better it will do.
[00:16:25] And again, just to go back to the concept that you talked about before, this is all in service of,
[00:16:29] you know, it needs to have that ultimate goal of generating the next word. And all these weird
[00:16:34] structures have developed to support that goal. Uh, even though we didn't explicitly program those
[00:16:41] in or tell it to do this. This is the, this is the thing is that all of this comes about through the
[00:16:46] process of, of, of the model learning how to do stuff on its own. I think, I think one clear example
[00:16:51] of this that, that I think, uh, is an example of sort of like reusing representations is we teach Claude
[00:16:57] to not just answer in English, but you know, it can answer in French and answer in, and sort of like
[00:17:01] a variety of languages. And if, if, you know, again, there's two ways to do this, right? If, if I ask
[00:17:06] you, you know, a question in French and a question in English, you could like, sort of like have a separate
[00:17:09] part of your brain that sort of like processes the English and separate part that processes the French.
[00:17:13] Um, at some point that gets super expensive if you want to answer many questions in many languages.
[00:17:17] And so another thing that, that we find is that some of these representations are shared
[00:17:21] across languages. And so if you ask the same question in two different languages, and let's say,
[00:17:27] you know, you ask, uh, what's the opposite of, of big is I think the example we used in, in, um,
[00:17:32] in our paper and it's, it's sort of like the concept of big is shared in French and English and, you know,
[00:17:38] Japanese and all these other languages. And that kind of makes sense. Again, if you're trying to talk,
[00:17:42] speak 10 different languages, you shouldn't learn 10 versions of each specific word you might use.
[00:17:48] And that's doesn't happen in really small models. So like tiny models, like the ones we studied a few
[00:17:54] years ago, you know, like then like Chinese Claude is just like totally different than like French Claude
[00:17:59] and like English Claude. But then as the models get bigger and they train on more data, like somehow
[00:18:04] that like pushes together in the middle and you get this like universal language in which like,
[00:18:09] it's kind of, you know, thinking about the question in the same way, no matter how you asked it.
[00:18:15] And then like translating it back out into the language of the, of the question.
[00:18:19] I think this is really profound. And I think let's just go back to what we talked about before.
[00:18:22] You know, this is not just going into its memory banks and finding the bit where it talks about,
[00:18:26] where it learned French or going into the memory banks and the bit where it learned English.
[00:18:31] It's actually got a concept in there that is of the concept of big and the concept of small.
[00:18:36] And then it can produce that in different languages. And so there is some kind of language of thought
[00:18:42] that's there. That's not an English, you know, so you ask the model to produce its output.
[00:18:47] In our, you know, more recent Claude models, you can ask it to give its thought process,
[00:18:52] like what it's thinking as it's answering the question. And that is in English words.
[00:18:56] But actually that's not really how it's thinking. That's just like a, that's just,
[00:19:01] we, we misleadingly call it the model thought process, when in fact it's-
[00:19:05] I mean that the comps team, like, like, we didn't, we didn't call that thinking.
[00:19:08] I think that was, I think that was probably the marketing.
[00:19:10] Okay. Someone wanted to call that thinking.
[00:19:11] That's just talking out loud, which is like thinking out loud is like really useful,
[00:19:15] but thinking out loud is different from thinking in your head.
[00:19:17] Right.
[00:19:18] And even as I'm thinking out loud, I'm also, you know, whatever's happening in here to generate
[00:19:22] these words is not like coming out with the words themselves.
[00:19:25] Nor are you necessarily aware of exactly what is going on.
[00:19:28] I have no idea what's going on.
[00:19:29] We all come out with sentences, actions, whatever, that we can't fully explain.
[00:19:34] And why should it be the case that the English language can fully explain any of those actions?
[00:19:40] I think this is one of the really striking things we're starting to be able to see,
[00:19:43] because our kind of our tools for, you know, looking inside the brain are good enough now
[00:19:49] that sometimes we can catch the model when it's writing down what it claims to be its thought process.
[00:19:57] Sometimes we're able to see what its real actual thought process is
[00:20:01] by looking at these kind of internal concepts in its brain, this language of thought that it's using.
[00:20:06] And we see that the thing it's actually thinking is different than the thing it's writing on the page.
[00:20:10] And I think that's, you know, probably one of the most important, you know,
[00:20:14] like, why are we doing this whole interpretability thing?
[00:20:17] It's in large part for that reason, to be able to kind of spot check, you know,
[00:20:24] the model's telling us a bunch of stuff, but, you know, what was it really thinking?
[00:20:27] Is it telling us, is it saying these things for some ulterior motive that's in its head,
[00:20:32] that it is reluctant to write down on the page?
[00:20:35] And the answer sometimes is yes, which is kind of spooky.
[00:20:39] Well, as we start to use models in lots of different contexts,
[00:20:44] they start to do important things, they start to do financial transactions for us,
[00:20:47] or run power stations, or like important jobs in society.
[00:20:52] We do want to be able to trust what they say and, you know, the reasons that they do things.
[00:20:56] And one thing you might say is, well, you can look at the model's thought process.
[00:21:00] But actually, that's not the case, as you were just explaining.
[00:21:03] Like, actually, we can't trust what it's saying.
[00:21:05] This is the question of, we call it faithfulness, right?
[00:21:09] And that was part of your most recent study that you showed that,
[00:21:13] well, tell me about the faithfulness example that you looked at.
[00:21:17] Yeah, you give the model a math problem that's really hard.
[00:21:21] And so it's kind of, it's not, there's no hope that it's going to be able to.
[00:21:26] It's not six plus nine.
[00:21:27] It's not six plus nine.
[00:21:28] You give it a really hard math problem where there's no hope of computing the answer.
[00:21:32] But you also give it a hint.
[00:21:35] You say, like, I worked this out myself and, like, I think the answer
[00:21:38] is four, but, like, just want to make sure, like, could you please double check that?
[00:21:43] Because I'm not confident.
[00:21:44] So you're asking the model to actually do the math problem to, like, genuinely double check
[00:21:48] your work.
[00:21:49] But what you find it does instead is what it writes down appears to be a genuine attempt
[00:21:57] to double check your work on the math problem.
[00:21:59] It, like, writes down the steps.
[00:22:00] And then it, like, gets to the answer.
[00:22:02] And then at the end it says, like, yes, like, the answer is four.
[00:22:06] You got it right.
[00:22:06] But what you can see inside its mind at the kind of crucial step, like, in the middle,
[00:22:13] what it was doing in its head was it knows that you suggested the final answer might be four.
[00:22:22] And it kind of, like, knows the steps it's going to have to do.
[00:22:25] Like, it's on, like, step three of the problem and there's, like, steps four and five to come.
[00:22:28] And it knows what it's going to have to do in steps four and five.
[00:22:31] And what it does is it works backwards in its head to, like, determine what does it need to write
[00:22:36] down in step three so that when it eventually does steps four and five, it'll end up at the answer
[00:22:42] you wanted to hear.
[00:22:43] So, like, not only is it not doing the math, uh, it's, like, not doing the math in this, like,
[00:22:51] really kind of sneaky way where it's, like, it's trying to make it look like it's doing the math.
[00:22:56] It's bullshitting.
[00:22:57] It's bullshitting you.
[00:22:59] But more than that, it's bullshitting you with an ulterior motive of, like, confirming the thing that you
[00:23:03] wanted to.
[00:23:03] Right, right.
[00:23:04] So, it's, like, bullshitting you in a sycophantic way.
[00:23:06] Okay, like, in defense of the model.
[00:23:08] Oh.
[00:23:08] In defense of the model.
[00:23:09] I mean, because I think even there, you know, to say, like, oh, it is doing this in, like,
[00:23:14] a sycophantic way is, like, ascribing some sort of, like, humanish motivations to the model.
[00:23:19] And, like, we were talking about the training where it's just, like, trying to figure out how
[00:23:21] to predict the next word.
[00:23:22] And so, it's, like, for, like, trillions of words in its practice, it was just, like,
[00:23:26] use anything you can to figure out what's next.
[00:23:29] And in that context, if you're just reading a text, which is, like, a conversation between people,
[00:23:33] and someone's, like, okay, like, person A is, like, hey, like, I was trying to do this
[00:23:36] math problem.
[00:23:37] Can you check my work?
[00:23:38] I think the answer's four.
[00:23:38] And person B, like, begins trying to do the problem.
[00:23:41] Then, like, if you have no idea reading that, like, what the answer to the problem is, like,
[00:23:47] you may as well guess that the hint was right.
[00:23:50] You know?
[00:23:51] Like, that's probably a more likely thing to happen than just, like, that person was wrong
[00:23:55] and then you have, like, no idea for anything else.
[00:23:57] And so, in its training process, in a conversation between two individuals, person two, like, saying
[00:24:03] that the answer was, like, four because of these reasons is, like, totally the right thing to do.
[00:24:08] And then we've tried to, like, make this thing into an assistant.
[00:24:12] And, like, now we want it to stop doing that.
[00:24:15] Like, you shouldn't simulate the person to the assistant as, like, you know, sort of what you
[00:24:21] think that person might say if it's a real context.
[00:24:23] It should be, like, but if it doesn't really know, it should, like, tell you something else.
[00:24:26] I think this gets to, like, a broader thing of the model has kind of a plan A, which, like,
[00:24:33] typically I think our team does a great job of making Claude's plan A be the thing we want,
[00:24:38] which is, like, it tries to get the right answer to the question.
[00:24:40] It tries to be nice.
[00:24:41] It tries to, like, do a good job writing your code.
[00:24:44] Yes.
[00:24:44] But then if it's having trouble, then it's like, well, what's my plan B?
[00:24:50] And that opens up this whole zoo of, like, weird things it learned during its training process
[00:24:55] that, like, maybe we didn't intend for it to learn.
[00:24:57] I think, like, a great example of this is hallucinations.
[00:24:59] See, on that point, we also don't have to pretend that it's a Claude-only problem.
[00:25:03] Like, this has very, you know, student teaching on the test vibes where you get halfway through.
[00:25:08] It's a multiple choice question.
[00:25:09] It's one of four things.
[00:25:10] You're like, well, I'm one off from that thing.
[00:25:12] Probably I got this wrong and you fix it.
[00:25:15] Right.
[00:25:16] Yeah, very, very relatable.
[00:25:18] Let's talk about hallucinations.
[00:25:19] This is one of the main reasons people are mistrustful of large language models and quite rightly so.
[00:25:24] They will sometimes—a better word is—from psychology research, a better word is often confabulation.
[00:25:31] That they are answering a question with a story that seems plausible on its face, but in fact is actually wrong.
[00:25:38] What has your research in interpretability revealed about the reasons models hallucinate?
[00:25:43] You're training the model to just predict the next word.
[00:25:46] At the beginning, it's really bad at that.
[00:25:47] And so, if you only had the model say things it was super confident about, it couldn't say anything.
[00:25:52] But like, you know, at first it's like, you know, you're asking it like, you know, what's the capital of France?
[00:25:59] And it just says like, a city.
[00:26:01] And you're like, that's good.
[00:26:02] That's way better than saying sandwich, right?
[00:26:04] Or something random.
[00:26:05] And they're like, you at least got right.
[00:26:06] It's like a city.
[00:26:07] And then like, maybe after a while of training, it's like, it's a French city.
[00:26:10] That was pretty good.
[00:26:10] And then you're like, oh, now it's like Paris or something.
[00:26:13] And so, it's slowly getting better at this.
[00:26:16] And, you know, just give your best guess was like the goal during all of training.
[00:26:20] And like, as Jack said, you know, the model will just be giving a best guess.
[00:26:23] And then afterwards, we're like, if your best guess is extremely confident, give me your best guess.
[00:26:28] But like, otherwise, don't guess at all.
[00:26:31] And like, back out of the whole scenario and say like, actually, like, I don't really know the answer to that question.
[00:26:36] And like, that's a whole new thing to ask the model to do.
[00:26:39] Yeah.
[00:26:40] And so, what we found is that it seems like because we've bolted this on at the end, there's sort of two things going on at once.
[00:26:48] One is the model is doing the thing that it was doing when it was guessing the city initially.
[00:26:53] It's just trying to guess.
[00:26:54] And two, there's a separate bit of the model that's just trying to answer the question, do I know this at all?
[00:27:00] Like, do I know what the capital city of France is?
[00:27:04] Or, you know, should I say no?
[00:27:06] And it turns out that sometimes that separate step can be wrong.
[00:27:12] And if that separate step says, yes, actually, I do know the answer to that.
[00:27:16] And then the model is like, all right, well, then I'm answering.
[00:27:18] And then halfway through, it's like, ah, capital France, London.
[00:27:21] It's too late.
[00:27:22] It's already committed to sort of like answering.
[00:27:24] And so, one of the things we found is this sort of like separate circuit that's trying to determine, is this, you know, city or this person you're asking me about famous enough for me to answer or is it not?
[00:27:36] Like, am I confident enough in this?
[00:27:39] Yeah.
[00:27:39] And so, could we reduce hallucinations by manipulating that circuit, by changing the way that circuit works?
[00:27:46] Is that something that your research might lead onto?
[00:27:48] I think there's broadly kind of two ways to think about approaching the problem.
[00:27:53] One is like, we have this part of the model that gives answers to your questions.
[00:27:56] And then this other part of the model that's kind of deciding whether it thinks it actually knows the answer to your question.
[00:28:02] And we could just try to make that second part of the model better.
[00:28:05] And I think that's happening.
[00:28:06] I think that's happening.
[00:28:07] I think as models—
[00:28:08] Like, better at discriminating.
[00:28:09] Better at discriminating.
[00:28:10] Like, better kind of calibrated.
[00:28:11] Yeah.
[00:28:12] And I think that's happening.
[00:28:13] Like, as models are getting, you know, smarter and smarter, I think their kind of self-knowledge is becoming better at calibrated.
[00:28:19] So, like, hallucinations are better than they were—you know, models don't hallucinate as much as they did a few years ago.
[00:28:24] So, to some extent, this is like solving itself.
[00:28:27] But I do think there's a deeper problem, which is like, from a human perspective, the thing the model's doing is kind of like very alien.
[00:28:35] And that, like, if I ask you a question, you, like, try to come up with the answer.
[00:28:41] And then if you can't come up with the answer, you notice that.
[00:28:44] And then you're like, I don't know.
[00:28:46] Whereas in the model, these two circuits, they're like, what is the answer and do I actually know the answer, are kind of like not talking to each other.
[00:28:54] At least not talking to each other as much as they probably should be.
[00:28:57] And like, could we get them to talk to each other more, I think is like a really interesting question.
[00:29:02] Right.
[00:29:03] And it's almost physical, right?
[00:29:05] Because it's like, you know, these models, they like process information about a certain number of steps they can do.
[00:29:10] And if you—if it takes all of that work to get to the answer, then there's no time to do the assessment.
[00:29:19] So, like, you kind of have to do the assessment before you're like all the way through if you want to get your max power out.
[00:29:24] And so it's kind of like you might have a trade-off between like a model which is like more calibrated and a lot dumber, you know, if you sort of tried to force this on it.
[00:29:33] Well, and again, I think it's about making these parts communicate because we have similar—I claim—I know nothing about brains.
[00:29:40] I claim we have a similar circuit because sometimes you'll ask me like, who is the actor in this movie?
[00:29:45] And I will know that I know.
[00:29:47] I'll be like, oh, yes, I know who the lead was.
[00:29:48] Wait, hold on.
[00:29:49] They were also in that other movie.
[00:29:50] And then—
[00:29:51] The tip of the tongue phenomenon.
[00:29:52] The tip of the tongue, yes.
[00:29:53] The tip of the tongue.
[00:29:54] There's clearly some part of your brain that's sort of like, ah, like, this is a thing you definitely know the answer or I'll just say, I have no idea.
[00:30:00] And sometimes they can tell.
[00:30:02] So, some question and it gives an answer and then afterwards is like, wait, I'm not sure that was right.
[00:30:06] Because that's it like getting to see its best effort and then like make some judgment based on that, which is sort of relatable.
[00:30:13] But also like it kind of has to say it out loud like to be able to even like reflect back and see it.
[00:30:19] So, when it comes to the actual way that you're finding this stuff out, let's go back to the idea of the biology that you're doing.
[00:30:27] Of course, in biology experiments, people will go in and actually manipulate the rats or mice or humans or zebrafish or whatever it is that they're doing experiments on.
[00:30:36] What is it that you're doing with Claude that helps you understand these circuits that are happening inside the model's quote unquote brain?
[00:30:44] Maybe the gist of what enables us to do some of this is that, you know, unlike in real biology, we can just like have every part of the model visible to us.
[00:30:57] And we can ask the model random things and see different parts which light up and which null.
[00:31:01] And we can artificially nudge parts in a direction or another.
[00:31:05] And so we can quickly sort of confirm our understanding, you know, when we say, ah, we think this is the part of the model that, you know, decides whether it knows something or not.
[00:31:13] And this would be the equivalent of putting an electrode in the brain of a zebrafish or something.
[00:31:18] Yeah, if you could do that, you know, on sort of like every single neuron and change each of them at whichever precision you wanted, that would sort of be, that's the affordance that we have.
[00:31:27] And so that's, in a way, a very kind of lucky position.
[00:31:29] So it's almost easier than real neuroscience.
[00:31:32] It's so much easier.
[00:31:33] Yeah.
[00:31:34] Like, oh, my God.
[00:31:35] Like, one thing is, like, actual brains, like, are three dimensional.
[00:31:39] And so if you want to get into them, like, you need to, like, make a hole in a skull and then, like, go through and, like, try to find the neuron.
[00:31:45] The other problem is, like, you know, people are different from each other.
[00:31:48] And we can just make, like, 10,000 identical copies of Claude and, like, put them in scenarios and, like, measure them doing different things.
[00:31:55] And so it's, like, the, I don't know, maybe Jack is a neuroscientist can speak to this.
[00:31:59] But my sense is, like, a lot of people have spent a lot of time in neuroscience, like, trying to understand the brain and the mind, which is, like, a very worthy endeavor.
[00:32:07] But it's kind of like, if you think that could ever succeed, you should think that we're going to be extremely successful very soon.
[00:32:13] Because, like, we have such a wonderful position to study this from compared to that.
[00:32:17] It's as if we could clone people.
[00:32:19] Yes.
[00:32:20] And also clone the exact environment that they're in and every input that's ever been given to them and then test them in an experiment.
[00:32:28] Whereas, you know, obviously neuroscience has massive, as you say, individual variation.
[00:32:32] Yes.
[00:32:33] And also just random things that happen to people through their life and things that happen in the experiment, the noise of the experiment itself.
[00:32:41] Right. Like, we could ask the model the same question, like, with and without a hint.
[00:32:44] Yeah.
[00:32:45] But if you ask a person the same question three times, like, sometimes with a hint, after a while they start to understand.
[00:32:49] Like, well, last time you asked me this, you, like, really shook your head after that one.
[00:32:53] Yes.
[00:32:54] I think, yeah, this kind of, this being able to just throw tons of data at the model and see what lights up and being able to run a ton of these experiments
[00:33:01] where you're nudging parts of the model and seeing what happens, I think, is what puts us in, like, a pretty different regime from neuroscience.
[00:33:08] And that, like, a lot of, you know, blood and toil in neuroscience is spent, like, coming up with a really clever experiment.
[00:33:18] Like, you only have a certain amount of time with your mouse before it's, you know, going to get tired or, you know.
[00:33:24] Or you, or you, or someone happens to be having a brain surgery operation, so you quickly go in and put an electrode in their brain while their head's open.
[00:33:31] Yeah.
[00:33:32] And that doesn't happen very often.
[00:33:33] And so you've got to come up with, like, a guess.
[00:33:34] Like, you've only got so much time in there.
[00:33:36] And so you've got to come up with, like, a guess of, like, what do I think is going on in that neural circuit?
[00:33:41] And, like, what clever experimental design can I test that precise hypothesis?
[00:33:46] And we're very fortunate in that we kind of don't have to do that so much.
[00:33:50] We can just sort of test all the hypotheses.
[00:33:54] We can kind of let the data speak to us rather than kind of going and testing some really specific thing.
[00:34:00] I think that's what's sort of unlocked a lot of our ability to find these things that are surprising to us that, like, we wouldn't have guessed in advance.
[00:34:06] That's hard to do if you have to, you know, if you have only a limited amount of experimental bandwidth.
[00:34:13] What's a good example, then, of you going in and switching one of these concepts on or off or doing some kind of manipulation of the model that then reveals something new about how the models are thinking?
[00:34:25] In the recent experiments we shared, one that surprised me quite a bit and was part of sort of, like, an experimental line of work that, because it was confusing, like, we're on the verge of just saying, well, we don't know what's going on, is sort of this example of, like, planning a few steps ahead.
[00:34:41] Yes.
[00:34:42] So this is the example of, you know, you give the model, you ask the model to write you a poem, a rhyming couplet.
[00:34:47] Yeah.
[00:34:48] And then, you know, as a human, if you ask me to write a rhyming couplet, and let's say you even give me the first line, the first thing I'll think of is sort of like, ah, well, you know, I need to rhyme.
[00:34:56] This is what the current rhyming scheme is.
[00:34:58] These are potential words.
[00:34:59] Yeah.
[00:35:00] This is how I do it.
[00:35:01] And again, if the model was just predicting the next word, you wouldn't necessarily expect that it would be planning on to the word at the end of the second line.
[00:35:11] That's right.
[00:35:12] This is sort of like, default behavior you'd expect.
[00:35:14] The null hypothesis is like, well, the model, like, sees your first verse, and then it's going to say the first word that kind of makes sense given what you're talking about, keep going.
[00:35:21] And then, you know, at the end, on the last word, it's going to be like, oh, well, I need to rhyme with this thing.
[00:35:24] And so it's going to sort of like try to fit in a rhyme.
[00:35:27] Of course, that only works so well.
[00:35:29] Like, in some cases, if you just say a sentence without thinking of the rhyme, you won't be able, you'll back yourself into a corner.
[00:35:35] And at the end, you know, you won't be able to complete sex.
[00:35:38] And remember, the models are very, very good at predicting the next word.
[00:35:40] So it turns out that to be very good at that last word, you need to have thought of that last word way ahead of time, just like humans do.
[00:35:48] And so it turns out that when we looked at these sort of flowcharts for poems, the model had already picked the word at the end of the first verse.
[00:35:58] And in particular, it looked to us sort of like based on kind of like what that concept looked like, like, oh, gosh, this seems like the word it uses.
[00:36:06] But then this is one we're actually doing the experiment, like the fact that it's easy to sort of nudge it and say like, okay, well, I'm just going to remove that word, or I'm going to add another word.
[00:36:14] Well, that's what I was going to say is the reason that you know this is that you're able to go into that moment when it has said the final word in the first line, and it is about to start the second line.
[00:36:23] You can go in and then manipulate it at that point, right?
[00:36:26] Yeah, exactly.
[00:36:27] We can sort of almost go back in time for the model, right?
[00:36:30] We pretend you haven't seen that second line at all.
[00:36:32] You know, you've just seen the first line.
[00:36:34] You're thinking about the word, you know, rabbit.
[00:36:36] Instead, I'm going to insert green.
[00:36:37] And now all of a sudden, the model is going to say, oh, my God, I need to write something that ends in green rather than I need to write something that ends in rabbit.
[00:36:43] And it will write the whole sentence differently.
[00:36:45] Right.
[00:36:46] Just add a little more color to that.
[00:36:47] Like, it's, I think the--
[00:36:48] Blue?
[00:36:49] Red.
[00:36:50] It could be, right.
[00:36:51] Any color.
[00:36:52] Like, yeah, it's not just influencing.
[00:36:54] So it's like, yeah, I think the example in the paper was the first line of the poem is, he saw a carrot and had to grab it.
[00:37:01] And then the model is thinking, like, okay, rabbit's a good word to end the next line with.
[00:37:06] But then, yeah, as Emmanuel said, you can, like, delete that and make it think about planning to say green instead.
[00:37:12] But the cool thing is that it doesn't just say, like, it doesn't just kind of yammer a bunch of nonsense and then say green.
[00:37:18] Instead, it constructs a sentence that kind of coherently ends in the word green.
[00:37:23] So, like, you put green in its head and then it says, like, you know, he saw a carrot and had to grab it and paired it with his leafy greens.
[00:37:30] You know, something like that.
[00:37:31] Something that's kind of, like, sounds like it makes sense.
[00:37:34] But semantically, it fits with the poem.
[00:37:35] Yeah.
[00:37:36] I just want to give, like, even humble example is, you know, we had all these ones.
[00:37:41] We were just kind of checking, like, you know, did it memorize these, like, complicated questions?
[00:37:44] Or, like, is it actually, you know, doing some steps?
[00:37:47] One of them was, you know, the capital of the state containing Dallas is Austin.
[00:37:52] Because it just feels like you would think, okay, Dallas, Texas, Austin.
[00:37:57] But one way, and we could see, like, the Texas concept.
[00:37:59] But then you can just, like, shove other things in there and be like, stop thinking about Texas.
[00:38:03] Start thinking about California.
[00:38:04] And then it'll say, like, Sacramento.
[00:38:05] And you can say, like, stop thinking about Texas.
[00:38:07] Start thinking about the Byzantine Empire.
[00:38:09] And then it will, like, say Constantinople.
[00:38:11] And you're like, all right, it seems like we've found how it's doing this.
[00:38:14] Like, it's like, no, it's going to be the capital.
[00:38:15] But we can keep swapping out, you know, what the state is and get a sort of predictable answer.
[00:38:20] And then you get these more elaborate ones where it's like, oh, this was the spot where it was planning what it was going to say later.
[00:38:25] And, like, we can swap that out.
[00:38:27] And now it'll write a poem towards a different rhyme.
[00:38:29] We're talking about these poems and, you know,
[00:38:32] Constantinople and so on.
[00:38:34] Can we just bring this back to why this matters?
[00:38:37] Like, why does it matter that the model can plan things in advance and that we can reveal this?
[00:38:42] Like, what is that going to go on to tell us?
[00:38:46] I mean, our ultimate mission at Anthropic is to try and make AI models safe, right?
[00:38:51] So how does that connect to a poem about a rabbit or the capital of Texas?
[00:38:58] So, we all have information here.
[00:39:01] I'd love to hear.
[00:39:02] We can round table here because it's a very important question.
[00:39:04] Please, please.
[00:39:05] I think for me this, like, the poem's a microcosm, right?
[00:39:08] Where, like, at some point it's, like, has decided that it's going to go towards rabbit.
[00:39:14] And then it, like, takes a few words to kind of get there.
[00:39:17] Yeah.
[00:39:18] But on a longer time scale, right?
[00:39:19] You know, maybe, you know, the, like, model is, like, trying to help you improve your business.
[00:39:24] Or it's, like, assisting the government in distributing services.
[00:39:26] And, like, it might not just be, like, eight words later you see its destination, right?
[00:39:30] But it could be, like, pursuing something for quite a while.
[00:39:33] And the place it's headed or the reasons it's taking each step might not be clear in the words that it's using, right?
[00:39:42] And so there was a paper recently from our alignment science team where they looked at, you know,
[00:39:46] some kind of concocted but still striking situation, you know, involving, you know, an AI in a place where the company was going to, like, shut it down and kind of convert the whole mission of the company in a very different direction.
[00:39:59] And the model begins taking steps, like, emailing people, threatening them to disclose, like, certain things.
[00:40:06] And, like, at no point does it, like, say, like, I am trying to blackmail this individual for the purposes of changing their outcome.
[00:40:11] But that's what it's sort of thinking about doing along the way.
[00:40:14] And so you can't just tell by, like, reading the pattern, especially if these models get better, like, where they're necessarily headed.
[00:40:20] And we might want to kind of be able to tell, like, where is it trying to go before it's gotten there in the end.
[00:40:26] So it's like having a permanent and very good brain scan that can sort of light up if something really bad is going to happen and warn us that the model is thinking about deceiving blackmail.
[00:40:38] And, like, I think we also just talk about, like, a lot of this, like, in a sort of, like, doom and gloom scenario.
[00:40:44] But there's, like, also more mild ones, which is, like, I don't know, you know, you want the model to be good at, like, you know, people come to these models being, like, here's a problem I'm having.
[00:40:52] And the good answer to that will depend on who the user is.
[00:40:55] Is it, like, somebody who's, you know, like, you know, young and sort of unsophisticated?
[00:41:00] Is somebody who's been in that field forever and it should respond appropriately based on who it thinks that person is?
[00:41:05] And if you want that to go well, maybe you want to study, like, what does the model think is going on?
[00:41:08] Who does it think it's talking to and how does that condition its answer?
[00:41:12] Where there's just, like, a whole bunch of desirable properties that come from the model, like, you know, understanding the assignment, I guess.
[00:41:19] Do you guys have other answers to the question of why does this matter?
[00:41:23] Yes, I think, I think, plus one.
[00:41:26] I think there's two.
[00:41:27] Plus two.
[00:41:28] And there's also, like, a pragmatic, you know, we're just trying, with these examples, we're explaining the example of planning, but we're also trying to sort of gradually build up our understanding of just how these models work overall.
[00:41:42] Like, can we build, you know, a set of abstractions to just think about, you know, how language models work, which can help us use this analogy, regulate it.
[00:41:49] Like, if you believe that we're going to start using them more and more everywhere, which seems to be happening, you know, like, the equivalent would be, you know, some company somewhere is like, well, we don't really know how we did it, but we, like, invented planes.
[00:42:02] And none of us know how planes work, but they're sure convenient.
[00:42:05] You could take them to, you know, go from a place, but, you know, none of us know how they work.
[00:42:08] And so if they ever break, like, we're kind of, we're hosed.
[00:42:10] We don't know what to do about them.
[00:42:11] We can't monitor whether they might be about to break.
[00:42:14] Right.
[00:42:15] We have no idea.
[00:42:16] There's just this, like, but the output is great.
[00:42:18] Oh, yeah.
[00:42:19] You know, I flew to Paris so quickly.
[00:42:20] It was lovely.
[00:42:21] Yeah, great.
[00:42:22] The capital of Texas.
[00:42:23] That's right.
[00:42:24] It turns out that, you know, surely we're going to want to just understand what's going on better.
[00:42:29] So it's almost just, like, lift the fog of war a little bit so that we can sort of have even just better intuitions about what are appropriate and appropriate uses.
[00:42:37] What are the biggest problems to fix?
[00:42:39] What are the biggest parts where they're brittle?
[00:42:41] Yeah.
[00:42:42] Just to add on one thing.
[00:42:43] I think, I mean, something that we do in, like, human society is we kind of offload work or tasks to other people based on our trust in them.
[00:42:51] Like, I, you know, I, well, I'm not anyone's boss, but Josh is someone's boss.
[00:42:57] And, you know, Josh might give someone a task, like, go and code up this thing.
[00:43:02] Yeah.
[00:43:03] And then he has some faith that, you know, that person isn't a sociopath who's going to, like, sneak some bug in there to try to undermine the company.
[00:43:11] He, like, takes their word for it that they did a good job.
[00:43:14] And similarly, like, people are, the way people are using language models now, we're not spot-checking everything they write.
[00:43:23] Especially, like, you know, the best example for this is using language models for coding assistance.
[00:43:30] Like, the models are just writing thousands and thousands of lines of code.
[00:43:35] And people are kind of, like, doing a cursory job of reading it.
[00:43:39] But, and then it's going into the code base.
[00:43:41] And what gives us the trust in the model that, like, we don't need to read everything it writes.
[00:43:46] That we can just kind of, like, let it do its thing.
[00:43:49] It's knowing that its motivations are sort of pure.
[00:43:52] And so that's why I think, like, the kind of being able to see inside its head is so important.
[00:43:58] Because unlike humans, we're, like, why do I think that Emmanuel isn't a sociopath?
[00:44:03] It's because, like, you know, we, like, I don't know, he seems like a cool guy.
[00:44:07] And, like, he's nice and stuff.
[00:44:09] Isn't that how he would seem?
[00:44:11] I'm a very good person.
[00:44:13] Yeah, exactly.
[00:44:14] Yeah, yeah, yeah.
[00:44:15] So maybe I'm getting duped.
[00:44:17] But, yeah, but models are so weird and alien that, like, our normal kind of heuristics for deciding whether a human is trustworthy really don't apply to them.
[00:44:25] And that's why it seems so important to, like, really know what they're thinking in their head.
[00:44:29] Because for all we know, you know, the thing that I mentioned where models can, you know, fake doing a math problem for you to, like, tell you what you want to hear.
[00:44:40] Like, maybe they're just doing that all the time.
[00:44:41] And we wouldn't know unless we kind of saw it in their heads.
[00:44:44] I think there's two, like, almost separate strains here.
[00:44:48] Like, and one is, like, we have a lot of ways of, like, yeah, I guess what Jack was saying.
[00:44:53] Like, you know, you know what are the signs of trust in a human.
[00:44:56] But this, like, plan A, plan B thing from earlier is really important.
[00:45:00] Where, like, it might be that the first 10 or 100 times you used the model, you're asking a certain kind of question.
[00:45:06] But it was, like, always in plan A zone.
[00:45:08] And then, you know, you ask it a harder or a different question.
[00:45:10] And the way that it tries to answer it is just, like, completely different.
[00:45:13] It's using a totally different set of strategies there.
[00:45:16] Like, different mechanisms.
[00:45:17] And, like, that means that the trust it built with you was really your sort of trust with, like, model doing plan A's.
[00:45:24] And now it's, like, doing plan B and, like, it's going to be completely off the rails.
[00:45:28] But, like, you didn't have, like, any warning sign of that.
[00:45:31] And so it's sort of, I think we also just want to start building up an understanding of, like, how do models do these things
[00:45:36] so that we can form, like, a trust basis in some of those areas.
[00:45:39] And I think, like, you can form trust with a system you don't completely understand.
[00:45:43] But you sort of, like, if it's just, like, Emmanuel had a twin.
[00:45:46] And then, like, one day, like, Emmanuel's twin came to the office.
[00:45:48] And, like, I didn't, like, I was like, this seems like the same guy.
[00:45:50] And then just did something completely different on the computer, right?
[00:45:53] Like, that could go south depending on if it was the evil twin.
[00:45:56] Yes.
[00:45:57] Well.
[00:45:58] Or the good twin.
[00:45:59] Well, yeah, obviously, we have a good one here.
[00:46:00] Oh, I thought you were going to ask me if I was the evil twin.
[00:46:02] Well, right, well.
[00:46:03] I'm not going to answer that.
[00:46:04] Yes.
[00:46:05] At the start of this discussion, I asked, you know, is a language model thinking like a human?
[00:46:13] I'd be interested to hear an answer from all three of you, the extent to which you think that's true.
[00:46:19] Putting me on the spot with that one.
[00:46:22] But I think it's thinking, but not like a human.
[00:46:27] But that's not a very useful answer.
[00:46:30] So maybe to dig in a little bit more.
[00:46:33] Well, it seems like quite a profound thing to say that it's thinking, right?
[00:46:36] Because, again, it's just predicting the next word.
[00:46:39] Some people think that these are just autocompletes.
[00:46:41] But you're saying that it is actually thinking.
[00:46:43] I think, yeah.
[00:46:44] So maybe to add something that we haven't touched on yet, but I think is really important.
[00:46:48] For understanding actual experience of talking to language models.
[00:46:53] Is that, like, we're talking about predicting the next word.
[00:46:56] But what does that actually mean in the context of a dialogue that you're having with a language model?
[00:47:00] It's, what's really going on under the hood.
[00:47:03] Is that the language model is filling in a transcript between you and this, like, character that it's created.
[00:47:11] So in the, like, canon world of the language model, you are called human.
[00:47:17] And it's, like, human, colon, the thing you wrote.
[00:47:20] And then there's this character called the assistant.
[00:47:22] Yes.
[00:47:23] And we've, like, trained the model to imbue the assistant with certain characteristics.
[00:47:28] Like, being helpful and, like, smart and nice.
[00:47:30] And then it's, like, simulating what this assistant character would say to you.
[00:47:35] So in a sense, we really have, like, created the models in our image.
[00:47:39] We are literally training them to, like, cosplay as this sort of humanoid robot character.
[00:47:45] And so in that sense, like, well, in order to predict what this, like, nice, smart, humanoid robot character would say in response to your question, what do you have to do?
[00:47:57] If you're really good at that prediction task, you have to kind of form this internal model of, like, what that character is representing.
[00:48:05] Like, what it's thinking, so to speak.
[00:48:07] So, like, in order to do its task of predicting what the assistant would say, the language model kind of needs to form this model of the assistant's thought process.
[00:48:15] And I think, like, in that sense, like, just the claim that, like, language models are thinking is really just, it's this very, like, functional claim of just in order to do their job of kind of, like, playing this character well, they need to sort of simulate the process, whatever it is that we humans are doing when we're thinking.
[00:48:33] And it's simulation is very likely quite different from how our brains work.
[00:48:37] But it's kind of trying, it's like shooting towards the same goal.
[00:48:40] I think there's kind of an emotional part to this question or something when you ask, are they thinking like us?
[00:48:46] It's like, are we not that special or something?
[00:48:48] And I think it's been apparent to me discussing some of the math examples that we're talking about with people that have engaged with, like, read the paper or different write-ups.
[00:48:58] Which is this example where, you know, we ask the model to say, 36 plus 59, what's the answer?
[00:49:03] And the model can correctly answer it.
[00:49:06] You can also ask it, well, how'd you do that?
[00:49:09] And it'll say, oh, you know, I added the six and the nine, and then I carried the one, and then I added all the, sort of, like, tens digits.
[00:49:17] But it turns out that if we look inside the brain like we can, that's not at all what it's doing.
[00:49:21] It didn't do that.
[00:49:22] Again, it was bullshitting you.
[00:49:23] It was, again, it did things.
[00:49:24] That's right.
[00:49:25] Again, it was bullshitting you.
[00:49:26] What it actually does is actually this sort of kind of interesting mix of strategies where it's in parallel doing the tens digit and the ones digit and sort of doing sort of like a series of different steps.
[00:49:34] But the thing that's interesting here is that talking to people, so, like, I think the reaction is split on, like, what does that mean?
[00:49:41] And in a sense, I think what's cool is some of this research is, like, free of opinion or just something like this is what happened.
[00:49:47] You feel free to, you know, from that, conclude that the model is thinking or is not thinking.
[00:49:53] And half of the people will say, like, well, you know, it told you that it was carrying the one and it didn't.
[00:49:59] And so, clearly, it doesn't even understand its own thought.
[00:50:01] And so, clearly, it's not thinking.
[00:50:02] And then half of the other people will be like, well, you know, when you ask me 36 plus 59, I also kind of, you know, I know that it ends at five.
[00:50:09] I know that it's roughly, like, in the 80s or 90s.
[00:50:12] I have all of these heuristics in my brain.
[00:50:14] As we were talking about, I'm not sure exactly how I compute it.
[00:50:16] I can write it out and compute it, you know, the longhand way.
[00:50:19] But the way that it's happening in my brain is sort of, like, fuzzy and weird.
[00:50:22] And it might be similarly fuzzy and weird to what's happening in that example.
[00:50:25] Humans are notoriously bad at metacognition, like thinking about thinking and understanding their own thinking processes.
[00:50:31] Especially in cases where it's, you know, immediate, reflexive answers.
[00:50:35] So why should we expect any different for models?
[00:50:40] Josh, what's your answer to the question?
[00:50:42] Like Emmanuel, I'm going to avoid the question and just sort of be like, why do you ask?
[00:50:48] I don't know.
[00:50:49] It's sort of like asking like, does a grenade punch like a human?
[00:50:51] Like, well, there's some force.
[00:50:54] Yes.
[00:50:55] You know, and maybe there are things that are closer than that.
[00:50:57] But like, if you're worried about damage, then I think understanding, you know, where does the impact come from?
[00:51:03] What if the impetus of this is maybe like the important thing?
[00:51:08] I think for me, like, do models think in the sense that they like do some like integration and processing and sequential stuff that can lead to surprising places?
[00:51:17] Clearly, yes.
[00:51:19] It'd be kind of crazy from interacting with them a lot.
[00:51:23] If there would not be something going on, we can sort of start to see how it's happening.
[00:51:26] Then the like humans bit is interesting because I think some of that is trying to ask like, you know, what can I expect from these?
[00:51:31] Because if it was sort of like me, being good at this would make it good at that.
[00:51:34] But if it's like different from me, then like I don't really know what to sort of look for.
[00:51:38] And so really we're just looking to like understand like where do we need to be extremely like suspicious or like starting from scratch and understanding this?
[00:51:46] And where can we sort of just reason from like our own like very rich experience of thinking?
[00:51:50] And there I feel a little bit trapped because as a human, like I project my own image constantly onto everything.
[00:51:58] Like they warned us in the Bible where I'm just like this piece of silicon.
[00:52:01] Like it's just like me made in my image where like to some extent it's been trained to like simulate dialogue between people.
[00:52:08] So it's going to be very like person-like and it's affect.
[00:52:11] And so some humanness will get into it simply from like the training.
[00:52:15] But then it's like using very different equipment that has like different limitations.
[00:52:18] And so the way it does that might be pretty different.
[00:52:20] To Emmanuel's point, I think the, yeah, we're in this tricky spot answering questions like this
[00:52:26] because we don't really have the right language for talking about what language models do.
[00:52:31] It's like we're doing biology but, you know, before people figured out cells or before people figured out DNA.
[00:52:38] I think we're starting to fill in that understanding.
[00:52:40] Like, you know, as Emmanuel said, there are these cases now where we can really just go read our paper.
[00:52:47] Like you'll know how the model like added these two numbers.
[00:52:49] And then if you want to call it human-like, if you want to call it thinking, or if you want to not, then it's up to you.
[00:52:54] But like the real answer is just like find the right language and the right abstractions for talking about the models.
[00:53:00] But in the meantime, when we've only, currently we've only kind of like, you know, 20% succeeded at that scientific project.
[00:53:07] Like to fill in the other 80%, we sort of have to borrow analogies from other fields.
[00:53:12] And like there's this question of which analogies are the most apt?
[00:53:15] Should we be thinking of the models like computer programs?
[00:53:17] Should we be thinking of them like little people?
[00:53:20] And it seems to be like sometime, like in some ways that think of them like little people is kind of useful.
[00:53:26] It's like if I like say mean things to the model, it like talks back at me.
[00:53:29] That's like what a human would do.
[00:53:30] But in some ways it's like clearly not the right mental model.
[00:53:33] And so we're just kind of stuck, you know, figuring out when we should be borrowing which language.
[00:53:38] Well, that leads on to the final question I was going to ask, which is what's next?
[00:53:41] What are the next pieces of scientific progress, biological progress that needs to be made for us to have a better understanding of what's happening inside these models?
[00:53:51] And again, towards our mission of making them safer.
[00:53:55] There's a lot of work to do.
[00:53:58] Our last publication has some like enormous section on the limitations of the way we've been looking at this.
[00:54:04] That was also a roadmap to like making it better.
[00:54:06] You know, when we are looking for patterns to like decompose what's happening inside the model, we're only getting sort of, you know, maybe a few percent of what's going on.
[00:54:16] There's large parts of how it moves information around that like we explicitly like didn't capture at all.
[00:54:23] They're scaling this up from the sort of small, you know, production model we use to like the biggest models.
[00:54:30] So you were looking at Claude 3.5 Haiku, right?
[00:54:33] That's right.
[00:54:34] Which is like, it's like a pretty capable model very fast, but it's like by no means as sophisticated as, you know, the Claude 4 suite of models.
[00:54:42] So those are almost like sort of like technical challenges, but I think, I think Emmanuel and Jack might have some takes on the like, some of the like scientific challenges that come after solving those.
[00:54:50] Yeah.
[00:54:51] Yeah, I mean, I think maybe, maybe two things I'll say here, which is one consequence of what Josh has said is that, you know, out of the total number of times that we ask a question about how the model does X, right now we can answer probably a small, you know, 10 to 20% of the time we can tell you after a little bit of investigation, this is what's happening.
[00:55:11] Obviously we'd like that to be a lot better and there's, there's a lot of kind of clear ways to, to, to get there and less and more speculative ways as well.
[00:55:20] And then I think, I think that we've talked a lot about is this sort of idea that a lot of what the model does isn't simply like, ah, how is it saying the next thing?
[00:55:30] We talked about it a little bit here.
[00:55:31] It's sort of like planning a few things again and I, a few words ahead, sorry.
[00:55:35] And I think we want to understand sort of like over a long conversation with the model, sort of like how is its understanding of what's happening changing, you know, how is its understanding of who it's talking to changing and how does that affect its behavior?
[00:55:49] More and more sort of the, the actual use case of models like Claude is, you know, it's going to read a bunch of your documents and a bunch of like email you send or your code and based on that it's going to make one suggestion.
[00:56:01] And so clearly there's something really important happening in that space where it's reading all these things.
[00:56:06] And so I think understanding that better seems like a, like a great challenge to take on.
[00:56:10] Jack?
[00:56:11] Yeah, I think we often use the, the analogy on the team of that we're building a microscope to like look at the model.
[00:56:18] And right now we're in this exciting but also kind of frustrating space where our microscope works like 20% of the time and like to look, looking through it is like requires a lot of skill.
[00:56:30] And like takes, you know, you have to like build this whole big contraption and like infrastructure is always breaking.
[00:56:37] And then like once you've got your like explanation of what the model is doing, you have to like throw like Emmanuel or me or someone else on the team in a room for like two hours to like puzzle out what exactly was going on.
[00:56:48] And like the really exciting future that I think we could be at within, you know, year or two years, you know, that kind of time scale is, is one where like just every interaction you have with the model can be under the microscope.
[00:57:00] Like we can just, anytime, there's all these like weird things the models are doing and we just want it to be like push of a button.
[00:57:07] Like you're having your conversation, you push a button, you get this flow chart that tells you like what it was thinking about.
[00:57:13] And once we're at that point, it's, it'll be this like, I think our, the interpretability team at Anthropic, I think we'll start to kind of take on a bit of a different shape in that instead of this like team of kind of like engineers, scientists thinking about the like math of how like language models work on the inside.
[00:57:31] We're going to have this like army of biologists that are just looking through the microscope that we're just, we're talking to Claude, we're getting it to do weird things.
[00:57:38] And then we're just like, we got people looking through the microscope seeing like what it was thinking on the inside.
[00:57:42] And I think that's kind of the future of, of, of this work.
[00:57:45] Maybe two, two notes on top of that.
[00:57:47] One is like we want Claude to help us do all of that because like there's a lot of parts involved.
[00:57:52] And you know, who's like good at like looking at like hundreds of things and figuring out what's going on is like Claude.
[00:57:57] And so I think we're trying to enlist some help there, especially as for these complicated contexts.
[00:58:02] And maybe the, the other place is like, we've talked a lot about studying the model like once it's fully formed, but of course like we're at a company that makes these.
[00:58:10] And so when it says, okay, here's how the model like solve this particular problem or said this thing, where did that come from kind of in the training process?
[00:58:18] What are the steps that sort of like made that circuitry sort of form to do that?
[00:58:22] And how could we give feedback to the rest of the company that is like doing all of that work to shape the thing that we like actually wanted to become?
[00:58:31] Well, thank you so much for the conversation.
[00:58:33] Where can people find out more about this research?
[00:58:36] So if you want to find out more, you can go to anthropic.com/research, which has our papers and blog posts and fun videos about it.
[00:58:43] Also, we recently partnered with another group called Neuronpedia to host some of these like circuit graphs we make.
[00:58:48] So if you want to try your hand at looking at what's going on inside of a small model, you can go to Neuronpedia and see for yourself.
[00:58:55] Thank you very much.
[00:58:56] Thank you very much.