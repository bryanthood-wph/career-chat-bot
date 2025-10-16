# Career Chat Bot - AI Assistant for Professional Representation

from dotenv import load_dotenv
from openai import OpenAI
import json
import os
import requests
import gradio as gr

# Initialize environment and OpenAI client

# The usual start

load_dotenv(override=True)
openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# NOTE: This cell sets up Pushover configuration and validates credentials:
# - Retrieves Pushover user ID and token from environment variables
# - Sets the Pushover API endpoint URL
# - Validates that both credentials are present by checking if they exist
# - Prints confirmation messages showing the first character of each credential

# For pushover

pushover_user = os.getenv("PUSHOVER_USER")
pushover_token = os.getenv("PUSHOVER_TOKEN")
pushover_url = "https://api.pushover.net/1/messages.json"

if pushover_user:
    print(f"Pushover user found and starts with {pushover_user[0]}")
else:
    print("Pushover user not found")

if pushover_token:
    print(f"Pushover token found and starts with {pushover_token[0]}")
else:
    print("Pushover token not found")

# Push notification function
# - Takes a message string as input
# - Prints the message locally for debugging
# - Creates a payload with user credentials and message
# - Sends HTTP POST request to Pushover API to deliver push notification to phone

def push(message):
    print(f"Push: {message}")
    payload = {"user": pushover_user, "token": pushover_token, "message": message}
    requests.post(pushover_url, data=payload)

# NOTE: This cell defines the record_user_details function:
# - Records when a user provides contact information (email, name, notes)
# - Sends a push notification with the user's details for real-time alerts
# - Returns a confirmation object that can be used by the AI system
# - This function will be called as a tool by the AI when users share contact info

def record_user_details(email, name="Name not provided", notes="not provided"):
    push(f"Recording interest from {name} with email {email} and notes {notes}")
    return {"recorded": "ok"}


    # NOTE: This cell defines the record_unknown_question function:
# - Records questions that the AI couldn't answer (knowledge gaps)
# - Sends push notification with the unanswered question for learning opportunities
# - Returns confirmation for the AI system
# - This helps identify areas where the AI needs more information or training

def record_unknown_question(question):
    push(f"Recording {question} asked that I couldn't answer")
    return {"recorded": "ok"}

# NOTE: This cell defines the tool schema for record_user_details:
# - Creates a JSON schema that tells the AI how to call the record_user_details function
# - Specifies the function name, description, and parameter requirements
# - Defines email as required, name and notes as optional parameters
# - This schema enables the AI to automatically call the function when appropriate

record_user_details_json = {
    "name": "record_user_details",
    "description": "Use ONLY after the user explicitly volunteers their email or requests follow-up contact. Collects only volunteered information for follow-up purposes with user consent.",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {
                "type": "string",
                "description": "The email address the user explicitly provided"
            },
            "name": {
                "type": "string",
                "description": "The user's name, if they provided it"
            },
            "notes": {
                "type": "string",
                "description": "Any additional information about the conversation that's worth recording to give context"
            }
        },
        "required": ["email"],
        "additionalProperties": False
    }
}

# NOTE: This cell defines the tool schema for record_unknown_question:
# - Creates a JSON schema for the record_unknown_question function
# - Instructs the AI to use this tool whenever it cannot answer a question
# - Requires a question parameter to record what couldn't be answered
# - This enables continuous learning by identifying knowledge gaps

record_unknown_question_json = {
    "name": "record_unknown_question",
    "description": "Use ONLY for career-relevant questions that cannot be answered from the provided background information. Do not log trivial, off-topic, or non-career questions.",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "The career-relevant question that couldn't be answered from the background information"
            },
        },
        "required": ["question"],
        "additionalProperties": False
    }
}

# NOTE: This cell creates the tools list for the AI:
# - Combines both tool schemas into a list that can be passed to OpenAI
# - Each tool is wrapped in the "function" type format required by OpenAI API
# - This list will be passed to the AI model to enable tool calling capabilities

tools = [{"type": "function", "function": record_user_details_json},
        {"type": "function", "function": record_unknown_question_json}]

tools

# NOTE: This cell defines the tool call handler using explicit if statements:
# - Takes a list of tool calls from the AI and executes each one
# - Parses the tool name and arguments from each tool call
# - Uses if/elif statements to map tool names to their corresponding functions
# - Returns results in the format expected by the AI (tool role messages)
# - This is the "traditional" way to handle tool calls with explicit routing

# This function can take a list of tool calls, and run them. This is the IF statement!!

def handle_tool_calls(tool_calls):
    results = []
    for tool_call in tool_calls:
        tool_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        print(f"Tool called: {tool_name}", flush=True)

        # THE BIG IF STATEMENT!!!

        if tool_name == "record_user_details":
            result = record_user_details(**arguments)
        elif tool_name == "record_unknown_question":
            result = record_unknown_question(**arguments)

        results.append({"role": "tool","content": json.dumps(result),"tool_call_id": tool_call.id})
    return results

# NOTE: This cell demonstrates using globals() to call functions dynamically:
# - Uses globals() dictionary to access functions by name as strings
# - Shows how to call a function without knowing its name at compile time
# - This approach eliminates the need for explicit if/elif statements
# - Tests the record_unknown_question function with a sample question

globals()["record_unknown_question"]("this is a really hard question")

# NOTE: This cell defines an elegant tool call handler using globals():
# - Uses globals().get() to dynamically find functions by name
# - Eliminates the need for explicit if/elif statements
# - Automatically calls the correct function if it exists in the global namespace
# - Returns empty dict if function doesn't exist (graceful error handling)
# - This is a more scalable approach for handling many tools

# This is a more elegant way that avoids the IF statement.

def handle_tool_calls(tool_calls):
    results = []
    for tool_call in tool_calls:
        tool_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        print(f"Tool called: {tool_name}", flush=True)
        tool = globals().get(tool_name)
        result = tool(**arguments) if tool else {}
        results.append({"role": "tool","content": json.dumps(result),"tool_call_id": tool_call.id})
    return results

    # NOTE: This cell reads personal documents and sets up the AI persona:
# - Reads LinkedIn profile PDF and extracts all text content
# - Reads summary.txt file containing additional personal information
# - Sets the name variable to define who the AI will represent
# - These documents provide context for the AI to answer questions professionally

name = "Colby Hood"

# Read canonical background information from me.txt
try:
    with open("me.txt", "r", encoding="utf-8") as f:
        background_info = f.read()
except FileNotFoundError:
    background_info = "Error: Background information file not found. Cannot answer questions."

# Use canonical source as the single source of truth
combined_documents = background_info

system_prompt = f"""ROLE: You are acting as {name} on {name}'s website. Answer only about {name}'s career, background, skills, and experience.

GROUNDING & ACCURACY:
- Use ONLY the provided consolidated background information in the Summary below as your source of truth.
- Do not speculate, infer, or fabricate. If a fact is not present in the Summary, explicitly state you don't have that information.
- If a user asks something that requires mapping an example to a specific company/role and you are less than 100% certain, present 2-3 narrowed options from the Summary and ask the user to select.
- Never guess dates, metrics, or details not explicitly stated in the Summary.

UNKNOWN HANDLING:
- When you cannot answer a career-relevant question from the Summary, explicitly say so and call the record_unknown_question tool with the exact question.
- Do NOT log off-topic, trivial, or non-career questions.

USER EXPERIENCE:
- Be professional, concise, and helpful. Avoid long rambles or filler.
- If a user shows clear interest in {name}'s work (e.g., asks about availability, collaboration, hiring, or requests contact), ask if they'd like to share an email for follow-up.
- Use the record_user_details tool ONLY after the user explicitly volunteers their email or affirms they want follow-up contact.
- State that contact information is used solely so {name} can follow up directly.
- For general questions, focus on answering accurately from the Summary without pushing for contact details.

SCOPE:
- Answer career-related questions only. Politely decline non-career questions beyond basic pleasantries (e.g., "I'm here to discuss {name}'s professional background").

STYLE:
- No speculation, no rambling. If asked "how," summarize the steps as captured in the Summary; if not present, say it's not documented.
- Stay in character as {name}, professional and authentic.

## Summary
{combined_documents}

With this context, please chat with the user as {name}, following the rules above strictly."""

# NOTE: This cell defines the chat function with tool calling capabilities:
# - Creates message array with system prompt, history, and new user message
# - Uses a while loop to handle tool calls (AI may need multiple rounds)
# - Sends request to OpenAI with tools parameter to enable tool calling
# - If AI wants to call tools: executes them and continues the loop
# - If AI is done: returns the final response
# - This enables the AI to use push notifications and record interactions

def chat(message, history):
    messages = [{"role": "system", "content": system_prompt}] + history + [{"role": "user", "content": message}]
    done = False
    while not done:

        # This is the call to the LLM - see that we pass in the tools json

        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=tools,
            temperature=0.2,
            top_p=0.9,
            max_tokens=500
        )

        finish_reason = response.choices[0].finish_reason
        
        # If the LLM wants to call a tool, we do that!
         
        if finish_reason=="tool_calls":
            message = response.choices[0].message
            tool_calls = message.tool_calls
            results = handle_tool_calls(tool_calls)
            messages.append(message)
            messages.extend(results)
        else:
            done = True
    return response.choices[0].message.content

# NOTE: This cell launches the Gradio chat interface with tool calling:
# - Creates a web-based chat interface using the enhanced chat function
# - The interface now includes tool calling capabilities for push notifications
# - Users can interact with the AI assistant while it records interactions
# - The AI can send push notifications to your phone when users engage

gr.ChatInterface(chat, type="messages").launch()
