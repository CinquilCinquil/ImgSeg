import os

for f in os.listdir("test_files/"):
    os.system("python main.py " + "test_files/" + f)