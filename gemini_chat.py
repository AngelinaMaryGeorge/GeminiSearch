import os
import google.generativeai as genai
from googleapiclient.discovery import build
from dotenv import load_dotenv



load_dotenv()


genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

SEARCH_API_KEY = os.getenv("SEARCH_API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")


# List all available models
for m in genai.list_models():
  print(f"Model Name: {m.name}")
  print(f"Supported Methods: {m.supported_generation_methods}\n")

def google_search(query: str, num_results: int = 3) -> list:
    """
    Performs a Google search and returns a list of snippets from the results.
    """
    try:
        service = build("customsearch", "v1", developerKey=SEARCH_API_KEY)
        res = service.cse().list(q=query, cx=SEARCH_ENGINE_ID, num=num_results).execute()
        
        snippets = [item['snippet'] for item in res.get('items', [])]
        return snippets
    except Exception as e:
        print(f"An error occurred during Google search: {e}")
        return []

def main():
    """
    The main function to run the chat application.
    """
    print("🤖 Gemini Chatbot Initialized. Type 'quit' to exit.")
    print("To get real-time data, start your prompt with 'search for:'.")
    print("-" * 30)

    # Initialize the Gemini model
    model = genai.GenerativeModel('gemini-1.5-flash')

    chat = model.start_chat(history=[])

    while True:
        prompt = input("You: ").strip()
        if prompt.lower() == 'quit':
            print("🤖 Goodbye!")
            break

        if prompt.lower().startswith("search for:"):
            search_query = prompt[len("search for:"):].strip()
            print(f"🔍 Searching for '{search_query}'...")
           
            search_results = google_search(search_query)

            if not search_results:
                print("🤖 I couldn't find any information for that search.")
                continue

            augmented_prompt = (
                f"Based on the following real-time search information, answer the user's question.\n\n"
                f"--- Search Results ---\n"
                f"{' | '.join(search_results)}\n"
                f"--- End of Search Results ---\n\n"
                f"User's Question: {search_query}"
            )
            
            response = chat.send_message(augmented_prompt)
            print(f"Gemini: {response.text}")

        else:
            response = chat.send_message(prompt)
            print(f"Gemini: {response.text}")

if __name__ == "__main__":
    main()