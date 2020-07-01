# Facebook Messenger JSON Parser
Parse your (downloaded) Facebook Chats!

As someone who uses Messenger for a majority of their chats, 
I always wanted to know my chat's stats, such as common words, phrases,
emoji reactions (Given and Received), total messages sent, etc. All the good stuff.

So, I designed this application (As well as an HTML version if you want the legacy way - Check it out 
[Here](https://github.com/artyomos/facebook-messenger-parser)) to parse my chats (and yours too if you want)



## How it Works
As it works right now:
1. Take your data from facebook take-out for messenger
2. Wait for Facebook to eventually look at your request in 5 years
3. Open your zip file containing your data (after downloading), and look for the inbox folder for messenger
4. Select one of your chats you would like to parse (I usually choose my largest one) and open that folder for the corresponding chat
5. The structure will be `/Inbox/<your chat>/message_1.json` within the folder (If not, facebook may have changed file structures and please submit an issue)
6. Please take `message_1.json` and copy it into this script's main folder
7. The structure will be `/Facebook-Messenger-JSON-Parser/main.py + message_1.json`
8. Assuming you have Python Installed `(3.8 Recommended, 3.6 minimum)`, double click `main.py`
9. The file will run, complete, and create a text file of your chat as `messenger_stats_<your_chat>.txt`
10. Browse your file to your heart's content! If you have suggestions please let me know what I can add 😄

***Have this Happy Fox for making it all the way down***
![image](http://i.imgur.com/WhZThdw.jpg)
