# Home Sweet Home by Boots
Home Sweet Home is a website that allows users to hang out and explore their virtual home. Each tab will represent a different room and will contain its own interactive features, operated using APIs, to explore.

# Roster:
<br>
Sophia C ~ Project Manager <br>
Emaan A ~ Devo 1 <br>
Jun Jie L ~ Devo 2 <br>

<br>

# App Description:
When you enter the website, you will end up on the house's front lawn. To unlock the door and enter the home, you will need to create an account and log in. In the bedroom, you can browse the book of jokes (Joke API) and the MET Museum book (MET API) you bought recently on your bookshelf during your vacation. In the living room, you can browse the movie catalog and the cat album (Cat API) on the table. In the kitchen, you can flip through the Recipe book (FreeRecipe API) and click on the wall calendar to get facts about holidays (Holiday API).


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
