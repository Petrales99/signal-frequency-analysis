# -*- coding: utf-8 -*-
"""
@author: Alessio
"""

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import scipy as sci
import statistics as stat
from scipy.io import savemat
import json

data = pd.read_json("dataSetFourierPython.json")
data1 = pd.read_parquet("dataSet_Fourier.parquet")

#Per ogni porzione del segnale rettilineo si vuole osservare come le frequenze
#variano in funzione della velocità media.
#Si inizializzano i vettori utili a conservare i dati necessari per l'analisi e
#si effettua lo spettrogramma di ogni tratta dal quale prelevare le frequenze
#più
#L'analisi viene effettuata utilizzando le function del pacchetto statistics.
velRett = np.zeros([29, ])
modaRett = np.zeros([29, ])
medianaRett = np.zeros([29, ])
mediaRett = np.zeros([29, ])
varianzaRett = np.zeros([29, ])
for i in range(0, 29):
    f, t, spettrogramma = sci.signal.spectrogram(np.array(data["signalRett"][i]), fs=2000.0, window=('tukey', 0.25), nperseg=None, noverlap=None, nfft=None, detrend='constant', return_onesided=True, scaling='density', axis=0, mode='psd')
    spettrogramma=np.squeeze(spettrogramma)
    modaRett[i] = stat.mode(f[np.argmax(spettrogramma, axis=0)])
    medianaRett[i] = stat.median(f[np.argmax(spettrogramma, axis=0)])
    mediaRett[i] = stat.mean(f[np.argmax(spettrogramma, axis=0)])
    varianzaRett[i] = stat.variance(f[np.argmax(spettrogramma, axis=0)])
    velRett[i] = np.sum(data["speedRett"][i])/np.size(data["speedRett"][i])
    
# Per ogni porzione del segnale curvilineo si vuole osservare come le frequenze
#variano in funzione della velocità media.
#L'analisi viene effettuata utilizzando le function del pacchetto statistics.
velCur = np.zeros([29, ])
modaCur = np.zeros([29, ])
medianaCur = np.zeros([29, ])
mediaCur = np.zeros([29, ])
varianzaCur = np.zeros([29, ])
for i in range(0, 29):
    f, t, spettrogramma = sci.signal.spectrogram(np.array(data["signalCur"][i]), fs=2000.0, window=('tukey', 0.25), nperseg=None, noverlap=None, nfft=None, detrend='constant', return_onesided=True, scaling='density', axis=0, mode='psd')
    spettrogramma=np.squeeze(spettrogramma)
    modaCur[i] = stat.mode(f[np.argmax(spettrogramma, axis=0)])
    medianaCur[i] = stat.median(f[np.argmax(spettrogramma, axis=0)])
    mediaCur[i] = stat.mean(f[np.argmax(spettrogramma, axis=0)])
    varianzaCur[i] = stat.variance(f[np.argmax(spettrogramma, axis=0)])
    velCur[i] = np.sum(data["speedCur"][i])/np.size(data["speedCur"][i])
    
plt.figure()
plt.title('Numero Tratto vs. Moda (tratto rettilineo)')
plt.ylabel('Moda [Hz]')
plt.xlabel('Numero Tratto')
plt.plot(range(1, 30), modaRett, 'o')
#Graficando la moda delle frequenze rispetto al relativo tratto rettilineo considerato
#si può osservare che quasi in tutti i casi queste si mantengono nell'intervallo
#tra 300Hz e 350Hz


plt.figure()
plt.title('Numero Tratto vs. Moda (tratto curvilineo)')
plt.ylabel('Moda [Hz]')
plt.xlabel('Numero Tratto')
plt.plot(range(1, 30), modaCur, 'o')
#Graficando invece la moda delle frequenze rispetto al relativo tratto curvilineo
#si osserva che si mantengono nell'intervallo di frequenze tra 140Hz e 180Hz

# Per poter interpolare i dati bisogna ordinare gli array in ordine crescente
# (equivalentemente in ordine decrescente). Per fare ciò si utilizza una
# matrice di permutazione.

p = np.argsort(velRett)[::-1]  # ordine decrescente
plt.figure()
plt.title('Velocità media vs. Moda (tratto rettilineo)')
plt.ylabel('Frequenza [Hz]')
plt.xlabel('Velocità media [m/s]')
plt.plot(velRett[p], modaRett[p], 'o-')
#Osservando come la moda delle frequenze varia in funzione della velocità media
#nel caso rettilineo, è evidente che l'andamento è rettilineo, quindi
#le frequenze restano costanti.

p = np.argsort(velCur)[::-1]  # ordine decrescente
plt.figure()
plt.title('Velocità media vs. Moda (tratto curvilineo)')
plt.ylabel('Frequenza [Hz]')
plt.xlabel('Velocità media [m/s]')
plt.plot(velCur[p], modaCur[p], 'o-')
#Nel caso dei tratti curvilinei invece si può osservare che vi è una crescenza
#delle frequenze e che nella maggior parte dei casi si mantengono tra 140Hz e 180Hz

#------------------------------------------------------------------------------------

#signal= segnale da filtrare
#fs= frequenza sample (2000Hz nel nostro caso)
#lowcut-highcut estremi dell'intervallo delle frequenze da elaborare

def bandstop_filter(signal,fs,lowcut,highcut,order):
    #Il filtro bandstop attenua le frequenze all'interno dell'intervallo
    nyqs=0.5*fs
    low= lowcut/nyqs
    high=highcut/nyqs
    b,a =sci.signal.butter(order,[low,high], 'bandstop', analog=False)
    y=sci.signal.filtfilt(b,a,signal,axis=0)
    return(y)

def bandpass_filter(signal,fs,lowcut,highcut,order):
    #Il filtro bandpass attenua le frequenze fuori dall'intervallo
    nyqs=0.5*fs
    low= lowcut/nyqs
    high=highcut/nyqs
    b,a =sci.signal.butter(order,[low,high], 'bandpass', analog=False)
    y=sci.signal.filtfilt(b,a,signal,axis=0)
    return(y)

#Poniamo num=1 per plottare solamente il primo dei 29 segnali
num=1
#Si plottano i segnali mascherati di ogni tratta e si confrontano rispettivamente
#con i segnali curvilinei e rettilinei originali
for i in range(0,num):
    #Si utilizza il filtro bandpass per frequenze da 140 Hz a 160 Hz
    segnalefiltrato1=bandpass_filter(data['signalCur'][i],2000,140,160,5)
    figure, axis = plt.subplots(2, 1)

    axis[0].plot(data['signalCur'][i])
    axis[0].plot(segnalefiltrato1)
    axis[0].set_title("Segnale curvilineo mascherato (Bandpass) vs Segnale Curvilineo")

    axis[1].plot(data['signalRett'][i])
    axis[1].plot(segnalefiltrato1)
    axis[1].set_title("Segnale curvilineo mascherato (Bandpass) vs Segnale rettilineo")
    plt.tight_layout()

    #Si utilizza il filtro Bandstop per frequenze da 140 Hz a 160 Hz
    segnalefiltrato2=bandstop_filter(data['signalCur'][0],2000,140,160,5)
    figure, axis = plt.subplots(2, 1)

    axis[0].plot(data['signalCur'][i])
    axis[0].plot(segnalefiltrato2)
    axis[0].set_title("Segnale curvilineo mascherato (Bandstop) vs Segnale Curvilineo")

    axis[1].plot(data['signalRett'][i])
    axis[1].plot(segnalefiltrato2)
    axis[1].set_title("Segnale curvilineo mascherato (Bandstop) vs Segnale rettilineo")
    plt.tight_layout()
    
#Fissiamo un punto di partenza per osservare come variano le frequenze di ogni
#tratto in quel preciso punto. Indichiamo con km1 il punto di partenza, misurato in metri.
#Stiamo quindi cercando di sincronizzare i percorsi e visualizzare come variano in
#una porzione specifica.
km1 = data1.pk[0][1516+data.idxCur[0][0][0]]
ind = int(np.where(data1.pk[0] < km1)[0][-1])
figure, axis = plt.subplots(2, 1)
axis[0].plot(data1.signalCur[0][int(ind-data.idxCur[0][0][0]-500):int(ind-data.idxCur[0][0][0]+500)])
axis[0].plot(segnalefiltrato1[int(ind-data.idxCur[0][0][0]-500):int(ind-data.idxCur[0][0][0]+500)])
axis[0].set_title("Evento con filtro Bandpass")
#ind conterrà l'indice dell'inizio della
#porzione di percorso presa in considerazione a partire da km1 e per ogni tratto
#questa non è altro che il più grande valore contenuto in data1.pk (che contiene i chilometraggi
#di ogni tratto) che è più piccolo di km1.
#Dopo aver individuato l'indice di partenza per ogni tratto, si plotta la porzione
#di segnale centrata in ind e contenente 2000 dati. (Troveremo ind[s]-data.idxCur[s]
#perché data1.pk contiene il chilometraggio dell'intera tratta e non del solo tratto
#curvilineo, per questo va adattato)
axis[1].plot(data1.signalCur[0][int(ind-data.idxCur[0][0][0]-500):int(ind-data.idxCur[0][0][0]+500)])
axis[1].plot(segnalefiltrato2[int(ind-data.idxCur[0][0][0]-500):int(ind-data.idxCur[0][0][0]+500)])
axis[1].set_title("Evento con filtro Bandstop")
plt.tight_layout()
    

segnalefiltrato1=bandpass_filter(data['signalCur'][3],2000,220,260,5)
figure, axis = plt.subplots(2, 1)

axis[0].plot(data['signalCur'][3])
axis[0].plot(segnalefiltrato1)
axis[0].set_title("Segnale curvilineo mascherato (Bandpass) vs Segnale Curvilineo")

axis[1].plot(data['signalRett'][3])
axis[1].plot(segnalefiltrato1)
axis[1].set_title("Segnale curvilineo mascherato (Bandpass) vs Segnale rettilineo")
plt.tight_layout()

#------------------------------------------------------------------------------

print('RMS segnale curvilineo', np.sqrt(np.mean(np.power(data['signalCur'][0],2))) )
print('RMS segnale rettilineo', np.sqrt(np.mean(np.power(data['signalRett'][0],2))) )
print('RMS segnale curvilineo filtrato con Bandpass', np.sqrt(np.mean(np.power(bandpass_filter(data['signalCur'][0],2000,140,160,5),2))) )
print('RMS segnale curvilineo filtrato con Bandstop', np.sqrt(np.mean(np.power(bandstop_filter(data['signalCur'][0],2000,140,160,5),2))) )

print('RMS segnale curvilineo', np.sqrt(np.mean(np.power(data['signalCur'][0],2))) )
print('RMS segnale rettilineo', np.sqrt(np.mean(np.power(data['signalRett'][0],2))) )
print('RMS segnale curvilineo filtrato con Bandpass', np.sqrt(np.mean(np.power(bandpass_filter(data['signalCur'][0],2000,110,190,5),2))) )
print('RMS segnale curvilineo filtrato con Bandstop', np.sqrt(np.mean(np.power(bandstop_filter(data['signalCur'][0],2000,110,190,5),2))) )

segnalefiltrato=bandstop_filter(data['signalCur'][0],2000,110,190,5)
figure, axis = plt.subplots(2, 1)

axis[0].plot(data['signalCur'][0])
axis[0].plot(segnalefiltrato)
axis[0].set_title("Segnale curvilineo mascherato (Bandstop) vs Segnale Curvilineo")

axis[1].plot(data['signalRett'][0])
axis[1].plot(segnalefiltrato)
axis[1].set_title("Segnale curvilineo mascherato (Bandstop) vs Segnale rettilineo")
plt.tight_layout()