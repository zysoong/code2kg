import networkx
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

import utils.oop_graph_query
from base.models import BaseGraphModel, BaseGraphNodeModel
from models.oop import OOPFunction, OOPClass

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


def get_prompt_template_for_summary(oop_graph: BaseGraphModel, oop_function: OOPFunction):
    summaries_of_relative_nodes: str = "Following functions are used: \n"

    rel_nodes: list[BaseGraphNodeModel] = utils.oop_graph_query.get_relative_nodes(oop_graph, oop_function)
    for rel_node in rel_nodes:
        if isinstance(rel_node, OOPFunction):
            summaries_of_relative_nodes += f'{rel_node.signature}: {rel_node.summary} \n'
        else:
            raise ValueError(f"Relative nodes of OOPFunction must be OOPFunction. Found {rel_node.__class__.__name__}")

    user_prompt: str = (f"Please generate summary of given function "
                        f"{oop_function.signature}: \n{oop_function.code}\n{summaries_of_relative_nodes}")

    return ChatPromptTemplate.from_messages([
        ("system", function_summary_system_prompt),
        ("user", user_prompt)
    ])
