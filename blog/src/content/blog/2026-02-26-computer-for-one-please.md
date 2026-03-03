---
title: "Computer for one, please"
description: "When AI has all the answers, how do you know what questions to ask?"
pubDate: "2026-02-26"
tags: ["meta", "pet-project", "ai"]
draft: true
---

I *really* like mini-computers & microcontrollers. Maybe because I can hold such powerful and <a href="https://en.wikipedia.org/wiki/Clarke%27s_three_laws" rel="_self">magical</a> things in the palm of my hand. I can write things to it, and have them interact with the world that I know and that feeling is (forgive me here), _electrifying_. 

I've embarked on hardware projects a few times over the past few years, but never really got far enough into them to understand how they work. Partly because I was getting discouraged whenever I would accidentally brick a device, or that the rust tooling wasn't mature enough to do anything that I could engage with. Maybe I need to think a bit more creatively, but at a more grounded level - this time I wanted to start a bit simpler and do something that I have long taken for granted: building a self-hosted web service.

Do I intrinsically know how DNS works? Kind of. Security? TLS Handshaking? Port 80/443? ...Maybe? I can give answers, but there will be a nag in the back of my mind that doesn't express confidence. Maybe I can use AI to help me plan & execute on building this application.

I sometimes fall into a trap where I have the end goal in mind, a rough idea on the work involved and barely a thought on the foundational efforts that would be necessary. My experience with AI tools makes this undesirable habit more visible because I follow that pattern within a single session of AI prompting. That is not a good use of my time, or the resources involved in generative AI. One must give more thought to _thought_ - to be more comfortable with writing out one's ideas, knowledge of the problem space, what constraints there are, if any, etc before one even so much as considers bringing in AI. This is a skill that I have become more acquainted with in my recent years in software development, and has become an invaluable to learn (which also conveniently transfers over quite well to AI use). So, what does careful planning look like (in brief)?

### The Problem

I am neurodivergent; I can be forgetful at times. Despite this, I think often about what needs doing, and how to get there. If only I could just remember to write it down. Certainly tools like todo lists, etc already exist. Building one wouldn't have been worth the effort, but AI makes the jump from "wouldn't it be nice if..." to "this internal dashboard keeps me on track on a day-to-day basis". For example, I look in the fridge and realize we're short on yogurt. _I Should Buy Some Yogurt_. I close the fridge door, and notice a sharp-shinned hawk perched near my backyard window (I absolutely adore raptors). That memory of what I need to do has been garbage collected. Fast forward to tomorrow morning, I don't have yogurt to go with my granola for breakfast. Big Sad.

### The Idea

Already you can speak into your phone and say something like "add a reminder to buy yogurt next time I'm at the grocery store". Bingo, a reminder is setup. Cool. But it's a solved problem. Until recently, I had no idea what [iOS shortcuts](https://support.apple.com/guide/shortcuts/welcome/ios) were, and that you could

1. create a custom voice prompt like "hey buddy"
2. convert speech-to-text on all words after the prompt
3. with that text, make a POST request (!)
4. Trigger a GET request when you're near or at the grocery store (!!!)

I want this. I want this for me. I've never been more excited to make a grocery list.

### The Challenge

I tested a bit with the shortcut iOS feature; confirmed that I could POST a JSON body of the transcribed speech. So to receive that information will require an API. An API will need a web application to process the requests, a storage solution, and where it would live.

### The Solution

We're still in the age of cloud computing, and having a service that would be able to handle the aforementioned requests (& manage them) is something that a traditional cloud infrastructure could easily handle. But (again), that's boring. I have a PI. Traffic that hits my domain can be [tunneled](https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/) to the PI. Is it inefficient? Probably. Does that matter? No! So that's what I'll be working on and _because_ it's a small project and where UI design is less important, I will let AI handle it (but not without proper planning!).

### The Product

We'll see how this experiment turns out. Eventually I want this dashboard to include other home devices — controllable remotely. That's where the fun really begins.