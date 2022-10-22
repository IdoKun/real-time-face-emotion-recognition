# This is just a Template to create Test during devellopements should be remove in final version
import os
from importlib.util import find_spec

def test_0():
    assert True# == os.path.join(","..","requirements.txt")

def test_1():
    print(os.getcwd())
    with open("requirements.txt","r") as requirements:
        #os.path.join("..","requirements.txt"))

        for module in requirements :
            if module[0:1] not in ["\n","# "]:
                print(find_spec(module.strip("\n")))
                assert None != find_spec(module.strip("\n"))

if __name__=="__main__":
    test_1()
