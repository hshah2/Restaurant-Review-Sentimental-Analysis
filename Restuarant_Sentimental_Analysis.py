# -*- coding: utf-8 -*-
"""
Created on Sat Nov 10 21:38:43 2018

@author: harsh2356
"""
import pandas as pd
import numpy as np
from textblob import TextBlob
import csv

#reading the file
df = pd.read_csv('restaurant_week_2018_final.csv')

#sentimental analysis
reviews=[]
lineCount=0
with open('restaurant_week_2018_final.csv',encoding = 'utf-8', newline = '') as file:
    reader = csv.reader(file)
    for row in (reader):
        if (lineCount!=0):
            text = row[27]
            sentiments = TextBlob(text)
            setup = sentiments.sentiment.polarity
            polarity = "positive"
            if setup >= 0.1:
                polarity = 'positive'
            elif setup <= -0.1:
                polarity = 'negative'
            else:
                polarity = 'neutral'
            reviews.append(polarity)
            lineCount+=1
        else:
            lineCount+=1
df['Review type']=reviews

# %%
# GUI
from tkinter import *

#output on clicking submit
def result():
    enteredText = textBox.get()
    chosenRange = var.get()
    outputTextBox.delete(0.0,END)
    if float(enteredText) in np.linspace(0,5,51): #check for input to be a float between 0 and 5
        if (var1.get()==1) & (var2.get()==1) & (var3.get()==1):
            ansDF = df[(df['average review']>float(enteredText)) & (df['price range']==chosenRange) & (df['Parking Availability']=='Yes')& (df['Outdoor Seating facility']=='Yes')&(df['Smoking Allowed']=='Yes')]
        elif (var1.get()==0) & (var2.get()==1) & (var3.get()==1):
            ansDF = df[(df['average review']>float(enteredText)) & (df['price range']==chosenRange) & (df['Parking Availability']=='No')& (df['Outdoor Seating facility']=='Yes')&(df['Smoking Allowed']=='Yes')]
        elif (var1.get()==1) & (var2.get()==0) & (var3.get()==1):
            ansDF = df[(df['average review']>float(enteredText)) & (df['price range']==chosenRange) & (df['Parking Availability']=='Yes')& (df['Outdoor Seating facility']=='No')&(df['Smoking Allowed']=='Yes')]
        elif (var1.get()==1) & (var2.get()==1) & (var3.get()==0):
            ansDF = df[(df['average review']>float(enteredText)) & (df['price range']==chosenRange) & (df['Parking Availability']=='Yes')& (df['Outdoor Seating facility']=='Yes')&(df['Smoking Allowed']=='No')]
        elif (var1.get()==0) & (var2.get()==0) & (var3.get()==1):
            ansDF = df[(df['average review']>float(enteredText)) & (df['price range']==chosenRange) & (df['Parking Availability']=='No')& (df['Outdoor Seating facility']=='No')&(df['Smoking Allowed']=='Yes')]
        elif (var1.get()==0) & (var2.get()==1) & (var3.get()==0):
            ansDF = df[(df['average review']>float(enteredText)) & (df['price range']==chosenRange) & (df['Parking Availability']=='No')& (df['Outdoor Seating facility']=='Yes')&(df['Smoking Allowed']=='No')]
        elif (var1.get()==1) & (var2.get()==0) & (var3.get()==0):
            ansDF = df[(df['average review']>float(enteredText)) & (df['price range']==chosenRange) & (df['Parking Availability']=='Yes')& (df['Outdoor Seating facility']=='No')&(df['Smoking Allowed']=='No')]
        elif (var1.get()==0) & (var2.get()==0) & (var3.get()==0):
            ansDF = df[(df['average review']>float(enteredText)) & (df['price range']==chosenRange) & (df['Parking Availability']=='No')& (df['Outdoor Seating facility']=='No')&(df['Smoking Allowed']=='No')]
        ansDF = ansDF.reset_index(drop=True)
        outputTextBox.insert(END,ansDF[['name','Review type']])
        outputTextBox.tag_configure('left',justify = 'left')
        outputTextBox.tag_add('left',1.0,END)
    else:
        outputTextBox.insert(END,'Please enter a valid input')

#output on clicking enter
def restaurant():
    enteredText1 = textBox.get()
    outputTextBox.delete(0.0,END)
    if df['name'].str.contains(enteredText1).any():
        resdf = df[df['name']==enteredText1]
        resdf = resdf.reset_index(drop=True)
        outputTextBox.insert(END,resdf[['name','phone','Restaurant Type','food','ambience','service']])
        outputTextBox.tag_configure('left',justify = 'left')
        outputTextBox.tag_add('left',1.0,END)
    else:
        outputTextBox.insert(END,'Enter a valid restaurant name')

#action on clicking exit
def closeWindow():
    window.destroy()
    exit()    
        
window = Tk()
window.title('Project')
window.geometry('800x500')
window.configure(bg = 'black')

#label
Label(window, text = 'Apply the filters of your choice: ', bg = 'black',fg = 'white', font = 'Helvetica 12 bold' ).grid(row=0,column=0,sticky = W)
Label(window, text = 'Average Review greater than:  ', bg = 'black',fg = 'white', font = 'Helvetica 12 bold' ).grid(row=1,column=0,sticky = W)
Label(window, text = 'Choose Price Range', bg = 'black',fg = 'white', font = 'Helvetica 12 bold' ).grid(row=1,column=1,sticky = W)
Label(window, text = 'Check boxes', bg = 'black',fg = 'white', font = 'Helvetica 12 bold' ).grid(row=1,column=4,sticky = W)

#text entry box
textBox = Entry(window,width = 20,bg = 'white',insertwidth=4)
textBox.grid(row=2,column=0,sticky = W)

#DropDown List
var = StringVar()
priceRange = OptionMenu(window,var,'$30 and under','$31 to $50','$50 and over')
priceRange.configure(font = 'Helvetica 12 bold' )
priceRange.grid(row=2,column=1,sticky = W)

#checkbutton
var1 = IntVar()
Checkbutton(window,text = 'Parking Availability',variable = var1).grid(row=2,column=3,sticky=W)
var2 = IntVar()
Checkbutton(window,text = 'Outdoor Seating facility',variable = var2).grid(row=2,column=4,sticky=W)
var3 = IntVar()
Checkbutton(window,text = 'Smoking Allowed',variable = var3).grid(row=2,column=5,sticky=W)

#Submit Button
Button(window, text = 'SUBMIT',width=6,command=result).grid(row=3,column=0,sticky = W)
Button(window, text = 'ENTER',width=6,command=restaurant).grid(row=4,column=0,sticky = W)

#output Label
Label(window, text = '\nRestaurants list', bg = 'black',fg = 'white', font = 'Helvetica 12 bold' ).grid(row=5,column=0,sticky = W)

#output Text
outputTextBox = Text(window,width =85,height = 30,bg='white')
outputTextBox.grid(row=6,column=0,sticky = W)

#ExitLabel
Label(window, text = 'Click to exit: ', bg = 'black',fg = 'white', font = 'Helvetica 12 bold' ).grid(row=7,column=0,sticky = W)

#Exit Button
Button(window,text = 'Exit',width =6,command = closeWindow).grid(row=8,column = 0,sticky = W)
window.mainloop()
