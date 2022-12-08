import openai

def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()

openai.api_key = open_file('openaiapikey.txt').strip()

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

def start_chat(user1, user2, scenario = '', style = ''):
    conversation = list()
    gpt3_stop = [user1, user2]
    
    try:
        style = open_file(f'chats/styles/{style}.txt')
    except:
        pass
    try:
        scenario = open_file(f'chats/scenario/{scenario}.txt')
    except:
        pass

    user1_desc = open_file(f'chats/characters/{user1}.txt')
    user2_desc = open_file(f'chats/characters/{user2}.txt')
    prompt_template = open_file('chat_container.txt')

    prompt_template = prompt_template.replace('<<USER1 PROFILE>>', user1_desc)
    prompt_template = prompt_template.replace('<<USER2 PROFILE>>', user2_desc)
    prompt_template = prompt_template.replace('<<SCENARIO>>', scenario)
    prompt_template = prompt_template.replace('<<ROLEPLAY>>', style)
    prompt_template = prompt_template.replace('<<USER1>>', user1)
    prompt_template = prompt_template.replace('<<USER2>>', user2)


    while True:
        user_input = input(f'\n{user1} : ')
        conversation.append(f'\n{user1} : {user_input}')
        text_block = '\n'.join(conversation)

        prompt = prompt_template.replace('<<BLOCK>>', text_block)
        prompt = prompt + f'\n{user2} :'
        response = gpt3_completion(prompt, stop=gpt3_stop)

        print(f'\n{user2} :', response)
        conversation.append(f'\n{user2} : {response}')