from langchain_core.prompts import ChatPromptTemplate

import prompts.summary_templates
import utils.graph_query
from models.oop.oop_graph import OOPGraph


def summary_workflow(oop_graph: OOPGraph):
    pass


def query_summary(oop_graph: OOPGraph, nx_node):
    has_summary_for_each_rel_node: bool = True
    for rel_node in utils.graph_query.get_relative_nodes(oop_graph.graph, nx_node):
        if "summary" in rel_node:
            has_summary_for_each_rel_node = has_summary_for_each_rel_node and True
        else:
            has_summary_for_each_rel_node = has_summary_for_each_rel_node and False
    if has_summary_for_each_rel_node:
        summary_prompt_template = (
            prompts.summary_templates.get_prompt_template_for_function_extraction(oop_graph.graph, nx_node)
        )








#def query_summaries_for_oop_graph(oop_graph: OOPGraph):
#    for node in oop_graph.graph.nodes:
#        if oop_graph.graph.nodes[node].get("type") == "oop_function":
