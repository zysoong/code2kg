import networkx
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

import utils.graph_query
from models.oop import OOPFunction

function_summary_system_prompt: str = """
-Target activity-
You are an intelligent assistant that helps a software developer to understand 
and write summary for {language} functions. 

-Goal-
Given source codes of a {language} function. If the function calls other dependant functions, 
the summaries of the dependant functions will also be given.
Consider the functionalities of other dependant functions, 
and extract the summary of the function with given source codes.
"""


def get_prompt_template_for_function_extraction(graph: networkx.DiGraph, nx_func_node):
    signature: str = nx_func_node["signature"]
    code: str = nx_func_node["code"]
    summaries_of_calls: str = "Following functions are used: \n"

    rel_nodes: list = utils.graph_query.get_relative_nodes(graph, nx_func_node)
    for rel_node in rel_nodes:
        summaries_of_calls += f'{rel_node["signature"]}: {rel_node["summary"]} \n'

    user_prompt: str = f"Please generate summary of given function {signature}: \n{code}\n{summaries_of_calls}"

    return ChatPromptTemplate.from_messages([
        ("system", function_summary_system_prompt),
        ("user", user_prompt)
    ])
