''' Facebook Messenger Chat Parser Version 1.0.0 - Designed on 05.05.20 by
 /$$   /$$             /$$                     /$$$$$$$                                                      /$$
| $$$ | $$            | $$                    | $$__  $$                                                    | $$
| $$$$| $$  /$$$$$$  /$$$$$$    /$$$$$$       | $$  \ $$ /$$   /$$  /$$$$$$   /$$$$$$   /$$$$$$   /$$$$$$  /$$$$$$
| $$ $$ $$ |____  $$|_  $$_/   /$$__  $$      | $$$$$$$/| $$  | $$ /$$__  $$ /$$__  $$ /$$__  $$ /$$__  $$|_  $$_/
| $$  $$$$  /$$$$$$$  | $$    | $$$$$$$$      | $$__  $$| $$  | $$| $$  \ $$| $$  \ $$| $$$$$$$$| $$  \__/  | $$
| $$\  $$$ /$$__  $$  | $$ /$$| $$_____/      | $$  \ $$| $$  | $$| $$  | $$| $$  | $$| $$_____/| $$        | $$ /$$
| $$ \  $$|  $$$$$$$  |  $$$$/|  $$$$$$$      | $$  | $$|  $$$$$$/| $$$$$$$/| $$$$$$$/|  $$$$$$$| $$        |  $$$$/
|__/  \__/ \_______/   \___/   \_______/      |__/  |__/ \______/ | $$____/ | $$____/  \_______/|__/         \___/
                                                                  | $$      | $$
                                                                  | $$      | $$
                                                                  |__/      |__/

Please see the README.md file for help in running this file.
'''



import re #regex
import json
from collections import Counter

''' messages stuff 
    "messages": [
    {
      "sender_name": "Alexander Romios",
      "timestamp_ms": 1566414701429,
      "content": "Bruh",
      "type": "Generic"
    },
    {
      "sender_name": "Tyler Batistic",
      "timestamp_ms": 1566414679970,
      "content": "Nigga meme",
      "type": "Generic"
    },
    {
      "sender_name": "Tyler Batistic",
      "timestamp_ms": 1566414674739,
      "photos": [
        {
          "uri": "messages/inbox/JammyJimmysJauntyJazzEnsemble_lIGHrATAlA/photos/69245220_1583140321820673_4997171011259465728_n_1583140318487340.jpg",
          "creation_timestamp": 1566414674
        }
      ],
      "type": "Generic"
    },
'''

def main(messenger_chat):
    print('Nate\'s Messenger (JSON) Chat Parser - Version 1.0.0')

    try:
        print('\nPlease wait while the document loads... For large files this could take upwards of several minutes...')
        with open('message_1.json') as chat:
            file = json.load(chat)
        print('File has finished loading. Parsing data...\n')
    except FileNotFoundError:
        print('Error! File not found. You must give me a message.html file to work with from Facebook Messenger!')
        return None

    # Get the current title
    current_title = file['title']

    #TODO possibly delve into images / list image amount by person etc?

    # Tell the user analysis has begun
    print(f'Performing analysis on {current_title}...')

    # Navigate to where messenger stores messages
    parser = file['messages']

    # Organizes the participants
    parse_participants(file['participants'])

    # Get the messages and sets the chat's total messages
    messages = file['messages']
    messenger_chat['total_messages'] = len(messages)

    print('\nParsing Chat Messages...')

    # Iterate through all messages and parse data
    for message in messages:
        user = message['sender_name']
        date = message['timestamp_ms']
        if 'content' in message:
            content = message['content']
        if 'reactions' in message:
            # Parse through the reactions
            parse_reactions(message)
            
        # Increase User's total message count
        try:
            messenger_chat['members'][user]['total_messages'] += 1
        except KeyError:
            print(f"Error! Discovered Missing User! (User {user})")
            continue #Skip Loop for this Individual

#below here untouched
        # Parse through the words
        if not parse_words(payload):
            # If the message is not None/empty, fix the mesage with no linebreak (</br>) statements
            if not content[1].div.contents[1]:
                message = ''
                for item in content[1].div.contents[1].contents:
                    if isinstance(item, str):
                        message += item
                payload['message'] = message
                if not parse_words(payload):
                    print("A Secondary Parse Failed... :(")
        
        # Parse through for images and videos
        parse_media(payload, message)
        # Find and parse links send in the chat
        parse_links(payload, message)

    print("Done! Analysis was successful!")
    print('\nWriting to file anaylsis results...')

    # Give a usable list in console and write to file
    with open('messenger_stats.txt', 'w') as f:
        # Header
        f.write('File Generated Using Nate\'s Messenger Parser (https://github.com/artyomos/messenger-parser)\nVersion 1.0.0\n\n')

        # Group Chat Title
        f.write('Messenger Chat: {0}\n\n'.format(currentTitle))

        # Stats
        f.write('Total Messages: {0}\n'.format(
            messenger_chat['total_messages']))
        f.write('Word Count: {0}\n'.format(messenger_chat['word_count']))
        f.write('Character Count: {0}\n'.format(
            messenger_chat['character_count']))
        f.write('Images Sent: {0}\n'.format(messenger_chat['image_count']))
        f.write('Gifs Sent: {0}\n'.format(messenger_chat['gif_count']))
        f.write('Videos Sent: {0}\n'.format(messenger_chat['video_count']))
        f.write('Audio Files Sent: {0}\n'.format(
            messenger_chat['audio_count']))
        f.write('Links Sent: {0}\n'.format(messenger_chat['link_count']))
        f.write('Reactions Given: {0}\n'.format(
            messenger_chat['reaction_count']['given']))
        for reaction in messenger_chat['reaction_count']['reaction_counter']:
            f.write('\t{0}:{1}'.format(
                reaction, messenger_chat['reaction_count']['reaction_counter'][reaction]))
        # TODO Add other section
        f.write('\nThe 50 Most Common Words:\n')
        words = remove_common(messenger_chat['words_counter']).most_common(50)
        for num in range(len(words)):
            f.write('\t{0}. {1} ({2}x)'.format(
                num + 1, words[num][0], words[num][1]))

        # User Stats
        f.write('\n\nStats by Member:')
        for user in messenger_chat['members']:
            individual = messenger_chat['members'][user]
            f.write('\n\n{0}\n\n'.format(user))
            f.write('Total Messages: {0}\n'.format(
                individual['total_messages']))
            f.write('Word Count: {0}\n'.format(individual['word_count']))
            f.write('Character Count: {0}\n'.format(
                individual['character_count']))
            f.write('Images Sent: {0}\n'.format(individual['image_count']))
            f.write('Gifs Sent: {0}\n'.format(individual['gif_count']))
            f.write('Videos Sent: {0}\n'.format(individual['video_count']))
            f.write('Audio Files Sent: {0}\n'.format(
                individual['audio_count']))
            f.write('Links Sent: {0}\n'.format(individual['link_count']))
            f.write('Reactions Given: {0}\n'.format(
                individual['reaction_count']['given']))
            for reaction in individual['reaction_count']['given_counter']:
                f.write('\t{0}:{1}'.format(
                    reaction, individual['reaction_count']['given_counter'][reaction]))
            f.write('\nReactions Received: {0}\n'.format(
                individual['reaction_count']['received']))
            for reaction in individual['reaction_count']['received_counter']:
                f.write('\t{0}:{1}'.format(
                    reaction, individual['reaction_count']['received_counter'][reaction]))
            # TODO Add other section
            f.write('\nThe 25 Most Common Words:\n')
            words = remove_common(individual['words_counter']).most_common(25)
            for num in range(len(words)):
                f.write('\t{0}. {1} ({2}x)'.format(
                    num + 1, words[num][0], words[num][1]))
    print('Wrote Results to messenger_stats.txt. Please check that file for details!\n\nThanks for using my program :)!')


def remove_common(counter):
    # Common useless messenger words
    common_words = ['A', 'An', 'The', 'I', 'To', 'And', 'That', 'Sent', 'Is', 'Photo', 'S', 'T', 'You', 'Of', 'Like', 'It',
                    'In', 'My', 'This', 'For', 'M', 'We', 'At', 'Was', 'On', 'So', 'But', 'Just', 'Be', 'Good', 'If', 'Ll', 'Attachment']
    for word in common_words:
        del counter[word]
    return counter


def parse_words(message_list):
    try:
        words = re.findall(r'\w+', payload['message'])
        words = [word.title() for word in words]
        messenger_chat['words_counter'].update(words)
        messenger_chat['word_count'] += len(words)
        messenger_chat['character_count'] += len(''.join(words))
        user = messenger_chat['members'][payload['user']]
        user['words_counter'].update(words)
        user['word_count'] += len(words)
        user['character_count'] += len(''.join(words))
    except TypeError:
        if payload['message'] is not None:
            print('Error: TimeStamp of {0}'.format(payload['date']))
            print('Message: "{0}"'.format(payload['message']))
        return False
    except KeyError:
        print("Discovered person who left chat!")
        return False
    return True

#have to decode etc this is hard
def parse_reactions(message):
    reactions = message.find_all('li')
    if reactions:
        pure_reactions = [obj.string[:1] for obj in reactions]
        messenger_chat['reaction_count']['given'] += len(reactions)
        messenger_chat['reaction_count']['reaction_counter'].update(
            pure_reactions)
        receiving_user = messenger_chat['members'][payload['user']]
        giving_users = [obj.string[1:] for obj in reactions]
        receiving_user['reaction_count']['received'] += len(reactions)
        receiving_user['reaction_count']['received_counter'].update(
            pure_reactions)

        for index, user in enumerate(giving_users):
            individual = messenger_chat['members'][user]
            individual['reaction_count']['given'] += 1
            individual['reaction_count']['given_counter'].update(
                pure_reactions[index])


def parse_media(payload, message):
    user = messenger_chat['members'][payload['user']]
    images = message.find_all('img')
    if images:
        for image in images:
            # If image is a gif
            if image['src'][-3:] == 'gif':
                messenger_chat['gif_count'] += 1
                user['gif_count'] += 1
            else:
                messenger_chat['image_count'] += 1
                user['image_count'] += 1
    videos = message.find_all('video')
    if videos:
        messenger_chat['video_count'] += len(videos)
        user['video_count'] += len(videos)
    audio = message.find_all('audio')
    if audio:
        messenger_chat['audio_count'] += len(audio)
        user['audio_count'] += len(audio)


def parse_links(payload, message):
    user = messenger_chat['members'][payload['user']]
    links = message.find_all('a')
    if links:
        for link in links:
            if link['href'][:4] == 'http':
                messenger_chat['link_count'] += 1
                user['link_count'] += 1


def parse_participants(participant_list):
    # Add Member to members
    for member in participant_list:
        messenger_chat['members'][member['name']] = {
            'total_messages': 0,
            'word_count': 0,
            'character_count': 0,
            'image_count': 0,
            'gif_count': 0,
            'video_count': 0,
            'audio_count': 0,
            'link_count': 0,
            'reaction_count': {
                'given': 0,
                'received': 0,
                'given_counter': Counter(),
                'received_counter': Counter(),
            },
            'other': {
                'like_usage': 0,
                'emoji_usage': 0,
                'emoji_counter': Counter(),
                'sticker_usage': 0,
                'sticker_counter': Counter(),
            },
            'words_counter': Counter(),
        }


# Dictionary containing everything about the chat
messenger_chat = {
    'total_messages': 0,
    'word_count': 0,
    'character_count': 0,
    'image_count': 0,
    'gif_count': 0,
    'video_count': 0,
    'audio_count': 0,
    'link_count': 0,
    'reaction_count': {
        'given': 0,
        'reaction_counter': Counter(),
    },
    'other': {
        'like_usage': 0,
        'emoji_usage': 0,
        'emoji_counter': Counter(),
        'sticker_usage': 0,
        'sticker_counter': Counter(),
    },
    'words_counter': Counter(),
    'members': {},
}

# Runs the file
main(messenger_chat)
