// Implements a dictionary's functionality

#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <strings.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 65536;

// Hash table
node *table[N];

// Loadedwords
unsigned int loadedWords = 0;


// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // Get hashvalue of word
    unsigned int val = hash(word);
    
    // Set cursor to the head of list
    node *cursor = table[val];
    
    // Check words
    while (cursor != NULL)
    {
        if (strcasecmp(word, cursor->word) == 0)
        {
            return true;
        }
        
        cursor = cursor->next;
    }
    return false;
}

// Hashes word to a number FROM:https://www.reddit.com/r/cs50/comments/1x6vc8/pset6_trie_vs_hashtable/cf9189q/
unsigned int hash(const char *word)
{
    // Get hash value using function and ensure all words hashed in lowercase
    unsigned int hash = 0;
    for (int i = 0, n = strlen(word); i < n; i++)
    {
        hash = (hash << 2) ^ tolower(word[i]);
    }
    return hash % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // Storage for word
    char word[LENGTH + 1]; 
    
    // Open file
    FILE *infile = fopen(dictionary, "r");
    if (infile == NULL)
    {
        return false;
    }
    
    // Insert word in harshtable
    while (fscanf(infile, "%s", word) != EOF)
    {
        // Allocate memory
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            return false;
        }
        
        // Hash word
        unsigned int val = hash(word);
        
        // Insert word into new node
        strcpy(n->word, word);
        // Set new pointer 
        n->next = table[val];
        // Set head to new pointer
        table[val] = n;
        // Count words
        loadedWords++;
    }
    
    // Close dictionary
    fclose(infile);
    
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // return words counted
    return loadedWords;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // Loop through hashtable
    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];
        // Free memory one by one
        while (cursor != NULL)
        {
            node *tmp = cursor;
            cursor = cursor->next;
            free(tmp);
        }
    }
    return true;
}
