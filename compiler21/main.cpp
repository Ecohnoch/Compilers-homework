#include <iostream>
#include <fstream>
#include <string>

using namespace std;

string myName("大傻逼");
string ID("201545036");

bool isRealWord(string s){
    if(!s.length()) return false;

    for(int i = 0; i < s.length(); ++i)
        if(!((s.at(i) >= 'a' && s.at(i) <= 'z') || (s.at(i) >= 'A' && s.at(i) <= 'Z')))
            return false;

    return true;
}

bool eachWord(string s, int &wordNum){
    int x = 0;
    for(int i = 0; i < s.length(); ++i)
        if(s.at(i) == ' ') x++;
    x++;

    string *words = new string[x];
    int seq = 0;
    for(int i = 0; i < s.length(); ++i){
        if(s.at(i) == ' '){
            seq++;
            continue;
        }
        words[seq] = words[seq] + s.at(i);
    }

    for(int i = 0; i < x; ++i){
        if(words[i] == ID)
            words[i] = myName;

        if(isRealWord(words[i])) wordNum++;
        cout<<words[i]<<" ";
    }

    cout<<endl;
    return true;
}


int main()
{
    ifstream in("/Users/ecohnoch/compiler21/input.txt");

    if(!in)
        cout<< "***Error to open file"<<endl;

    int wordNum = 0, allCharNum = 0;
    string all;

    while(!in.eof()){
        string s;
        getline(in, s);
        allCharNum += s.length();
        eachWord(s, wordNum);
    }

    cout<<wordNum<<" "<<allCharNum<<endl;
    return 0;
}
