# =========== Copyright 2023 @ CAMEL-AI.org. All Rights Reserved. ===========
# Licensed under the Apache License, Version 2.0 (the “License”);
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an “AS IS” BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =========== Copyright 2023 @ CAMEL-AI.org. All Rights Reserved. ===========
import argparse
import logging
import os
import sys
from camel.typing import ModelType
import subprocess
import json
import time
import signal
import random
from chatdev.process_agent import  *
from chatdev.trace_container import TraceContainer
from playmusic import MusicPlayer


root = os.path.dirname(__file__)
sys.path.append(root)

from chatdev.chat_chain import ChatChain

try:
    from openai.types.chat.chat_completion_message_tool_call import ChatCompletionMessageToolCall
    from openai.types.chat.chat_completion_message import FunctionCall

    openai_new_api = True  # new openai api version
except ImportError:
    openai_new_api = False  # old openai api version
    print(
        "Warning: Your OpenAI version is outdated. \n "
        "Please update as specified in requirement.txt. \n "
        "The old API interface is deprecated and will no longer be supported.")



def trace_hallucination_judgment(main_directory: str):
    directory = main_directory
    main_script = os.path.join(directory, "main.py")
    # check whether the main.py exist 
    if not os.path.exists(main_script):
        return True, f"Error: {main_script} not found."
    success_info = "The software run successfully without errors."
    try:

        # check if we are on windows or linux
        if os.name == 'nt':
            command = "cd {} && dir && python main.py".format(directory)
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
            )
        else:
            command = "cd {}; ls -l; python3 main.py;".format(directory)
            process = subprocess.Popen(command,
                                        shell=True,
                                        preexec_fn=os.setsid,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE
                                        )
        time.sleep(3)
        return_code = process.returncode
        # Check if the software is still running
        if process.poll() is None:
            if "killpg" in dir(os):
                os.killpg(os.getpgid(process.pid), signal.SIGTERM)
            else:
                os.kill(process.pid, signal.SIGTERM)
                if process.poll() is None:
                    os.kill(process.pid, signal.CTRL_BREAK_EVENT)

        if return_code == 0:
            return False, success_info
        else:
            error_output = process.stderr.read().decode('utf-8')
            if error_output:
                if "Traceback".lower() in error_output.lower():
                    errs = error_output.replace(directory + "/", "")
                    return True, errs
            else:
                return False, success_info
    except subprocess.CalledProcessError as e:
        return True, f"Error: {e}"
    except Exception as ex:
        return True, f"An error occurred: {ex}"

    return False, success_info



def get_config(company):
    """
    return configuration json files for ChatChain
    user can customize only parts of configuration json files, other files will be left for default
    Args:
        company: customized configuration name under CompanyConfig/

    Returns:
        path to three configuration jsons: [config_path, config_phase_path, config_role_path]
    """
    config_dir = os.path.join(root, "CompanyConfig", company)
    default_config_dir = os.path.join(root, "CompanyConfig", "Default")

    config_files = [
        "ChatChainConfig.json",
        "PhaseConfig.json",
        "RoleConfig.json"
    ]

    config_paths = []

    for config_file in config_files:
        company_config_path = os.path.join(config_dir, config_file)
        default_config_path = os.path.join(default_config_dir, config_file)

        if os.path.exists(company_config_path):
            config_paths.append(company_config_path)
        else:
            config_paths.append(default_config_path)

    return tuple(config_paths)


parser = argparse.ArgumentParser(description='argparse')
parser.add_argument('--config', type=str, default="Default",
                    help="Name of config, which is used to load configuration under CompanyConfig/")
parser.add_argument('--org', type=str, default="DefaultOrganization",
                    help="Name of organization, your software will be generated in WareHouse/name_org_timestamp")
parser.add_argument('--task', type=str, default="Develop a basic Gomoku game.",
                    help="Prompt of software")
parser.add_argument('--name', type=str, default="Gomoku",
                    help="Name of software, your software will be generated in WareHouse/name_org_timestamp")
parser.add_argument('--model', type=str, default="GPT_4",
                    help="GPT Model, choose from {'GPT_3_5_TURBO','GPT_4','GPT_4_32K', 'GPT_4_TURBO'}")
# parser.add_argument('--model', type=str, default="GPT_4",
#                     help="GPT Model, choose from {'GPT_3_5_TURBO','GPT_4','GPT_4_32K', 'GPT_4_TURBO'}")
parser.add_argument('--path', type=str, default="",
                    help="Your file directory, ChatDev will build upon your software in the Incremental mode")
args = parser.parse_args()

# ----------------------------------------
#          Init TraceContainer
# ----------------------------------------

trace_file = 'traces_data.txt'
with open(trace_file, 'r') as file:
    data = file.read()
    traces = json.loads(data)

trace_container = TraceContainer(traces)


# DynPro Experimential Evaculation (extract the process from instance pool)
   
# process_trace = random.choice(list(traces.keys()))
# process_trace_list = process_trace.split(' -> ')



# DynPro argument(input the process text to llm, and argument the capability of the llm to generate better instance)

# agent = ProcessAgent()
# total_prompt = get_PoT_prompt(args.task)
# agent.setPrompt(total_prompt)
# response = agent.ask(0.6)
# print(response)
# process_trace_list = extract_trace(response)
# process_trace = " -> ".join(process_trace_list)
# append_to_hyperparameters_json(args.name, 0.6, args.task, total_prompt, process_trace, None, "traces_hyperparameters.txt")

# print("**[INFO]**  <This trace is a new trace, ready to execute:>  " + process_trace)



# before argument
agent = ProcessAgent()
example_trace = list(trace_container.traces.keys())

total_prompt = get_total_prompt(args.task, example_trace)
agent.setPrompt(total_prompt)


# ----------------------------------------
#         choose traces by UCT
# ----------------------------------------   
temperature = init_temperature()
response = agent.ask(temperature)
process_trace_list = extract_trace(response)
process_trace = " -> ".join(process_trace_list)
append_to_hyperparameters_json(args.name, temperature, args.task, total_prompt, process_trace, None, "traces_hyperparameters.txt")


#if the trace has been visited, then calculate the uct and make the distribution 
if process_trace in example_trace:
    print("**[INFO]**  <Generated trace is:>  " + process_trace)
    process_trace = trace_container.select_action_distribution() 
    process_trace_list = extract_trace(process_trace)
    print("**[INFO]**  <This trace is exist, compared by all traces' UCT, the execution trace is:>  " + process_trace)
    
else:
    print("**[INFO]**  <This trace is a new trace, ready to execute:>  " + process_trace)


    

# Start ChatDev

# ----------------------------------------
#          Init ChatChain
# ----------------------------------------
config_path, config_phase_path, config_role_path = get_config(args.config)
args2type = {'GPT_3_5_TURBO': ModelType.GPT_3_5_TURBO,
             'GPT_4': ModelType.GPT_4,
             'GPT_4_32K': ModelType.GPT_4_32k,
             'GPT_4_TURBO': ModelType.GPT_4_TURBO,
             'GPT_4_TURBO_V': ModelType.GPT_4_TURBO_V
             }
if openai_new_api:
    args2type['GPT_3_5_TURBO'] = ModelType.GPT_3_5_TURBO_NEW

chat_chain = ChatChain(config_path=config_path,
                       config_phase_path=config_phase_path,
                       config_role_path=config_role_path,
                       task_prompt=args.task,
                       project_name=args.name,
                       org_name=args.org,
                       model_type=args2type[args.model],
                       code_path=args.path,
                       trace_list=process_trace_list)

# ----------------------------------------
#          Init Log
# ----------------------------------------
logging.basicConfig(filename=chat_chain.log_filepath, level=logging.INFO,
                    format='[%(asctime)s %(levelname)s] %(message)s',
                    datefmt='%Y-%d-%m %H:%M:%S', encoding="utf-8")

# ----------------------------------------
#          Pre Processing
# ----------------------------------------

chat_chain.pre_processing()

# ----------------------------------------
#          Personnel Recruitment
# ----------------------------------------

chat_chain.make_recruitment()

# ----------------------------------------
#          Chat Chain
# ----------------------------------------

chat_chain.execute_chain()

# ----------------------------------------
#          Post Processing
# ----------------------------------------

chat_chain.post_processing()

# ----------------------------------------
#          Environment Check
# ----------------------------------------


if  chat_chain.chat_env.env_dict['break_flag']:
    trace_hallucination_flag = True
    message = "**[INFO]**  <Trace Structure error>"
else:

    (trace_hallucination_flag, message) = trace_hallucination_judgment(chat_chain.chat_env.env_dict['directory'])
    print(chat_chain.chat_env.env_dict['directory'])
    


# ----------------------------------------------------------------
#             update trace_container
# ----------------------------------------------------------------
print("The hallucination_flag is:  " + str(trace_hallucination_flag))
trace_container.update(process_trace, trace_hallucination_flag)
print(message)
with open(trace_file, 'w') as file:
    json.dump(trace_container.traces, file)
    
# process over
player = MusicPlayer('music.wav')
# play over music
player.play()

print("Complete the trace analysis  Container update:   " + process_trace)
