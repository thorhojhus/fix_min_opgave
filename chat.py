import openai

def chat_with_openai(message, past_messages):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-1106-preview", 
            messages=past_messages + [message]
        )
        return response.choices[0].message['content']
    except Exception as e:
        return str(e)

def main():
    past_messages = []
    print("Chat with AI (type 'exit' to end):")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break

        message = {
            "role": "user",
            "content": user_input
        }

        response = chat_with_openai(message, past_messages)
        print("AI: ", response)

        past_messages.append(message)
        past_messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
