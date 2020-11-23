#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void)
{
    float dollar;
    int n = 0;
    do
    {
         dollar = get_float("Change owed: ");
    }
    while (dollar <= 0);
    int cents = round(dollar*100);
    while (cents >= 25)
    {
        cents -= 25;
        n++;
    }
    while (cents >= 10)
    {
        cents -= 10;
        n++;
    }
    while (cents >= 5)
    {
        cents -= 5;
        n++;
    }
    while (cents >= 1)
    {
        cents -= 1;
        n++;
    }
    printf("%i\n", n);
}