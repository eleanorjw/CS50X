#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

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
 BYTE buffer[512];
 //Create var
 FILE *img;
 char *imgn = NULL;
 int found = 0;
 int fileopen = 0;
 //Read file to find jpg n create jpg
 while (fread(&buffer, sizeof(buffer), 1, inptr))
 {
     //find jpg
     if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xff) == 0xe0 )
     {
        if (found == 0)
        {
            sprintf(imgn,"000.jpg");
            img = fopen(imgn, "w");
        }
        else
        {
            fclose(img);
            found ++;
            sprintf(imgn,"%03i.jpg", found);
            img = fopen(imgn, "w");
        }
        fwrite(&buffer, sizeof(buffer), 1, img);
        fileopen = 1;
     }
     //write blocks of jpg
     if (fileopen == 1)
     {
         fwrite(&buffer, sizeof(buffer), 1, img);
     }
 }
 fclose(img);
 fclose(inptr);
}