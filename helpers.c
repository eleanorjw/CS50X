#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            
            image[i][j].rgbtBlue 
            = image[i][j].rgbtGreen 
            = image[i][j].rgbtRed 
            = round((image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) / 3.0);
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            long red = round(.393 * image[i][j].rgbtRed + .769 * image[i][j].rgbtGreen + .189 * image[i][j].rgbtBlue);
            long green = round(.349 * image[i][j].rgbtRed + .686 * image[i][j].rgbtGreen + .168 * image[i][j].rgbtBlue);
            long blue = round(.272 * image[i][j].rgbtRed + .534 * image[i][j].rgbtGreen + .131 * image[i][j].rgbtBlue);
            if (red > 255)
            {
                image[i][j].rgbtRed = 255;
            }
            else
            {
                image[i][j].rgbtRed = red;
            }
            if (blue > 255)
            {
                image[i][j].rgbtBlue = 255;
            }
            else
            {
                image[i][j].rgbtBlue = blue;
            }
            if (green > 255)
            {
                image[i][j].rgbtGreen = 255;
            }
            else
            {
                image[i][j].rgbtGreen = green;
            }
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0, k = width - 1; j < k; j++, k--)
        {
            RGBTRIPLE buff = image[i][j];
            image[i][j] = image[i][k];
            image[i][k] = buff;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE imageC[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            imageC[i][j] = image[i][j];
        }
    }
    
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            if (i == 0)
            {
                if (j == 0)
                {
                    image[i][j].rgbtRed = (imageC[i][j].rgbtRed + imageC[i][j+1].rgbtRed + imageC[i+1][j].rgbtRed + imageC[i+1][j+1].rgbtRed) / 4;
                    image[i][j].rgbtGreen = (imageC[i][j].rgbtGreen + imageC[i][j+1].rgbtGreen + imageC[i+1][j].rgbtGreen + imageC[i+1][j+1].rgbtGreen) / 4;
                    image[i][j].rgbtBlue = (imageC[i][j].rgbtBlue + imageC[i][j+1].rgbtBlue + imageC[i+1][j].rgbtBlue + imageC[i+1][j+1].rgbtBlue) / 4;
                }
                else if (j == width - 1)
                {
                    image[i][j].rgbtRed = (imageC[i][j].rgbtRed + imageC[i][j-1].rgbtRed + imageC[i][j].rgbtRed + imageC[i][j-1].rgbtRed) / 4;
                    image[i][j].rgbtGreen = (imageC[i][j].rgbtGreen + imageC[i][j-1].rgbtGreen + imageC[i][j].rgbtGreen + imageC[i][j-1].rgbtGreen) / 4;
                    image[i][j].rgbtBlue = (imageC[i][j].rgbtBlue + imageC[i][j-1].rgbtBlue + imageC[i][j].rgbtBlue + imageC[i][j-1].rgbtBlue) / 4;
                }
                else
                {
                    image[i][j].rgbtRed = (imageC[i][j].rgbtRed + imageC[i][j-1].rgbtRed + imageC[i][j+1].rgbtRed + imageC[i+1][j].rgbtRed + imageC[i+1][j-1].rgbtRed + imageC[i+1][j+1].rgbtRed) / 6;
                    image[i][j].rgbtGreen = (imageC[i][j].rgbtGreen + imageC[i][j-1].rgbtGreen + imageC[i][j+1].rgbtGreen + imageC[i+1][j].rgbtGreen + imageC[i+1][j-1].rgbtGreen + imageC[i+1][j+1].rgbtGreen) / 6;
                    image[i][j].rgbtBlue = (imageC[i][j].rgbtBlue + imageC[i][j-1].rgbtBlue + imageC[i][j+1].rgbtBlue + imageC[i+1][j].rgbtBlue + imageC[i+1][j-1].rgbtBlue + imageC[i+1][j+1].rgbtBlue) / 6;
                }
            }
            else if (i == height - 1)
            {
                if (j == 0)
                {
                    image[i][j].rgbtRed = (imageC[i][j].rgbtRed + imageC[i][j+1].rgbtRed + imageC[i-1][j].rgbtRed + imageC[i-1][j+1].rgbtRed) / 4;
                    image[i][j].rgbtGreen = (imageC[i][j].rgbtGreen + imageC[i][j+1].rgbtGreen + imageC[i-1][j].rgbtGreen + imageC[i-1][j+1].rgbtGreen) / 4;
                    image[i][j].rgbtBlue = (imageC[i][j].rgbtBlue + imageC[i][j+1].rgbtBlue + imageC[i-1][j].rgbtBlue + imageC[i-1][j+1].rgbtBlue) / 4;
                }
                else if (j == width - 1)
                {
                    image[i][j].rgbtRed = (imageC[i][j].rgbtRed + imageC[i][j-1].rgbtRed + imageC[i-1][j].rgbtRed + imageC[i-1][j-1].rgbtRed) / 4;
                    image[i][j].rgbtGreen = (imageC[i][j].rgbtGreen + imageC[i][j-1].rgbtGreen + imageC[i-1][j].rgbtGreen + imageC[i-1][j-1].rgbtGreen) / 4;
                    image[i][j].rgbtBlue = (imageC[i][j].rgbtBlue + imageC[i][j-1].rgbtBlue + imageC[i-1][j].rgbtBlue + imageC[i-1][j-1].rgbtBlue) / 4;
                }
                else
                {
                    image[i][j].rgbtRed = (imageC[i][j].rgbtRed + imageC[i][j-1].rgbtRed + imageC[i][j+1].rgbtRed + imageC[i-1][j].rgbtRed + imageC[i-1][j-1].rgbtRed + imageC[i-1][j+1].rgbtRed) / 6;
                    image[i][j].rgbtGreen = (imageC[i][j].rgbtGreen + imageC[i][j-1].rgbtGreen + imageC[i][j+1].rgbtGreen + imageC[i-1][j].rgbtGreen + imageC[i-1][j-1].rgbtGreen + imageC[i-1][j+1].rgbtGreen) / 6;
                    image[i][j].rgbtBlue = (imageC[i][j].rgbtBlue + imageC[i][j-1].rgbtBlue + imageC[i][j+1].rgbtBlue + imageC[i-1][j].rgbtBlue + imageC[i-1][j-1].rgbtBlue + imageC[i-1][j+1].rgbtBlue) / 6;
                }
            }
            else
            {
                if (j == 0)
                {
                    image[i][j].rgbtRed = (imageC[i][j].rgbtRed + imageC[i][j+1].rgbtRed + imageC[i+1][j+1].rgbtRed + imageC[i-1][j].rgbtRed + imageC[i-1][j+1].rgbtRed + imageC[i+1][j].rgbtRed) / 6;
                    image[i][j].rgbtGreen = (imageC[i][j].rgbtGreen + imageC[i][j+1].rgbtGreen + imageC[i+1][j+1].rgbtGreen + imageC[i-1][j].rgbtGreen + imageC[i-1][j+1].rgbtGreen + imageC[i+1][j].rgbtGreen) / 6;
                    image[i][j].rgbtBlue = (imageC[i][j].rgbtBlue + imageC[i][j+1].rgbtBlue + imageC[i+1][j+1].rgbtBlue + imageC[i-1][j].rgbtBlue + imageC[i-1][j+1].rgbtBlue + imageC[i+1][j].rgbtBlue) / 6;
                }
                else if (j == width - 1)
                {
                    image[i][j].rgbtRed = (imageC[i][j].rgbtRed + imageC[i][j-1].rgbtRed + imageC[i+1][j].rgbtRed + imageC[i-1][j].rgbtRed + imageC[i-1][j-1].rgbtRed + imageC[i+1][j+1].rgbtRed) / 6;
                    image[i][j].rgbtGreen = (imageC[i][j].rgbtGreen + imageC[i][j-1].rgbtGreen + imageC[i+1][j].rgbtGreen + imageC[i-1][j].rgbtGreen + imageC[i-1][j-1].rgbtGreen + imageC[i+1][j+1].rgbtGreen) / 6;
                    image[i][j].rgbtBlue = (imageC[i][j].rgbtBlue + imageC[i][j-1].rgbtBlue + imageC[i+1][j].rgbtBlue + imageC[i-1][j].rgbtBlue + imageC[i-1][j-1].rgbtBlue + imageC[i+1][j+1].rgbtBlue) / 6;
                }
                else
                {
                    image[i][j].rgbtRed = (imageC[i][j].rgbtRed + imageC[i][j-1].rgbtRed + imageC[i][j+1].rgbtRed + imageC[i-1][j].rgbtRed + imageC[i-1][j-1].rgbtRed + imageC[i+1][j-1].rgbtRed + imageC[i+1][j].rgbtRed + imageC[i+1][j-1].rgbtRed + imageC[i+1][j+1].rgbtRed) / 9;
                    image[i][j].rgbtGreen = (imageC[i][j].rgbtGreen + imageC[i][j-1].rgbtGreen + imageC[i][j+1].rgbtGreen + imageC[i-1][j].rgbtGreen + imageC[i-1][j-1].rgbtGreen + imageC[i+1][j-1].rgbtGreen + imageC[i+1][j].rgbtGreen + imageC[i+1][j-1].rgbtGreen + imageC[i+1][j+1].rgbtGreen) / 9;
                    image[i][j].rgbtBlue = (imageC[i][j].rgbtBlue + imageC[i][j-1].rgbtBlue + imageC[i][j+1].rgbtBlue + imageC[i-1][j].rgbtBlue + imageC[i-1][j-1].rgbtBlue + imageC[i+1][j-1].rgbtBlue + imageC[i+1][j].rgbtBlue + imageC[i+1][j-1].rgbtBlue + imageC[i+1][j+1].rgbtBlue) / 9;
                }
            }
        }
    }
    return;
}
