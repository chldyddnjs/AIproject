from tkinter import Tk, ttk, Label, Button, Text, END
import json

stationfares = []
with open('stationfares.json', 'r',encoding='utf-8') as stationfares_file:
    stationfares = json.load(stationfares_file)

selected_index = 0

def stationfares_selected(event):
    global selected_index
    for item in treeStationfares.selection():
        selected_index = int(treeStationfares.item(item, "text"))
    stationfare = stationfares[selected_index]
    station = stationfare['station']
    fare = str(stationfare['fare'])
    text_Station.delete("1.0",END)
    text_Station.insert("end", station)
    text_Fare.delete("1.0",END)
    text_Fare.insert("end", fare)    

def setTreeItems():
    # 기존에 treeStationfares에 정보를 가져온 것이 있으면 모두 지워줌
    treeStationfares.delete(*treeStationfares.get_children())
    for idx, stationfare in enumerate(stationfares):
        station = stationfare['station']
        fare = stationfare['fare']
        treeStationfares.insert("", 'end', iid=None, text=str(idx), values=[station, fare])

def insert_content():
    station = text_Station.get("1.0",END)
    fare = int(text_Fare.get("1.0",END))
    stationfare = { 'station': station.rstrip(), 'fare': fare }
    stationfares.append(stationfare)
    setTreeItems()

def update_content():
    global selected_index
    station = text_Station.get("1.0",END)
    fare = int(text_Fare.get("1.0",END))
    selectedItem = stationfares[selected_index]
    selectedItem['station'] = station.rstrip()   
    selectedItem['fare'] = fare 
    setTreeItems()  

def delete_content():
    global selected_index
    stationfares.pop(selected_index)
    setTreeItems()

def save_content():
    with open('stationfares.json', 'w', encoding='UTF-8') as f:
        jsonString = json.dumps(stationfares, ensure_ascii=False)
        f.write(jsonString)
    f.close()

window = Tk()
window.title("Station Fare Management")
window.geometry("600x600")
window.resizable(0,0)
title = "정류장 요금관리"
lbl_title = Label(window,text=title,font=("돋움체",20))
lbl_title.pack(padx=5, pady=15)

# 정류장 요금관리을 표시하는 treeStationfares
treeStationfares = ttk.Treeview(window)
treeStationfares["columns"]=("station", "fare")
treeStationfares.column("#0", width=50 )
treeStationfares.column("station", width=200 )
treeStationfares.column("fare", width=150 )
# treeStationfares에는 순번, 정류장, 요금 표시
treeStationfares.heading("#0", text="순번")
treeStationfares.heading("station", text="정류장")
treeStationfares.heading("fare", text="요금")
treeStationfares.place(x = 100, y = 100, width=400, height=250 )
# 검색한 정류장 요금를 선택하면 stationfares_selected을 실행함 
treeStationfares.bind("<<TreeviewSelect>>", stationfares_selected)

btn_Insert=Button(window, text="Insert", command=insert_content, font=("돋움체",14))
btn_Insert.place(x = 100, y = 400, width=100, height=30 )

btn_Update=Button(window, text="Update", command=update_content, font=("돋움체",14))
btn_Update.place(x = 200, y = 400, width=100, height=30 )

btn_Delete=Button(window, text="Delete", command=delete_content, font=("돋움체",14))
btn_Delete.place(x = 300, y = 400, width=100, height=30 )

btn_Save=Button(window, text="Save", command=save_content, font=("돋움체",14))
btn_Save.place(x = 400, y = 400, width=100, height=30 )

labelStation = Label(window, text="정류장")
labelStation.place(x = 100, y = 450, width=50, height=25 )
labelFare = Label(window, text="요금")
labelFare.place(x = 100, y = 500, width=50, height=25 )
text_Station = Text(window, width=30, height=1)
text_Station.place(x = 200, y = 450)
text_Fare = Text(window, width=30, height=1)
text_Fare.place(x = 200, y = 500)

# treeStationfares 초기입력
setTreeItems()

window.mainloop()