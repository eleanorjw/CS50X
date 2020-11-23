#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int n;
    //prompt for n between 1 & 8 inclusive
    do
    {
        n = get_int("Height:");
    }
    while (n < 1 || n > 8);
    //print n*n block
    for (int i = 0; i < n; i++)
    {
        //print decreasing space for each line
        for (int j = 1 + i; j < n; j++)
        {
            printf(" ");
        }
        //print increasing # for each line
        for (int k = 0; k < 1 + i; k++)
        {
            printf("#");
        }
        printf("\n");
    }
}



