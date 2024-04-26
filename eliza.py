"""
eliza.py
Ricardo Garriga-Ramos
CMSC-416-001 - INTRO TO NATURAL LANG PROCESS - feb 4 Spring 2024

Description : 
This is a reinterpritation of the Eliza chat bot developed at MIT in 1964.
The program reads user inputs and matches them to a colection of regular expressions.
These regular expressions act as phrases which have a set of short risponses which atempt to invite more conversation.
The final intent of this project is for the risponces to mimic a human psychologist.
Inorder to acomplish this goal, 
regluar expressions used sigle out the subjexts of a user's statment and restates it,
with every known phrase there is a paired risponse list which allows for some randomization between runs,
and when the program doesn't register a user input with a set risponse it has several varied statments
which atempt to change the subject or extract information that it could use.


Example exchange : 
-> [eliza] Hi, I'm a psychotherapist. What is your name?

=> [user] My name is Bridget.

-> [eliza] Hi Bridget. How can I help you today?

=> [Bridget] I want to rule the world.

-> [eliza] Bridget, why do you want to rule the world? [transform statement into ?]

=> [Bridget] I don't know, I think I crave power.

-> [eliza] Why don't you tell me more about your cravings. [word spot "crave" and respond.]

=> [Bridget] ... [uses the elips as the break keyword]

Use Instructions : 
Run the program in a Python 3 interpriter and type as the user into the command line.
At first the program will be looking for a name to personlize the epxrence.
If it doesn't find one it will continue with the option to change the user's name later on if prompted.
Otherwise it will continue to ingage with the user to the best of it's ability unless prompted with the string "..."
"""



import re
import random


def start():
    username = 'user'
    eliza = '\n-> [eliza] '
    print(eliza + 'Hi, I\'m a psychotherapist. What is your name?')
    user_stmt = input ('\n=> ['+ username +'] ')
    phrase_risponse_pairs, unknown_stmt_risponses = load_risponses(username)
    greetings = ["Hi " + username + ". How can I help you today?", "Nice to meet you " + username + ". How can I help you today?"]
    greeting = random.choice(greetings)
    regex = re.compile("(.*my name is|.*call me) (.*)", re.IGNORECASE)
    

    # start up greeting and name selection sequence
    if regex.match(user_stmt):
        username = regex.match(user_stmt).group(2)
        phrase_risponse_pairs, unknown_stmt_risponses = load_risponses(username)
        print(eliza + greeting)

    else:
        print(eliza + "Is your name " + user_stmt + "?")
        username = user_stmt
        phrase_risponse_pairs, unknown_stmt_risponses = load_risponses(username)
        user_stmt = input ('\n=> ['+ username +'] ')

        if re.compile("yes", re.IGNORECASE).match(user_stmt):
            print(eliza + greeting)

        else: 
            print(eliza + "Okay, I will continue with your name as user. What would you like to talk about today?")
            username = 'user'
            phrase_risponse_pairs, unknown_stmt_risponses = load_risponses(username)



    # start of normal loop
    user_stmt = input ('\n=> ['+ username +'] ')
    while user_stmt != '...':
        # keeps score on how often it was able to rispond to a user's input (used for testing)
        output = 0
        
        for phrase, risponses in phrase_risponse_pairs.items():

            regex = re.compile(phrase, re.IGNORECASE)
            phrase_known = regex.match(user_stmt)

            # in the case that they havent sent their name or want to change it
            if phrase_known and ((phrase == "my name is (.*)") or (phrase == "call me (.*)") or (phrase == ".*change.* name to (.*)")):
                
                username = phrase_known.group(1)
                phrase_risponse_pairs, unknown_stmt_risponses = load_risponses(username)
                
                risponse = random.choice(risponses)
                print(eliza + risponse.format(*phrase_known.groups()))
                output = 1

            # normal risponse procedure
            elif phrase_known:

                risponse = random.choice(risponses)
                print(eliza + risponse.format(*phrase_known.groups()))

                output = 1
        

        # user input was not found
        if output == 0:
            print(eliza + random.choice(unknown_stmt_risponses))
            output = -1





        # starts next iteration
        user_stmt = input ('\n=> ['+ username +'] ')

def load_risponses(username):
    

    phrase_risponse_pairs = {
        ".*my name is (.*)":["Hi {}. How can I help you today?", "Nice to meet you {}. How can I help you today?", "Thank you for telling me your name, {}."],
        ".*call me (.*)":["Hi {}. How can I help you today?", "Nice to meet you {}. How can I help you today?", "Thank you for telling me your name, {}."],
        "i want (.*)":[username + ", why do you want {}?", "What makes you want {}?", "{}?"],
        ".*i crave (.*)":["Why don't you tell me more about your cravings.", "Why do you crave {}?", "{}?"],
        "how are you??":["I'm doing well. How are you?"],
        "i (just)? wante?d? to say (hello|hi)":["Hi. How can I help you today?", "Hello, How can I help you today?"],
        "i am (.*)":["How long have you been {}?", "Why are you {}?"],
        "i'?m (.*)":["How long have you been {}?", "Why are you {}?"],
        ".*mom.*|.*mother.*":["Tell me more about your mom.", "Tell me more about your mother.", "How does your mom make you feel?"],
        ".*dad.*|.*father.*":["Tell me more about your dad.", "Tell me more about your father.", "How does your dad make you feel?"],
        ".*friend.*":["Tell me more about your friend.", "How do your friends make you feel?"],
        "i (.*) you":["Why do you {} me?", "What makes you think you {} me?", "I {} you too" + username],
        ".*thank you.*":["Your Welcome.","I bill by the hour."],
        ".*sorry.*":["No need to apologize " + username + ".", "There's no need to apologize.","Why are you sorry?","What are you apologizing for?", "It's okay " + username + ", no need to say sorry."],
        "i (.*) myself":["Wy do you {} yourself?", "What makes you {} yourself?", "What makes you think you {} yourself?"],
        "i feel (.*)":["Why do you feel {}?", "What makes you feel {}?", "How long have you felt {}?", "How long have you been feeling {}?"],
        ".*job.*":["Tell me about your job?"],
        ".*childhood.*|.*kid.*|.*younge?r?.*|.*growing up.*":["Tell me about your childhood.", "What was it like when you where a kid?", "what was it like growing up?"],
        "i was (.*)":["What changed?", "Are you still {}?", "Why were you {}?"],
        "it'?s? good|it is good|it was good":["Why is it good?","What was good about it?"],
        "it'?s? bad|it was bad|it is bad":["Why is it bad?","What was bad about it?"],
        ".*i'?m sure.*":["What makes you so sure?","Why are you so sure?",username + ", what makes you so sure?"],
        ".*yes.*":["Yes?", "What makes you so sure?","Yes? Could you elaborate?"],
        ".*no.*":["No?", "No? Could you elaborate?"],
        "i don'?t (.*)":["Why don't you {}?"],
        "i like (.*)":["why do you like {}?"],
        "i love (.*)":["why do you love {}?"],
        "i hate (.*)":["why do you hate {}?"],
        "good":["What makes it good?"],
        "bad":["What makes it bad?"],
        ".*i got (.*)":["What was it like to get {}?", "How did that make you feel?"],
        "i use to (.*)":["Why did you {}?", "Why did you stop?"],
        "i do(n'?t| not) know what to talk about|i do(n'?t| not) know what to say|i do(n'?t| not) know":["Tell me about your hobies.","Tell me about your family.", "Tell me about your friends.", "How do you spend your free time?","Tell me about your childood.","Why did you come talk to me today?"],
        ".*hobie.*":["Tell me more about your hobie."],
        ".*i get (.*)":["Why do you get {}?"],
        ".*change.* name to (.*)":["Okay I'll call you {}."]
        

    }

    unknown_stmt_risponses = [
        "Go on.",
        "Please tell me more.",
        "Could we talk about something else?",
        "Elaborate.",
        "Is there something else you'd like to talk about?",
        "Tell me more.",
        "Elaborate on that.",
        "How does that make you feel?",
        "How did that make you feel?",
        "Tell me more about yourself.",
        "How do you feel?"
    ]
        
    return phrase_risponse_pairs, unknown_stmt_risponses


start()




