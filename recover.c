#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#define BLOCK 512

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    //Ensure correct command-line arg
    if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }
 
    //Open file
    FILE *inptr = fopen(argv[1], "r");
    //Ensure file open
    if (inptr == NULL)
    {
        printf("Couldn't open %s\n", argv[1]);
        return 1;
    }
 
    //Create buffer
    BYTE buffer[BLOCK];
 
    //Create var
    FILE *img;
    char filename[8];
    int found = 0;
    int fileopen = 0;
 
    //Read file to find jpg n create jpg
    while (fread(buffer, BLOCK, 1, inptr))
    {
        int fileread = 0;
        //find jpg
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xff) == 0xe0)
        {
            if (found == 0)
            {
                fileopen = 1;
            }
            else
            {
                fclose(img);
            }
        
            //create img.jpg
            sprintf(filename, "%03i.jpg", found++);
            img = fopen(filename, "w");
            if (img == NULL)
            {
                return 1;
            }
            fwrite(buffer, BLOCK, 1, img);
            fileread = 1;
        }
        //write blocks of jpg
        if (fileopen == 1 && fileread == 0)
        {
            fwrite(buffer, BLOCK, 1, img);
        }
    }
    fclose(img);
    fclose(inptr);
}