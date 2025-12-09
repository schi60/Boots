# Home Sweet Home by Boots
Home Sweet Home is a murder-mystery game: a website designed like a house, with interactive features and clues posted throughout each room for the user to explore. To enter the house, the user needs to register and log in. At the end of the exploration, you will need to figure out the murderer to win. Found clues can be tracked on the homepage. 


# Roster:
<br>
Sophia C ~ Project Manager <br>
Emaan A ~ Devo 1 <br>
Jun Jie L ~ Devo 2 <br>

<br>

# Description:
When you enter the website, you will end up on the house's front lawn. To unlock the door and enter the home, you will need to create an account and log in. In the bedroom, you can browse the book of jokes (Joke API) and the MET Museum book (MET API) you bought recently on your bookshelf during your vacation. In the living room, you can browse the movie catalog and the cat album (Cat API) on the table. In the kitchen, you can flip through the Recipe book (FreeRecipe API) and click on the wall calendar to get facts about holidays (Holiday API). Clues will be scattered throughout each room for user to find. 


# Install Guide:
#### Prerequisites
- python 3 installed
- git installed

```
git clone https://github.com/schi60/Boots.git
cd Boots
python -m venv ~venv
source venv/bin/activate
pip install -r requirements.txt
```

# Launch Codes: 
```
cd Boots
cd app 
python build_db.py
python __init__.py
```
