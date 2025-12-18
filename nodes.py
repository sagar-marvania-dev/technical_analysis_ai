from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

from tools import custom_tool_node, tool_kit
from state_models import ShastraState
from utils.utilities import read_price_data

import json

# Bind tools
llm_with_tools = ChatOpenAI(model="gpt-4o-mini").bind_tools(tool_kit)


def data_loader(state: ShastraState):

    symbol = state["symbol"]
    timeframe = state["timeframe"]

    price_data = read_price_data(symbol, timeframe)

    if "ohlcv_data" in price_data:
        state["ohlcv_data"] = price_data["ohlcv_data"]
    else:
        raise ValueError(f"There was some error while fetchig the price data for {symbol}.Kindly check the data source availability of the data for the provided symbol.")

    print("\n=== Data has Been loaded and updated ===")
    
    # MUST return tool_call so LangGraph executes it
    return state


def compute_indicators(state: ShastraState):

    timeframe = state["timeframe"]

    # --- System prompt for LLM ---
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a high-frequency trading (HFT) analyst assistant operating under time-sensitive conditions. "
                "You must analyze technical indicators to support fast-paced trading execution.\n\n"
                "You have access to tools: ma_crossover, price_crossover. "
                "Use them by providing appropriate arguments like `ohlcv_data` and the respective periods.\n\n"
                f"⚠️ The OHLC data provided is from a {timeframe} intervals, reflecting recent market behavior. "
                "You must interpret this data quickly and accurately.\n\n"
                "Here is the OHLC data:\n{ohlcv_data}.\n\n"
                "Call necessary tools strictly only once and not more than that, and analyze the results. While tool calling make sure your lookback window are appropriate compared to amound to ohlcv_data that is provided.\n"

            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    ).partial(ohlcv_data=json.dumps(state["ohlcv_data"], indent=2, default = str))

    chain = prompt | llm_with_tools

    messages = state.get("messages", [])
    if not messages:
        messages = [HumanMessage(content="Begin indicator analysis.")]

    # --- Step 1: Ask for tool calls ---
    print(messages[-1])
    print("#"*10)
    ai_response = chain.invoke(messages)
    messages.append(ai_response)
    
    state["messages"] = messages

    return state