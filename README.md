# Writing Spells in D&D

The goal of this is to make a more robust package for my spellwriting system (detailed [here](https://www.drivethrurpg.com/en/product/429711/the-spell-writing-guide), though it has updated now)

I'll eventually make a short explainer video and link it here but also maybe a better short explanation here too.

I like to think I've grown as a developer since I wrote the original repo so fingers crossed that's true...

# TODO

There's a few things I want to add to this that should make life easier

- [ ] a spell json so that the attributes can be loaded (i.e. you could run `writer.py -<spell_name>` and get the output)

- [ ] Functions for outputting the two parsable methods, one is the connections array and the other is the more standard binary string method
    - I will add some detail about these but basically the connections array is a NxN array that has elements $N_{i,j}$. If points $i$ and $j$ are connected then element $N_{i,j}$ is 1, if not its 0. This is really useful for some things like encription and graph making so it's a useful form of the spell.
- [ ] Compatibility with non-wizard systems too