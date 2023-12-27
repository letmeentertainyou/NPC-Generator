This program combines a bunch of text files representing DM tables and uses them to generate custom
NPCs or level 1 player characters. My DM guide is still in the mail so I apologize for any incorrect
stats those will be fixed soon.

I did apply a few stat buffs beyond level 1 for the NPCs because they won't have all the cool class/race
abilities the player characters have.

You may use your own tables as drop in replacements for everything except jobs.txt and race.txt
because those tables have hardcoded bonuses. I will explain how to expand that part of the code in
another document.

To use simply run:
$ python3 NPC.py

Without any arguments a level one character will be created. 
You can also give a single integer as an argument to generate a character at that level.
$ python3 NPC.py 20

Note that NPC.py needs to be in the same directory as the tables/ directory or nothing will happen.

---

For my private games I am using some custom tables not provided in this repo. I do not have the 
rights to publish those tables so I provided some very short example tables instead. 

I do have the ability to link you to the custom tables I used and you can do with those links what 
you wish!

TABLE LINKS!
I do not in any way vouch for the security or safety of these websites. Always use an ad-blocker
and HTTPs when visiting random websites.

Female Names:
https://www.cs.cmu.edu/Groups/AI/areas/nlp/corpora/names/female.txt

Male Names:
https://www.cs.cmu.edu/Groups/AI/areas/nlp/corpora/names/male.txt

Family Names:
The family names list is unsorted, and contains duplicates of every name. As well as names that
don't contain any vowels which are useless in English. You can adjust that list with a few
simple commands in Bash/Python. Good luck, and God Speed!
https://www.cs.cmu.edu/Groups/AI/areas/nlp/corpora/names/other/family.txt

Quirks:
This link is an awesome resource that really inspired my creativity. There are over 200 quirks listed
and a few of them are repetitive or don't seem fun to role-play. I just read through the list and
picked out my favorite 70ish. This should get you started and you can easily add more as you think
of them.
https://kindlepreneur.com/character-quirks/

Motivations:
These are 30 very well written prompts!
https://www.writerswrite.co.za/30-character-motivations-to-kickstart-your-story/

Hair, Eyes, Skin-tone:
This link has almost the exact same table for all three attributes. I liked their hair table enough
to use it and I recommend you copy that table yourself. I did need more creative/expressive colors
for eyes and skin-tones and so I have provided the full tables that I wrote after doing a fair
amount of research. Feel free to use the provided eyes/skin-tones tables for any OGL/CC compatible
purposes.
https://www.dandwiki.com/wiki/Random_Hair_and_Eye_Color_(DnD_Other)
