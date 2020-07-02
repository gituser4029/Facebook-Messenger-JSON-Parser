''' Facebook Messenger Chat Parser Version 1.1.0 - Designed on 06.30.20 by
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

# TODO check through folder(s) for message.json and potentially other files if can support it
# TODO nickname check/parse/indication
# TODO fix word counts and filtered word list(s)
# TODO csv formatting :)))
# TODO graphical / data analysis

import json
from collections import Counter


def main(messenger_chat):
    print('Nate\'s Messenger (JSON) Chat Parser - Version 1.1.0')  # uwu

    try:
        print('\nPlease wait while the document loads.')
        # TODO setup to load either different file names or multiple files in different folders
        with open('message_1.json') as chat:
            file = json.load(chat)
        print('File has finished loading. Parsing data.\n')
    except FileNotFoundError:
        print('Error! File not found. You must give me a message_1.json file to '
              'work with in the same directory as this script!')
        return None

    # Get the current title
    messenger_chat['title'] = file['title']

    # TODO possibly delve into images / list image amount by person etc?
    # As in: List of photos/media/videos sent by user by chat O_o

    # Tell the user analysis has begun
    print(f"Performing analysis on {messenger_chat['title']}...")

    # Organizes the participants
    parse_participants(file['participants'])

    # Get the messages and sets the chat's total messages
    messages = file['messages']
    messenger_chat['total_messages'] = len(messages)

    print('\nParsing Chat Messages...')

    # Iterate through all messages and parse data
    for message in messages:
        parse_chat(message)

    print("Done! Analysis was successful!")
    print('\nWriting to file analysis results...')

    # Give a usable list in console and write to file
    with open(f"messenger_stats_{messenger_chat['title'].replace(' ', '_')}.txt", 'w+', encoding='utf-8')  as f:
        # Header
        f.write('File Generated Using Nate\'s Messenger Parser (https://github.com/'
                'artyomos/Facebook-Messenger-JSON-Parser)\nVersion 1.1.0\n\n')

        # Group Chat Title
        f.write(f'Messenger Chat: {messenger_chat["title"]}\n\n')

        # Stats
        f.write(f'Previous Members: {", ".join(messenger_chat["missing_members"]).strip(", ")}\n')
        f.write(f'Member Changes (Additions/Subtractions: {messenger_chat["user_add"]}'
                f'/{messenger_chat["user_remove"]})\n')
        f.write(f"Name Change Count: {messenger_chat['name_change_count']}x\n")
        f.write(f'Total Messages: {messenger_chat["total_messages"]}\n')
        f.write(f'Word Count: {messenger_chat["word_count"]}\n')
        f.write(f'Character Count: {messenger_chat["character_count"]}\n')
        f.write(f'Images Sent: {messenger_chat["image_count"]}\n')
        f.write(f'GIFs Sent: {messenger_chat["gif_count"]}\n')
        f.write(f'Videos Sent: {messenger_chat["video_count"]}\n')
        f.write(f'Audio Files Sent: {messenger_chat["audio_count"]}\n')
        f.write(f'Links Sent: {messenger_chat["link_count"]}\n')
        f.write(f"Reactions Given: {messenger_chat['reaction_count']['given']}\n")
        for reaction in messenger_chat['reaction_count']['reaction_counter']:
            f.write(f"\t{reaction}:{messenger_chat['reaction_count']['reaction_counter'][reaction]}")
        # TODO Add other section(s)
        f.write('\nThe 50 Most Common Words:\n')
        words = remove_common(messenger_chat['words_counter']).most_common(50)
        for num in range(len(words)):
            f.write(f"\t{num + 1}. {words[num][0]} ({words[num][1]}x)")

        # Write Name changes the group experienced
        f.write(f'\n\nChanges in name to {messenger_chat["title"]} '
                f'(Ordered by date of last change reverse chronological)\n')
        num = 0
        for name in messenger_chat['name_changes'].items():
            num += 1
            f.write(f"\t{num}. {name[0]} ({name[1]}x)")

        # User Stats
        f.write('\n\nStats by Member:')
        print('N-Word Count(s)! Lets see if you are being naughty!! >:(')
        for user in messenger_chat['members']:
            # Skip the catch-all missing user
            if user == 'unknown_user':
                continue
            individual = messenger_chat['members'][user]

            # Optional CONSOLE ONLY N-Word Count - I'm sorry but I needed to type the words to search for them,
            # I promise I don't mean them TODO https://pypi.org/project/profanity-check/
            # TODO regex whatever it is for [*]gga (and exclude ni -   of course) so I don't have any n-words in code
            print(
                f"{user.split()[0]:>15} N-word Count: {individual['words_counter']['Nigga']:>4} Soft "
                f"{individual['words_counter']['Nigger']:>4} Hard {individual['words_counter']['Nig']:>4} Cut-off "
                f"{individual['words_counter']['Niggar']:>4} Weird Format O_o")

            f.write(f'\n\n{user}\n\n')
            f.write(f"Total Messages: {individual['total_messages']}\n")
            f.write(f"Word Count: {individual['word_count']}\n")
            f.write(f"Character Count: {individual['character_count']}\n")
            f.write(f"Images Sent: {individual['image_count']}\n")
            f.write(f"GIFs Sent: {individual['gif_count']}\n")
            f.write(f"Videos Sent: {individual['video_count']}\n")
            f.write(f"Audio Files Sent: {individual['audio_count']}\n")
            f.write(f"Links Sent: {individual['link_count']}\n")
            f.write(f"Reactions Given: {individual['reaction_count']['given']}\n")
            for reaction in individual['reaction_count']['given_counter']:
                f.write(f"\t{reaction}:{individual['reaction_count']['given_counter'][reaction]}")
            f.write(f"\nReactions Received: {individual['reaction_count']['received']}\n")
            for reaction in individual['reaction_count']['received_counter']:
                f.write(f"\t{reaction}:{individual['reaction_count']['received_counter'][reaction]}")
            # TODO Add other section(s)
            f.write('\nThe 25 Most Common Words:\n')
            words = remove_common(individual['words_counter']).most_common(25)
            for num in range(len(words)):
                f.write(f"\t{num + 1}. {words[num][0]} ({words[num][1]}x)")

    print('Wrote Results to messenger_stats.txt. Please check that file for details!'
          '\n\nThanks for using my program :)!')


def remove_common(counter):
    """
    Given a counter remove common words
    :param counter:Counter Counter containing words used in the chat
    :return: counter Returns the sanitized Counter
    """
    # TODO fix remove common it removes stuff it shouldn't - maybe smaller curated list
    # Top 10000 common english words are removed from messeenger chat statistics on top 25 words
    # with open('google-10000-english.txt') as f:
    #    common_words = list(map(str.strip, f.readlines()))
    #    print(common_words)

    # Extra list to include any other words you would like to filter
    extra_exceptions = ['I\'m', 'It\'s', 'Don\'t', 'That\'s', 'Should', 'About']
    with open('google-10000-english-usa-no-swears-short.txt') as f:
        common_words = list(map(str.strip, f.readlines())) + extra_exceptions
        # print(common_words)
        for word in common_words:
            del counter[word.capitalize()]
    return counter


def parse_chat(message):
    """
    Parses a given message, placing within the (global) chat dictionary the additions this message provides
    :rtype: boolean
    :param message:dict Dictionary containing information on a message (Author, Message, Photos, Videos, etc.)
    :return: False if the message cannot be parsed, True otherwise
    """
    try:
        # Assume content exists, attempt to get user and increment his message count
        content = True

        # If user doesn't exist, use placeholder user 'unknown_user'
        try:
            user = messenger_chat['members'][message['sender_name']]
        except KeyError:
            # Skip Missing Members if already found
            if message['sender_name'] not in messenger_chat['members'] and \
                    message['sender_name'] not in messenger_chat['missing_members']:
                print(f"Found a missing user! {message['sender_name']}")
                messenger_chat['missing_members'].append(message['sender_name'])
            user = messenger_chat['members']['unknown_user']

        # Increment User's total messages
        user['total_messages'] += 1

        # Fix messenger problems with Unicode Encoding
        if 'content' in message.keys():
            # messenger has improperly encoded text - needs to be re-encoded
            # and then decoded - I don't want to explain its just annoying
            words = message['content'].encode('latin1').decode('utf-8')
            message['content'] = words
        else:
            words = ''
            content = False

        # TODO use these 'sent X' to determine previous nicknames in chat (as well as likely time it changed)
        # Checks to see if special events have occurred
        # Or if X sent X exists 0 content in message
        if 'sent an attachment' in words:
            content = False
        elif 'sent a photo' in words:
            content = False
        elif 'sent a video' in words:
            content = False
        elif 'the group.' in words:
            parse_member_changes(message, user)
            content = False
        elif 'named the group' in words:
            parse_group_changes(message, user)
            content = False
        #TODO group photo changes "X changed the group photo." - no real info for this one
        #TODO chat color changes "You changed the chat colors." - no real info for this one
        #TODO chat emoji changes "X set the emoji to X."
        #TODO nickname changes "X set the nickname for X to X."



        if 'share' in message.keys():
            parse_links(message, user)
        elif 'photos' in message.keys():
            parse_photos(message, user)
        elif 'videos' in message.keys():
            parse_videos(message, user)
        elif 'audio_files' in message.keys():
            parse_audio(message, user)

        if 'reactions' in message.keys():
            parse_reactions(message, user)

        if content:
            words = [word.capitalize() for word in words.split()]
            word_count = len(words)
            char_count = len(''.join(words))
            messenger_chat['words_counter'].update(words)
            messenger_chat['word_count'] += word_count
            messenger_chat['character_count'] += char_count
            user['words_counter'].update(words)
            user['word_count'] += word_count
            user['character_count'] += char_count
    except TypeError:
        print(f"TypeError for Message: {message['timestamp_ms']}")
        if 'content' in message.keys():
            print(f"Message Content: {message['content']}")
        return False
    except KeyError:
        # Otherwise describe the problem to console
        print(f"KeyError for Message: {message['timestamp_ms']}")
        # if 'content' in message.keys():
        #     print(f"Message Content: {message['content']}")
        return False
    return True


def parse_member_changes(message, user):
    """
    Given a message adds to the (global) chat dictionary the additions and changes to users
    :param message:dict Dictionary containing information on a message (Author, Message, Photos, Videos, etc.)
    :param user:dict Dictionary of the user in the chat
    """

    # Checks to ensure message truly is changing users (either additions or removals)
    if 'users' not in message.keys():
        return None
    if message['type'] == 'Subscribe':
        add = True
    else:
        add = False

    # Adds to counters the amount of times user X was added / removed
    # TODO indicate in file time of user addition/removal and who did it
    for user in message['users']:
        # print(f'User Status Change: {user["name"]} Add: {add}')
        if user['name'] not in messenger_chat['members'] and \
                user['name'] not in messenger_chat['missing_members']:
            print(f"Found a missing user! {user['name']}")
            messenger_chat['missing_members'].append(user['name'])

        if add:
            messenger_chat['user_add'] += 1
            messenger_chat['user_additions'].update(user)
        else:
            messenger_chat['user_remove'] += 1
            messenger_chat['user_removals'].update(user)


def parse_group_changes(message, user):
    """
    Given a message adds to the (global) chat dictionary the changes to the group name
    :param message:dict Dictionary containing information on a message (Author, Message, Photos, Videos, etc.)
    :param user:dict Dictionary of the user in the chat
    """

    name_change = message['content'].split('the group')[1].strip('.').strip()
    messenger_chat['name_changes'][name_change] += 1
    # name_change = f"{message['sender_name']:>20} changed the group name to {name_change.encode('latin1').decode('utf-8')}"
    # print(name_change)

    # Adds to counters the amount of times group was changed
    # TODO indicate in file time of group change and who did it
    messenger_chat['name_change_count'] += 1


def parse_reactions(message, user):
    """
    Given a message adds to the (global) chat dictionary the reactions given and received by the user
    :param message:dict Dictionary containing information on a message (Author, Message, Photos, Videos, etc.)
    :param user:dict Dictionary of the user in the chat
    """
    reactions = message['reactions']
    messenger_chat['reaction_count']['given'] += len(reactions)

    for reaction in reactions:
        # This line fixes messenger unicode encoding
        reaction_emoji = reaction['reaction'].encode('latin1').decode('utf-8')

        # Update totals for chat
        messenger_chat['reaction_count']['reaction_counter'].update(reaction_emoji)
        giving_user = reaction['actor']
        user['reaction_count']['received'] += 1
        user['reaction_count']['received_counter'].update(reaction_emoji)
        messenger_chat['members'][giving_user]['reaction_count']['given'] += 1
        messenger_chat['members'][giving_user]['reaction_count']['given_counter'].update(reaction_emoji)


def parse_photos(message, user):
    """
    Given a message adds to the (global) chat dictionary the photos sent by the user
    :param message:dict Dictionary containing information on a message (Author, Message, Photos, Videos, etc.)
    :param user:dict Dictionary of the user in the chat
    """
    for image in message['photos']:
        image_check = image['uri']
        if 'gif' in image_check:
            messenger_chat['gif_count'] += 1
            user['gif_count'] += 1
        else:
            messenger_chat['image_count'] += 1
            user['image_count'] += 1


def parse_videos(message, user):
    """
    Given a message adds to the (global) chat dictionary the videos sent by the user
    :param message:dict Dictionary containing information on a message (Author, Message, Photos, Videos, etc.)
    :param user:dict Dictionary of the user in the chat
    """
    for video in message['videos']:
        # TODO Potentially create a list of sent video files and where to find it
        video_file = video['uri']
        messenger_chat['video_count'] += 1
        user['video_count'] += 1


def parse_audio(message, user):
    """
    Given a message adds to the (global) chat dictionary the audio files sent by the user
    :param message:dict Dictionary containing information on a message (Author, Message, Photos, Videos, etc.)
    :param user:dict Dictionary of the user in the chat
    """
    for audio in message['audio_files']:
        # TODO Potentially create a list of sent audio files and where to find it
        audio_file = audio['uri']
        messenger_chat['audio_count'] += 1
        user['audio_count'] += 1


def parse_links(message, user):
    """
    Given a message adds to the (global) chat dictionary the links sent by the user
    :param message:dict Dictionary containing information on a message (Author, Message, Photos, Videos, etc.)
    :param user:dict Dictionary of the user in the chat
    """
    try:
        links = message['share']['link']
        # Check if link is to the Web
        if links[:4] == 'http':
            messenger_chat['link_count'] += 1
            user['link_count'] += 1
    except Exception as e:
        # TODO deal with new sharing feature(s)
        # Example includes the new share location trips this except block
        print(f"Error for (Sharing) Message {message['timestamp_ms']}")


def parse_participants(participant_list):
    """
    Adds a list of participants in the chat to the (global) chat dictionary
    :param participant_list:dict Dictionary containing users in the chat
    """
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
    # Finally, add a catch-all missing user
    messenger_chat['members']['unknown_user'] = {
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
    'title': '',
    'total_messages': 0,
    'name_changes': Counter(),
    'name_change_count': 0,
    'word_count': 0,
    'character_count': 0,
    'image_count': 0,
    'gif_count': 0,
    'video_count': 0,
    'audio_count': 0,
    'link_count': 0,
    'reaction_count': {
        'given': 0,
        'given_counter': Counter(),
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
    'missing_members': [],
    'user_additions': Counter(),
    'user_removals': Counter(),
    'user_add': 0,
    'user_remove': 0,
}

# import cProfile
# cProfile.run('main(messenger_chat)')
main(messenger_chat)