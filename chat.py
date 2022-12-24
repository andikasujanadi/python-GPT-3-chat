import openai
from os.path import exists
import datetime

def open_file(filepath, exception=''):
    try:
        with open(filepath, 'r', encoding='utf-8') as infile:
            return infile.read().strip()
    except:
        return exception

openai.api_key = open_file('openaiapikey.txt')

def gpt3_completion(prompt, 
    stop, 
    engine='text-davinci-003', 
    temp=0.9, 
    top_p=1, 
    tokens=400, 
    freq_pen=0.0, 
    pres_pen=0.6):
    prompt = prompt.encode(encoding='ASCII',errors='ignore').decode()
    response = openai.Completion.create(
        engine=engine,
        prompt=prompt,
        temperature=temp,
        max_tokens=tokens,
        top_p=top_p,
        frequency_penalty=freq_pen,
        presence_penalty=pres_pen,
        stop=stop)
    text = response['choices'][0]['text'].strip()
    return text

def cut_history(history, user):
    lenght = int(len(history)/2)
    point = lenght
    while (point<len(history)):
        try:
            if f'{user}:' in history[point]:
                point-=1
                break
        except:
            pass
        point +=1
    return (history[-point:])

def get_prompt(user1, user2, scenario = '', style = ''):
    style = open_file(f'chats/styles/{style}.txt')
    scenario = open_file(f'chats/scenario/{scenario}.txt')
    now = datetime.datetime.now()
    today = now.strftime("today is %A, %d %B %Y")

    user1_desc = open_file(f'chats/characters/{user1}.txt')
    user2_desc = open_file(f'chats/characters/{user2}.txt')
    prompt_template = open_file('chat_container.txt')

    prompt_template = prompt_template.replace('<<USER1 PROFILE>>', user1_desc)
    prompt_template = prompt_template.replace('<<USER2 PROFILE>>', user2_desc)
    
    prompt_template = prompt_template.replace('<<SCENARIO>>', scenario)
    prompt_template = prompt_template.replace('<<STYLE>>', style)
    prompt_template = prompt_template.replace('<<DATE>>', today)

    prompt_template = prompt_template.replace('<<USER1>>', user1)
    prompt_template = prompt_template.replace('<<USER2>>', user2)

    return prompt_template

def start_chat(user1, user2, scenario = '', style = '', history = False, cli = True):
    conversation = list()
    gpt3_stop = [user1, user2]
    prompt_template = get_prompt(user1, user2, scenario, style)
    
    if (history != False) or (history == ''):
        history_data = open_file(f'chats/history/{history}.txt', history)
    if exists(f'chats/history/{history}.txt'):
        if cli:
            print(history_data)
        conversation = history_data.split('\n')
    else:
        with open(f'chats/history/{history}.txt', 'w') as f:
            pass
    
    err = 'no error'
    response = ''
    
    while True:
        user_input = input(f'\n{user1}: ')
        conversation.append(f'\n{user1}: {user_input}')
        text_block = '\n'.join(conversation)

        prompt = prompt_template.replace('<<BLOCK>>', text_block)
        prompt = prompt + f'\n{user2}:'
        
        try:
            response = gpt3_completion(prompt, stop=gpt3_stop)
            err = 'no error'
        except Exception as e:
            if ('Please reduce your prompt' in str(e)):
                err = 'max prompt'
                conversation = cut_history(conversation, user1)
                text_block = ('\n'.join(conversation))
                prompt = prompt_template.replace('<<BLOCK>>', text_block)
                prompt = prompt + f'\n{user2}:'
                try:
                    response = gpt3_completion(prompt, stop=gpt3_stop)
                    err = 'no error'
                except:
                    pass
            elif ('Error communicating with OpenAI' in str(e)):
                err = 'offline'
                pass
            else:
                pass

        if err in ['no error']:
            if cli:
                print(f'\n{user2}:', response)

            conversation.append(f'\n{user2}: {response}')
            if (history != False) or (history == ''):
                with open(f'chats/history/{history}.txt', 'w') as f:
                    f.write('\n'.join(conversation))
        else:
            print(f'[[SYSTEM ERROR, ERROR CODE: {err}]]')