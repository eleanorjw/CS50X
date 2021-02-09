#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

int main(void)
{
    int L = 0;
    int W = 1;
    int S = 0;
    //prompt for text
    string text = get_string("Text: ");
    
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        //find numbers of letters
        if (isalpha(text[i]))
        {
            L++;
        }
        //find numbers of words
        else if (text[i] == ' ')
        {
            W++;
        }
        //find numbers of sentences
        else if (text[i] == '.' || text[i] == '?' || text[i] == '!')
        {
            S++;
        }
    }

    //cal index
    float index = 0.0588 * L / W * 100 - 0.296 * S / W * 100 - 15.8;
    //round to int
    int grade = round(index);
    //print outcome
    if (grade < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (grade >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", grade);
    }
}