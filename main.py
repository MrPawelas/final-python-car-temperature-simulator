import tkinter as tk
import time
import  matplotlib
from PIL import ImageTk, Image
matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import calculations
def get_data(entry, backend):

    backend.mass=float(entry[0].get())
    backend.surfaceOfCar= float(entry[1].get())
    backend.powerOfHeater= float(entry[2].get())
    backend.airTemp = float(entry[3].get()) + 273.15
    backend.desiredTemp = float(entry[4].get()) + 273.15
    backend.thickness=float(entry[5].get())
    backend.isStarted+=1 #czy wcisnieto przycisk danych

def update_time(backend,start_time):

    if (backend.isStarted==0):
        start_time=time.time()
    else:
        current_time = int(time.time() - start_time)
        backend.times.append(current_time)
        label2['text'] = "Upłynęło {0} sekund".format(current_time)
    root.after(1000, update_time,backend,start_time)


def show_temperature(Backend):
    if Backend.isStarted == 1:
        Backend.carTemp = Backend.airTemp
        Backend.isStarted+=1
    if Backend.isStarted >= 1:
        message = Backend.calculate(1) -273.15
        Backend.actualTemperatures.append(message)
        Backend.desiredTemperatures.append(Backend.desiredTemp-273.15)
        label3['text'] = "Temperatura w samochodzie: "+str(round(message,3)) +" C"

        label4['text'] = "Klimatyzator wykonał łącznie: " + str(int(Backend.allWorkOfHeater/1000)) + "KJ pracy"

    root.after(1000,show_temperature,Backend)


def update_car():
    if Backend.isStarted >=1:
        temerature = Backend.carTemp-273.15
        temerature = min(35,max(temerature,10))

        print(((int(255*(temerature/35)),50,int(255*(45 - temerature)/35))))
        print(str(temerature//35))
        for (x, y) in pixels:
            image.putpixel((x, y), (int(255*temerature//35),50,int(255*(35 - temerature)//35)))

        img1= ImageTk.PhotoImage(image)
        panel.configure(image=img1)
        panel.image = img1
        panel.place(rely=0.375)
    root.after(1000,update_car)




def right_pixels(pixels):
    width, height = image.size
    for x in range(width):
        for y in range(height):
            current_pixel = image.getpixel((x, y))
            if current_pixel[0] >= 150 and current_pixel[1] < 150 and current_pixel[2] < 150:
               pixels.append((x,y))


def finish():
    plotWindow = tk.Toplevel(root)
    plotWindow.title('Plots')
    plotWindow.withdraw()

    f = Figure(figsize=(5, 5))
    a = f.add_subplot(111)
    a.plot(Backend.times, Backend.actualTemperatures, label ="temperatura w samochodzie",color ='r')
    a.legend(loc="upper right")
    b= f.add_subplot(111)
    b.plot(Backend.times,Backend.desiredTemperatures, label = "pożądana temperatura")
    b.legend(loc="upper right")

    dataPlot = FigureCanvasTkAgg(f, master=plotWindow)
    dataPlot.get_tk_widget().pack(expand=1)


    plotWindow.deiconify()



Backend = calculations.backend(0, 0, 0, 0, 0, 293.15)
HEIGHT = 900
WIDTH = 800

root = tk.Tk()
 # hide lab window

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH, bg="azure")

canvas.pack()



################LEWY FRAME
frame1 = tk.Frame(root, bg='alice blue')
frame1.place(relx=0, rely=0.1, relwidth=0.4, relheight=0.8)

button = tk.Button(frame1, text="Zatwierdź dane", command=lambda: get_data([i for i in data_entry],Backend))
button.pack()
data_entry = [tk.Entry(frame1, bg='LightSkyBlue2',) for _ in range(6)]
default_values = [1500,36, 400000,31,23,0.05]

for i, x in enumerate(data_entry):
    x.place(rely=0.2 + 0.15 * i, relx=0.5, anchor=tk.CENTER)
    x.insert(i,default_values[i])
data_names = ["Masa Samochodu[kg]", "Pole Powierzchni Samochodu[m^2]", "Maksymalna moc klimatyzacji[W/t]",
              "Temperatura Powietrza[C]", "Tempetatura docelowa[C]", "Grubość blachy samochodu[m]"]
data_lables = [tk.Label(frame1, text=data_names[i], bg='powder blue') for i in range(6)]

for i, x in enumerate(data_lables):
    x.place(rely=0.15 + 0.15 * i, relx=0.5, anchor=tk.CENTER)
################# LEWY FRAME


#################PRAWY FRAME

frame2 = tk.Frame(root, bg='alice blue')
frame2.place(relx=0.55, rely=0.1, relwidth=0.35, relheight=0.5)



label2 = tk.Label(frame2,text = "Upłynęło 0 sekund",bg='cornflower blue')
label2.place(rely=0.8, relx=0.5, anchor=tk.CENTER)

label3 = tk.Label(frame2,text = "0",bg='cornflower blue')
label3['text'] = "Temperatura w samochodzie: " + str(round(0, 3)) + " C"

label3.place(rely=0.1, relx=0.5, anchor=tk.CENTER)

label4 = tk.Label(frame2,text = "Klimatyzator wykonał łącznie 0 KJ pracy",bg='cornflower blue')
label4.place(rely=0.9, relx=0.5,anchor=tk.CENTER)


frame3 = tk.Frame(root, bg='azure')
frame3.place(relx=0.55, rely=0.8,relheight=0.2,relwidth=0.35)
button = tk.Button(frame3, text="Zakończ i wygneruj wykres", command=finish)
button.pack()



image = Image.open("venv/nowe.jpg")
root.update()
new_size = (frame2.winfo_width(),frame2.winfo_height()//4)
print(new_size)
image = image.resize(new_size)
img = ImageTk.PhotoImage(image)

panel=tk.Label(frame2,image=img,anchor=tk.CENTER)
panel.place(rely = 0.375)
pixels = []
right_pixels(pixels)



start_time = time.time()
update_time(Backend,start_time)
show_temperature(Backend)
update_car()
root.mainloop()
