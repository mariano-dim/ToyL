#include <stdio.h>
#include <stdlib.h>

int main()
{
    int Y;
    int S;
    int P = 1;

    Y = 10;
    S = 1;

    for(int e=0; e<3; e++){
        printf("Iniciando bloque interior %d \n", e);
        printf("P vale %d\n", P);

        int P = 2;

        printf("P vale %d\n", P);

        P = 10 + e;
        printf("P vale %d\n", P);
        while(Y > 0){
            printf("Iniciando bloque intermedio  %d\n", Y);
 //           while(P > 5){
 //               printf("Iniciando bloque mas profundo %d %d\n", Y , P);
 //               P = P -1;
 //               S = 5;
  //          }
            Y = Y -1;
        }

    }






    return 0;
}
