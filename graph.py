from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage
from model import my_model
from mcp.server.fastmcp import FastMCP
from mcp_return import main
from model import my_model
import asyncio
from langgraph.graph import StateGraph,START,END
from langgraph.checkpoint.memory import MemorySaver

class research(TypedDict):
    topic: str
    search_data: str
    tavily_data : str
    combine_data : str
    score : int
    final_report : str

llm = my_model()
tools2 = asyncio.run(main())
binded_model = llm.bind_tools(tools2)

def llm_write(state):
    res = binded_model.invoke(state["topic"])
    return {"search_data" : res.content}

async def tavily_data(state):
    res1 = await tools2[0].ainvoke({"query" : state["topic"]})
    return {"tavily_data": str(res1)}


def compare(state):
    res3 = binded_model.invoke(
        f"""compare the both the data of the llm result and the tavily result and give which result is best.
        The llm information is {state["search_data"]}.
        The tavily information is {state["tavily_data"]}.
        If the both the results are correct for this {state["topic"]} then merge it based on information
        """)
    return {"combine_data" : res3.content}

def score(state):
    res4 = binded_model.invoke(
        f"""
        for this topic {state["topic"]} the results are {state["combine_data"]}.
        Give the score for the information upto 10 and the output contain only single number nothing else.
        ex: 2,3,4,5
        """
    )
    return {"score" : float(res4.content.strip())}


def score_based(state):
    if(state["score"] < 5):
        return "rewrite"
    return "final_report"

def rewrite(state):
    """
    refine the information
    """
    res5 = binded_model.invoke(state["combine_data"])
    return {"combine_data" : res5.content}


def final_report(state):
    "make a good summarization on the data"
    res6 = binded_model.invoke(state["combine_data"])
    return {"final_report" : res6.content}



graph = StateGraph(research)

graph.add_node("llm_write",llm_write)
graph.add_node("tavily_data",tavily_data)
graph.add_node("compare",compare)
graph.add_node("score",score)
graph.add_node("rewrite",rewrite)
graph.add_node("score_based",score_based)
graph.add_node("final_report",final_report)

graph.add_edge(START,"llm_write")
graph.add_edge("llm_write","tavily_data")
graph.add_edge("tavily_data","compare")
graph.add_edge("compare","score")
graph.add_conditional_edges(
    "score",
    score_based,
    {"rewrite" : "rewrite","final_report" : "final_report"}
)
graph.add_edge("rewrite","score")
graph.add_edge("final_report",END)

memory = MemorySaver()

graph_build = graph.compile(checkpointer = memory)
config = {"configurable" : {"thread_id" : "user1"}}












    
