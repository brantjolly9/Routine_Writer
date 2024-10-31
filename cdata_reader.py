import re
from pprint import pprint
sampleRungPath = "sample_rung.txt"
sampleRung = ""
with open(sampleRungPath, "r") as sr:
    sampleRung = sr.read()

def split_block(blockText):
    command = re.search("^[A-Z]+", blockText)
    value = re.search(r"\(\w\,", blockText)
    param = re.search(r"\,*.", blockText)
    print(f"Command: {command}")
    print(f"Value: {value}")
    print(f"Param: {param}")

def split_rungs(rungText=str()):
    finalRungs = []
    rungText = rungText.replace("<![CDATA[[", "")
    rungText = rungText.replace("];]]>","")
    rungs = re.split(r"\s\,", rungText)
    for rung in rungs:
        blocks = rung.split(" ")
        print(len(blocks))
        finalRungs.append(blocks)
        rung = blocks

    return finalRungs

rungs = split_rungs(sampleRung)
testRung = rungs[1]
testBlock = testRung[0]
print(testBlock)
split_block(testBlock)
