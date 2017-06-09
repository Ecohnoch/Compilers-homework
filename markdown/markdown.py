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

## LL language judge is there has strong
def hasStrong(test):
    ll = {
        'S': ['ABABA', 'ABABA'],
        'A': ['aA', '*'],
        'B': ['e', '**']
    }

    zhan = ['S']
    start = 0
    num = ''
    indice = 0

    while(len(zhan) > 0):
        s = zhan.pop(0)
        # when test has analysed completely
        if start > (len(test) - 1):
            if s == 'A' and len(zhan) <= 1:
                return True
            else:
                return False

        # switch the chinese or other charater to a or *
        if test[start] == '*':
            num = '*'
            indice = 1
        else:
            num = 'a'
            indice = 0

        # do the offset
        if s == num:
            start = start + 1

        elif s == 'A' and indice == 1:
            if start + 1 > (len(test) - 1):
                pass
                # print('A -> e')
            elif test[start + 1] == '*':
                pass
                # print('A -> e')
            else:
                zhan.insert(0, 'A')
                zhan.insert(0, '*')
                # print('A -> *')

    
        elif ll[s][indice] != 'e':
            # print(s, ' ->', ll[s][indice])
            for i in range(len(ll[s][indice]) - 1, -1, -1):
                zhan.insert(0, ll[s][indice][i])

        # not match the language
        else:
            return False
    return True

def handleStrong(test):
    match = 0
    while(test.find('**') != -1):
        pos = test.find('**')
        if match % 2 == 0:
            if pos + 2 < len(test):
                test = test[: pos] + '<strong>' + test[pos + 2:]
                match = match + 1
            else:
                test = test[: pos] + '<strong>'
                match = match + 1
        elif match % 2 == 1:
            if pos + 2 < len(test):
                test = test[: pos] + '</strong>' + test[pos + 2:]
                match = match + 1
            else:
                test = test[: pos] + '</strong>'
                match = match + 1
    if match % 2 == 1:
        if pos + 8 < len(test):
            test = test[: pos] + '**' + test[pos + 8:]
        else:
            test = test[: pos] + '**'
    return test

## LL language judge is there has underline
def hasUnderline(test):
    ll = {
        'S': ['ABABA', 'ABABA'],
        'A': ['aA', '+'],
        'B': ['e', '++']
    }

    zhan = ['S']
    start = 0
    num = ''
    indice = 0

    while(len(zhan) > 0):
        s = zhan.pop(0)
        # when test has analysed completely
        if start > (len(test) - 1):
            if s == 'A' and len(zhan) <= 1:
                return True
            else:
                return False

        # switch the chinese or other charater to a or *
        if test[start] == '+':
            num = '+'
            indice = 1
        else:
            num = 'a'
            indice = 0

        # do the offset
        if s == num:
            start = start + 1

        elif s == 'A' and indice == 1:
            if start + 1 > (len(test) - 1):
                pass
                # print('A -> e')
            elif test[start + 1] == '+':
                pass
                # print('A -> e')
            else:
                zhan.insert(0, 'A')
                zhan.insert(0, '+')
                # print('A -> *')

    
        elif ll[s][indice] != 'e':
            # print(s, ' ->', ll[s][indice])
            for i in range(len(ll[s][indice]) - 1, -1, -1):
                zhan.insert(0, ll[s][indice][i])

        # not match the language
        else:
            return False
    return True

def handleUnderline(test):
    match = 0
    while(test.find('++') != -1):
        pos = test.find('++')
        if match % 2 == 0:
            if pos + 2 < len(test):
                test = test[: pos] + '<u>' + test[pos + 2:]
                match = match + 1
            else:
                test = test[: pos] + '<u>'
                match = match + 1
        elif match % 2 == 1:
            if pos + 2 < len(test):
                test = test[: pos] + '<u>' + test[pos + 2:]
                match = match + 1
            else:
                test = test[: pos] + '</u>'
                match = match + 1
    if match % 2 == 1:
        if pos + 8 < len(test):
            test = test[: pos] + '++' + test[pos + 3:]
        else:
            test = test[: pos] + '++'
    return test

## LL language judge is there has underline
def hasBackground(test):
    ll = {
        'S': ['ABABA', 'ABABA'],
        'A': ['aA', '='],
        'B': ['e', '==']
    }

    zhan = ['S']
    start = 0
    num = ''
    indice = 0

    while(len(zhan) > 0):
        s = zhan.pop(0)
        # when test has analysed completely
        if start > (len(test) - 1):
            if s == 'A' and len(zhan) <= 1:
                return True
            else:
                return False

        # switch the chinese or other charater to a or *
        if test[start] == '=':
            num = '='
            indice = 1
        else:
            num = 'a'
            indice = 0

        # do the offset
        if s == num:
            start = start + 1

        elif s == 'A' and indice == 1:
            if start + 1 > (len(test) - 1):
                pass
                # print('A -> e')
            elif test[start + 1] == '=':
                pass
                # print('A -> e')
            else:
                zhan.insert(0, 'A')
                zhan.insert(0, '=')
                # print('A -> *')

    
        elif ll[s][indice] != 'e':
            # print(s, ' ->', ll[s][indice])
            for i in range(len(ll[s][indice]) - 1, -1, -1):
                zhan.insert(0, ll[s][indice][i])

        # not match the language
        else:
            return False
    return True

def handleBackground(test):
    match = 0
    while(test.find('==') != -1):
        pos = test.find('==')
        if match % 2 == 0:
            if pos + 2 < len(test):
                test = test[: pos] + '<strong style = \"background:red\">' + test[pos + 2:]
                match = match + 1
            else:
                test = test[: pos] + '<strong style = \"background:red\">'
                match = match + 1
        elif match % 2 == 1:
            if pos + 2 < len(test):
                test = test[: pos] + '</strong>' + test[pos + 2:]
                match = match + 1
            else:
                test = test[: pos] + '</strong>'
                match = match + 1
    if match % 2 == 1:
        if pos + 8 < len(test):
            test = test[: pos] + '++' + test[pos + 33:]
        else:
            test = test[: pos] + '++'
    return test

# normal block, such as:
# 0. paragraph
# 1. title
# 2. cutline
# 3. list
# 4. quote
def roughParse(eachLine):
    if hasStrong(eachLine):
        eachLine = handleStrong(eachLine)
    if hasUnderline(eachLine):
        eachLine = handleUnderline(eachLine)
    if hasBackground(eachLine):
        eachLine = handleBackground(eachLine)
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
