#include <bits/stdc++.h>
using namespace std;


int main(){
    int n,count=0;
    cin >> n;
    int grade[1005][4] = {0};
    int sum[1005] = {0};
    for(int i=1; i<=n; i++){
        scanf("%d %d %d", &grade[i][1], &grade[i][2], &grade[i][3]);
        sum[i] = grade[i][1] + grade[i][2] + grade[i][3];
    }

    for(int i=1; i<=n; i++){
        for(int j=i+1; j<=n; j++){
            if(abs(grade[i][1]-grade[j][1])<=5 && abs(grade[i][2]-grade[j][2])<=5 && abs(grade[i][3]-grade[j][3])<=5 && abs(sum[i]-sum[j])<=10){
                count++;
            }
        }
    }





    cout << count << endl;



    return 0;
}