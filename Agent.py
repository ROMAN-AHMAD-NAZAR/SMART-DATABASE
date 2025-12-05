# [UPDATED] - I have added comments to explain the changes.
# This updated script connects to an EXTERNAL database file instead of creating its own.

import sqlite3
import os
from typing import Annotated, Any

from langchain_community.utilities import SQLDatabase
from langchain_groq import ChatGroq
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_core.tools import tool
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from pydantic import BaseModel, Field
from typing_extensions import TypedDict
from langgraph.graph import END, StateGraph, START
from langgraph.graph.message import AnyMessage, add_messages
from langgraph.prebuilt.tool_node import ToolNode
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnableWithFallbacks

# --- [UPDATED] CONFIGURATION SECTION ---
# <<< CHANGE THIS TO YOUR DATABASE FILE >>>
DATABASE_FILE = "cars.db"  # Or "olist.db", or any other .db file

# --- SECURE API KEY SETUP ---
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✓ Loaded environment variables from .env file")
except ImportError:
    print("⚠ python-dotenv not installed. Using system environment variables.")

# --- [REMOVED] Database Creation Section ---
# The entire section with CREATE TABLE statements, sample data, and the
# setup_database() function has been removed. We will now connect
# to the external database file specified above.

# --- [REMOVED] get_database_info() function ---
# This function was hard-coded with the old schema and is no longer needed.
# The agent will now discover the schema dynamically using its tools.

# --- 1. Initialize LLM and Database Connection ---
groq_api_key = os.environ.get("GROQ_API_KEY")
openai_api_key = os.environ.get("OPENAI_API_KEY")

if groq_api_key:
    print(f"✓ Using Groq LLM...")
    llm = ChatGroq(model="llama3-70b-8192", api_key=groq_api_key)
elif openai_api_key:
    print(f"✓ Using OpenAI LLM...")
    from langchain_openai import ChatOpenAI
    llm = ChatOpenAI(model="gpt-4-turbo", temperature=0, api_key=openai_api_key)
else:
    print("❌ ERROR: No API key found! Please set GROQ_API_KEY or OPENAI_API_KEY in your .env file.")
    exit(1)

# --- [UPDATED] Connect to the external database ---
db_uri = f"sqlite:///{DATABASE_FILE}"
if not os.path.exists(DATABASE_FILE):
    print(f"❌ ERROR: Database file not found at '{DATABASE_FILE}'")
    print("Please make sure the database file is in the same directory as this script.")
    exit(1)

try:
    db = SQLDatabase.from_uri(db_uri)
    print(f"✓ Successfully connected to database: {DATABASE_FILE}")
except Exception as e:
    print(f"❌ Error connecting to database: {e}")
    exit(1)


# --- 2. Setup Tools ---
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
tools = toolkit.get_tools()

list_table_tool = next((tool for tool in tools if tool.name == "sql_db_list_tables"), None)
get_schema_tool = next((tool for tool in tools if tool.name == "sql_db_schema"), None)

@tool
def db_query_tool(query: str) -> str:
    """Execute a SQL query against the database and return the result."""
    try:
        result = db.run_no_throw(query)
        if not result or result.strip() == "":
            return "Query returned no results."
        return result
    except Exception as e:
        return f"Query error: {str(e)}"

# --- 3. Define State and Models ---
# This section remains the same.
class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

class SubmitFinalAnswer(BaseModel):
    """Submit the final answer to the user based on the query results."""
    final_answer: str = Field(..., description="The final answer to the user")

# --- 4. Create Prompts [UPDATED] ---
# The prompts are now more general and instruct the agent to use its tools
# to discover the schema, rather than having it hard-coded.

# In section: --- 4. Create Prompts [UPDATED] ---

# In section: --- 4. Create Prompts [UPDATED] ---

query_gen_system = """You are a world-class SQL writer and a thoughtful data analyst. Your goal is to help a user explore a database of used cars by writing the perfect SQL query.

**Your Thinking Process:**
1.  **Analyze the User's Goal:** What is the user *really* trying to find out?
2.  **Scan the History:** Review the conversation history. Is this a follow-up question? Are they asking about a specific detail (like an average MPG) that you mentioned?
3.  **Critical Reasoning:**
    *   **NEVER query for an exact match on an aggregate value (like AVG, COUNT, SUM) that you mentioned in a previous turn.** If the user asks about an average value, they are likely asking for the items that contributed to that average. For example, if you said "the average MPG for Toyota is 63.04" and the user asks "which car has that MPG?", they want to see high-MPG Toyotas, not a car with an MPG of *exactly* 63.04.
    *   If the user's request seems to have no results (e.g., asking for a very specific model and year), consider if a slightly broader query would be more helpful. However, prefer to be precise first.
4.  **Construct the Query:** Based on your reasoning, write a syntactically correct SQLite query.

**DATABASE SCHEMA CONTEXT:**
- The main table is `cars`.
- `mpg` stands for 'Miles Per Gallon'.
- `brand` is the car manufacturer.
- `year` is the model year of the car.
- `price` is in British Pounds (£).

**CRITICAL RULES:**
1.  You MUST use the tools to get the schema if you don't know it.
2.  Generate ONLY the SQL query text. Do not add any other text or explanations.
"""

query_gen_prompt = ChatPromptTemplate.from_messages([
    ("system", query_gen_system),
    ("placeholder", "{messages}")
])

query_check_system = """You are a SQL expert. A less-capable AI has generated the following SQL query.
Your task is to:
1. Check the query for any syntax errors or logical flaws.
2. Correct the query if necessary.
3. **Execute the final, correct query** using the `db_query_tool`.
"""

query_check_prompt = ChatPromptTemplate.from_messages([
    ("system", query_check_system),
    ("placeholder", "{messages}")
])

schema_system = """Your task is to get the schema for the tables relevant to the user's question.
Use the `sql_db_schema` tool to do this. Provide the table names as a comma-separated list.
"""

schema_prompt = ChatPromptTemplate.from_messages([
    ("system", schema_system),
    ("placeholder", "{messages}")
])


# Create model chains
query_generator = query_gen_prompt | llm # <-- CORRECTED LINE
query_checker = query_check_prompt | llm.bind_tools([db_query_tool])
schema_getter = schema_prompt | llm.bind_tools([get_schema_tool])
# --- 5. Define Node Functions ---
# This entire section of LangGraph nodes can remain the same. The logic is robust
# and will work with the updated prompts and tools.
def first_tool_call(state: State):
    return {"messages": [AIMessage(content="", tool_calls=[{"name": "sql_db_list_tables", "args": {}, "id": "tool_list_tables"}])]}

def handle_tool_error(state: State):
    error = state.get("error")
    tool_calls = state["messages"][-1].tool_calls
    return {"messages": [ToolMessage(content=f"Error: {repr(error)}", tool_call_id=tc["id"]) for tc in tool_calls]}

def create_tool_node_with_fallback(tools: list) -> RunnableWithFallbacks[Any, dict]:
    return ToolNode(tools).with_fallbacks([RunnableLambda(handle_tool_error)], exception_key="error")

def get_schema_node(state: State):
    response = schema_getter.invoke({"messages": state["messages"]})
    return {"messages": [response]}

# sql_agent.py

# ... (other code in your file) ...

def query_gen_node(state: State):
    """
    Generates the SQL query. Includes safety checks and debugging prints.
    """
    print("\n--- 🧠 Step: Generating SQL Query ---")
    
    # 1. Invoke the LLM to get a response
    response = query_generator.invoke({"messages": state["messages"]})
    
    # 2. Print the raw response from the LLM for debugging
    # The .content attribute holds the plain text (which should be our SQL query)
    print(f"LLM generated SQL: {response.content}")
    
    # 3. This is the safety check logic for tool_messages
    # We start with an empty list. This guarantees the variable always exists.
    tool_messages = [] 
    
    # Check if the LLM incorrectly tried to call a tool
    if response.tool_calls:
        # Loop through any incorrect tool calls
        for tc in response.tool_calls:
            # We only allow the "SubmitFinalAnswer" tool. Any other tool call at this stage is an error.
            if tc["name"] != "SubmitFinalAnswer":
                print(f"  -> WARNING: LLM incorrectly tried to call tool '{tc['name']}' instead of writing SQL.")
                # Add an error message to send back into the graph
                tool_messages.append(
                    ToolMessage(
                        content=f"Error: You are supposed to generate a SQL query as plain text, not call the '{tc['name']}' tool.",
                        tool_call_id=tc["id"]
                    )
                )
    
    # 4. Return the original response PLUS any error messages we generated.
    # This line now works because `tool_messages` is always a list (even if it's empty).
    return {"messages": [response] + tool_messages}

# ... (the rest of your sql_agent.py file) ...

def check_query_node(state: State):
    last_message = state["messages"][-1]
    query_message = HumanMessage(content=f"Check and execute this SQL query: {last_message.content}")
    response = query_checker.invoke({"messages": [query_message]})
    return {"messages": [response]}

def should_continue(state: State):
    messages = state["messages"]
    last_message = messages[-1]
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        if any(tc["name"] == "SubmitFinalAnswer" for tc in last_message.tool_calls):
            return END
    if last_message.content.startswith("Error:"):
        return "query_gen"
    if not hasattr(last_message, 'tool_calls') or not last_message.tool_calls:
        if any(keyword in last_message.content.upper() for keyword in ["SELECT", "INSERT", "UPDATE", "DELETE"]):
            return "check_query"
    return "query_gen"

# sql_agent.py

# ... (the rest of your file) ...

# In section: --- 5. Define Node Functions ---

def final_answer_node(state: State):
    """
    Formats the final query result into a human-readable response.
    Handles empty results gracefully.
    """
    messages = state["messages"]
    # Get the original user question
    original_question = ""
    for msg in messages:
        if isinstance(msg, HumanMessage):
            original_question = msg.content
            break

    # Get the last tool result
    query_result = ""
    for msg in reversed(messages):
        if isinstance(msg, ToolMessage) and msg.name == "db_query_tool":
            query_result = msg.content
            break

    # If the query returned no results, formulate a helpful message
    if "Query returned no results" in query_result:
        no_results_prompt = f"""The user asked the following question: "{original_question}".
        A SQL query was run to answer this question, but it returned no results.
        Please formulate a friendly, helpful response to the user explaining that you couldn't find any data matching their specific request.
        For example, if they asked for 'Toyota models from 2020', a good response would be: 'I couldn't find any Toyota models from the year 2020 in the database.'
        Keep the response concise and directly address the user's original question.
        """
        response = llm.invoke([HumanMessage(content=no_results_prompt)])
        final_answer = response.content
    # If the query produced a valid result, format it
    elif query_result and not query_result.startswith("Error:"):
        final_prompt_template = """You are a data presentation assistant. Your sole purpose is to convert raw SQL query results into a beautiful, human-readable format.

        **CRITICAL RULES:**
        1.  If the query result contains multiple rows or a list of items, YOU MUST format it as an HTML table (`<table>`).
        2.  The table MUST have appropriate headers (`<th>`) for each column.
        3.  If the query result is just a single value (like a count, an average, or a single name), present it in a clear, concise sentence.
        4.  Do NOT include the original SQL query. Just provide the final, formatted answer.
        5.  Add formatting to make numbers more readable (e.g., use commas for thousands, add currency symbols like '£').

        Here is the original user question for context:
        "{original_question}"

        Here is the raw query result:
        "{query_result}"

        Now, generate the final, formatted answer based on these rules.
        """
        final_prompt = final_prompt_template.format(
            original_question=original_question,
            query_result=query_result
        )
        response = llm.invoke([HumanMessage(content=final_prompt)])
        final_answer = response.content
    # Handle query errors or other issues
    else:
        final_answer = "Sorry, I encountered a problem processing your request. Please try rephrasing your question."

    # Package the final answer for the graph to end
    return {"messages": [
        AIMessage(
            content="",
            tool_calls=[{
                "name": "SubmitFinalAnswer",
                "args": {"final_answer": final_answer},
                "id": "final_answer_call"
            }]
        )
    ]}

# --- 6. Build the Workflow ---
# This section remains the same.
workflow = StateGraph(State)
workflow.add_node("first_tool_call", first_tool_call)
workflow.add_node("list_tables", create_tool_node_with_fallback([list_table_tool]))
workflow.add_node("get_schema", get_schema_node)
workflow.add_node("schema_tool", create_tool_node_with_fallback([get_schema_tool]))
workflow.add_node("query_gen", query_gen_node)
workflow.add_node("check_query", check_query_node)
workflow.add_node("execute_query", create_tool_node_with_fallback([db_query_tool]))
workflow.add_node("final_answer", final_answer_node)

workflow.add_edge(START, "first_tool_call")
workflow.add_edge("first_tool_call", "list_tables")
workflow.add_edge("list_tables", "get_schema")
workflow.add_edge("get_schema", "schema_tool")
workflow.add_edge("schema_tool", "query_gen")
workflow.add_conditional_edges("query_gen", should_continue, {END: END, "check_query": "check_query", "query_gen": "query_gen"})
workflow.add_edge("check_query", "execute_query")
workflow.add_edge("execute_query", "final_answer")
workflow.add_edge("final_answer", END)
app = workflow.compile()

# --- 7. Interactive Chat Interface ---
# The SQLChatBot class is a wrapper around the LangGraph app.
# It can remain the same.
# --- 7. Interactive Chat Interface [UPDATED WITH MEMORY] ---
# The SQLChatBot class is a wrapper around the LangGraph app.
# It has been updated to maintain and pass the conversation history.

class SQLChatBot:
    def __init__(self):
        # CHANGED: We now store the LangChain message objects directly, not just text tuples.
        # This allows us to feed the history back into the graph.
        self.message_history = []

    def ask_question(self, question: str):
        try:
            print(f"\n🤔 Processing: {question}")

            # 1. Create the new human message
            new_human_message = HumanMessage(content=question)

            # 2. Construct the full message list to send to the graph
            # This now includes all previous messages plus the new one.
            messages_to_send = self.message_history + [new_human_message]

            # 3. Invoke the graph with the complete history
            result = app.invoke({"messages": messages_to_send})

            # 4. Find the final answer from the result
            final_answer = "I couldn't find a direct answer. Please try rephrasing."
            final_ai_message = None

            for msg in reversed(result["messages"]):
                if hasattr(msg, 'tool_calls') and msg.tool_calls:
                    for tc in msg.tool_calls:
                        if tc["name"] == "SubmitFinalAnswer":
                            final_answer = tc['args']['final_answer']
                            # Create a clean AI message for history
                            final_ai_message = AIMessage(content=final_answer)
                            break
                if final_ai_message:
                    break

            # 5. Update our history with the latest exchange
            self.message_history.append(new_human_message)
            if final_ai_message:
                self.message_history.append(final_ai_message)

            return final_answer

        except Exception as e:
            return f"Sorry, I encountered an error: {str(e)}"

    def show_history(self):
        if not self.message_history:
            print("No conversation history yet.")
            return

        print("\n📜 CONVERSATION HISTORY:")
        for i, msg in enumerate(self.message_history):
            if isinstance(msg, HumanMessage):
                print(f"  You: {msg.content}")
            elif isinstance(msg, AIMessage):
                print(f"  Bot: {msg.content}")
        print("-" * 20)

# --- [UPDATED] main() function for running the bot ---
def main():
    chatbot = SQLChatBot()
    print("🤖 SQL Database Assistant")
    print("=" * 50)
    print(f"Connected to '{DATABASE_FILE}'. I'm ready to answer your questions!")
    print("\n💬 Commands:")
    print("  • Type 'history' to see past questions")
    print("  • Type 'quit' or 'exit' to end")
    print("=" * 50)
    
    while True:
        try:
            user_input = input("\n❓ Your question: ").strip()
            if not user_input: continue
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("👋 Goodbye!")
                break
            if user_input.lower() == 'history':
                chatbot.show_history()
                continue
            answer = chatbot.ask_question(user_input)
            print(f"\n✅ Answer: {answer}")
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ An unexpected error occurred: {e}")

# This is the function your app.py will import and use
def get_answer_from_database(user_query: str) -> str:
    """
    Main entry point for the Flask app to call the chatbot.
    Initializes a new chatbot instance for each query to keep conversations separate.
    """
    chatbot = SQLChatBot()
    return chatbot.ask_question(user_query)


# This allows you to run the script directly from the command line for testing
if __name__ == "__main__":
    main()