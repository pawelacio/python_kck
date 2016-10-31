import matplotlib.pyplot as plt
import numpy as np

#funkcja wczytujaca z plikow i liczaca sredni czas dla kazdej generacji
def wczytaj_srednie_czasy(nazwa_pliku):
    czasy = []
    with open(nazwa_pliku) as f:
        for j, line in enumerate(f):
            if j > 0:
                helparr = line.split(',')
                for i, a in enumerate(helparr):
                    if i == 2:
                        suma = float(a)
                    if i > 2:
                        suma = suma + float(a)
                czasy.append((suma/32)*100)
    return czasy

#funkcja wczytujaca drugie kolumny plikow czyli rozegrane gry
def wczytaj_gry(nazwa_pliku):
    roz_gry = []
    with open(nazwa_pliku) as f:
        for j, line in enumerate(f):
            if j > 0:
                helparr = line.split(',')
                for i, a in enumerate(helparr):
                    if i == 1:
                        roz_gry.append(int(a))
    return roz_gry

#funkcja wczytujaca dane z wszystkich podanych plikow
# w celu prezentacji ich w boxplocie
def wczytaj_dane_boxplot(pliki):
    for plik in pliki:
        with open(plik) as f:
            lines = f.readlines()
        # print(lines[-1])
        helparr = lines[-1].split(',')
        for i in range(len(helparr)):
            helparr[i] = float(helparr[i])*100
        data.append(helparr[2:])
    return data

#stworzenie tablicy z nazwami plikow oraz etykietami i znacznikami na wykresie
data_arr = [['rsel.csv', 'cel-rs.csv', '2cel-rs.csv', 'cel.csv', '2cel.csv'],['1-Evol-RS','1-Coev-RS','2-Coev-RS','1-Coev','2-Coev'],['o','v','D','s','d']]
data = []

plt.subplot(121) # pierwszy subplot
plt.grid() #nakladam sietke
#ustawienie etykiet osi
plt.ylabel('Odsetek wygranych gier [%]')
plt.xlabel('Rozegranych gier (x1000)')
#zakres osi x
plt.xlim(0,500)
# tworzene osi rowniez u gory
plt.twiny()
plt.xlabel("Pokolenie")
plt.xlim(0,500)
#wczytanie gier
roz_gry = wczytaj_gry('2cel-rs.csv')
#podzielenie wszystkich wartosci przez 1000 w celu
# aby toprowadzic do odpowiednich jednostek
for i in range(len(roz_gry)):
    roz_gry[i] = roz_gry[i]/1000

# wykonanie funkcji plot dla kazdego z plikow z danymy
for i in range(len(data_arr[0])):
    plt.plot(roz_gry, wczytaj_srednie_czasy(data_arr[0][i]), label=data_arr[1][i], marker=data_arr[2][i], markevery=25)
#dodanie legendy do wykresy liniowego
plt.legend(loc='lower right')

ax = plt.subplot(122)#drugi subplot
#wczytanie danych do boxplota
boxdata = wczytaj_dane_boxplot(data_arr[0])
#etykiety do wykresu
boxlab = data_arr[1]
#nalozenie siatki
plt.grid()
#slownik - kropki o kolorze niebieskim
boxplot_dots = dict(marker='o', markerfacecolor='blue')
#utworzenie wykresu
plt.boxplot(boxdata, labels=boxlab, notch=True, showmeans=True, meanprops=boxplot_dots)
#okreslenie zakresu na osi y
plt.ylim(60,100)
# obrot etyket poszczegolnych blokow
ax.set_xticklabels(ax.get_xticklabels(),rotation=15)
#przeniesienie osi y na prawa strone
ax.yaxis.tick_right()
#zapisanie wykresow
plt.savefig('wykresy.pdf')
#pokazanie wykresow
plt.show()
