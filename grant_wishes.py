from langchain_community.llms.llamacpp import LlamaCpp
from langchain.prompts import PromptTemplate, FewShotPromptTemplate
from langchain.chains.llm import LLMChain
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field

llm = LlamaCpp(model_path='../models/Phi-3-mini-4k-instruct-q4.gguf', verbose=False, temperature=0.7)

class Goal(BaseModel):
    goal: str = Field(description = "Answer for goal")
    
json_output_parser = JsonOutputParser(pydantic_object=Goal)

examples = [
    {
        "topic": "Generate a goal for topic fitness",
        "goal": "Do 30 mins cardio"
    },
    {
        "topic": "Generate a goal for eating habit",
        "goal": "Take one serving only"
    },
]
example_prompt = PromptTemplate(
    template = "topic: {topic}\n goal: {goal}",
    input_variables=["topic","goal"]
)
wish_template = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    suffix = "Generate a single-line goal for {topic} in strict JSON format. \n{format_instructions}",
    input_variables=["topic"],
    partial_variables={"format_instructions": json_output_parser.get_format_instructions()}
)

llmChain = wish_template | llm | json_output_parser

def getwish(wish):
    try:
        ans = llmChain.invoke({"topic": wish})
        return ans
    except err:
        raise err
        
        
if __name__ == "__main__":
    print(getwish("Get rich"))