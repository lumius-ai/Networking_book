
import os
    
if __name__ == '__main__':
    try:
        cwd = os.getcwd()
        print(cwd)
        os.remove(cwd +"/application_layer/webserver/deletethis.html")
    except FileNotFoundError as e:
        print(e)
