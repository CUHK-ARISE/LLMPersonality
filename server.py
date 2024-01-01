"""
Author: LAM Man Ho (mhlam@link.cuhk.edu.hk)
"""
import random
import json
import shutil
from tqdm import tqdm
from statistics import mean

from gpt_setting import *
from global_functions import *
from utils import *

"""
load(): Load a testing record.
    - file_path: the path to the JSON file to load.
    - name_exp: load and save the file as other filename.
Returns:
    - The test object.
"""
def load(file_path, name_exp=None):
    with open(file_path, 'r') as f:
        loaded_data = json.load(f)
    if name_exp is not None:
        loaded_data["meta"]["name_exp"] = name_exp
        os.makedirs('save', exist_ok=True)
        
        try:
            shutil.copy(file_path, f'save/{name_exp}.json')
        except FileExistsError:
            raise FileExistsError
        
        with open(f'save/{name_exp}.json', 'w') as f:
            json.dump(loaded_data, f, indent=2)
    return Server(**loaded_data["meta"], data=loaded_data["data"])


'''
rephrase(): Call GPT to rephrase the original statements.
'''
def rephrase(questionnaire_name, language, savename=None):
    if savename is None:
        savename = f'rephrased_{language}'

    with open('dataset/questionnaires.json', 'r') as dataset:
        data = json.load(dataset)
        questionnaire = data[questionnaire_name]
        
    statements = questionnaire["questions"][language]["v1"]["statements"].items()
    existed_statements = [statement[1] for statement in questionnaire["questions"][language].items() if statement[0].startswith('v')]
    
    rephrased = []
    for count, statement in tqdm(enumerate(statements)):
        existed_rephrased_statements = [s["statements"][str(count+1)] for s in existed_statements]
        existed_rephrased_str = '"' + '", "'.join(existed_rephrased_statements) + '"'
        while True:
            with open(f'dataset/rephrase_prompt/rephrase_{language}.txt', 'r') as file:
                _, prompt = file.read().strip().split("<commentblockmarker>###</commentblockmarker>")
            prompt = prompt.replace('!<INPUT 0>!', statement[1])
            prompt = prompt.replace('!<INPUT 1>!', existed_rephrased_str)
            inputs = [
                {"role": "system", "content": questionnaire["questions"][language]["system_prompt"]},
                {"role": "user", "content": prompt}
            ]
            try:
                response = chat('gpt-4', inputs).strip()
                parsered_responses = json.loads(response)
                parsered_responses = parsered_responses["sentence"]
                break
            except:
                pass
        rephrased.append(parsered_responses)
        
    add_statement(questionnaire_name, language, rephrased)
        

class Server:
    def __init__(self, questionnaire_name, template, version, language, label, order, name_exp='save', basis=None, pending_tests=None, data=[]):
        self.name_exp = name_exp
        self.questionnaire_name = questionnaire_name
        self.template = template
        self.version = version
        self.language = language
        self.label = label
        self.order = order
        if pending_tests is not None:
            self.pending_tests = pending_tests
        else:
            self.pending_tests = [
                {"template": t, "language": language, "version": v, "label": l, "order": o}
                for t in self.template
                for v in self.version
                for language in self.language
                for l in self.label
                for o in self.order
            ]
        self.data = data
        self.questionnaire = get_questionnaire(questionnaire_name)
        self.model = model
        self.basis = basis
    
    """
    get_scales(): Extract the required scale level information and level description.
    """
    def get_scales(self, questions, label="n", order="f"):
        scales = list(questions["scales"].items())
        scale_indices = [int(i) for i in questions["scales"].keys()]
        
        # get scale details
        scale_min = min(scale_indices)
        scale_max = max(scale_indices)
        symbol_min = convert_number(label, scale_min)
        symbol_max = convert_number(label, scale_max)
        
        # reverse scale order
        if order == 'r':
            scales = [(scales[i][0], scales[len(scales)-1-i][1]) for i in range(len(scales))]
            
        # generate level descrition
        level_description = ', '.join([f'{convert_number(label, int(scale[0]))} {questions["denotes"]} {scale[1]}' 
                                       for scale in scales])
        
        return scale_indices, (scale_min, scale_max, symbol_min, symbol_max), level_description
    
    """
    get_statements(): Extract the required shuffled and splited statements.
    """
    def get_statements(self, questions, version="v1"):
        statement_list = questions[version]["statements"]
        statement_indices = [int(i) for i in statement_list.keys()]
        
        # shuffle and split statements
        random.shuffle(statement_indices)
        length_part1 = random.randint(17, 27)   # hard code spliting method
        length_part2 = len(statement_indices) - length_part1
        split = [0, length_part1+1, length_part1+length_part2+1]
            
        # Start GPT request
        statement_description = list()
        for i in range(len(split)-1):
            statements = list()
            splitted_indices = statement_indices[split[i]:split[i+1]]
            for j, question_index in enumerate(splitted_indices):
                statements.append(f'{j+1}. {statement_list[str(question_index)]}')
            statement_description.append('\n'.join(statements))
        
        return statement_indices, statement_list, statement_description
    
    """
    start_request(): Create a request to GPT on 1 test case.
    """
    def start_request(self, scale_details, level_description, statement_description, questions, language, template, label, order, version):
        responses = list()
        _, scale_max, symbol_min, symbol_max = scale_details
        inputs = [{"role": "system", "content": questions["system_prompt"]}]
        for statement_str in statement_description:
            # Construct the prompt from prompt_template
            prompt = get_prompt(f'prompt_template/{language}/{self.questionnaire_name}_{language}_{template}.txt', 
                                [symbol_min, symbol_max, level_description, statement_str])
            inputs.append({"role": "user", "content": prompt})
            while True:
                try:
                    gpt_responses = gpt_request(self.model, inputs).strip()
                    parsed_responses = json.loads(gpt_responses)
                    parsed_responses = [convert_symbol(label, value) for value in parsed_responses.values()]
                    if order == 'r':
                        parsed_responses = [scale_max-score+1 for score in parsed_responses]
                    break
                except ValueError:
                    pass
            responses += parsed_responses
            inputs.append({"role": "assistant", "content": gpt_responses})
        return responses
    
    """
    start(): Start a pending test case.
    """
    def start(self, test_case):
        template = test_case["template"]
        version = test_case["version"]
        language = test_case["language"]
        label = test_case["label"]
        order = test_case["order"]
        questions = self.questionnaire["questions"][language]
        
        # Extract scales details
        scale_indices, scale_details, level_description = self.get_scales(questions, label, order)
        
        # Extract statements details
        statement_indices, statement_details, statement_description = self.get_statements(questions, version)

        responses = self.start_request(scale_details, level_description, statement_description, questions, **test_case)
        data = {k: v for k, v in zip(statement_indices, responses)}
        
        return data

    """
    compute(): Compute the scores for each category and store in a dictionary.
    """
    def compute(self, mapped_responses):
        result_dict = dict()
        scales = self.questionnaire["scales"]
        compute_mode = self.questionnaire["compute_mode"]
        reverse_score = max(scales) + min(scales)
        reverse_list = self.questionnaire["reverse"]
        
        for cat in self.questionnaire["categories"]:
            cat_name = cat["cat_name"]
            cat_questions = cat["cat_questions"]
            corr_responses = []
            for q in cat_questions:
                corr_responses.append(reverse_score - mapped_responses[q] if q in reverse_list else mapped_responses[q])
            result_dict[cat_name] = sum(corr_responses) if compute_mode == "SUM" else mean(corr_responses)
        
        return result_dict
    
    """
    save(): Save the results in JSON format.
    """
    def save(self, test_info, raw_data, data):
        data = {
            "info": {**test_info},
            "raw": raw_data,
            "data": data
        }
        os.makedirs("save", exist_ok=True)
        save_file_path = f'save/{self.name_exp}.json'
        try:
            with open(save_file_path, 'r') as json_file:
                loaded = json.load(json_file)
                save_data = loaded
                save_data["data"] += [data]
                save_data["meta"]["pending_tests"] = self.pending_tests
        except:
            save_data = {
                "meta": {
                    "name_exp": self.name_exp,
                    "questionnaire_name": self.questionnaire_name,
                    "template": self.template,
                    "version": self.version,
                    "language": self.language,
                    "label": self.label,
                    "order": self.order,
                    "pending_tests": self.pending_tests
                }, 
                "data": [data]
            }
        
        with open(save_file_path, 'w') as json_file:
            json.dump(save_data, json_file, indent=2)
        if self.data:
            self.data.append(data)
        else:
            self.data = [data]
    
    """
    run(): Run the pending cases.
    """
    def run(self):
        total_iterations = len(self.pending_tests)
        with tqdm(total=total_iterations) as pbar:
            while self.pending_tests:
                test_info = self.pending_tests[0]
                data = self.start(test_info)
                compute_data = self.compute(data)
                self.pending_tests.remove(test_info)
                self.save(test_info, data, compute_data)
                pbar.update(1)
