import cv2
import pandas as pd
import time as t
import warnings
import PySimpleGUI as sg

from Final_Project import Final_Project

layout_1=[[sg.Push(),sg.Image(None,size=(10,10),tooltip='Jai Balayyaa',key='-CV-'),sg.Push()],[sg.HSeparator()],[sg.Push(),sg.Button("START",key='-start-'),sg.Button("STOP",key='-stop-'),sg.Push()]]
window=sg.Window("Demo",layout_1,resizable=True).Finalize()
window.maximize()
warnings.filterwarnings("ignore")

obj=Final_Project()
cap = cv2.VideoCapture(0)
success=True

trigger=0
l = []
prev = []
curr = []
d = dict()
#df = pd.read_csv('obj_time.csv',index_col=0)
df = pd.DataFrame(columns={"label","time"})
#df = df.iloc[0:0,:]
time_list = []
while success:
    event, values = window.read(timeout=10)
    
    aaaa = t.time()
    success,img = cap.read()
    #img=cv2.imread('test.png')
    
    if event == sg.WIN_CLOSED:
        for i in prev:
            print(curr,prev)
            if i in curr:
                df2 = {'label':i,'time':d[i]*avg}
                df = df.append(df2,ignore_index=True)
                print(df)
                d.pop(i)
        break
        
    if event== "-start-":
        trigger=1

    if trigger==1 :
        
        f,s=obj.run(img)
        for i in s:
            if i in prev:
                curr.append(i)
                d[i]+=1
            else:
                curr.append(i)
                d[i]=1
        for i in prev:
            if i in curr:
                pass
            else:
                df2 = {'label':i,'time':d[i]*avg}
                df = df.append(df2,ignore_index=True)
                d.pop(i)
        #print(prev,curr,d)

        time_list.append(t.time()-aaaa)
        avg = sum(time_list)/len(time_list)
        
        image=f
        imgbytes = cv2.imencode('.png',image)[1].tobytes()
        
        window['-CV-'].update(data=imgbytes)
    else:
        imgbytes = cv2.imencode('.png',img)[1].tobytes()
        window['-CV-'].update(data=imgbytes)
        
    if event == "-stop-":
        trigger=0
        for i in prev:
            print(curr,prev)
            if i in curr:
                df2 = {'label':i,'time':d[i]*avg}
                df = df.append(df2,ignore_index=True)
                print(df)
                d.pop(i)
    
    prev = curr
    curr = []
df.to_csv('obj_time.csv')
import matplotlib.pyplot as plt
import pandas as pd
data = pd.read_csv('obj_time.csv')
df = pd.DataFrame(data)
Y = list(df.iloc[:, 0])
X = list(df.iloc[:, 1])
# Plot the data using bar() method
print(X,Y)

plt.plot(X, Y, color = 'g',marker = 'o',label = "Screen Presence Time")
#plt.scatter(X,Y, color = 'g',s = 100)

plt.xticks(rotation = 25)
plt.xlabel('Objects')
plt.ylabel('Time')
plt.grid()
plt.legend()
plt.show()
cap.release()
window.close()
