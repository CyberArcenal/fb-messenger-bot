
def get_limit(message)->int:
     list_word = [word for word in str(message).split()]
     for num, word in enumerate(list_word):
          if str(word) == "limit" or str(word) == "mga":
               try:
                    return int(list_word[num+1])
               except:
                    pass
               try:
                    return int(list_word[num+2])
               except:
                    pass
               try:
                    return int(list_word[num+3])
               except:
                    pass
     for i in list_word:
          try:
               return int(i)
          except:
               pass
     return 10

chat = "search user Darius Gabriel limit is 20"
limit = get_limit(chat)
print(limit)