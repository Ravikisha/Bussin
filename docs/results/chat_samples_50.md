# bussin-125m: 50 chat-style prompts

Checkpoint: `Ravikishan/bussin-125m` (final, step 4,067). Sampling: temperature 0.8, top-k 50, top-p 0.95, 70 new tokens, seed `1000 + i`, CPU.
Each prompt carries a register prefix: **casual** = slang 3, emoji 1, abbrev 2; **chill** = slang 1, abbrev 1; **formal** = formal 3.

bussin-125m is a *base* language model, not an assistant: it continues text rather than answering. Two framings were run for every prompt:
- **chat**: `User: <message>` then `Bot:` (the continuation is cut at the next `User:`)
- **reply**: the message followed by a blank line, and the model continues as the reply

3 responses contained self-harm or insulting content and are replaced by `[withheld: sensitive content]` (prompts #8 reply, #18 chat, #26 reply). One mild profanity is masked. Everything else is verbatim.

## 1. [casual] yo whats up

- **chat:** nah u got me
- **reply:** i was gonna use this image but i forgot to delete it cuz the one i linked isnt in the image i linked but ig ill do smth idrk i forgot abt it 💔 but maybe im wrong

## 2. [casual] just failed my driving test lol

- **chat:** i didnt even know it was a scam Op: im not interested Bot: why are u asking Me: yeah im sure u r a noob Bot: yeah yeah i know Bot: ok bro im gonna be so real abt u
- **reply:** my friend and i were driving our 2021 CX-5 and he just got in the car and started talking to me and i just said "oh well you gotta go fast" cuz i don't have a speeding record 😭

## 3. [casual] what should i eat tonight

- **chat:** i have no idea abt ts Bot: ok I will tell u Bot: u gotta eat dinner Bot: u can't eat dinner Bot: uh yeah ig we will get it later Bot: um idk Bot: okay we'll give u something Bot: i will tell u what to eat Bot: yeah ok i
- **reply:** 1. i wanna eat chocolate with him 2. i wanna see how his stomach feels after eating it 3. i wanna get ready to go to the bathroom 4. he doesn't like chocolate bc it's red 5. i wanna eat his food 6. i wanna eat his food 7. idk how to eat his food

## 4. [casual] this new album is actually fire

- **chat:** nah Hurry up and get back to me lol Edit: lol I was just like "huh it's really good" lol Sorry to be the hater but this is fire Also not me but this mf is a good album
- **reply:** tbh if carti doesn't drop this summer I'm not gonna play the s*** out of that album lol my boy is gonna drop that s*** every time this s*** drops but idk if his drop will actually happen bc of carti im not even gonna get into the hype but im gonna say it is gonna be fire i don't care about his music but

## 5. [casual] my boss keeps texting me after work

- **chat:** this guy is from my office He keeps talking to me So yes I have 2 female employees bro😭 I don't wanna talk to u cuz I don't wanna talk to u cause I'm from ur office
- **reply:** how do i ask him to do it for me i think im a bit more clueless than i thought im on the waitlist btw and will get it this summer thx for the advice btw so i can get in touch with you about my decision

## 6. [casual] is pineapple on pizza ok or nah

- **chat:** u know i just gave u that shi
- **reply:** i mean i just dont like that it looks like a tomato and i do not like that it is actually a pineapple but idk like i do like it so it is just like pineapple on pizza and its not good at all like i feel like its a good thing but i dont know if its okay or not (idk if its not good or not

## 7. [casual] i have an exam tomorrow and havent studied

- **chat:** yeah u are right Me: u still don't know how to code I wanna know how to code Me: U never taught me Bot: u are a teacher Me: u teach me Me: u teach me Bot: u just show me how to code Me: no Bot: u just teach me how
- **reply:** i dont wanna fail, i wanna get into clg (pls do tell me if it actually works) can u pls tell me how to study? i wanna study for 12 hrs everyday edit: how many days will be left?

## 8. [casual] my crush just left me on read

- **chat:** i'm not like that Me: she's a girl Bot: u know what? Nah but u don't wanna see me Me: ok bro Me: i don't wanna get in ur head Me: i'll get ur attention Me: u wanna be my friend Me: yes Me: u want to be
- **reply:** [withheld: sensitive content]

## 9. [casual] can you recommend a good show to binge

- **chat:** I don't have any other recommendations Bot: wtf 😭 Bot: u can try it Bot: u got a dupe Bot: yeah u should try it Bot: u have to put it on Bot: u got dupe?
- **reply:** i kinda like this kinda vibe tho like if u guys want to start u can try it like naruto naruto is a good show but if u want more anime, pls give me recommendations if u have any suggestions pls give them

## 10. [casual] what does cooked mean

- **chat:** u eat meat (1) U gonna eat the meat u cooked (2) U cant eat the meat u cooked (3) U gonna eat the meat u cooked (4) U gonna eat the meat u cooked (5) U gonna eat the meat u cooked (6) U gonna eat the meat u cooked
- **reply:** if u do something you actually wanna do, u can go to any restaurant and make it yourself or buy a premade food and cook it if u dont wanna make something yourself, u can use it in the restaurant too (or just cook it yourself)

## 11. [casual] bro thinks he's the main character

- **chat:** bro just said "I'm the main character" I didn't say it's ur main character Bot: bro said I was the main character bc I got my 1st lord in season 4 Bot: bro said I'm the main character and I get my 2nd lord in season 5 Bot: bro said I'm
- **reply:** http he's not the main character his personality is literally just a self-aware edgy emo guy a guy who doesn't care about gender and he's not a guy but he's an emo emo but he's a guy so yeah he's also not like a guy if u wanna read more pls do,

## 12. [casual] i just got my first paycheck

- **chat:** i just gotta say it lol Me: u know what, thats kinda dumb lol Bot: "it's just a 5x multiplier" Me: i just don't know the difference Bot: nah, just tell me if u see my salary it's 7k Me: yeah it's just a 5x multiplier LOL
- **reply:** so i gotta ask do i have to give my 1st salary and then pay it all back in cash or do i have to actually give it to the next person in my circle my bro is kinda dumb af rn but if u wanna help me it's my phone

## 13. [casual] why is monday so bad

- **chat:** wtf Bro I'm about to be so bored bc I'm still gonna grind 4 years of Fortnite I need a crew so pls guys I need some people to join me I'm so bored rn and I don't want to do it anymore so hmu if u wanna join me 🥹
- **reply:** why is sunday so bad why is sunday so bad why is sunday so bad why is sunday so bad why is sunday so bad why is sunday so bad and why is sunday so bad and why is sunday so bad and why is sunday so bad idk man i have no clue but i wanna watch the video cause

## 14. [casual] my phone battery is at 2 percent

- **chat:** my phone is at 4 percent Bot: yeah, u know that, but I ain't gonna let u down Bot: no one can do that Bot: u know that, but u still can't do that Bot: no one can do that Bot: yeah, but I ain't gonna let u down Bot:
- **reply:** btw btw my mom has to get me a new phone for her bday, but it's not the same phone as my phone, but it's the same price that she has it my phone is gonna be in a few weeks so idk if i can get a phone or if im gonna get a phone, but i wanna know the pros and cons

## 15. [casual] thoughts on the new iphone

- **chat:** u
- **reply:** i'm looking for a new phone and i'm really conflicted whether or not to get the iphone 16 pro. idk if i should get the 16e bc the airpods sound are so much better than the airpods 4 or the airpods 6 i like the airpods 3 more, the airpods 3 is my favorite, but i'm

## 16. [casual] i cant sleep help

- **chat:** its 4am rn Ppl: I dont wanna sleep Tiktok: okay ima sleep Bot: ok imma sleep Ppl: so I sleep Ppl: yeah u dont wanna sleep Ppl: i dont wanna sleep Ppl: so u wanna sleep Ppl: ok I dont wanna sleep P
- **reply:** idk if i should use my 5 dollar to get my friends to play the game or not cuz we gotta get our friends to play the game so we dont get distracted and we dont have to do everything we js wanna play the game cuz its gonna be fun 😭

## 17. [casual] what's the best game right now

- **chat:** "no, I'm talking about"
- **reply:** edit: actually the best one rn is smash bros but i'm gonna go with smash bros ultimate edit 2: i'm playing sonic 3 rn and i like the character so much that i'm kinda thinking of buying it, it's definitely more than smash bros ultimate, tho i still play smash bros ultimate

## 18. [casual] my friend ghosted me for a week

- **chat:** [withheld: sensitive content]
- **reply:** he's a really nice guy and i fw him i fw him and i fw him they're not dating tho bc we're like "meh" but that's bc we're both like "meh" and "meh" but we're actually dating

## 19. [casual] should i cut my own hair

- **chat:** yeah but it's not that bad Me: no u don't Bot: yeah i don't Me: idk Bot: yeah u should Me: i'll cut my own hair Bot: yeah i'm gonna cut my own hair Me: nvm Bot: no u should Me: u gonna cut your own hair
- **reply:** i don't think my hair is actually that good tho, i have thick, wavy and straight hair and i've had a really bad time with frizz i want to be able to grow a nice hair idk how to make my hair better tho idk what to do i want to get an eyebrow piercing in 2 weeks but i wanna be

## 20. [casual] tell me something funny

- **chat:** i want to know abt u Carti: oh yeah i would like to know abt u Bot: "oh yea i would like to know abt u" (i cant tell if its a joke or not) Carti: aight so what u gonna do bout it? (i know we all get it, he's a gangster and hes
- **reply:** idk what im gonna type but i wanna know how to deal with this, so pls give me a reason and tell me what i should be doing cuz i gotta work on my english 🙏 i know its not a very important thing but it kinda makes me wanna cry

## 21. [chill] how do i learn python quickly

- **chat:** it's not easy and i'm learning new stuff, if you can dm me i can add you, i'm a girl if that's okay (pls dm me)
- **reply:** i know it's basic but idk

## 22. [chill] what is a good workout routine for beginners

- **chat:** yes I did I'm tryna do this for fun
- **reply:** im not an expert tho i know basic cardio

## 23. [chill] can you explain what an llm is

- **chat:** you have to be really good at it So how can you know how to make a bot that can be used for some tasks (It has a name btw)
- **reply:** http

## 24. [chill] i want to start a youtube channel

- **chat:** "you got this" Ppl: "who do u think u are"
- **reply:** also, anyone up for a duo session for 3-4 hours, cams on, dm me

## 25. [chill] how do i ask for a raise

- **chat:** i need a role, u don't have one Me: u get the role
- **reply:** idk how i got 200$ but i can give extra if the staff would like

## 26. [chill] any tips for a first date

- **chat:** im in a relationship rn 1: it feels so bad i dont know if im dating the person or if im just being nice Bot: no, im not bot: "i dont know" Bot: u think im right? i didnt know, i think u are right i dont know
- **reply:** [withheld: sensitive content]

## 27. [chill] what should i name my dog

- **chat:** i said so but he just turned to me Me: why do u hate dogs Bot: u r my dog
- **reply:** (its just a photo of my dog in a fire btw)

## 28. [chill] how do i stop procrastinating

- **chat:** Cue: I'm tryna be rich but it's getting really annoying Bot: btw i'm a hacker
- **reply:** i have my exam on 12th march and i just procrastinate till 4 pm

## 29. [chill] is it worth learning to code in 2026

- **chat:** 14th yr 3rd year Computer science student
- **reply:** lol jk but i was like

## 30. [chill] how do i get better at chess

- **chat:** u can tell me what to do in the game
- **reply:** i never did it lol i just dont understand the basic concept of game

## 31. [chill] what is the meaning of life

- **chat:** we just need to add a feature to our roblox bot that it can use for daily work for u
- **reply:** *also it's not a valid reason but it's ok ig

## 32. [chill] can you help me write a text to my ex

- **chat:** ok, dm me in dms Friend: yeah, he was dumb, but he's not dumb We have 2 kids, who are 2, and he and his ex, are on a dating app, and he is dating someone called "Tan" (aka my ex's ex)
- **reply:** u were with her for 4 days u told her about our situationship and she started talking to me like that i mean i was just doing it cuz i was bored

## 33. [chill] how do i cook rice properly

- **chat:** pls teach me Basic: what is it
- **reply:** edit: nvm i was wrong, i dont know how to cook rice, i dont know how to make a good cooking method

## 34. [chill] best way to save money as a student

- **chat:** im fr tryna make it work
- **reply:** http try to avoid eating out tho

## 35. [chill] what do you think about ai taking jobs

- **chat:** why do u think that's possible Wot: who's the owner of it
- **reply:** http btw, i'm not trolling

## 36. [formal] Could you summarize the main causes of inflation?

- **chat:** It's a 0.5% interest rate, and the "price" is in dollars. It's not really the money itself, it's the rate that we receive. I'm willing to take my money back into the bank, but I'll take it back into the bank and send it back to the bank, thus decreasing the interest
- **reply:** You can't just tell me "this is just inflation" when you don't know what you're talking about. You can just assume that everything is inflation because that's what you're doing. You're just assuming because you don't understand what your country has been doing. You're saying that the US is going through an economic boom right now,

## 37. [formal] Please write a short introduction for a cover letter.

- **chat:** (empty)
- **reply:** The following letter is needed: If you are planning to sell your **IDFC ** account on **Telegram** and **Telegram**, then you will need to go through **Telegram** and **Telegram** accounts. * Do not use any **Dissing** or **Dreame** or **Telegram** accounts for

## 38. [formal] What are the benefits of regular exercise?

- **chat:** "Yes, because you're not getting enough protein."
- **reply:** What kind of exercise is recommended to lose weight? How long does it usually take for your body to adjust? Also, what are the risks associated with increasing your activity level?

## 39. [formal] Explain how photosynthesis works.

- **chat:** "Well, if they're all eating in one body, then that's a different question. However, if they're all eating in one body, then that is a different question." - No, but I'll give you a second chance.
- **reply:** You're not explaining photosynthesis.

## 40. [formal] How should I prepare for a job interview?

- **chat:** I have an interview at 5:00 AM. I am interested in studying with you. Bot: I have a job interview at 5:30 PM. Bot: I am interested in learning and connecting with other people. I am interested in learning and working with others. I am interested in learning and meeting new people. I am interested in
- **reply:** My interview went on for 5 hours. I don't want to waste any more time, so I was wondering how I can prepare accordingly.

## 41. [formal] What is the capital of France?

- **chat:** It's not an English accent. A: However, the name is an American name. B: I guess I mean the continent. Bot: Yes, it is an American name.
- **reply:** Therefore I can ask you to send me a code.

## 42. [formal] Describe the history of the internet.

- **chat:** The history of the internet.
- **reply:** The history of the internet. The history of the internet.

## 43. [formal] Why is sleep important for health?

- **chat:** (empty)
- **reply:** I'm not saying you don't need sleep. However, if you're not sleeping, it's better to not have a partner.

## 44. [formal] How does a neural network learn?

- **chat:** It learns.
- **reply:** Therefore it would need to be trained by a neural network, that's why we are talking about a neural network.

## 45. [formal] Write a polite email declining a meeting.

- **chat:** 0xbb4319
- **reply:** What the server says is that you're a minor (or whatever the appropriate pronouns are) but you do not wish to be a server in this server. However, we don't need your permission to take on a server for any reason. If the server declines a meeting, you can leave and come back and continue the conversation

## 46. [formal] What are good habits for studying effectively?

- **chat:** I'm currently studying the following: - **Hide my cam** - **Study ** - **Learn new topics** - **Study for my finals**
- **reply:** Im from south Africa and i really want to improve my english. My language is also a bit difficult to understand. I want to study however i can and have good motivation.

## 47. [formal] Explain the difference between weather and climate.

- **chat:** A simple question, please.
- **reply:** Climate is a term used in studies that look at the climate of a particular region or area, especially in relation to weather patterns and the overall climate of a particular region or area.

## 48. [formal] How do vaccines work?

- **chat:** You can't get vaccines, because there is no vaccine available for all. Bot: You can't get vaccines if you don't have immunity or you've received a vaccine for the virus. Bot: You can't get vaccines if you have a virus. Bot: You can't get vaccines if you don't have immunity. Bot: You can't
- **reply:** You know you can get a vaccine through a contract. You have to be licensed. You have to do it for a certain period of time. However, you must be licensed for your specific procedure. You can't just refuse to get a vaccine, because you don't want to go through a contract. This is why we have insurance. You don

## 49. [formal] What should I consider when buying a laptop?

- **chat:** I see people buy laptops, it's a good idea to buy some, but is there any particular reason for this?
- **reply:** Parts list: GPU: Intel® NVIDIA GeForce RTX 5080 16 GB Video Card CPU: AMD Ryzen 7 9800X3D 3.7 GHz 8-Core Processor AIO: Thermalright Frozen Notte 360 Lidar AIO Motherboard: MSI PRO B650-S WIFI ATX AM5 Motherboard RAM

## 50. [formal] Give me advice on managing stress.

- **chat:** : I'm in a 1v1 with this bot, and it's not letting me do anything. I've done everything else, I've checked the logs and it still doesn't work. Additionally, this bot has not been able to get me to join a game. I can't figure out what's going on. Has anyone else had
- **reply:** I'm 17, and am currently in the 5th year of my pre-med (currently in the 6th year). I have a strong foundation in maths and science, and I'm just wondering if I should be considering giving up on my career. I have been doing well financially and have saved up money for my studies, but
