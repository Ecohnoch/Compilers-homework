#include<iostream>
#include<string>
#include<algorithm>
using namespace std;


#define MAXS 50

int NONE[MAXS]={0};


string strings;//产生式
string Vn;//非终结符
string Vt;//终结符
string first[MAXS];// 用于存放每个终结符的first集
string First[MAXS];// 用于存放每个非终结符的first集
string Follow[MAXS]; // 用于存放每个非终结符的follow集
int N;//产生式个数

string cannotDo;

struct STR
{
    string left;
    string right;
};


//求VN和VT
void VNVT(STR *p){
    int i,j;
    for(i=0;i<N;i++){ // 对每一个产生式
        for(j=0;j<(int)p[i].left.length();j++){ // 左边
            if((p[i].left[j]>='A'&&p[i].left[j]<='Z')){ // 如果是终结符
                if(Vn.find(p[i].left[j])>100)
                    Vn+=p[i].left[j];
            }else{  // 如果是非终结符
                 if(Vt.find(p[i].left[j])>100)
                    Vt +=p[i].left[j];
            }
        }

        for(j=0;j<(int)p[i].right.length();j++){  // 右边
            if(!(p[i].right[j]>='A'&&p[i].right[j]<='Z')){ // 如果是终结符
                if(Vt.find(p[i].right[j])>100)
                    Vt +=p[i].right[j];
            }else{ // 如果是非终结符
                if(Vn.find(p[i].right[j])>100)
                    Vn+=p[i].right[j];
            }
        }
    }
}

void getlr(STR *p,int i){
    int j;
    for(j=0; j < strings.length(); j++){
        if(strings[j] == '-' && strings[j + 1] == '>'){
            p[i].left = strings.substr(0,j);
            p[i].right = strings.substr(j+2,strings.length()-j);
        }
    }
}

//对每个文法符号求first集
string Letter_First(STR *p,char ch){
    int t;
    if(!(Vt.find(ch)>100)){  // 文法符号是终结符，就是本身
        first[Vt.find(ch)]="ch";
        return first[Vt.find(ch)-1];
    }
    if(!(Vn.find(ch)>100)){
        for(int i = 0;i < N; i++){ // 对每个产生式
            if(p[i].left[0] == ch){// 必须要左边是这个非终结符
                cannotDo += ch;

                if(!(Vt.find(p[i].right[0]) > 100)){ // 如果右边的第一个是终结符且在first中不重复
                    if((First[Vn.find(ch)].find(p[i].right[0]) > 100))
                        First[Vn.find(ch)] += p[i].right[0];   // 加入first集合
                    continue;
                }

                if(p[i].right[0]=='*' && (First[Vn.find(ch)].find('*') > 100)){ // 如果右边第一个是空
                    First[Vn.find(ch)] += '*';
                    continue;
                }


                if(!(Vn.find(p[i].right[0]) > 100)){ // 如果右边第一个是非终结符
                    if(p[i].right.length() == 1){ // 如果右边只有一个非终结符
                        string ff;
                        if(cannotDo.find(p[i].right[0]) > 100){

                            ff = Letter_First(p,p[i].right[0]); // 找到这个非终结符的first集合
                            for(int i_i=0; i_i<ff.length(); i_i++)
                                if(First[Vn.find(ch)].find(ff[i_i]) > 100) // 如果不包含有该元素
                                    First[Vn.find(ch)] += ff[i_i];      // 加进去

                        }
                    }else{
                        for(int j=0; j<p[i].right.length(); j++){ // 对右边每一个字符
                            if(p[i].right[j] == ch) continue;

                            string TT;
                            if(cannotDo.find(p[i].right[j]) > 100){
                                TT = Letter_First(p,p[i].right[j]); // 找到每一个字符的first集合

                                if(!(TT.find('*') > 100) && (j+1) < p[i].right.length()){
                                    sort(TT.begin(),TT.end());
                                    string tt;
                                    for(int t = 1;t < TT.length(); t++)
                                        tt += TT[t];

                                    TT = tt;
                                    tt = "";
                                    for(t=0; t<TT.length(); t++)
                                        if(First[Vn.find(ch)].find(TT[t])>100)
                                            First[Vn.find(ch)] += TT[t];
                                }else{
                                    for(t=0; t<TT.length(); t++)
                                        if(First[Vn.find(ch)].find(TT[t])>100)
                                            First[Vn.find(ch)] += TT[t];
                                    break;
                                }
                            }
                        }
                    }

                }
                cannotDo.substr(0, cannotDo.length() - 1);
            }
        }
        return  First[Vn.find(ch)];
    }
}
// 求每个非终结符的Follow集
string Letter_Follow(STR *p,char ch){
    int t, k;
    NONE[Vn.find(ch)]++;

    if(NONE[Vn.find(ch)] == 2){
        NONE[Vn.find(ch)]=0;
        return Follow[Vn.find(ch)];
    }

    for(int i = 0; i < N; i++){  // 对每一个产生式
        for(int j = 0; j < p[i].right.length(); j++){
            if(p[i].right[j] == ch){
                if(j + 1 == p[i].right.length()){
                    string gg;
                    gg = Letter_Follow(p,p[i].left[0]);

                    NONE[Vn.find(p[i].left[0])] = 0;

                    for(int k = 0; k < gg.length(); k++){
                        if(Follow[Vn.find(ch)].find(gg[k]) > 100){
                            Follow[Vn.find(ch)] += gg[k];
                        }
                    }
                }
                else{
                      string FF;
                      for(int jj=j+1;jj<p[i].right.length();jj++){
                          string TT;
                          TT = First[Vn.find(p[i].right[jj])];
                          if((jj + 1) < p[i].right.length()){
                              if(!(TT.find('*') > 100)){
                                sort(TT.begin(), TT.end());
                                string tt;
                                for(int t = 1; t < TT.length(); t++){
                                      tt += TT[t];
                                }
                                TT = tt;
                                tt = "";
                                 for(t=0; t<TT.length(); t++){
                                   if(TT[t] != '*'){
                                        if(FF.find(TT[t]) > 100)
                                          FF += TT[t];
                                    }
                                 }
                              }
                          }else{
                              if(!(TT.find('*') > 100)){
                                for(t=0; t < TT.length(); t++){
                                    if(FF.find(TT[t]) > 100){
                                         FF += TT[t];
                                    }
                                }
                                break;
                              }
                          }
                      }

                      if(FF.find('*') > 100){
                          for(k = 0; k < FF.length(); k++){
                              if(Follow[Vn.find(ch)].find(FF[k]) > 100){
                                  Follow[Vn.find(ch)] += FF[k];
                              }
                          }
                      }else{
                          for(k = 0; k < FF.length(); k++){
                              if(FF[k] != '*'){
                                  if(Follow[Vn.find(ch)].find(FF[k]) > 100)
                                      Follow[Vn.find(ch)] += FF[k];
                              }
                          }
                          string dd;
                          if(ch == p[i].left[0]) continue;
                          dd = Letter_Follow(p, p[i].left[0]);
                          NONE[Vn.find(p[i].left[0])] = 0;
                          for(k = 0; k < dd.length(); k++){
                              if(Follow[Vn.find(ch)].find(dd[k]) > 100){
                                  Follow[Vn.find(ch)] += dd[k];
                              }
                          }
                      }
                }
            }
        }
    }
    return Follow[Vn.find(ch)];
}

int main()
{
    int i,j,k;
    cout<<"产生式总数:";
    cin>>N;
    cout<<"\n请输入各产生式（*代表空）:"<<endl;
    STR *p=new STR[MAXS];
    for(i=0;i<N;i++){
        cin>>strings;
        getlr(p,i);
    }
    VNVT(p);
    cout<<endl;
    for(int i = 0; i < Vn.length(); ++i){
        cout<<Vn[i]<<" first: {";
        string pp;
        pp = Letter_First(p, Vn[i]);
        for(int j = 0; j + 1 < pp.length(); ++j){
            cout<<pp[j]<<", ";
        }
        cout<<pp[pp.length() - 1]<<"} "<<endl;
    }


    for(int i = 0; i < Vn.length(); ++i){
        Follow[0] += '#';
        cout<< Vn[i]<<" follow: {";
        string ppp;
        ppp = Letter_Follow(p, Vn[i]);
        for(int k = 0; k + 1 < ppp.length(); k++){
            cout<<ppp[k]<<", ";
        }
        cout<<ppp[k]<<"}"<<endl;
    }
    return 0;
}
