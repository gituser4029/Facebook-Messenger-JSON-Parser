''' Facebook Messenger Chat Parser Version 1.0.0 - Designed on 06.30.20 by
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
# TODO missing member indication(s)
# TODO fix gif_counts for new messenger format for new(er) chats
# TODO fix word counts and filtered word list(s)
# TODO fstring formatting
# TODO csv formatting :)))
# TODO graphical / data analysis
# TODO TODO TODO :P

# import re #regex
import json
from collections import Counter


def main(messenger_chat):
    print('Nate\'s Messenger (JSON) Chat Parser - Version 1.1.0')

    try:
        print('\nPlease wait while the document loads.')
        with open('message_1.json') as chat: #TODO setup to load either different file names or multiple files in different folders
            file = json.load(chat)
        print('File has finished loading. Parsing data.\n')
    except FileNotFoundError:
        print('Error! File not found. You must give me a message.html file to work with from Facebook Messenger!')
        return None

    # Get the current title
    messenger_chat['title'] = file['title']

    # TODO possibly delve into images / list image amount by person etc?

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
        # checks for words, images, links, etc
        parse_words(message)

        # Increase User's total message count
        try:
            messenger_chat['members'][message['sender_name']]['total_messages'] += 1
        except KeyError:
            if message['sender_name'] not in messenger_chat['missing_members']:
                print(f"Discovered person who left chat! {message['sender_name']}")
                messenger_chat['missing_members'].append(message['sender_name'])
            continue

        # TODO check media / photos
        # Parse through for images and videos
        # parse_media(payload, message)
        # Find and parse links send in the chat
        # parse_links(payload, message)

    print("Done! Analysis was successful!")
    print('\nWriting to file anaylsis results...')

    # Give a usable list in console and write to file
    with open(f"messenger_stats_{messenger_chat['title'].replace(' ', '_')}.txt", 'w+', encoding='utf-8')  as f:
        # Header
        f.write(
            'File Generated Using Nate\'s Messenger Parser (https://github.com/artyomos/Facebook-Messenger-JSON-Parser)\nVersion 1.1.0\n\n')

        # Group Chat Title
        f.write('Messenger Chat: {0}\n\n'.format(messenger_chat['title']))

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
            try:
                f.write('\t{0}. {1} ({2}x)'.format(
                    num + 1, words[num][0], words[num][1]))
            except UnicodeEncodeError:
                f.write('\t{0}. {1} ({2}x)'.format(
                    num + 1, words[num][0].encode('utf-8'), words[num][1]))

        # User Stats
        f.write('\n\nStats by Member:')
        print('N-Word Count(s)! Lets see if you are being naughty!! >:(')
        for user in messenger_chat['members']:
            individual = messenger_chat['members'][user]

            # Optional CONSOLE ONLY N-Word Count - I'm sorry but I needed to type the words to search for them, I promise I don't mean them
            # TODO https://pypi.org/project/profanity-check/
            # regex whatever it is for [*]gga (and exclude ni -   of course) to see all the hilarious -gga's we've come up with
            print(
                f"{user.split()[0]:>15} N-word Count: {individual['words_counter']['Nigga']:>4} Soft {individual['words_counter']['Nigger']:>4} Hard {individual['words_counter']['Nig']:>4} Cut-off {individual['words_counter']['Niggar']:>4} Weird Format O_o")

            # TODO convert everything to fstring - this old code is before 3.6 added them
            f.write(f'\n\n{user}\n\n')
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
            try:
                for reaction in individual['reaction_count']['given_counter']:
                    f.write('\t{0}:{1}'.format(
                        reaction, individual['reaction_count']['given_counter'][reaction]))
            except UnicodeEncodeError:
                f.write('\t{0}:{1}'.format(
                    reaction.decode('utf-8'), individual['reaction_count']['given_counter'][reaction]))
            f.write('\nReactions Received: {0}\n'.format(
                individual['reaction_count']['received']))
            for reaction in individual['reaction_count']['received_counter']:
                f.write('\t{0}:{1}'.format(
                    reaction, individual['reaction_count']['received_counter'][reaction]))
            # TODO Add other section
            f.write('\nThe 25 Most Common Words:\n')
            words = remove_common(individual['words_counter']).most_common(25)
            for num in range(len(words)):
                try:
                    f.write('\t{0}. {1} ({2}x)'.format(
                        num + 1, words[num][0], words[num][1]))
                except UnicodeEncodeError:
                    f.write('\t{0}. {1} ({2}x)'.format(
                        num + 1, words[num][0].encode('utf-8'), words[num][1]))
    print(
        'Wrote Results to messenger_stats.txt. Please check that file for details!\n\nThanks for using my program :)!')


def remove_common(counter):
    # TODO fix remove common it removes stuff it shouldn't - maybe smaller curated list
    # Top 10000 common english words are removed from messeenger chat statistics on top 25 words
    # with open('google-10000-english.txt') as f:
    #    common_words = list(map(str.strip, f.readlines()))
    #    print(common_words)
    extra_exceptions = ['I\'m', 'It\'s', 'Don\'t', 'That\'s', 'Should', 'About']
    with open('google-10000-english-usa-no-swears-short.txt') as f:
        common_words = list(map(str.strip, f.readlines())) + extra_exceptions
        # print(common_words)
        for word in common_words:
            del counter[word.capitalize()]
    return counter


def parse_words(message):
    # TODO fix parsing of X sent (photo/attachmentdeo/link etc)
    try:
        content = True  # assume content exists
        user = messenger_chat['members'][message['sender_name']]
        # words = re.findall(r'\w+', message['content'])
        try:
            words = message['content'].encode('latin1').decode('utf-8')  # messenger has improperly encoded text
        except KeyError:
            words = ''
            content = False

        # if X sent X exists 0 content in message, ignore
        if 'sent an attachment' in words:
            content = False  # skip or TODO notify share
        elif 'sent a photo' in words:
            content = False  # TODO notify photo
        elif 'sent a video' in words:
            content = False  # TODO notify video
        # TODO use these 'sent X' to determine previous nicknames in chat (as well as likely time it changed)

        # Otherwise (Messenger messed wihm prev chats and separated 'sent X' from the actual content into two messages) search for these keys
        if 'share' in message.keys():
            parse_links(message)

        if 'photos' in message.keys():
            parse_photos(message)
        elif 'videos' in message.keys():
            parse_videos(message)
        elif 'audio_files' in message.keys():
            parse_audio(message)

        if 'reactions' in message.keys():
            parse_reactions(message)

        if content:
            words = [word.capitalize() for word in words.split()]
            messenger_chat['words_counter'].update(words)
            messenger_chat['word_count'] += len(words)
            messenger_chat['character_count'] += len(''.join(words))
            user['words_counter'].update(words)
            user['word_count'] += len(words)
            user['character_count'] += len(''.join(words))
    except TypeError as e:
        print(message['timestamp_ms'])
        raise (e)
        if message['content'] is not None:
            print('Error: TimeStamp of {0}'.format(message['timestamp_ms']))
            print('Message: "{0}"'.format(message['content']))
        return False
    except KeyError as e:
        f = str(e)
        if 'Matthew' in f or 'David' in f or 'Kearsen' in f:
            return None
        print(message['timestamp_ms'])
        raise (e)
        if message['sender_name'] not in messenger_chat['missing_members']:
            print(f"Discovered person who left chat! {message['sender_name']}")
            messenger_chat['missing_members'].append(message['sender_name'])
        return False
    return True


def parse_reactions(message):
    user = messenger_chat['members'][message['sender_name']]
    reactions = message['reactions']
    messenger_chat['reaction_count']['given'] += len(reactions)

    for reaction in reactions:
        # messenger has broken utf-8 encoding
        reaction_list = {
            '\u00f0\u009f\u0091\u008d': '👍',
            '\u00f0\u009f\u0098\u00a0': '😮',

        }
        reaction_emoji = reaction['reaction'].encode('latin1').decode('utf-8')  # messenger has improperly encoded text
        # print(reaction_emoji)
        # update totals for chat
        messenger_chat['reaction_count']['reaction_counter'].update(
            reaction_emoji)
        giving_user = reaction['actor']

        # gives user his reactions
        user['reaction_count']['received'] += 1
        user['reaction_count']['received_counter'].update(reaction_emoji)
        # gives giver his reactions given
        messenger_chat['members'][giving_user]['reaction_count']['given'] += 1
        messenger_chat['members'][giving_user]['reaction_count']['given_counter'].update(reaction_emoji)


def parse_photos(message):
    user = messenger_chat['members'][message['sender_name']]
    for image in message['photos']:
        image_check = image['uri']  # messenger formatting is shit
        if 'gif' in image_check:
            messenger_chat['gif_count'] += 1
            user['gif_count'] += 1
        else:
            messenger_chat['image_count'] += 1
            user['image_count'] += 1
    return None


def parse_videos(message):
    user = messenger_chat['members'][message['sender_name']]
    for video in message['videos']:
        videos = video[
            'uri']  # TODO idk do nothing with it for now (possibly showcase it/create a searchable list of who said what with what vid?)
        messenger_chat['video_count'] += len(videos)
        user['video_count'] += len(videos)
    return None


def parse_audio(message):
    user = messenger_chat['members'][message['sender_name']]
    for audio_file in message['audio_files']:
        audio = audio_file[
            'uri']  # TODO idk do nothing with it for now (possibly showcase it/create a searchable list of who said what)
        messenger_chat['audio_count'] += 1
        user['audio_count'] += 1
    return None


def parse_links(message):
    user = messenger_chat['members'][message['sender_name']]
    try:
        links = message['share']['link']
        if links[:4] == 'http':  # checks if links to web - thats all we care about
            messenger_chat['link_count'] += 1
            user['link_count'] += 1
    except:
        pass  # TODO deal with new sharing feature(s)
    return None


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
    'title': '',
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
}

# Runs the file
main(messenger_chat)
