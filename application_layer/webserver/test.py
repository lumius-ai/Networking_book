
import os
    
if __name__ == '__main__':
    try:
        os.remove("deletethis.html")
    except FileNotFoundError as e:
        print(e)
