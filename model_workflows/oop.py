from langchain_core.prompts import ChatPromptTemplate

import prompts.summary_templates
import utils.oop_graph_query
from base.models import BaseGraphModel
from models.oop import OOPClass, OOPFunction


def summary_workflow(oop_graph: BaseGraphModel):
    pass


def query_summary(oop_graph: BaseGraphModel, node: OOPFunction | OOPClass):
    has_summary_for_each_rel_node: bool = True

    for rel_node in utils.oop_graph_query.get_relative_nodes(oop_graph, node):
        if "summary" in rel_node:
            has_summary_for_each_rel_node = has_summary_for_each_rel_node and True
        else:
            has_summary_for_each_rel_node = has_summary_for_each_rel_node and False

    if has_summary_for_each_rel_node:
        summary_prompt_template = (
            prompts.summary_templates.get_prompt_template_for_summary(oop_graph, node)
        )

#def query_summaries_for_oop_graph(oop_graph: OOPGraph):
#    for node in oop_graph.graph.nodes:
#        if oop_graph.graph.nodes[node].get("type") == "oop_function":
