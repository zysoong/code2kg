import networkx
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

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

    incoming_within_edges = [(u, v) for u, v, data
                             in graph.in_edges(nx_func_node, data=True) if data.get('edge_type') == 'within']
    outgoing_call_edges = [(u, v) for u, v, data
                           in graph.out_edges(nx_func_node, data=True) if data.get('edge_type') == 'calls']

    for u, _ in incoming_within_edges:
        if graph.nodes[u].get("node_type") == "oop_function":
            func_signature: str = graph.nodes[u]["signature"]
            func_summary: str = graph.nodes[u]["summary"]
            summaries_of_calls += f"{func_signature}: {func_summary} \n"
    for _, v in outgoing_call_edges:
        if graph.nodes[v].get("node_type") == "oop_function":
            func_signature: str = graph.nodes[v]["signature"]
            func_summary: str = graph.nodes[v]["summary"]
            summaries_of_calls += f"{func_signature}: {func_summary} \n"

    user_prompt: str = f"Please generate summary of given function {signature}: \n{code}\n{summaries_of_calls}"

    return ChatPromptTemplate.from_messages([
        ("system", function_summary_system_prompt),
        ("user", user_prompt)
    ])
