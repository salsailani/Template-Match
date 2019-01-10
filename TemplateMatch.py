from __future__ import print_function
import os, sys
from PIL import Image

template = Image.open("C:/Users/saleh/pictures/tinywaldo.jpg")   
searchImage= Image.open("C:/Users/saleh/pictures/tinyscene.jpg")   
widthT, heightT = template.size 
width, height = searchImage.size
out = Image.new('RGB', searchImage.size, 0xffffff)

def grayscale(picture): #grayscale function
  for x in range(widthT): #loop through x
    for y in range(heightT):
      r,g,b = searchImage.getpixel((x,y))
      L=r+g+b/3 #gray
      out.putpixel((x,y), (int(L),int(L),int(L)))

def compareOne(template,searchImage,x1,y1): #compare one function 
  SAD=0
  for x in range(widthT): #loop through x
    for y in range(heightT): #loop through y       
      r,g,b = searchImage.getpixel((x+1,y+1)) # from the starting x1 and y1
      r1,g1,b1 = template.getpixel((x,y))
      SAD=SAD+abs(g - g1) # sum of absolute difference
  return SAD
  
def compareAll(template,searchImage): # compare all function
  BIG = 1000000   # Big is this big because luminance never reaches this
  matrix = [[BIG for i in range(width)] for j in range(height)] #creating a matrix with big values for the bounds
  for y in range(width):  #loop through x
    for x in range(height):  #loop through y   
      if width -x >= widthT and height-y>=heightT: #if not on out of bounds
        SAD=compareOne(template,searchImage,x,y) # Set SAD to the function commpare one
        matrix[x][y]=SAD # put the SAD values in matrix
      else:
        break
  return matrix
    
def find2Dmin(matrix): #minimum SAD and starting row and Col
  m=matrix[0][0] # first
  for x in range(len(matrix)):  #loop through x
    for y in range(len(matrix)): #loop through y 
      if matrix[x][y]<m: # check for each next one if less assign
        m=matrix[x][y] #min SAD
        x1=x #min row
        y1=y #min col
  return (x1,y1)
             
def displayMatch(searchImage, x1, y1, w1, h1): #call it and specify your color
  borderwidth=2 
  for y in range(width):  #loop through x
    for x in range(height):  #loop through pixels
      r,g,b = searchImage.getpixel((x,y))
      if x1-borderwidth<=x<=x1 and y<=y1+h1+borderwidth and y>=y1-borderwidth  : # left border
        out.putpixel((x,y), 0)#set the border
      if y1-borderwidth<=y<=y1 and x<=x1+w1 and x>=x1: # top border
        out.putpixel((x,y), 0) #set border
      if x1+w1+borderwidth>=x>=x1+w1 and y<=y1+h1+borderwidth and y>=y1-borderwidth: #right border
        out.putpixel((x,y), 0)    #set border
      if y1+h1+borderwidth>=y>=y1+h1 and x<=x1+w1 and x>=x1: #bottom border
        out.putpixel((x,y), 0)  #set border
   
def findWaldo(template, searchImage): #driver function
  grayscale(template) #calling grayscale
  grayscale(searchImage) #calling grayscale  
  matrix = compareAll(template,searchImage) #we assign a global variable to the matrix to use in find2Dmin function 
  (x1,y1)= find2Dmin(matrix) #assign global valuables to row and col to use in displaymatch
  displayMatch(searchImage, x1, y1, w1, h1) #calling display match
  return out

findWaldo(template,searchImage)
