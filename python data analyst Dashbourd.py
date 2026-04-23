import pandas as pd
import matplotlib.pyplot as plt
import sqlalchemy as sqq
from tkinter import ttk,filedialog,messagebox,END
import tkinter as tk
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mysql.connector as sq
import io
import warnings
warnings.filterwarnings("ignore")

# --------------------------------------------------------------
# Backend
# Global variable
df=None
pages={}
val=None
x=None
y=None
file_ext=None

# Database connection
try:
    db=sq.connect(
        host="localhost",
        user="root",
        password="1234",
        database="op"
    )
except Exception as e:
    messagebox.showinfo("Failed","Connection problem arive")

# for query execution
exe=db.cursor()

# theme part
ctk.set_appearance_mode("dark")
root=ctk.CTk()
root.geometry("1300x730")
default_font = ctk.CTkFont(family="Showcard Gothic", size=15)

# rightbar
rightbar=ctk.CTkFrame(root)
rightbar.pack(side="right",fill="both",expand=True)

# for canvas don't show anything
def on_close():
    try:
        plt.close('all')
    except:
        pass
    root.quit()
    root.destroy()

# first impresion
def show_page(name):
    for event in pages.values():
        event.pack_forget()
    pages[name].pack(fill="both",expand=True)

def treee():
    tree.delete(*tree.get_children())
    tree["column"]=list(df.columns)
    tree["show"]="headings"
    for col in df.columns:
        tree.heading(col,text=col)
        tree.column(col,width=140,anchor="center")
    for row in df.itertuples(index=False):
        tree.insert("","end",values=row)

def show_in_bar():
    global df
    buffer=io.StringIO()
    df.info(buf=buffer)
    infoo=buffer.getvalue()
    return infoo

def display_inbars():
    # For Analysis widget
    text.delete("1.0","end")
    text.insert("1.1",df.head(28).to_string(index=False))
    text2.delete("1.0","end")
    text2.insert("1.1",df.to_string(index=False))
    text3.delete("1.0","end")
    text3.insert("1.0",df.head(50).to_string(index=False))
    textwidget.delete("1.0","end")
    textwidget.insert("1.0",df.head(40).to_string(index=False))

    # update the combobox
    val=df.columns.tolist()
    combo.configure(values=val)
    x=df.columns.tolist()
    x_axis.configure(values=x)
    y=df.columns.tolist()
    y_axis.configure(values=y)
    combo2=df.columns.tolist()
    column_name.configure(values=combo2)
    old_col.configure(values=combo2)
    new_data_column.configure(values=combo2)
    confimation_col.configure(values=combo2)
    stats_combo.configure(values=combo2)

def load_data():
    global df,val,x,y
    try:
        df=pd.read_sql(f"select *from {table_name.get()}",db)
    except Exception as e:
        messagebox.showinfo("Failed","File is not loaded")
    # data display part
    file_ext=True
    treee()
    display_inbars()

def load_data_excel():
    global df
    try:
        path=filedialog.askopenfilename(filetypes=[("excel","*.xlsx")])
        df=pd.read_excel(path)
    except Exception:
        messagebox.showinfo("Failed","Data in not loaded")
    file_ext=False
    treee()
    display_inbars()

def line():
    try:
        selected_column=combo.get()
        if df[selected_column].dtype in ['int64','float64']:
            fig,ax=plt.subplots()
            ax.plot(df.iloc[:, 0],df[selected_column],marker="o")
            ax.set_title(f"{selected_column} line graph")
            ax.set_xlabel("ID")
            ax.set_ylabel(selected_column)
            canvas=FigureCanvasTkAgg(fig,master=graph)
            canvas.draw()
            canvas.get_tk_widget().place(x=449,y=220)
        else:
            messagebox.showinfo("Failed","The Given column in String")
    except Exception as e:
        messagebox.showinfo("Failed","Select column first")

def pie():
    try:
        selected_column=combo.get()
        if df[selected_column].dtype in ['int64','float64']:
            fig,ax=plt.subplots()
            ax.pie(df[selected_column],labels=df.iloc[:, 0],autopct="%1.1f%%")
            ax.set_title(f"{selected_column} pie chart")
            canvas=FigureCanvasTkAgg(fig,master=graph)
            canvas.draw()
            canvas.get_tk_widget().place(x=449,y=220)
        else:
            messagebox.showinfo("Failed","The Given column in String")
    except Exception as e:
        messagebox.showinfo("Failed","Select column first")

def histo():
    try:
        selected_column=combo.get()
        if df[selected_column].dtype in ['int64','float64']:
            fig,ax=plt.subplots()
            ax.hist(df[selected_column],bins=30 )
            ax.set_title(f"{selected_column} Histogram graph")
            ax.set_xlabel(selected_column)
            ax.set_ylabel("Frequency")
            canvas=FigureCanvasTkAgg(fig,master=graph)
            canvas.draw()
            canvas.get_tk_widget().place(x=449,y=220)
        else:
            messagebox.showinfo("Failed","The Given column in String")
    except Exception as e:
        messagebox.showinfo("Failed","Select column first")

def bar():
    try:
        selected_column=combo.get()
        if df[selected_column].dtype in ['int64','float64']:
            fig,ax=plt.subplots()
            ax.bar(df.iloc[:, 0],df[selected_column])
            ax.set_title(f"{selected_column} Line graph")
            ax.set_xlabel("ID")
            ax.set_ylabel(selected_column)
            canvas=FigureCanvasTkAgg(fig,master=graph)
            canvas.draw()
            canvas.get_tk_widget().place(x=449,y=220)

        else:
            messagebox.showinfo("Failed","The Given column in String")
    except Exception as e:
        messagebox.showinfo("Failed","Select column first")

def scatter():
    try:
        x_col=x_axis.get()
        y_col=y_axis.get()
        # if df[x_col].dtype in ['int64','float64'] and df[y_col].dtype in ['int64','float64']:
        fig,ax=plt.subplots()
        ax.scatter(df[x_col],df[y_col],alpha=0.8)
        ax.set_title(f"{x_col} vs {y_col} Histogram graph")
        ax.set_xlabel(f"{x_col}")
        ax.set_ylabel(f"{y_col}")
        canvas=FigureCanvasTkAgg(fig,master=graph)
        canvas.draw()
        canvas.get_tk_widget().place(x=449,y=220)
        # else:
        #     messagebox.showinfo("Failed","The Given column in String")
    except Exception as e:
        messagebox.showinfo("Failed","Select both columns first")

def search():
    searching=inputt.get()
    if file_ext is True:
        try:
            
            colom=column_name.get()
            exe.execute(f"select * from {table_name.get()} where {colom}='{searching}';")
            data =exe.fetchall()
            column_head=[i[0] for i in exe.description]
            dff=pd.DataFrame(data,columns=column_head)
            text2.delete("1.0","end")
            text2.insert("1.0",dff.to_string(index=False))
        except Exception as e:
            messagebox.showinfo("Failed","Enter valid data for search.")
    else:
        try:
            if searching.isdigit():
                searching=int(searching)
                for row in df.itertuples():
                    if searching in row:
                        text2.delete("1.0","end")
                        text2.insert("1.0",row[1:])
            else:
                for row in df.itertuples():
                    if searching in row:
                        text2.delete("1.0","end")
                        text2.insert("1.0",row[1:])
        except Exception:
            messagebox.showinfo("Failed","Enter valid data for search.")

def show_data():
    try:
        exe.execute(f"select *from {table_name.get()};")
        row=exe.fetchall()
        column_head=[i[0] for i in exe.description]
        dfff=pd.DataFrame(row,columns=column_head)
        text3.delete("1.0","end")
        text3.insert("1.0",dfff.to_string(index=False))
        load_data()
    except Exception:
        messagebox.showinfo("failed","data can't be show!")

def Change_col_nama():
    try:
        old_name=old_col.get()
        new_name=new_col.get()
        constrain=data_type.get()
        if constrain=="Alphabet":
            exe.execute(f"alter table {table_name.get()} change {old_name} {new_name} varchar(80);")
        else:
            exe.execute(f"alter table {table_name.get()} change {old_name} {new_name} int(50);")
    except Exception:
        messagebox.showinfo("Failed","Invalid input given!")
    db.commit()
    show_data()

def Change_table_data():
    try:
        column_name1=new_data_column.get()
        valuee=new_val.get()
        primary_col=confimation_col.get()
        address=confirm_data.get()
        if address in ['int64','float64']:
            exe.execute(f"update {table_name.get()} set {column_name1}={valuee} where {primary_col}={address};")
        else:
            exe.execute(f"update {table_name.get()} set {column_name1}='{valuee}' where {primary_col}='{address}';")
        db.commit()
    except Exception:
        messagebox.showinfo("Failed","Invalid input given!")
    show_data()
        
def export_csv():
    df.to_csv(f"{file_name.get()}.csv",index=False)

def export_excel():
    df.to_excel(f"{file_name.get()}.xlsx",index=False)

def export_json():
    df.to_json(f"{file_name.get()}.json",orient="split",indent=3,index=False)

def statics():
    try:
        line=stats_combo.get()
        if df[line].dtype in ['int64','float64']:
            show_data=f"""This is the first 5 row from your data:\n{df.head().to_string()}\n\nOther Information about data\n{show_in_bar()}"""
            statics.delete("1.0","end")
            statics.insert(tk.END,show_data)
            text_box2=f"\nMean:{df[line].mean()}\nMinimum:{df[line].min()}\nMax:{df[line].max()}\nSum:{df[line].sum()}\nVarience:{df[line].var()}\nStandard derivation:{df[line].std()}\n"
            text_box3=f"\nAdditional Information\nTotal Number of rows:{df[line].count()}\ndata type:{df[line].dtype}"
            statics.insert(tk.END,text_box2)
            statics.insert(tk.END,text_box3)
        else:
            messagebox.showinfo("Failed","The Given column  data in String")
    except Exception as e:
         messagebox.showinfo("Failed","Select column")
# ----------------------------------------------------------------------------------------------------
# Fronted
# Load data
# for combobox to show available tabel name
tables=pd.read_sql("show tables;",db)
tables_list = tables.iloc[:, 0].tolist()

# for window
data_page=ctk.CTkFrame(rightbar)
pages["l_file"]=data_page

# display in tree page
table_name=ctk.CTkComboBox(data_page,values=tables_list)
table_name.place(x=495,y=630)
tree=ttk.Treeview(data_page)
tree.place(x=0,y=0,height=600,width=1090)
load=ctk.CTkButton(data_page,text="Load MySQL Data",font=("Showcard Gothic",25),command=load_data)
load.place(x=445,y=660)

# load data in Excel
excel_page=ctk.CTkFrame(rightbar)
pages["ex_file"]=excel_page
ctk.CTkButton(excel_page,text="Load Excel File",command=load_data_excel,font=("Showcard Gothic",25)).place(x=445,y=660)
textwidget=tk.Text(excel_page)
textwidget.place(x=0,y=0,height=600,width=1090)

# Analysis
graph=ctk.CTkFrame(rightbar)
pages["analysis"]=graph
combo=ctk.CTkComboBox(graph,values=[])
combo.set("Select column")
combo.place(x=10,y=5)
line=ctk.CTkButton(graph,text="Line graph",command=line,font=("Showcard Gothic",18)).place(x=170,y=5)
pie=ctk.CTkButton(graph,text="Pie graph",command=pie,font=("Showcard Gothic",18)).place(x=325,y=5)
histogram=ctk.CTkButton(graph,text="Histogram graph",command=histo,font=("Showcard Gothic",18)).place(x=480,y=5)
bar=ctk.CTkButton(graph,text="Bar graph",command=bar,font=("Showcard Gothic",18)).place(x=675,y=5)
scatter=ctk.CTkButton(graph,text="Scatter plot",command=scatter,font=("Showcard Gothic",18)).place(x=325,y=60)

x_axis=ctk.CTkComboBox(graph,values=[])
x_axis.set("Select x Axis")
x_axis.place(x=10,y=60)

y_axis=ctk.CTkComboBox(graph,values=[])
y_axis.set("Select y Axis")
y_axis.place(x=170,y=60)

# text bar
text=tk.Text(graph,height=30,width=55,wrap=tk.NONE)
text.place(x=5,y=220)

# border
border=ctk.CTkFrame(graph,height=480,width=2,fg_color="grey")
border.place(x=447,y=220)

# Searching
clean=ctk.CTkFrame(rightbar)
pages["searching"]=clean
ctk.CTkLabel(clean,text="What you want ot search:",font=("Showcard Gothic",25)).pack(pady=10)
column_name=ctk.CTkComboBox(clean,values=[])
column_name.set("Choose column")
column_name.place(x=330,y=52)
inputt=ctk.CTkEntry(clean,placeholder_text="eg:1,Mobile,etc...")
inputt.pack()
search=ctk.CTkButton(clean,text="Search",font=default_font,command=search)
search.pack()

text2=tk.Text(clean,height=37,width=136,wrap=tk.NONE)
text2.pack(side="top")

cleaning_button=ctk.CTkButton(clean,text="Clean button",font=("Showcard Gothic",25))
cleaning_button.pack(side="top",pady=20)

# Edit
E=ctk.CTkFrame(rightbar)
pages["edit"]=E 
ctk.CTkLabel(E,text="Let's Edit Data(Only MySQL)",font=("Showcard Gothic",25)).pack(side="top",pady=10)

# change column name
ctk.CTkLabel(E,text="→Change Columns name:",font=default_font).place(x=10,y=45)
old_col=ctk.CTkComboBox(E,values=[])
old_col.set("Enter old column")
old_col.place(x=10,y=70)
new_col=ctk.CTkEntry(E,placeholder_text="Enter new column name")
new_col.place(x=160,y=70)
data_type=ctk.CTkComboBox(E,values=["Numeric","Alphabet"])
data_type.set("which data type contain")
data_type.place(x=310,y=70)
change_col=ctk.CTkButton(E,text="Change name",command=Change_col_nama)
change_col.place(x=150,y=110)

# change table data
ctk.CTkLabel(E,text="→Change Table data:",font=default_font).place(x=10,y=160)
new_data_column=ctk.CTkComboBox(E,values=[])
new_data_column.set("which column change")
new_data_column.place(x=10,y=190)
new_val=ctk.CTkEntry(E,placeholder_text="Enter new value")
new_val.place(x=160,y=190)
confimation_col=ctk.CTkComboBox(E,values=[])
confimation_col.set("for confirm the row")
confimation_col.place(x=10,y=230)
confirm_data=ctk.CTkEntry(E,placeholder_text="confirm the row")
confirm_data.place(x=160,y=230)
change_value=ctk.CTkButton(E,text="Change value",command=Change_table_data).place(x=160,y=270)

# display part
text3=tk.Text(E,height=44,width=68,wrap=tk.NONE)
text3.pack(side="right")

# Insight
stats=ctk.CTkFrame(rightbar)
pages["insight"]=stats
stats_combo=ctk.CTkComboBox(stats,values=[])
stats_combo.place(x=495,y=630)
ctk.CTkButton(stats,text="Load Stats",command=statics,font=("Showcard Gothic",25)).place(x=487,y=660)
statics=tk.Text(stats,wrap=tk.NONE)
statics.place(x=0,y=0,width=1087,height=600)

# Export
export=ctk.CTkFrame(rightbar)
pages["export"]=export
ctk.CTkLabel(export,text="Export",font=("Showcard Gothic",25)).pack(pady=10)
ctk.CTkLabel(export,text="Enter file name:",font=("Showcard Gothic",16)).place(x=40,y=50)
file_name=ctk.CTkEntry(export,placeholder_text="Enter file name:")
file_name.place(x=185,y=50)
csv=ctk.CTkButton(export,text="CSV",font=default_font,command=export_csv).place(x=50,y=100)
excel=ctk.CTkButton(export,text="Excel",font=default_font,command=export_excel).place(x=300,y=100)
json=ctk.CTkButton(export,text="Json",font=default_font,command=export_json).place(x=550,y=100)

# Side bar
sidebar=ctk.CTkFrame(root,width=100)
sidebar.pack(side="left",fill="y")
# tabes neme
t_names=[("MySQL","l_file"),
        ("Excel","ex_file"),
        ("Analysis","analysis"),
        ("Searching","searching"),
        ("Edit","edit"),
        ("Insight","insight"),
        ("Export","export")]

# sidebar Label
ctk.CTkLabel(sidebar,text="Advance Dashbourd",font=("Bodoni MT Black",25)).pack(pady=7,padx=10)
# sidebar tabs
for name,tab in t_names:
    ctk.CTkButton(sidebar,text=name,font=default_font,command=lambda t=tab:show_page(t)).pack(pady=7,padx=10)
show_page("insight")

# border
divider=ctk.CTkFrame(root,width=1.5,fg_color="gray")
divider.pack(side="left",fill="y")
root.protocol("WM_DELETE_WINDOW",on_close)
root.mainloop()