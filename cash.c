#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void)
{
    float dollars;
    int n = 0;
    //prompt for dollars of non-zero positive value
    do
    {
        dollars = get_float("Change owed: ");
    }
    while (dollars <= 0);
    //round dollars to int cents
    int cents = round(dollars * 100);
    //determine number of coins
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
    //print number of coins
    printf("%i\n", n);
}