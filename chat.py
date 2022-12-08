import openai
from os.path import exists

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
    temp=0.7, 
    top_p=1.0, 
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

    user1_desc = open_file(f'chats/characters/{user1}.txt')
    user2_desc = open_file(f'chats/characters/{user2}.txt')
    prompt_template = open_file('chat_container.txt')

    prompt_template = prompt_template.replace('<<USER1 PROFILE>>', user1_desc)
    prompt_template = prompt_template.replace('<<USER2 PROFILE>>', user2_desc)
    
    prompt_template = prompt_template.replace('<<SCENARIO>>', scenario)
    prompt_template = prompt_template.replace('<<ROLEPLAY>>', style)

    prompt_template = prompt_template.replace('<<USER1>>', user1)
    prompt_template = prompt_template.replace('<<USER2>>', user2)

    return prompt_template

def start_chat(user1, user2, scenario = '', style = '', history = ''):
    conversation = list()
    gpt3_stop = [user1, user2]
    prompt_template = get_prompt(user1, user2, scenario, style)
    
    history_data = open_file(f'chats/history/{history}.txt', history)
    if exists(f'chats/history/{history}.txt'):
        print(history_data)
        conversation = history_data.split('\n')
    else:
        with open(f'chats/history/{history}.txt', 'w') as f:
            pass

    while True:
        user_input = input(f'\n{user1}: ')
        conversation.append(f'\n{user1}: {user_input}')
        text_block = '\n'.join(conversation)

        prompt = prompt_template.replace('<<BLOCK>>', text_block)
        prompt = prompt + f'\n{user2}:'
        
        try:
            response = gpt3_completion(prompt, stop=gpt3_stop)
        except Exception as e:
            if ('Please reduce your prompt' in str(e)):
                conversation = cut_history(conversation, user1)
                text_block = ('\n'.join(conversation))
                prompt = prompt_template.replace('<<BLOCK>>', text_block)
                prompt = prompt + f'\n{user2}:'
                response = gpt3_completion(prompt, stop=gpt3_stop)
            else:
                pass

        print(f'\n{user2}:', response)
        conversation.append(f'\n{user2}: {response}')
        with open(f'chats/history/{history}.txt', 'w') as f:
            f.write('\n'.join(conversation))