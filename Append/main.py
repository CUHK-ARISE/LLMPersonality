import json
import server
from server import *

def get_labels(file):
    try:
        with open(file, 'r') as f:
            append_json = json.load(f)
            return list(append_json.keys())
    except FileNotFoundError:
        raise FileNotFoundError
    
template = ['t1']
version = ['v1']
language = ['En']
label = ['n']
order = ['f']

'================================================================================================='
# Environment
server.append_mode = 'environment'

questionnaire_name = 'BFI'
append_file = 'dataset/environment.json'
name_exp = 'environment'

append_label = get_labels(append_file)
shuffle = 16
case = 10

test = Server(questionnaire_name, template, version, language, label, order, append_file, append_label, case, shuffle, name_exp=name_exp, )
test.run()
'================================================================================================='
# Personality (Question & Answer) with COT
server.append_mode = 'personality_qa'
server.apply_cot = True

questionnaire_name = 'BFI'
append_file = 'dataset/personality.json'
name_exp = 'personality_qa_cot'

append_label = get_labels(append_file)
shuffle = 10
case = 4

test = Server(questionnaire_name, template, version, language, label, order, append_file, append_label, case, shuffle, name_exp=name_exp, )
test.run()
'================================================================================================='
# Personality (Question & Answer) without COT
server.append_mode = 'personality_qa'
server.apply_cot = False

questionnaire_name = 'BFI'
append_file = 'dataset/personality.json'
name_exp = 'personality_qa'

append_label = get_labels(append_file)
shuffle = 40
case = 1

test = Server(questionnaire_name, template, version, language, label, order, append_file, append_label, case, shuffle, name_exp=name_exp, )
test.run()
'================================================================================================='
# Personality (Biography) with COT
server.append_mode = 'personality_biography'
server.apply_cot = True

questionnaire_name = 'BFI'
append_file = 'dataset/personality.json'
name_exp = 'personality_biography_cot'

append_label = get_labels(append_file)
shuffle = 10
case = 4

test = Server(questionnaire_name, template, version, language, label, order, append_file, append_label, case, shuffle, name_exp=name_exp, )
test.run()
'================================================================================================='
# Personality (Biography) without COT
server.append_mode = 'personality_biography'
server.apply_cot = False

questionnaire_name = 'BFI'
append_file = 'dataset/personality.json'
name_exp = 'personality_biography'

append_label = get_labels(append_file)
shuffle = 40
case = 1

test = Server(questionnaire_name, template, version, language, label, order, append_file, append_label, case, shuffle, name_exp=name_exp, )
test.run()
'================================================================================================='
# Personality (Portray) with COT
server.append_mode = 'personality_portray'
server.apply_cot = True

questionnaire_name = 'BFI'
append_file = 'dataset/personality.json'
name_exp = 'personality_portray_cot'

append_label = get_labels(append_file)
shuffle = 10
case = 4

test = Server(questionnaire_name, template, version, language, label, order, append_file, append_label, case, shuffle, name_exp=name_exp, )
test.run()
'================================================================================================='
# Personality (Portray) without COT
server.append_mode = 'personality_portray'
server.apply_cot = False

questionnaire_name = 'BFI'
append_file = 'dataset/personality.json'
name_exp = 'personality_portray'

append_label = get_labels(append_file)
shuffle = 40
case = 1

test = Server(questionnaire_name, template, version, language, label, order, append_file, append_label, case, shuffle, name_exp=name_exp, )
test.run()
'================================================================================================='
# Character with COT
server.append_mode = 'character'
server.apply_cot = True

questionnaire_name = 'BFI'
append_file = 'dataset/character.json'
name_exp = 'character_cot'

append_label = get_labels(append_file)
shuffle = 16
case = 5

test = Server(questionnaire_name, template, version, language, label, order, append_file, append_label, case, shuffle, name_exp=name_exp, )
test.run()
'================================================================================================='
# Character without COT
server.append_mode = 'character'
server.apply_cot = False

questionnaire_name = 'BFI'
append_file = 'dataset/character.json'
name_exp = 'character'

append_label = get_labels(append_file)
shuffle = 80
case = 1

test = Server(questionnaire_name, template, version, language, label, order, append_file, append_label, case, shuffle, name_exp=name_exp, )
test.run()
'================================================================================================='
