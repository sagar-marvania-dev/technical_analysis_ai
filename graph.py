from langgraph.graph.state import StateGraph, START, END
from langgraph.prebuilt import tools_condition

from nodes import (data_loader, compute_indicators)
from state_models import ShastraState
from tools import custom_tool_node

# graph = StateGraph(ShastraState)

# graph.add_node("data_loader", data_loader)
# graph.add_node("tools", TOOL_NODE)

# graph.add_edge(START, "data_loader")

# graph.add_conditional_edges("data_loader", tools_condition)

# graph.add_edge("tools", "data_loader")

# workflow = graph.compile()



graph = StateGraph(ShastraState)

graph.add_node("data_loader", data_loader)
graph.add_node("indicators", compute_indicators)
graph.add_node("tools", custom_tool_node)

graph.add_edge(START, "data_loader")
graph.add_edge("data_loader", "indicators")

graph.add_conditional_edges("indicators", tools_condition)
graph.add_edge("tools", "indicators")

graph.add_edge("indicators", END)

workflow = graph.compile()











