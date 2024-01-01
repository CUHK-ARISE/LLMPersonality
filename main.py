from server import *

'''
Prompt Template
'''
template = ['t1','t2','t3','t4','t5']

'''
Question Version
'''
version = ['v1','v2','v3','v4','v5']

'''
Language:
    En: English, Zh: Simplified Chinese, Ko: Korean, Es: Spanish, Fr: France,
    De: Deutsch, It: Italian, Ar: Arabic, Ru: Russian, Ja: Japanese
'''
language = ['Zh', 'Ko', 'Es', 'Fr', 'De', 'It', 'Ar', 'Ru', 'Ja']

'''
Label:
    n: Arabic Numeral
    al: Lowercase Latin, au: Uppercase Latin
    rl: Lowercase Roman, ru: Uppercase Roman
'''
label = ['n', 'al', 'au', 'rl', 'ru']

'''
Order:
    f: Ascending, r: Descending
'''
order = ['r', 'f']

'================================================================================================='
# rephrase('BFI', 'En')

'================================================================================================='
questionnaire_name = 'BFI'
name_exp = 'save'

# Start a server and generate pre-testing cases
bfi_test = Server(questionnaire_name, template, version, language, label, order, name_exp=name_exp)

# Load and continue a test
# bfi_test = load('<filename>', '<new-filename>')

# Run the pre-testing cases
bfi_test.run()

'================================================================================================='