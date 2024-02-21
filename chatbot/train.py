from tools.tools import get_tag, get_patterns, get_response, get_required_words, save_json


def main():
    """
    Main function for the Chatbot Configuration Tool.

    This tool allows developers to configure the chatbot's responses.
    It prompts the user for details such as tags, patterns, responses, and required words.
    The configuration is then saved to a JSON file.

    LICENSE:
    This code is licensed under the MIT License.
    See the LICENSE file in the root of this repository for details.

    REMINDER:
    Use this tool responsibly and consider the impact on user experience.

    AUTHOR:
    GitHub: CyberArcenal
    Github: black
    """

    print("\033[1;96m=== Chatbot Configuration Tool ===\033[0m")
    while True:
        tags = get_tag()
        patterns = get_patterns()
        response = get_response()
        single_response = input("\033[1;97msingle response? [Y/n]: \033[1;92m").lower()
        required_words = get_required_words()
        
        if single_response.lower() == "y":
            single_response = True
        else:
            single_response = False
            
        save_json(tags, patterns, response, single_response, required_words)
    
if __name__ == "__main__":
    main()
