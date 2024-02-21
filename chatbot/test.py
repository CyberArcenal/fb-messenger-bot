from mybot import get_response
while True:
    user_input = input("You: ")
    
    if user_input.lower() == 'exit':
        print("Exiting the chat.")
        break
    
    bot_response = get_response(user_input)
    print(f"Bot: {bot_response}")
