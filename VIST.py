try:
    # external modules
    import speech_recognition as sr  # for speech to text
    from gtts import gTTS  # google text to speech
    from playsound import playsound  # audio manipulator
    import requests
    import geocoder  # for APIs
    from func_timeout import func_timeout, FunctionTimedOut

    # built-in modules
    from random import choice  # gives random choice in a list
    from ast import literal_eval  # ast module
    from sys import platform, version_info, exit  # system module
    from os import system, name, path, remove  # os module
    import webbrowser as wb  # web browser
    from time import sleep, time  # sleep
    from datetime import datetime
    import re


except ImportError:
    # if modules are not intalled, ask the user to install them.
    print("Please install the pre-requisites.\nRun the install_dependencies file and they will be installed automatically.")
    quit()


# Variables
upper_and_lower = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
beep = 'beep.mp3'
say_again = 'couldYouSayThatAgain.mp3'
data = {}
mic_id = None
greetings = ['Namaste', 'Ram Ram', 'Jai Jinendra',
             'Jai Shri Krishna', 'Satsriakaal', 'Hello', 'Hi', 'Salaam Vaalaikum']
what_am_i_doing_list = ['I am talking to you right now!',
                        'I know everything, so i am chilling!',
                        "I'm drinking tea.",
                        "I'm preparing for J.E.E. Advance for the past 10 years but cannot clear it!",
                        "Damn, you woke me up! I was sleeping bruh."
                        ]
how_am_i_list = ['Talking to you makes me feel great!',
                 "I'm depressed. Anyways.",
                 "I'm great but you should be studying right now...",
                 "I don't have any feelings!",
                 "I think I will not be able to make it through the day!"
                 ]
operators = {
    '+': ['plus'],
    '-': ['minus'],
    '*': ['times', 'into', 'multiplied'],
    '/': ['divided by', 'upon']
}
mic_id = ''

# location
city = geocoder.ip('me').city

# API URLs
covid_api_url = 'https://api.rootnet.in/covid19-in/stats/latest'
joke_api_url = 'https://official-joke-api.appspot.com/jokes/random'
weather_api_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid=4153fb471c99f9f74d20c091db20bd22'


# Utility functions
def cls():
    # Clear the console
    system('cls') if name == 'nt' else system('clear')


def save_to_file(data):
    # Save data to file
    with open('config.txt', 'w') as file:
        file.write(str(data))


def get_mics():
    speak("Which microphone do you want to use? (Enter the corresponding number)")
    mics = sr.Microphone.list_microphone_names()
    new_list_of_mics = []
    for id, mic in enumerate(mics):
        if mic == ' - Output':
            break
        elif mic == ' - Input':
            continue
        else:
            new_list_of_mics.append(mic)
            print(f"{id} - {mic}")
    which_mic = input(
        "? ")
    if which_mic.isnumeric() and int(which_mic) in range(0, len(new_list_of_mics)+1):
        return int(which_mic)
    else:
        print("Please enter correctly!")
        get_mics()


def is_internet_active():
    # Check if the user has an active internet connection
    # By requesting Google's search engine
    try:
        _ = requests.get('https://www.google.com', timeout=1)
        return True
    except requests.ConnectionError:
        return False


def quit_program():
    # Exit the program with goodbye message!
    speak("It was nice talking to you, hope to see you soon!")
    quit()


# Request and response function
def listen():

    def audio_equals_r_dot_listen(r, source):
        print("Listening..")
        playsound(beep)
        audio = r.listen(source)
        return audio

    r = sr.Recognizer()
    while True:
        with sr.Microphone(device_index=data['mic']) as source:
            r.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = func_timeout(
                    20, audio_equals_r_dot_listen, args=(r, source)
                )
                break
            except FunctionTimedOut:
                print("Could you say that again?")
                playsound(say_again)
                continue
    try:
        # Recognize the audio using Google
        print(r.recognize_google(audio))
        # Play the recognized audio
        playsound(beep)
        return r.recognize_google(audio)
    except sr.UnknownValueError:
        speak('Voice not clear! Please repeat!')
    except sr.RequestError:
        speak("Server didn't respond!")


def speak(text):
    # Name of the mp3 to be played
    mp3 = ''
    for i in range(10):
        mp3 += choice(upper_and_lower)
    mp3 += '.mp3'
    txt2speech = gTTS(text, lang='en-in')
    # Save the audio as speech.mp3
    txt2speech.save(mp3)
    # Print and Play the saved audio (will print it two times)
    print(text)
    playsound(mp3)
    remove(mp3)


# Common functions
def web_search(q):
    exceptions = ['search for', 'search',
                  'tell me about', 'what is', 'what are']
    for exception in exceptions:
        if exception in q:
            q = q.replace(exception, '')
    if not q or q.isspace():
        speak("Please specify what you want to say.")
    else:
        query = q.split()
        parsed_query = '+'.join(query)  # Replace spaces with '+' sign
        google_url = f'https://www.google.com/search?q={parsed_query}'
        speak(f"Okay! Searching for {q}")
        wb.open_new_tab(google_url)


# API functions
def india_covid():
    try:
        # Get information about the covid in form of a JSON file
        res = requests.get(covid_api_url)
        res.raise_for_status()
    # Look for errors and report to the user
    except (requests.HTTPError, Exception, requests.exceptions.ConnectionError):
        print("Please check your network connection.")
    else:
        # Store data as JSON temporarily in a variable
        rJSON = res.json()
        # Extract data from JSON
        data = rJSON['data']
        # Speak out the extracted data
        speak(
            f"Total cases of COVID-19 in India are {data['summary']['total']}; whereas {data['summary']['discharged']} have been discharged and {data['summary']['deaths']} people died!"
        )


def jokeAPI():
    try:
        # Try to connect to the endpoint of the API
        res = requests.get(joke_api_url)
        res.raise_for_status()
    # Look for errors and report them
    except (requests.HTTPError, Exception, requests.exceptions.ConnectionError):
        print("Please check your network connection.")
    else:
        # Store data as JSON temporarily in a variable
        json = res.json()
        # Speak out the extracted joke setup
        speak(json['setup'])
        # Wait for 1 second
        sleep(1)
        # Speak out the extracted joke punchline
        speak(json['punchline'])


def weather_api():
    try:
        res = requests.get(weather_api_url)

    except (requests.HTTPError, Exception, requests.exceptions.ConnectionError):
        print("Please check your network connection.")

    else:
        # extract data from json
        res = res.json()

        # data dictionaries
        main_obj_data = res['main']
        weather_data = res['weather'][0]

        # variables
        temperature = main_obj_data['temp']
        feels_like = main_obj_data['feels_like']
        weather = weather_data['main']

        # say the weather
        speak(
            f"The current weather in {city} is {weather}. The temperature is {temperature} degree celsius. It feels like {feels_like} degree celsius.")


# Commands' functions
def date_time():
    # Get the current time
    now = datetime.now()
    # Create a date string
    dt_string = now.strftime("%d/%m/%Y! ")
    day_string = now.strftime("%A")
    # Speak out today's date and time
    speak(f"Today is {day_string} and date is {dt_string}")


def hi():
    # Speak hi while blushing ;)
    speak(f'{choice(greetings)} {data["name"]}!')


def show_abilities():
    # Tell about VIST's abilities
    speak(
        "I can do a lot of things! I'm opening a webpage, there you can see all the commands!"
    )
    wb.open_new_tab(
        'https://github.com/adityatrips/VIST#commands-that-can-be-used-for'
    )


def solve(expression):
    try:
        # remove extra words
        extra_words = ['what is ', 'solve ', 'evaluate ', 'calculate ']
        for word in extra_words:
            if word in expression:
                expression = expression.replace(word, '')

        # replace words with operators
        operators = [{'*': ['x', 'X', 'into']}, {'/': ['divided by', 'upon']}]
        for dictionary in operators:
            for operator, operator_words in dictionary.items():
                for operator_word in operator_words:
                    if operator_word in expression:
                        expression = expression.replace(
                            operator_word, operator)
        else:
            # evaluate
            answer = eval(expression)

    except:
        speak("Could not understand you. Please say it again.")
    else:
        speak(f"The answer is {answer}")


def pronunciation():
    # Pronounces the given word
    while True:
        # VIST speaks out
        speak("Which word's pronunciation do you want to check?")
        # User enters the word
        word = input("? ").lower()
        # Check if the word is all alphabets
        if word.isalpha():
            # Speak out
            speak(f'This word is pronounced as {word}!')
            break
        else:
            # Speak out
            speak(f"Please enter a correct word {data['name']}!")


def feedback():
    # Ask for feedback
    speak("Please send your feedback at one of the following email IDs:\naxityatrips@gmail.com\nor\nprayagjain2@gmail.com")


def countdown():
    # User enters the countdown time
    sec = int(input("Enter seconds for the countdown\n? "))
    while sec > 0:
        # Print the second
        print(sec)
        # Wait one second
        sleep(1)
        # Decrement second by one
        sec -= 1
    # Play the beep
    playsound(beep)


def answer_the_question(q):
    func_list = [
        {'keywords': ['solve', 'calculate', 'evaluate', 'divide', ' x ', ' X ', '+', '-', 'into'],
            'func': solve, 'args_r': True},
        {'keywords': ['corona', 'covid'],
            'func': india_covid, 'args_r': False},
        {'keywords': ['date', 'day'], 'func': date_time, 'args_r': False},
        {'keywords': ['search'], 'func': web_search, 'args_r': True},
        {'keywords': ['place', 'location'],
            'func': where_am_i, 'args_r': False},
        {'keywords': ['you'], 'func': tell_about_itself, 'args_r': True},
        {'keywords': ['weather', 'temp', 'temperature'],
            'func': weather_api, 'args_r': False},
        {'keywords': ['pronounce', 'pronunciation'],
            'func': pronunciation, 'args_r': False},
        {'keywords': ['abilities'], 'func': show_abilities, 'args_r': False}
    ]

    for dictionary in func_list:
        for keyword in dictionary['keywords']:
            if keyword in q:
                if dictionary['args_r']:
                    dictionary['func'](q)
                else:
                    dictionary['func']()
                break
        break


def tell_about_itself(q):
    replies = [
        {'id': 1, 'ques': ['how are', 'sup', 'what\'s up'],
            'reply': how_am_i_list},
        {'id': 2, 'ques': ['doing'], 'reply': what_am_i_doing_list},
        {'id': 3, 'ques': ['who'], 'reply': [
            'I am Vist, your own virtual assistant! Try saying, "What can you do?" to see my abilities!']},
        {'id': 4, 'ques': ['age', 'old'], 'reply': [
            'You should never ask a girl her age.']},
    ]
    for dictionary in replies:
        for ques in dictionary['ques']:
            if ques in q:
                speak(choice(dictionary['reply']))


def where_am_i():
    speak(f'You are currently located in {city}!')


def cmd_prompt():
    # Run functions corresponding to a command
    # list of commands corresponding to their functions
    commands = [
        {'trigger_on': ['what can you do', 'help',
                        'what you can do', 'what are your abilities'], 'func': show_abilities, 'args_required': False},
        {'trigger_on': ['covid status', 'covid', 'corona', 'corona virus', 'covid-19 status',
                        'corona status', 'corona virus status', 'covid-19', 'coronavirus'], 'func': india_covid, 'args_required': False},
        {'trigger_on': ['calculate', 'solve',
                        'calculator', 'evaluate', '+', '-', ' x ', ' X ', 'divided by', 'upon', 'into'], 'func': solve, 'args_required': True},
        {'trigger_on': ['search', 'web search', 'web', 'search for', 'tell me about'],
         'func': web_search, 'args_required': True},
        {'trigger_on': ['crack a joke', 'tell me a joke', 'joke', 'fun', 'laugh',
                        'make me laugh', 'tell me something funny'], 'func':jokeAPI, 'args_required': False},
        {'trigger_on': ['bye', 'exit', 'good bye'],
         'func': quit_program, 'args_required': False},
        {'trigger_on': ['countdown', 'timer'],
         'func': countdown, 'args_required': False},
        {'trigger_on': greetings, 'func': hi, 'args_required': False},
        {'trigger_on': ['pronunciation', 'how is this word pronounced',
                        'pronounced', 'how do you speak this', 'how to pronounce'], 'func': pronunciation, 'args_required': False},
        {'trigger_on': ['support', 'feedback'],
         'func': feedback, 'args_required': False},
        {'trigger_on': ['weather'],
            'func': weather_api, 'args_required': False},
        {'trigger_on': ['where am i', 'what is this place',
                        'my location'], 'func': where_am_i, 'args_required': False},
        {'trigger_on': ['who are you', 'how are you', 'how old are you', 'what are you doing', 'your name',
                        'how are you doing', 'your age', 'you doing', 'sup', 'what\'s up'], 'func': tell_about_itself, 'args_required': True},
        {'trigger_on': ['what is', 'who is', 'where is', 'how is', 'what are', 'who are', 'how are', 'where are'],
            'func': answer_the_question, 'args_required': True},
        {'trigger_on': ['date', 'day'],
         'func': date_time, 'args_required': False},
    ]
    # Run the code block inside, unless the loop is broken.
    while True:
        try:
            # Listen for the command
            speak("How can I help you?")
            inp = listen().lower()
        except AttributeError:
            # If there's an error, continue to the top and ask again.
            continue
        else:
            # Internet search is set to True by default
            internet_search = True
            # For each dictionary in the commands list
            for dictionary_index in range(len(commands)):
                # For each sentence in the 'trigger_on' list.
                for keysentence in commands[dictionary_index]['trigger_on']:
                    # If the user input contains the keysentence,
                    # Then run its corresponding # function and set internet search to true
                    if keysentence.lower() in inp:
                        # pass arguments if arguments are requie
                        if commands[dictionary_index]['args_required']:
                            commands[dictionary_index]['func'](inp)
                        else:
                            commands[dictionary_index]['func']()
                        internet_search = False
                        break
                else:
                    # If user input doesn't match any of the sentences in the 'trigger_on'
                    # list, then look in the next dictionary
                    continue
            else:
                if internet_search:
                    # Search the internet for unrecognized commands
                    web_search(inp)


def main():
    cls()
    global data, mic_id

    def save_to_file(data):
        with open('config.txt', 'w') as file:
            file.write(str(data))

    # Save details in a config file
    def save_data(name_key, name_value):
        data[str(name_key)] = name_value
        save_to_file(data)

    def save_mic(mic_key, mic_val):
        data[str(mic_key)] = mic_val
        save_to_file(data)

    # Check if config.txt exists
    if path.isfile('config.txt'):
        # If yes then read config.txt
        with open('config.txt', 'r') as file:
            try:
                # Store the data in a variable
                data = literal_eval(file.read())
                print("Checking saved data...",
                      data['name'], "Mic ID:", data['mic']
                      )
            except:
                # If data is corrupted
                speak('Your data is corrupted. Clearing cache...')
                # Remove config file and run main again
                remove('config.txt')
                main()
            else:
                # Speak one of the greetings in the greetings list and the name of the user
                speak('Do you want to change the mic configuration')
                change_config = listen().lower()
                if change_config == 'yes':
                    get_mics()
                else:
                    speak(f"{choice(greetings)}, {data['name']}!")

    else:
        mic_id = get_mics()
        save_mic('mic', mic_id)
        speak("Hey there! I am Vist, your virtual and personal assistant! Can you please enter your name?")
        name = input("? ")
        speak(f'That\'s a nice name, {name}!')
        save_data('name', name)


if __name__ == "__main__":
    if is_internet_active():
        main()
        cmd_prompt()
    else:
        print("Connect to a working network and try again!")
