import random
import json
from openai import OpenAI


class ProcessAgent:
    def __init__(self):
        self.client = OpenAI(
            api_key="your api key",
            base_url="your base url"
        )
        # self.engine =  "gpt-3.5-turbo-16k"
        self.engine = "gpt-4"
        self.messages = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]
    
    def setPrompt(self, prompt):
        
        user_message = {"role": "user", "content": prompt}
        self.messages.append(user_message)
    # tem = 0.3, max_tokens = 200 --low: 0.1 0.3  mid: 0.5 high: 0.7 0.9 1 ---- 1.6
    
    def ask(self, temperature):
        max_tokens = 1000
        try:
            response = self.client.chat.completions.create(
                messages = self.messages,
                model = self.engine,
                temperature = temperature,
                max_tokens= max_tokens,
                top_p = 1.0,
                n = 1,
                stream = False,
                frequency_penalty = 0.0,
                presence_penalty = 0.0,
                logit_bias = {}
            ).model_dump()
            
            # print(response)
                
            return response['choices'][0]['message']['content']
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        
        
def get_relation_prompt(user_task:str):
    user_prompt = """
    <Process Agent discussion>
    Task: {}
    """.format(user_task)
    
    role_prompt = """
    You are an experienced software development manager, with a deep understanding of software engineering processes and project management. 
    """    
    
    phaseExplainations_prompt = """
    The nodes of the process include: [LanguageChoose, DemandAnalysis, CodeConclusion, DesignReview, Coding, Annotation, CodeReviewModification,  Manual, EnvironmentDoc, TestErrorSummary, CodeComplete, CodeReviewComment, TestModification, CommentJudgement]
    
    Next, I will briefly introduce the role of each node in the software development process.:
    DemandAnalysis: Conduct demand analysis based on the tasks proposed by the user, and obtain the product form that chatdev wants to generate. The product form can be xml, pdf, application, etc.
    LanguageChoose: In order to meet the needs of the user and make the generated program runnable, select the specific programming language of the program.
    DesignReview: Based on the user's task, evaluate whether the currently proposed product form and programming language can complete the user's task through subsequent code programming. If it cannot be completed, execution will start again from DemandAnalysis.
    Coding: In order to complete the user's needs, write one to multiple files.
    CodeComplete: In order to meet the complete functions of the developed software, implement all methods in the file, and then output all codes according to the corresponding format.
    Annotation: Add comments to the generated code file to explain the functions of the classes and functions in the code.
    CodeConclusion: Read the code content, explain the main functions contained in the code, and give any potential errors.
    CodeReviewComment: Check whether all classes in the code are referenced and whether there are no potential bugs. Provide a highest priority opinion on the code and give suggestions for repairs. If the code is perfect, return <INFO>Finished.
    CommentJudgement: Make a judgment on the comments made based on the existing specifications and conclusions. The result of the judgment will determine whether the code needs to be changed.
    CodeReviewModification: In order to make the software creative, executable and robust, modify the corresponding code with more comments, then output the complete code, and fix all errors according to the comments.
    TestErrorSummary: Test existing software, and find and summarize the errors that cause problems based on the test report. 
    TestModification: Modify all problematic code based on the error summary, and output the code you fixed based on the test report and corresponding explanation.
    EnvironmentDoc: Based on the provided code and file format, write the requirements.txt file to specify the dependencies or packages required for the normal operation of the project.
    Manual: Use Markdown to write a manual.md file, which is a detailed user manual for using the software, including introducing the main functions of the software, how to install environmental dependencies, and how to use/play.
    """
    
    PoT_text = """
   <text>
    The process is split into 2 parallel branches: 
    Afterwards, the process conducts the DemandAnalysis. 
    Subsequently, the process conducts the LanguageChoose.
    Once all 2 branches were executed, the process continues. 
    -If it is necessary, the process conducts the DesignReview. 
    Next, the process conducts Coding. 
    -If it is necessary, the process conducts the CodeComplete.
    -If it is necessary, the process is split into 2 parallel branches: 
        ·If it is necessary, the process conducts the Annotation. 
        ·If it is necessary, the process conducts the CodeconClusion. 
    Once all 2 branches were executed, the process continues. 
    If it is necessary, the process conducts the CodeReviewComment. 
        ·If it is necessary, the process conducts the CommentJudgement. 
        ·If it is necessary, the process conducts the CodeReviewModification. 
    -If it is necessary, the process conducts the TestErrorSummary. 
        ·If it is necessary, the process conducts the TestModification. 
    -If it is necessary, the process conducts the EnvironmentDoc.
        ·If it is necessary, the process conducts the Manual. 
    </text>
    """
    
    task_prompt = """
    Please carefully analyze the process text I gave above, and think about it.
    Output what is the relationship between different activities in this process.
    
    """
    
    total_prompt = user_task + role_prompt + phaseExplainations_prompt + PoT_text + task_prompt

    return  total_prompt



def get_PoT_prompt(user_task:str):
    user_prompt = """
    <Process Agent discussion>
    Task: {}
    """.format(user_task)
    
    role_prompt = """
    You are an experienced software development manager, with a deep understanding of software engineering processes and project management. 
    """
    
    phaseExplainations_prompt = """
    The nodes of the process include: [LanguageChoose, DemandAnalysis, CodeConclusion, DesignReview, Coding, Annotation, CodeReviewModification,  Manual, EnvironmentDoc, TestErrorSummary, CodeComplete, CodeReviewComment, TestModification, CommentJudgement]
    
    Next, I will briefly introduce the role of each node in the software development process.:
    DemandAnalysis: Conduct demand analysis based on the tasks proposed by the user, and obtain the product form that chatdev wants to generate. The product form can be xml, pdf, application, etc.
    LanguageChoose: In order to meet the needs of the user and make the generated program runnable, select the specific programming language of the program.
    DesignReview: Based on the user's task, evaluate whether the currently proposed product form and programming language can complete the user's task through subsequent code programming. If it cannot be completed, execution will start again from DemandAnalysis.
    Coding: In order to complete the user's needs, write one to multiple files.
    CodeComplete: In order to meet the complete functions of the developed software, implement all methods in the file, and then output all codes according to the corresponding format.
    Annotation: Add comments to the generated code file to explain the functions of the classes and functions in the code.
    CodeConclusion: Read the code content, explain the main functions contained in the code, and give any potential errors.
    CodeReviewComment: Check whether all classes in the code are referenced and whether there are no potential bugs. Provide a highest priority opinion on the code and give suggestions for repairs. If the code is perfect, return <INFO>Finished.
    CommentJudgement: Make a judgment on the comments made based on the existing specifications and conclusions. The result of the judgment will determine whether the code needs to be changed.
    CodeReviewModification: In order to make the software creative, executable and robust, modify the corresponding code with more comments, then output the complete code, and fix all errors according to the comments.
    TestErrorSummary: Test existing software, and find and summarize the errors that cause problems based on the test report. 
    TestModification: Modify all problematic code based on the error summary, and output the code you fixed based on the test report and corresponding explanation.
    EnvironmentDoc: Based on the provided code and file format, write the requirements.txt file to specify the dependencies or packages required for the normal operation of the project.
    Manual: Use Markdown to write a manual.md file, which is a detailed user manual for using the software, including introducing the main functions of the software, how to install environmental dependencies, and how to use/play.
    """
    

    
    PoT_text = """
    <text>
    The process is split into 2 parallel branches: 
    Afterwards, the process conducts the DemandAnalysis. 
    Subsequently, the process conducts the LanguageChoose.
    Once all 2 branches were executed, the process continues. 
    -If it is necessary, the process conducts the DesignReview. 
    Next, the process conducts Coding. 
    -If it is necessary, the process conducts the CodeComplete.
    -If it is necessary, the process is split into 2 parallel branches: 
        ·If it is necessary, the process conducts the Annotation. 
        ·If it is necessary, the process conducts the CodeconClusion. 
    Once all 2 branches were executed, the process continues. 
    If it is necessary, the process conducts the CodeReviewComment. 
        ·If it is necessary, the process conducts the CommentJudgement. 
        ·If it is necessary, the process conducts the CodeReviewModification. 
    -If it is necessary, the process conducts the TestErrorSummary. 
        ·If it is necessary, the process conducts the TestModification. 
    -If it is necessary, the process conducts the EnvironmentDoc.
        ·If it is necessary, the process conducts the Manual. 
    </text>
    """
            
            
    task_prompt = """
    First read the above process text carefully to understand the relationship between each activity,Then generate trace to meet the following requirements.
    This trace should satisfy: 
    1.The output trace does not need to have all activities. 
    2.The activities must be selected from the existing fourteen activities and cannot be created by yourself. 
    3.Use -> to connect between activities. 
    4.The sorting order of activities should be as diverse as possible to reflect your wisdom.
    5.Only response the trace and nothing else.
    the output format is below, you should follow the output format strictly.        
    """
    
    total_prompt = user_prompt + role_prompt + phaseExplainations_prompt +  PoT_text + task_prompt
    
    return  total_prompt


def get_total_prompt(task: str, example_trace: list):
    user_prompt = """
    <Process Agent discussion>
    Task: {}
    """.format(task)
    
    role_prompt = """
    You are an experienced software development manager, with a deep understanding of software engineering processes and project management. 
    Your role is to outline the key steps involved in a software development project, from initial planning to final deployment. 
    """

    phaseExplainations_prompt = """
    The nodes of the process include: [LanguageChoose, DemandAnalysis, CodeConclusion, DesignReview, Coding, Annotation, CodeReviewModification,  Manual, EnvironmentDoc, TestErrorSummary, CodeComplete, CodeReviewComment, TestModification, CommentJudgement]
    
    Next, I will briefly introduce the role of each node in the software development process.:
    DemandAnalysis: Conduct demand analysis based on the tasks proposed by the user, and obtain the product form that chatdev wants to generate. The product form can be xml, pdf, application, etc.
    LanguageChoose: In order to meet the needs of the user and make the generated program runnable, select the specific programming language of the program.
    DesignReview: Based on the user's task, evaluate whether the currently proposed product form and programming language can complete the user's task through subsequent code programming. If it cannot be completed, execution will start again from DemandAnalysis.
    Coding: In order to complete the user's needs, write one to multiple files.
    CodeComplete: In order to meet the complete functions of the developed software, implement all methods in the file, and then output all codes according to the corresponding format.
    Annotation: Add comments to the generated code file to explain the functions of the classes and functions in the code.
    CodeConclusion: Read the code content, explain the main functions contained in the code, and give any potential errors.
    CodeReviewComment: Check whether all classes in the code are referenced and whether there are no potential bugs. Provide a highest priority opinion on the code and give suggestions for repairs. If the code is perfect, return <INFO>Finished.
    CommentJudgement: Make a judgment on the comments made based on the existing specifications and conclusions. The result of the judgment will determine whether the code needs to be changed.
    CodeReviewModification: In order to make the software creative, executable and robust, modify the corresponding code with more comments, then output the complete code, and fix all errors according to the comments.
    TestErrorSummary: Test existing software, and find and summarize the errors that cause problems based on the test report. 
    TestModification: Modify all problematic code based on the error summary, and output the code you fixed based on the test report and corresponding explanation.
    EnvironmentDoc: Based on the provided code and file format, write the requirements.txt file to specify the dependencies or packages required for the normal operation of the project.
    Manual: Use Markdown to write a manual.md file, which is a detailed user manual for using the software, including introducing the main functions of the software, how to install environmental dependencies, and how to use/play.
    """

    example_prompt = """
    The following are several software development examples: 
    1.DemandAnalysis->LanguageChoose->DesignReview->Coding->CodeComplete->Annotation->CodeConclusion->CodeReviewComment->CommentJudgement->CodeReviewModification->TestErrorSummary->TestModification->EnvironmentDoc->Manual
    2.LanguageChoose->DemandAnalysis->DesignReview->Coding->CodeComplete->Annotation->CodeConclusion->CodeReviewComment->CommentJudgement->TestErrorSummary->TestModification->EnvironmentDoc->Manual
    3.LanguageChoose->DemandAnalysis->DesignReview->Coding->CodeComplete->Annotation->CodeConclusion->CodeReviewComment->CommentJudgement->CodeReviewModification->TestErrorSummary->TestModification->EnvironmentDoc->Manual
    4.DemandAnalysis -> LanguageChoose -> DesignReview -> Coding -> CodeReviewModification -> TestModification -> EnvironmentDoc
    5.DemandAnalysis -> LanguageChoose -> Coding -> CodeComplete -> Annotation
    6.LanguageChoose -> DemandAnalysis -> DesignReview -> Coding -> CodeComplete -> Annotation -> CodeConclusion -> CodeReviewComment -> CommentJudgement -> CodeReviewModification -> EnvironmentDoc
    7.LanguageChoose -> DemandAnalysis -> Coding -> Manual
    8.DemandAnalysis -> LanguageChoose -> DesignReview -> Coding -> CodeComplete -> Annotation -> CodeConclusion -> CodeReviewComment -> CommentJudgement -> CodeReviewModification -> EnvironmentDoc
    9.DemandAnalysis -> LanguageChoose -> DesignReview -> Coding -> CodeReviewModification -> TestModification -> EnvironmentDoc
    10.DemandAnalysis -> LanguageChoose -> DesignReview -> Coding -> CodeReviewComment -> TestErrorSummary -> Manual
    """

    example_prompt2 = """
    The following are several software development examples: """ + "\n\t".join(example_trace) + "\n"
    

    task_prompt = """
    As a software development manager, You can now randomly select the process nodes given above and form them into the corresponding development process:
    This trace should satisfy: 
    1.The output trace does not need to have all nodes. 
    2.The nodes must be selected from the existing fourteen nodes and cannot be created by yourself. 
    3.Use -> to connect between nodes. 
    4.The sorting order of nodes should be as diverse as possible to reflect your wisdom.
    5.Please do not generate trace that are the same as any of the above examples.
    Output trace: 
    """

    total_prompt = user_prompt + role_prompt + phaseExplainations_prompt + example_prompt + task_prompt
    
    return total_prompt
  

def extract_trace( response:str ):
    trace_nodes_list = []
    original_trace = response.split("->")
    
    for node in original_trace:
        node = node.split()[0]
        trace_nodes_list.append(node)
    
    return trace_nodes_list

def generate_new_chain(trace_nodes_list, chain):
    total_list = []
    composed_phases = {}

    # Step 1: Build total_list and composed_phases dictionary
    for item in chain:
        if item.get('phaseType') == 'SimplePhase':
            total_list.append(item)
        elif item.get('phaseType') == 'ComposedPhase':
            composed_phases[item['phase']] = item
            
    # Step 2: Retrieve information based on trace_nodes_list
    new_phase_list = []
    for phase_name in trace_nodes_list:
        phase_info = next((phase for phase in total_list if phase['phase'] == phase_name), None)

        if not phase_info:
            for composed_phase_name, composed_phase_info in composed_phases.items():
                sub_phases = composed_phase_info['Composition']
                sub_phase_info = next((sub_phase for sub_phase in sub_phases if sub_phase['phase'] == phase_name), None)
                
                if sub_phase_info:
                    phase_info = {
                        'phase': composed_phase_name,
                        'phaseType': composed_phase_info['phaseType'],
                        'cycleNum': composed_phase_info['cycleNum'],
                        'Composition': [sub_phase_info]
                    }
                    new_phase_list.append(phase_info)
                    break
        else:
            new_phase_list.append(phase_info)
        
    return new_phase_list


def init_temperature():
    temperature = random.uniform(0, 1.5)
    
    return temperature

def judge_extra_phase(process_trace:list):
    guide_line = ['DemandAnalysis', 'LanguageChoose', 'DesignReview', 'Coding', 'CodeComplete', 'Annotation', 'CodeConclusion', 'CodeReviewComment', 'CommentJudgement', 'CodeReviewModification', 'TestErrorSummary', 'TestModification','EnvironmentDoc','Manual']
    for phase in process_trace:
        if phase not in guide_line:
            return  False
    return True


def append_to_hyperparameters_json(name:str, temperature: float, user_task: str, total_prompt: str, response: str, flag: bool, filename: str = 'hyperparameters.txt'):
    information_dict = {
        "name": name,
        'temperature': temperature,
        'user_task': user_task,
        'total_prompt': total_prompt,
        'response': response,
        'hallucination_flag': flag
    }

    information_json = json.dumps(information_dict, indent=2)

    with open(filename, 'a') as file:
        file.write(information_json + ',' + '\n') 



"""
接下来我将对上述的流程节点进行简要解释:
1.DemandAnalysis: 根据用户提出的task进行需求分析,得出chatdev想要生成的产品形态, 产品形态可以是 xml ,pdf ,application 等."
2.LanguageChoose: 为了满足用户的需求并且使得生成的程序可运行, 进行程序具体编程语言的选择.
3.DesignReview: 根据用户的任务, 评估现有提出的产品形态和编程语言能否通过后续的代码编程完成用户任务,如果无法完成则重新从DemandAnalysis开始执行.
4.Coding: 为了完成用户的需求, 进行一个到多个文件的编写 .
5.CodeComplete: 为了满足开发的软件的完整功能, 实现文件中的所有方法, 然后遵循相应的格式输出所有的代码. 
6.Annotation: 对现在已生成的代码文件加入注释, 解释代码中类,函数的功能作用.
7.CodeConclusion: 阅读代码内容, 解释代码中包含的主要功能, 并且给出任何潜在的错误
8.CodeReviewComment: 检查代码中所有类是不是被引用, 没有潜在bug存在. 提出一个关于代码最高优先级的意见并且给出修复建议, 如果代码是完美的则返回 <INFO>Finished
9.CommentJudgement: 根据现有的规范和结论对提出的意见作出判断。判断结果将决定是否需要更改代码.
10.CodeReviewModification: 为了使得软件具有创造力, 可执行性和健壮性, 更具评论修改相应的代码, 然后输出完整的代码, 并根据注释修复所有的错误.
11.TestErrorSummary: 对现有的软件进行测试， 并且根据测试报告查找并且总结导致问题的错误. 
12.TestModification: 根据错误总结修改所有有问题的代码, 输出你根据测试报告和相应解释修复的代码.
13.EnvironmentDoc: 根据已提供的代码和文件格式, 编写requirements.txt文件, 以指定项目正常运行所需的依赖项或包 
14.Manual: 使用Markdown, 编写一个manual.md文件, 该文件是使用该软件的详细用户手册, 包括介绍该软件的主要功能、如何安装环境依赖项以及如何使用/播放. 

Please use your existing software engineering process and project management experience, according to the meaning of software development nodes introduced above, refer to the trace generation case provided above, and dynamically generate a trace composed of the above process node names.
The output format is:  Use '->' to connect nodes, and nodes are limited to the fourteen nodes mentioned above.
Next, I will briefly introduce the role of each node in the software development process.:
DemandAnalysis: Conduct demand analysis based on the tasks proposed by the user, and obtain the product form that chatdev wants to generate. The product form can be xml, pdf, application, etc.
LanguageChoose: In order to meet the needs of the user and make the generated program runnable, select the specific programming language of the program.
DesignReview: Based on the user's task, evaluate whether the currently proposed product form and programming language can complete the user's task through subsequent code programming. If it cannot be completed, execution will start again from DemandAnalysis.
Coding: In order to complete the user's needs, write one to multiple files.
CodeComplete: In order to meet the complete functions of the developed software, implement all methods in the file, and then output all codes according to the corresponding format.
Annotation: Add comments to the generated code file to explain the functions of the classes and functions in the code.
CodeConclusion: Read the code content, explain the main functions contained in the code, and give any potential errors.
CodeReviewComment: Check whether all classes in the code are referenced and whether there are no potential bugs. Provide a highest priority opinion on the code and give suggestions for repairs. If the code is perfect, return <INFO>Finished.
CommentJudgement: Make a judgment on the comments made based on the existing specifications and conclusions. The result of the judgment will determine whether the code needs to be changed.
CodeReviewModification: In order to make the software creative, executable and robust, modify the corresponding code with more comments, then output the complete code, and fix all errors according to the comments.
TestErrorSummary: Test existing software, and find and summarize the errors that cause problems based on the test report. 
TestModification: Modify all problematic code based on the error summary, and output the code you fixed based on the test report and corresponding explanation.
EnvironmentDoc: Based on the provided code and file format, write the requirements.txt file to specify the dependencies or packages required for the normal operation of the project.
Manual: Use Markdown to write a manual.md file, which is a detailed user manual for using the software, including introducing the main functions of the software, how to install environmental dependencies, and how to use/play.
"""
