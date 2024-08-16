import random
import math

class TraceContainer:
    def __init__(self, traces):
        self.traces = traces

    def select_action(self):
        best_action = None
        best_value = float('-inf')
        total_visits = sum([info['visits'] for info in self.traces.values()])

        selection_list = []
        
        for trace, info in self.traces.items():
            failure_rate = info['failures'] / info['visits']
            
            # C = 0
            # uct_value = failure_rate 
            
            # C = 1
            uct_value = failure_rate + math.sqrt(math.log(total_visits) / info['visits'])
            
            # C = 2
            # uct_value = failure_rate + 2*( math.sqrt(math.log(total_visits) / info['visits']))
            
            # C = 3 
            # uct_value = failure_rate + 3*( math.sqrt(math.log(total_visits) / info['visits']))
            
            # C = 4
            # uct_value = failure_rate + 4*( math.sqrt(math.log(total_visits) / info['visits']))
            
            if uct_value > best_value:
                best_value = uct_value

        
        #  在UCT值相同的trace中随机抽取一条作为执行trace
        for trace, info in self.traces.items():
            failure_rate = info['failures'] / info['visits']
            # C = 0
            # uct_value = failure_rate 
            
            # C = 1
            # uct_value = failure_rate + math.sqrt(math.log(total_visits) / info['visits'])
            
            # C = 2
            # uct_value = failure_rate + 2*( math.sqrt(math.log(total_visits) / info['visits']))
            
            # C = 3
            # uct_value = failure_rate + 3*( math.sqrt(math.log(total_visits) / info['visits']))
            
            # C = 4
            # uct_value = failure_rate + 4*( math.sqrt(math.log(total_visits) / info['visits']))
            
            
            if uct_value == best_value:
                selection_list.append(trace)
            
        
        best_action = selection_list[random.randint(0,len(selection_list) - 1)]    
        return best_action


    def update(self, trace, failure):
        if trace not in self.traces:
            self.traces[trace] = {'visits': 0, 'failures': 0}

        self.traces[trace]['visits'] += 1
        
        if failure:
            self.traces[trace]['failures'] += 1
            
    
    def select_action_distribution(self):
        
        total_visits = sum([info['visits'] for info in self.traces.values()])

        uct_values = []
        for trace, info in self.traces.items():
            failure_rate = info['failures'] / info['visits']
            
            # C = 0 
            # uct_value = failure_rate 
            
            # C = 1
            # uct_value = failure_rate + math.sqrt(math.log(total_visits) / info['visits'])

            # C = 2
            # uct_value = failure_rate + 2*math.sqrt(math.log(total_visits) / info['visits'])
            
            # C = 3
            uct_value = failure_rate + 3*math.sqrt(math.log(total_visits) / info['visits'])
            
            # C = 4
            # uct_value = failure_rate + 4*math.sqrt(math.log(total_visits) / info['visits']) 
            
         
            
            uct_values.append(uct_value)  # 应用ReLU函数

        # 将UCT值转换为概率分布
        total_uct = sum(uct_values)    
        probabilities = [uct / total_uct for uct in uct_values]

        # print(probabilities)
        
        # 根据概率选择动作
        chosen_index = random.choices(range(len(self.traces)), weights=probabilities, k=1)[0]
        return list(self.traces.keys())[chosen_index]

