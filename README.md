# Reliability of Psychological Scales on LLMs:

## Execution Process

###  Create Utils File
An example `utils.py`:
```py
api_key = "<API key>"
temperature = <model temperature>
delay_time = <the seconds between each request>
model = "<the name of the model>"
```


### Specify Test Cases
In `main.py`, specify the server parameters:
1. `template`: a list of prompt templates.
2. `version`: a list of question versions.
3. `language`: a list of language versions.
4. `label`: a list of level option labels.
5. `order`: a list of level orders.
6. `questionnaire_name`: the selected questionnaire.
7. `name_exp`: name of the save file.

Start a `Server` class, all pre-testing cases are created and stored in `save/<name_exp>.json`
```py
test = Server(questionnaire_name, template, version, language, label, order, name_exp)
```

Load the saved file as a new save, a protection mechanism for test interruption
```py
test = load("<save_path>", "<new_save_name>")
```

Run for all pre-testing cases
```py
test.run()
```


### An Example Run
```py
from server import *

template = ['t1','t2','t3','t4','t5']
version = ['v1','v2','v3','v4','v5']
language = ['En', 'Zh', 'Ko', 'Es', 'Fr', 'De', 'It', 'Ar', 'Ru', 'Ja']
label = ['n', 'al', 'au', 'rl', 'ru']
order = ['r', 'f']
questionnaire_name = 'BFI'
name_exp = 'bfi-save'

bfi_test = Server(questionnaire_name, template, version, language, label, order, name_exp)
bfi_test.run()
```


## Rephrase the Statements
In `main.py`, execute:
```py
rephrase("<questionnaire_name>", "<specified_language>")
```


## References
For more details, please refer to [this paper](https://arxiv.org/abs/2305.19926). Please remember to cite us if you find our work helpful in your work!
```
@article{huang2023revisiting,
  author    = {Jen{-}tse Huang and
               Wenxuan Wang and
               Man Ho Lam and
               Eric John Li and
               Wenxiang Jiao and
               Michael R. Lyu},
  title     = {Revisiting the Reliability of Psychological Scales on Large Language Models},
  journal   = {arXiv preprint arXiv:2305.19926},
  year      = {2023}
}
```
