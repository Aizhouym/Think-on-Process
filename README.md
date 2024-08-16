# Dynamic Process Generation for Collaborative Development of Multi-Agent System

## Quick Start with terminal 💻
To get started, follow these steps:

1. **Setup Python Environment** Ensure you have a version 3.9 or higher Python environment. You can create and
   activate this environment using the following commands, replacing `ToP_env` with your preferred environment
   name:

   ```
   conda create -n ToP_env python=3.9 -y
   conda activate ToP_env
   ```

2. **Install Dependencies:** Move into the `ChatDev` directory and install the necessary dependencies by running:
   ```
   cd ChatDev
   pip3 install -r requirements.txt
    ```
3. **Set OpenAI API Key:** Export your OpenAI API key as an environment variable. Replace `"your_OpenAI_API_key"` with
   your actual API key. Remember that this environment variable is session-specific, so you need to set it again if you
   open a new terminal session.（ Notice：OpenAI Baes Url is the same operation if is necessary)
   On Unix/Linux:
   ```
   export OPENAI_API_KEY="your_OpenAI_API_key" or export OPENAI_BASE_URL="your_OpenAI_Base_Url"
   ```

   On Windows:
   ```
   $env:OPENAI_API_KEY="your_OpenAI_API_key" or $env:OPENAI_BASE_URL="your_OpenAI_Base_Url"
   ```
  
4. **Build Your Software:** Use the following command to initiate the building of your software,
   replacing `[idea]` with your idea's description and `[name]` with your desired project
   name:
   On Unix/Linux:

   ```
   python3 run.py --task "[idea]" --name "[name]"
   ```
   On Windows:

   ```
   python run.py --task "[idea]" --name "[name]"
   ```
   
5. **Check instance and Run Your Software:** Once over generated, you can find your dynamic instance in `traces_data.txt` and parameters in 
   `traces_hyperparameters.txt`, and you can find your software in the `WareHouse` directory under a specific
   project folder, such as `name_DefaultOrganization_timestamp`. Run your software using the following command
   within that directory:
   On Unix/Linux:

   ```
   cd WareHouse/project_name_DefaultOrganization_timestamp
   python3 main.py
   ```

   On Windows:

   ```
   cd WareHouse/project_name_DefaultOrganization_timestamp
   python main.py
   ```
6. **NLDD** Different software development tasks are included in the dataset which contains 5 categories, You can choose any software development task in it.


## BPMN transfer to process textual description 📃 and LLM enhancement 💪
1.  Use the desired __SR__ to filter the instances in `traces_data.txt`.
2.  If you don't install pm4py, following the below instructions:
   ```
   pip install pm4py
   from pm4py.objects.conversion.log import converter as log_converter
   from pm4py.algo.discovery.alpha import algorithm as alpha_miner
   from pm4py.visualization.petri_net import visualizer as pn_visualizer
   from pm4py.objects.bpmn.exporter import exporter as bpmn_exporter
   ```
   ```
   dataframe = pd.read_csv('/content/traces_eventlog.csv')
   event_log = pm4py.convert_to_event_log(dataframe)
   process_model = pm4py.discover_bpmn_inductive(event_log)
   pm4py.view_bpmn(process_model)
   
   # save the bpmn model to pdf
   pm4py.save_vis_bpmn(process_model, "bpmn.pdf")
   ```

3. Use the ''' https://github.com/woped/P2T.git ''' to clone tool used for process description transfering.
4. Put process description as prompt to enchance the LLM.
5. Compare the __SR__ of the generated instances of the same task before and after LLM enhancement.
