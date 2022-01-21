#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import tkinter as tk            # import the tkinter module as tk to the program
import time
import datetime
import smtplib

root = tk.Tk()                  #the main windows is called root

#root window configuring
root.title("E-commerce price comparison tool")               #Gives the title of the window
root.geometry("1920x1080")                                   #Gives the dimensions of window
root.configure(bg="#6495ED")                                 #setting window color


#Individual product label
iplabel = tk.Label(
    root,
    text="   Individual products  ",
    bg='white',
    fg='green'
)
iplabel.place(x=80, y=50)

#Individual output label
olabel = tk.Label(
    root,
    text="               Output               ",
    bg='white',
    fg='green'
)
olabel.place(x=80, y=300)


#Individual part labels
# Amazon label
alabel = tk.Label(
    root,
    text=" Amazon Link ",
    bg='white',
    fg='red'
)
alabel.place(x=30, y=100)

# Flipkart label
flabel = tk.Label(
    root,
    text=" Flipkart Link ",
    bg='white',
    fg='blue'
)
flabel.place(x=30, y=150)



#Individual Output part labels
#Amazon label
flabel = tk.Label(
    root,
    text=" Amazon ",
    bg='white',
    fg='red'
)
flabel.place(x=30, y=350)

# Flipkart label
flabel = tk.Label(
    root,
    text=" Flipkart ",
    bg='white',
    fg='blue'
)
flabel.place(x=30, y=550)


#Creating textbox

amazonValue = tk.StringVar()                                        #Taking string value
flipkartValue = tk.StringVar()


amazonEntry = tk.Entry(root, textvariable = amazonValue).place(x=150,y=100)            
flipkartEntry = tk.Entry(root, textvariable = flipkartValue).place(x=150,y=150)



import requests
from bs4 import BeautifulSoup as bs





#Amazon code
import re


def get_converted_price(price):
    converted_price = float(re.sub(r"[^\d.]", "", price)) 
    return converted_price


def extract_url(url):

    if url.find("www.amazon.in") != -1:
        index = url.find("/dp/")
        if index != -1:
            index2 = index + 14
            url = "https://www.amazon.in" + url[index:index2]
        else:
            index = url.find("/gp/")
            if index != -1:
                index2 = index + 22
                url = "https://www.amazon.in" + url[index:index2]
            else:
                url = None
    else:
        url = None
    return url

 

address_field = tk.Label(text="Enter your email address ").place(x=370,y=50)
address = tk.StringVar()
address_entry = tk.Entry(textvariable=address).place(x=370,y=100)


#Input desired price
#Label
adesire_field = tk.Label(text=" Enter your desire price ").place(x=580,y=50)
#Amazon
adesire_price = tk.StringVar()
adesire_entry = tk.Entry(textvariable=adesire_price).place(x=580,y=100)
#Flipkart
fdesire_price = tk.StringVar()
fdesire_entry = tk.Entry(textvariable=fdesire_price).place(x=580,y=150)


def agetValue():

    url = amazonValue.get()

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0"
    }
    details = {"name": "", "price": 0, "deal": True, "url": ""}
    _url = extract_url(url)
    if _url is None:
        details = None
    else:
        page = requests.get(_url, headers=headers)
        soup = bs(page.content, "html.parser")
        title = soup.find(id="productTitle")
        price = soup.find(id="priceblock_dealprice")
        
        if price is None:
            price = soup.find(id="priceblock_ourprice")
            
            details["deal"] = False
            
        if title is not None and price is not None:
            details["name"] = title.get_text().strip()
            details["price"] = get_converted_price(price.get_text())
            details["price"] = int(float(details["price"]))                    #converting float price to int
            details["url"] = _url
            
        else:
            details = None
    ct = datetime.datetime.now()
    converted_ct = str(ct)

    #Making Amazon.txt and storing details
    with open('Amazon.txt', 'a+') as a:
            a.write('Product Name = '+details["name"])
            a.write('\n\n')
            a.write("Price = "+str(details["price"]))
            a.write('\n')
            a.write('Time = '+converted_ct)
            a.write('\n\n')
            a.close()

    #Amazon output labels
    a1label = tk.Label(
    root,
    text=" Product name ",
    bg='white',
    fg='blue'
    )
    a1label.place(x=30, y=400)

    alabelpn = tk.Label(
    root,
    text=details["name"],
    bg='white',
    fg='blue'
    )
    alabelpn.place(x=150, y=400)

    #label for price
    a1label = tk.Label(
    root,
    text="        Price        ",
    bg='white',
    fg='blue'
    )
    a1label.place(x=30, y=430)
    
    labelpp = tk.Label(
    root,
    text=details["price"],
    bg='white',
    fg='blue'
    )
    labelpp.place(x=150, y=430)

    print("\nAmazon details:\n\n"+"Product: "+details["name"]+"\n\nPrice: ")
    print(details["price"])

    if address.get() != "":
        aprice = int(details["price"])
        adesire_int = int(adesire_price .get())

        if(aprice <= adesire_int):
        
            address_info = address.get()
            email_body = "Amazon - Your desired value has been reached."
                    
            print(address_info)
                    
            sender_email = "arnabmahato91@gmail.com" 
                    
            sender_password = "Excitedsky1!"
                    
            server = smtplib.SMTP('smtp.gmail.com',587)
                    
            server.starttls()
                    
            server.login(sender_email,sender_password)
                    
            print("Login successful")
                    
            server.sendmail(sender_email,address_info,email_body)
                    
            print("Message sent")
            
                    
        else:
            print("sab khatam") 

    return details["price"]


#Flipkart code
def fgetValue():
    
    url = flipkartValue.get()                                #To get the current text of a Entry widget as a string, we use the get() method
    
    request = requests.get(url)
    soup = bs(request.content,'html.parser')

    product_name = soup.find("span",{"class":"B_NuCI"}).get_text()
    price = soup.find("div",{"class":"_30jeq3 _16Jk6d"}).get_text()
    price = price.replace("₹", "")
    price = price.replace(",", "")

    ct = datetime.datetime.now()
    converted_ct = str(ct)
    
    #Making flipkart.txt and storing details
    with open('flipkart.txt', 'a+') as f:
            f.write('Product Name = '+product_name)
            f.write('\n\n')
            f.write('Price = '+price)
            f.write('\n')
            f.write('Time = '+converted_ct)
            f.write('\n\n')
            f.close()
    
    #labels for product name
    f1label = tk.Label(root,
    text=" Product name ",
    bg='white',
    fg='blue')
    f1label.place(x=30, y=600)

    labelpn = tk.Label(root,
    text=product_name,
    bg='white',
    fg='blue')
    labelpn.place(x=150, y=600)

    #label for price
    f1label = tk.Label(root,
    text="        Price        ",
    bg='white',
    fg='blue'
    )
    f1label.place(x=30, y=630)
    
    labelpp = tk.Label(
    root,
    text=price,
    bg='white',
    fg='blue'
    )
    labelpp.place(x=150, y=630)

    print("\n\nFlipkart details:\n\n"+"Product: "+product_name+"\n\nPrice: ")
    print(price)


    if address.get() != "":
        print(fdesire_price)
        fprice = int(price)
        fdesire_store = fdesire_price.get()
        fdesire_int = int(fdesire_store)

        if(fprice <= fdesire_int):#if desired_price becomes equal to or greater than flipkart price
        
            address_info = address.get()
            email_body = "Flipkart - Your desired value has been reached."
                    
            print(address_info)
                    
            sender_email = "arnabmahato91@gmail.com" 
                    
            sender_password = "Excitedsky1!"
                    
            server = smtplib.SMTP('smtp.gmail.com',587)
                    
            server.starttls()
                    
            server.login(sender_email,sender_password)
                    
            print("Login successful")
                    
            server.sendmail(sender_email,address_info,email_body)
                    
            print("Message sent")
                    
        else:
            print("sab khatam") 
        
    
    return price





def fauto():#Flipkart Automation
    while True: 
        time.sleep(10)
        f = fgetValue()#line 252

def aauto(): #Amazon Automation
    while True:
        time.sleep(10)
        a = agetValue()#line 137


#Automate button
tk.Button(text="Automate", command=fauto).place(x=760,y=145)
tk.Button(text="Automate", command=aauto).place(x=760,y=95)

import os
import subprocess
def Openfolder():   
    subprocess.Popen(r'explorer /select,"C:\Users\praty\Documents\Python Scripts\MAIN\Check"')


tk.Button(text="Open log folder", command=Openfolder).place(x=830,y=95)

def compare():#One time price check function
    fgetValue()#Line 252
    agetValue()#Line 137


tk.Button(text="Compare", command=compare).place(x=120,y=250)

root.mainloop()                 #mainloop() keeps the window visible on the screen. If you don’t call the mainloop() method, the windows will disappear


# In[ ]:




