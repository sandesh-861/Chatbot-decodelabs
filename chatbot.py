import os
from google import genai
from google.genai import types

# 🚨 API KEY IS ALREADY APPENDED BELOW
API_KEY = os.environ.get("GEMINI_API_KEY")

# Initialize the official GenAI Client using your API key
client = genai.Client(api_key=API_KEY)

# Maintain an active in-memory list array to store conversation history
chat_history = []

# Sliding Window constraint (Max pairs of turns to keep in RAM)
MAX_HISTORY_PAIRS = 5 

print("====================================================")
print("🤖 DecodeLabs Project 1: Live Gemini Chatbot with Memory")
print("Type your message and press Enter. Type 'quit' to exit.")
print("====================================================\n")

while True:
    user_input = input("You: ").strip()
    
    if user_input.lower() == 'quit':
        print("Goodbye!")
        break
        
    # --- STRUCTURAL VALIDATION GATE ---
    if not user_input:
        print("System Warning: Empty inputs are blocked. Please type something.\n")
        continue

    # --- SLIDING WINDOW (FIFO TRUNCATION) ---
    if len(chat_history) > (MAX_HISTORY_PAIRS * 2):
        chat_history.pop(0) 
        chat_history.pop(0) 
        print("💡 [System Note: Oldest conversation pair truncated to prevent token exhaustion]")

    # --- INGEST & APPEND (User Turn) ---
    user_turn = types.Content(
        role="user",
        parts=[types.Part.from_text(text=user_input)]
    )
    chat_history.append(user_turn)

    try:
        # --- TRANSMIT PAYLOAD & PROCESS ---
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=chat_history,
        )
        
        print(f"\nAI: {response.text}\n")
        
        # --- RECORD (Model Turn) ---
        model_turn = types.Content(
            role="model",
            parts=[types.Part.from_text(text=response.text)]
        )
        chat_history.append(model_turn)

    except Exception as e:
        print(f"An API/Payload Error Occurred: {e}")
        chat_history.pop()