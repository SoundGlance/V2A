#include <cstdio>
#include <vector>
#include <algorithm>
#include <set>
using namespace std;

typedef pair<int,int> pii;
typedef pair<pii,pii> rect;

rect make_rect(int i1, int i2, int j1, int j2){
    return rect(pii(i1, i2), pii(j1, j2));
}

// all possible tiling method with <= n segments
set<set<rect>> tiling(int i1, int i2, int j1, int j2, int n){
    set<set<rect>> ret;
    
    set<rect> itself; itself.insert(make_rect(i1, i2, j1, j2));
    ret.insert(itself);

    if(n > 1) for(int i=i1+1;i<i2;i++){
        for(int nn=2;nn<=n;nn++){
            for(int k=1;k<nn;k++){
                set<set<rect>> upper = tiling(i1, i, j1, j2, k);
                set<set<rect>> lower = tiling(i, i2, j1, j2, nn-k);
                for(const set<rect>& a: upper){
                    for(const set<rect>& b: lower){
                        set<rect> r = a;
                        r.insert(b.begin(), b.end());
                        ret.insert(r);
                    }
                }
            }
        }
    }

    if(n > 1) for(int j=j1+1;j<j2;j++){
        for(int nn=2;nn<=n;nn++){
            for(int k=1;k<nn;k++){
                set<set<rect>> upper = tiling(i1, i2, j1, j, k);
                set<set<rect>> lower = tiling(i1, i2, j, j2, nn-k);
                for(const set<rect>& a: upper){
                    for(const set<rect>& b: lower){
                        set<rect> r = a;
                        r.insert(b.begin(), b.end());
                        ret.insert(r);
                    }
                }
            }
        }
    }

    return ret;
}

int main(){
    int n, m; scanf("%d%d", &n, &m);
    set<set<rect>> ts = tiling(0, n, 0, m, 8);

    printf("%d\n", (int)ts.size());
    FILE *f = fopen("rects.txt", "w");
    for(const set<rect>& t : ts){
        fprintf(f, "%d: ", (int)t.size());
        for(const rect& r : t){
            fprintf(f, "(%d-%d,%d-%d) ", r.first.first, r.first.second, r.second.first, r.second.second);
        }
        fprintf(f, "\n");
    }

    return 0;
}
