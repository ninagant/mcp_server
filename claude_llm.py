import anthropic
import os

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Anthropic client
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def chat_with_claude(user_message, model_name="claude-sonnet-4-20250514"):
    """
    Sends a message to Claude and returns its response.
    """
    try:
        message = client.messages.create(
            model=model_name,
            max_tokens=1000, # Max tokens for Claude's response
            messages=[
                {"role": "user", "content": user_message}
            ]
        )
        return message.content[0].text # Access the text content of the response
    except anthropic.APIError as e:
        print(f"Anthropic API Error: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

if __name__ == "__main__":
    prompt = "Who will win NBA championship in 2026?"
    response = chat_with_claude(prompt)

    if response:
        print(f"User: {prompt}")
        print(f"Claude: {response}")

    # Example with a different model
    # response_opus = chat_with_claude("Write a short story about a futuristic city powered by renewable energy.", "claude-3-opus-20240229")
    # if response_opus:
    #     print(f"\nUser (Opus): Write a short story about a futuristic city powered by renewable energy.")
    #     print(f"Claude (Opus): {response_opus}")