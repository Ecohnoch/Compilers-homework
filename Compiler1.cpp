#include <iostream>
#include <string>

using namespace std;

bool isLetter(char c){
    if((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') || c == '-' || c == '_') return true;
    return false;
}

bool isDigit(char c){
    if(c >= '0' && c <= '9') return true;
    return false;
}

bool isNum(string s){
    int i = 0, l = s.length();
    while(i < l){
        if(!isDigit(s.at(i))) return false;
        i++;
    }
    return true;

}

bool isID(string s){
    if(!isLetter(s.at(0))) return false;
    int l = s.length();
    for(int i = 1; i < l; ++i)
        if((!isLetter(s.at(i))) && (!isDigit(s.at(i)))) return false;
    return true;
}

string keywords[24] = {
    "for", "if", "then", "else", "while", "do", "+", "-",
    "*", "/", ":", ":=", "<", "<>", "<=", ">", ">=", "=", ";",
    "(", ")", "#"
};

bool isKey(string s){
    for(int i = 0; i < 24; ++i)
        if(s == keywords[i]) return true;
    return false;
}

int getKey(string s){
    if(s == "for")        return 1;
    else if(s == "if")    return 2;
    else if(s == "then")  return 3;
    else if(s == "else")  return 4;
    else if(s == "while") return 5;
    else if(s == "do")    return 6;
    else if(isID(s))      return 10;
    else if(isNum(s))     return 11;
    else if(s == "+")     return 13;
    else if(s == "-")     return 14;
    else if(s == "*")     return 15;
    else if(s == "/")     return 16;
    else if(s == ":")     return 17;
    else if(s == ":=")    return 18;
    else if(s == "<")     return 20;
    else if(s == "<>")    return 21;
    else if(s == "<=")    return 22;
    else if(s == ">")     return 23;
    else if(s == ">=")    return 24;
    else if(s == "=")     return 25;
    else if(s == ";")     return 26;
    else if(s == "(")     return 27;
    else if(s == ")")     return 28;
    else if(s == "#")     return 0;
    else return -1;
}

int main(){
    string s;//("for(int i = 0; i < 10; i++");
    getline(cin, s);
    string a = "";
    int i = 0;
    int l = s.length();

    a.push_back(s[0]);
    while(++i <= l){
        a.push_back(s[i]);
        if(a == " "){
            a.pop_back();
            continue;
        }

        if(isID(a)){
            bool flag1 = false;
            while(isID(a)){
                if(isKey(a)) break;
                a.push_back(s[++i]);
                flag1 = true;
            }
            if(flag1 && !isKey(a)){
                i--;
                a.pop_back();
            }
        }
        if(isKey(a)){
            bool flag2 = false;
            while(isKey(a)){
                a.push_back(s[++i]);
                flag2 = true;
            }
            if(flag2){
                i--;
                a.pop_back();
            }
        }
        if(isNum(a)){
            bool flag3 = false;
            while(isNum(a)){
                a.push_back(s[++i]);
                flag3 = true;
            }
            if(flag3){
                i--;
                a.pop_back();
            }
        }


//        if(!isID(a) && !isKey(a) && !isNum(a) && i <= l)
//            cout<<"***Error! a: "<<a<<endl;
        cout<< "<"<<getKey(a)<<", "<<a<<">"<<endl;
        a = "";
    }
    return 0;
}
