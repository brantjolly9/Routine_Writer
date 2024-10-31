import lxml.etree as et

l5xPath = "exeTesting\\Exported_Files\\Configuration_Routine_RLL.L5X"
xmlDoc = et.parse(l5xPath)
root = xmlDoc.getroot()
RLLContent = root.findall('Controller/Programs/Program/Routines/Routine/RLLContent/Rung')

for rung in RLLContent[:10]:
    rungText = rung.find("Text").text
    print(rungText)