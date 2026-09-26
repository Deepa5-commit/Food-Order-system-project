import tkinter as tk
from tkinter import messagebox
import mysql.connector

def connect_db():
    con= mysql.connector.connect(
        host="localhost",
        user="root",
        password="Deepa125",
        port=3307,
        database="food_order"
        )
    return con

root=tk.Tk()
root.title("Food Order Management System")
root.geometry("800x500")
root.config(bg="lightblue")

def login():
    username=name.get()
    password1=password.get()

    con=connect_db()
    cur=con.cursor()
    query="select * from users where username=%s and password=%s"
    cur.execute(query,(username,password1))
    result=cur.fetchone()
    cur.close()
    con.close()

    if result:
        messagebox.showinfo("Login","Login Successful")
        menu(username)
    else:
        messagebox.showerror("Invalid username or password")

def menu(username):
    root2=tk.Toplevel(root)
    root2.title("Food Order Management System")
    root2.geometry("800x400")
    root2.config(bg="red")
    
    tk.Label(root2,text="Food Order Management System",font=("Algerian",25)).grid()
    tk.Button(root2,text="Recommended for you",command=lambda:recom(root2)).grid(columnspan=2,padx=10,pady=10)
    tk.Button(root2,text="Food Items Under 250rs",command=lambda:food(root2)).grid(columnspan=2,padx=10,pady=10)
    tk.Button(root2,text="Available foods",command=lambda:availfood(root2)).grid(columnspan=2,padx=10,pady=10)

def order(food_name):
    prices={
        "Noodles":120,
        "Dosa":80,
        "Biryani":260
        }
    if food_name== "":
        messagebox.showwarning(
            "Order","Please select a food"
            )
        return
    order_food(food_name,prices[food_name])
    
def recom(root2):
    win=tk.Toplevel(root2)
    win.title("Recommended Food")
    win.geometry("300x300")
    win.config(bg="pink")
    food=tk.StringVar()
    
    noodles=tk.Radiobutton(win,text="Noodles-Rs.120",variable=food,value="Noodles").grid()
    manchurian=tk.Radiobutton(win,text="Manchurian-Rs.110",variable=food,value="Manchurian").grid()
    dosa=tk.Radiobutton(win,text="Dosa-Rs.80",variable=food,value="Dosa").grid()
    vadapav=tk.Radiobutton(win,text="Vadapav-Rs.60",variable=food,value="Vadapav").grid()
    biryani=tk.Radiobutton(win,text="Biryani-Rs.260",variable=food,value="Biryani").grid()
    tk.Button(win,text="Order",command=lambda: order(food.get())).grid(columnspan=2,padx=10,pady=10)    


def food(root2):
    win=tk.Toplevel(root2)
    win.title("Food Items under 250rs")
    win.geometry("300x300")
    win.config(bg="pink")
    tk.Label(win,text="Food Items under 250Rs",font=("Algerian",15)).grid()

    con=connect_db()
    cur=con.cursor()
    cur.execute("select name,price from food where price< 250")
    foods=cur.fetchall()

    for food_name, price in foods:
        tk.Button(win,text=food_name +"-Rs." +str(price),command=lambda n=food_name,
                  p=price: order_food(n,p)).grid(pady=10)
       
    cur.close()
    con.close()
    
def availfood(root2):
    win=tk.Toplevel(root2)
    win.title("Available Foods")
    win.geometry("300x300")
    win.config(bg="pink")
    tk.Label(win,text="Available Foods",font=("Algerian",15)).grid()

    con=connect_db()
    cur=con.cursor()
    cur.execute("select name,price from food")
    foods=cur.fetchall()

    for food_name, price in foods:
        tk.Button(win,text=food_name +"-Rs." +str(price),command=lambda n=food_name,
                  p=price: order_food(n,p)).grid(pady=10)
    cur.close()
    con.close()

def order_food(food_name,price):
    username= name.get()
    con=connect_db()
    cur=con.cursor()

    query="""insert into orders(username,food_name,price) values(%s,%s,%s)"""
    cur.execute(query,(username, food_name, price))
    con.commit()
    cur.close()
    con.close()

    messagebox.showinfo(
        "Order","Order Successful!\nFood:" +food_name +"\nPrice:Rs." +str(price))

tk.Label(root,text="Login",font=("Algerian",20)).grid(columnspan=2,padx=10,pady=10)

tk.Label(root,text="Username").grid(row=1,column=0,padx=10,pady=10)
name=tk.Entry(root)
name.grid(row=1,column=1,padx=10,pady=10)

tk.Label(root,text="Password").grid(row=2,column=0,padx=10,pady=10)
password=tk.Entry(root,show="*")
password.grid(row=2,column=1,padx=10,pady=10)

tk.Button(root,text="Login",command=login).grid(row=3,column=0,columnspan=2,padx=10,pady=10)

    
root.mainloop()
