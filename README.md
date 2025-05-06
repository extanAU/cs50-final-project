# cs50-final-project
BlackjackBot! 

Ethan Tan & Christoph von Pezold

Planned Website Outlook: 
- Login (user/password with error message -> joker error message?)
- Home Page -> a "play" and three accordions on about us, what the game is/how to use it, why we wanted to code this game, what math went into the coding of this game -> Christoph can start to write this up? 
- Blackjack Game (normal interface with buttons for actions e.g. hit/stand/deal/split/double/increase bet with slider, chip counter and BOT mode, both basic and advanced help)
- User (showing name, password, chip counter, "reset" button to regain 100 chips and counter )


To Do List (In Pseudocode):
- Figure out Login System + User Database (probably same as finance, just pull the code out)
- Code up a basic home page with bootstrap and accordions (make it as fancy as possible with templates)
- Code the "user" interface -> just showing the user details and the chip counter/reset button, should start with 100 chips 
- Encode blackjack logic and map cards to the visual static JPEGs (animate hit/stand/double/split/bust)
    - Specifically make the "actions" for blackjack work and also create a viable "house" -> one that hits until 17 then stands 
    - Note: once we have this, we basically already have a working game which is great 
- Encode the "bot" which is the hard part (two parts to this as well)
    - There will be the "easy" bot -> where basically you calculate the number/size of the cards you already have, then build a SQL table using Flask that literally just matches the key for each of the information given to you, then just spits out an output (refer to the tables which we found online that encodes that information, yippee) -> bot should also tell you how much to bet, specifically around 1-2% but goes up to 5-10% depending on the count of the deck (see below) 
    - To BUILD UP this easy bot, we should incorporate the idea of "counting cards" -> ie. create a toggled "count" which counts 2-6 as +1 and 10-K as -1, then it will tell you how much to size the bet depending on that given count 
    - Then there will be a "hard" bot (we will actually have to do math for this lol) that will create an array or table that keeps track of every single hand that is dealt and just what cards are still in the deck (assuming a six deck casino) = we can also change the number of decks the casino is using as well maybe? from one to eight? that is something else entirely 

static: 
- Find bootstrap template we like for homepage + flask/Jinja/CSS code -> this is going to be for our homepage 
- Add in nice felt covers for board (and pile of chips maybe)  

Planning: 
- Encode everything up until the actual "bot" by Friday/Saturday
- By Sunday, the basic game should at least be up. Sunday we can spend tweaking or building up the bot -> also note we can do it after as well a little just to debug it if necessary 
