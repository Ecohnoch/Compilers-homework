import sys
import os
import shutil

def openFile(filename):
    f = open(filename, 'r')
    try:
        allText = f.read()
    finally:
        f.close
    return allText

def splitText(allText):
    return allText.split("\n\n")


# aaa -> <p>aaa</p>
def beThePara(para):
    return "<p>" + para + "</p>"

def beTheTitle(title, n):
    return "<h" + str(n) + ">" + title + "</h" + str(n) + ">"

def beTheCutOff(text):
    return "<hr>"

def beTheList(text):
    return "<li>" + text + "</li>"

def beTheQuote(text):
    return "<blockquote class = \"style2\">" + text + "</blockquote>"


# normal block, such as:
# 0. paragraph
# 1. title
# 2. cutline
# 3. list
# 4. quote
def roughParse(eachLine):
    # title
    if eachLine[: 2] == "# ":
        return beTheTitle(eachLine[2 :], 1)
    if eachLine[: 3] == "## ":
        return beTheTitle(eachLine[3 :], 2)
    if eachLine[: 4] == "### ":
        return beTheTitle(eachLine[4 :], 3)
    if eachLine[: 5] == "#### ":
        return beTheTitle(eachLine[5 :], 4)
    if eachLine[: 6] == "##### ":
        return beTheTitle(eachLine[6 :], 5)
    if eachLine[: 7] == "###### ":
        return beTheTitle(eachLine[7 :], 6)

    # cut off
    if eachLine[: 3] == "---":
        return beTheCutOff("cut off")

    # list
    if (eachLine[: 2] == "- ") or (eachLine[: 2] == "* "):
        return beTheList(eachLine[2 :])

    # quote
    if eachLine[: 2] == "> ":
        return beTheQuote(eachLine[2 :])
    return beThePara(eachLine)

# block
def beTheCode(codeBlock):
    return "<pre><code class = \"language-css\">\n" + codeBlock + "</code></pre>\n"



# HTML
def getHTML(allTextList):
    ans = ""
    code = ""
    isCode = False
    codeContinue = False
    for i in allTextList:
        # normal
        tmp = i.split("\n")
        for j in tmp:
             #code
            if (j == "```" and isCode == True):
                isCode = False
                codeContinue = False
                ans = ans + beTheCode(code)
                code = ""
                continue
            if (j == "```" and isCode == False) or codeContinue:
                isCode = True
                codeContinue = True
                if j != "```":
                    code = code + j + "\n"
                continue

            if isinstance(j, str):
                ans = ans + roughParse(j) + "\n"
    return ans

def outputHTML(html, filename):
    if os.path.exists('output'):
        pass
    else:
        os.mkdir('output')
    shutil.copy('prism.css', './output')
    shutil.copy('prism.js', './output')

    f = open('./output/' + filename, 'w')
    f.write(html)
    f.close()

def quoteStyle(html):
    html = html +   "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\"/>\n"
    html = html +   "<meta http-equiv=\"Content-Language\" content=\"zh-CN\" />\n"
    html = html +   "<meta http-equiv=\"Cache-Control\" content=\"no-transform \" /> \n"
    html = html +   "<meta http-equiv=\"Cache-Control\" content=\"no-siteapp\" />\n"
    html = html +   "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1.0,user-scalable=yes\" />\n"
    html = html +   "<style type=\"text/css\">\n"
    html = html +   "blockquote.style2 {\n"
    html = html +   "font: 14px/22px normal helvetica, sans-serif;\n"
    html = html +   "margin-top: 10px;\n"
    html = html +   "margin-bottom: 10px;\n"
    html = html +   "margin-left: 10px;\n"
    html = html +   "padding-left: 15px;\n"
    html = html +   "padding-top: 10px;\n"
    html = html +   "padding-right: 10px;\n"
    html = html +   "padding-bottom: 10px;\n"
    html = html +   "border-left: 3px solid #ccc;\n"
    html = html +   "background-color:#f1f1f1\n"
    html = html +   "          }\n" 
    html = html +   "</style>\n"

    return html

def codeStyle():
    return "<link href=\"prism.css\" rel=\"stylesheet\" />\n"

def codeJs():
    return "<script type=\"text/javascript\" src = \"prism.js\"></script>\n"

def main():
    # allText = openFile('test.md')
    filename = sys.argv[1]
    outputname = sys.argv[2]

    allText = openFile(filename)
    allTextList = splitText(allText)

    html = ""
    html = quoteStyle(html)

    html = html + codeStyle()
    html = html + getHTML(allTextList)
    html = html + codeJs()

    outputHTML(html, outputname)

if __name__ == "__main__":
    main()
