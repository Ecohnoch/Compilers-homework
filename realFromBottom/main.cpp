#include <iostream>
#include <stack>
#include <string>
using namespace std;

class basicElement{
public:
    basicElement(int s, int v, char sim):state(s), val(v), simbol(sim){}
    int state;
    int val;
    char simbol;
    bool showInfo(){
        cout<<"state: "<< state << endl;
        cout<<"val:   "<< val << endl;
        cout<<"simbol:"<< simbol << endl;
        return true;
    }
    bool set(int s, int v, char sim){
        state = s;
        val = v;
        simbol = sim;
    }
};

class tables{
    // E -> E + T
    // E -> T
    // T -> T*F
    // T -> F
    // F -> (E)
    // f -> i
public:
    char simbolTable[6] = {'i', '+', '*', '(', ')', '$'};
    char tokens[3] = {'E', 'T', 'F'};
    int rightLength[7] = {0, 3, 1, 3, 1, 3, 1};
    char leftSimbol[7] = {'0', 'E', 'E', 'T', 'T', 'F', 'F'};
    string producer[7] = {"0", "E -> E + T", "E -> T", "T -> T * F", "T -> F", "F -> (E)", "F -> i"};

    int e1 = 90, e2 = 91, e3 = 92, e4 = 93, e5 = 94, e6 = 95;
    int acc = 100;

    int actionTable[12][6] = {
        {5,  e1,  e1,  4, e2,  e1},
        {e3,  6,  e5, e3, e2, acc},
        {e2, -2,   7, e2, -2,  -2},
        {e4, -4,  -4, e4, -4,  -4},
        {5,  e1,  e1,  4, e2,  e1},
        {e6, -6,  -6, e6, -6,  -6},
        {5,  e1,  e1,  4, e2,  e1},
        {5,  e1,  e1,  4, e2,  e1},
        {e3,  6,  e5, e3, 11,  e4},
        {e1, -1,   7, e1, -1,  -1},
        {e3, -3,  -3, e3, -3,  -3},
        {e5, -5,  -5, e5, -5,  -5}
    };
    int gotoTable[12][3] = {
        {1,  2,  3},
        {0,  0,  0},
        {0,  0,  0},
        {0,  0,  0},
        {8,  2,  3},
        {0,  0,  0},
        {0,  9,  3},
        {0,  0, 10},
        {0,  0,  0},
        {0,  0,  0},
        {0,  0,  0},
        {0,  0,  0}
    };
    int getStatus(int s, char simbol){
        for(int i = 0; i < 6; ++i)
            if(simbol == simbolTable[i])
                return actionTable[s][i];
        cout<<"***Error, when getStatus"<<endl;
        return -1;
    }
    int getGoto(int s, char token){
        for(int i = 0; i < 3; ++i)
            if(token == tokens[i])
                return gotoTable[s][i];
        cout<<"***Error, when getGotoTable"<<endl;
        return -1;
    }
    bool reduce(int i){
        switch (-i){
        case 1:
            cout<< "Reduce: "<< producer[1]<<endl;
            return true;
        case 2:
            cout<< "Reduce: "<< producer[2]<<endl;
            return true;
        case 3:
            cout<< "Reduce: "<< producer[3]<<endl;
            return true;
        case 4:
            cout<< "Reduce: "<< producer[4]<<endl;
            return true;
        case 5:
            cout<< "Reduce: "<< producer[5]<<endl;
            return true;
        case 6:
            cout<< "Reduce: "<< producer[6]<<endl;
            return true;
        default:
            cout<< "***Error, when print reduce"<<endl;
            return false;
        }
    }
} t;

class input{
public:
    input(){start = 0;}
    string exp;
    int start;
};

int main(){
    stack<basicElement> zhan;
    input exp;
    cout<< "Input an exp: ";
    cin>>exp.exp;
    basicElement basicStatus(0, 0, '0');
    zhan.push(basicStatus);

    int times = 0;
    while(1){
        auto s = zhan.top();


        auto thisSimbol = exp.exp[exp.start];
        int thisAction;
        if(thisSimbol >= '0' && thisSimbol <= '9' )
            thisAction = t.getStatus(s.state, 'i');
        else
            thisAction = t.getStatus(s.state, thisSimbol);
        cout<<thisAction<<endl;

        if(thisAction > 0 && thisAction <= 11){
            basicElement tmp(0, 0, '0');
            if(thisSimbol >= '0' && thisSimbol <= '9')
                tmp.set(thisAction, thisSimbol - '0', 'i');
            else
                tmp.set(thisAction, 0, thisSimbol);
            zhan.push(tmp);
            exp.start ++;
            cout<< "Shift-In!"<<endl;
        }else if(thisAction >= t.e1 && thisAction <= t.e6){
            basicElement tmp(0, 0, '0');
            switch(thisAction){
            case 90:
                cout<<"Lack of id"<<endl;
                tmp.set(5, 0, 'i');
                zhan.push(tmp);
                break;
            case 91:
                cout<<"delete )"<<endl;
                exp.start ++;
                break;
            case 92:
                cout<<"Expect +"<<endl;
                tmp.set(6, 0, '+');
                zhan.push(tmp);
                break;
            case 93:
                cout<<"Expect )"<<endl;
                tmp.set(11, 0, ')');
                zhan.push(tmp);
                break;
            case 94:
                cout<<"Invaild *, expect +"<<endl;
                exp.start ++;
                break;
            case 95:
                cout<< s.val <<" Lack of op"<<endl;
                exp.start ++;
                break;
            }
            cout<<"Error Handled!!"<<endl;

        }else if(thisAction == t.acc){

            cout<< "SUC, value = "<<s.val<<endl;
            break;
        }else if(thisAction < 0){
            basicElement tmp(0, 0, '0');
            auto p1 = zhan.top();
            auto p2 = zhan.top();
            auto p3 = zhan.top();

            switch (-thisAction) {
            case 1:
                p1 = zhan.top();
                zhan.pop();
                p2 = zhan.top();
                zhan.pop();
                p3 = zhan.top();
                zhan.pop();
                s = zhan.top();
                tmp.set(t.getGoto(s.state, t.leftSimbol[1]), p1.val + p3.val, t.leftSimbol[1]);
                break;
            case 2:
                p1 = zhan.top();
                zhan.pop();
                s = zhan.top();
                tmp.set(t.getGoto(s.state, t.leftSimbol[2]), p1.val, t.leftSimbol[2]);
                break;
            case 3:
                p1 = zhan.top();
                zhan.pop();
                p2 = zhan.top();
                zhan.pop();
                p3 = zhan.top();
                zhan.pop();
                s = zhan.top();
                tmp.set(t.getGoto(s.state, t.leftSimbol[3]), p1.val * p3.val, t.leftSimbol[3]);
                break;
            case 4:
                p1 = zhan.top();
                zhan.pop();
                s = zhan.top();
                tmp.set(t.getGoto(s.state, t.leftSimbol[4]), p1.val, t.leftSimbol[4]);
                break;
            case 5:
                p1 = zhan.top();
                zhan.pop();
                p2 = zhan.top();
                zhan.pop();
                p3 = zhan.top();
                zhan.pop();
                s = zhan.top();
                tmp.set(t.getGoto(s.state, t.leftSimbol[5]), p2.val, t.leftSimbol[5]);
                break;
            case 6:
                p1 = zhan.top();
                zhan.pop();
                s = zhan.top();
                tmp.set(t.getGoto(s.state, t.leftSimbol[6]), p1.val, t.leftSimbol[6]);
                break;

            default:
                cout<<"***Error when reduce"<<endl;
                break;
            }
            zhan.push(tmp);
            t.reduce(thisAction);
        }




        times ++;
        if(times >= 50)
            break;
    }





    return 0;
}
