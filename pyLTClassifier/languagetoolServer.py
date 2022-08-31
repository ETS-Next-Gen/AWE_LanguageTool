import os
from importlib import resources


def runServer(fileName=None):

    MAPPING_PATH = \
        resources.path('pyLTClassifier',
                       'LanguageTool-5.5')

    os.chdir(MAPPING_PATH)
    print(os.getcwd())
    os.system("java -cp languagetool-server.jar \
              org.languagetool.server.HTTPServer \
              --port 8081 --allow-origin \"*\"")


if __name__ == '__main__':
    runServer()
