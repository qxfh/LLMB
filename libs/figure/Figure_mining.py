import os
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

#load openai key 
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

VALID = '''
From now on, you are expert of battery.
You are looking to determine the number of valid data lines from the list of text extracted from a legend of cycling performance graph. 
You must follow thoes rules:
- Treat discharge and charge for the same material as one data line.
- Account for the possibility of typos in the extracted text(e.g. Charge -> Charee , Coulomb -> Ooulomb)
- Exclude "Coulomb efficiency" as it is not considered valid data.
- There is the case that only contain information like the material name and composition without any details related to charge or capacity. (e.g. 15% electrolyte, material A, ...) )

Begin!
list of text : ["Discharge capacity of A", "charge capacity of A", "Coulomb efficiency"]
Json : 1

list of text : ["10% Li", "20% Li", "30% Li"]
Json : 3

list of text : ["Li-A", "Li-B", "Li-C"]
Json : 3

list of text : {list_of_text}
Json : 
'''

def test(text_list):
    llm = ChatOpenAI(temperature=0.0, model_name='gpt-4')
    prompt = PromptTemplate.from_template(VALID)
    print(prompt)
    output = llm.predict(prompt.format(list_of_text = text_list))
    print(output)