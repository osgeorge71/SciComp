import matplotlib.pyplot as plt
from scipy import constants # type: ignore
import numpy as np
import multiprocessing as mp
import time

class Funcion():
    #-Definición de constantes para la función*
    Me = 0.510998950 #Masa del electrón en MeV
    Mp = 938.272088  #Masa del protón en MeV
    Mn = 939.565420  #Masa del neutrón en MeV
    gw = 0.653 #Weak coupling constant
    Mw = 80.379 * 1000 #Masa del bosón W+- por 1000 para MeV
    hBar = 6.582119514e-22

    def __init__(self):
        self.dif_Mnp = self.Mn - self.Mp  #Diferencia Mn - Mp
        self.factorAmplitud = (1/(np.power(np.pi,3)*self.hBar)) * np.power(self.gw/(2*self.Mw),4)

    def f(self, x):
        return self.factorAmplitud * x * np.sqrt(np.power(x,2)-np.power(self.Me,2))*np.power(self.dif_Mnp-x,2)
    
    def graficar(self, x1, x2, tamPaso):
        #Componer muestras en la abscisa
        E = np.arange(x1,x2,tamPaso) #Iterar en tamaño de paso
        #Componer muestras en la ordenada
        dFdE_f = self.f(E)
        #-Graficar*
        plt.plot(E,dFdE_f)
        plt.show()

class Montecarlo():
    def __init__(self):
        pass

    def calcIntegral(self,f,x1,x2,nSamples):
        sum = 0.0
        xr = np.random.uniform(x1,x2,nSamples)
        for i in range(nSamples):
            sum += f(xr[i])
        return (sum/nSamples)*(x2-x1)

def main():
    #Intervalo de trabajo para la función particular
    x1 = 0.511
    x2 = 1.29
    tamPaso = 1e-6
    funcion = Funcion() #Instanciar el objeto función
    #funcion.graficar(x1,x2,tamPaso)
    
    #Constantes que maneja Griffiths
    factor1 = 1/(4*constants.pi**3*6.58212e-22)
    factor2 = (funcion.gw / (2*80423))**4
    factor3 = 0.5109989**5
    factor4 = 6.54438 #Término del extremo derecho de la integral resuelta
    #Calcular el resultado de la integral
    resultadoGriffiths = factor1*factor2*factor3*factor4
    
    #Constantes actualizadas desde el PDG
    factor1 = 1/(4*constants.pi**3*funcion.hBar)
    factor2 = (funcion.gw / (2*funcion.Mw))**4
    factor3 = funcion.Me**5
    #Calcular el resultado de la integral
    resultadoSoftware = factor1*factor2*factor3*factor4
    
    print("cálculo final del libro de Griffiths: ", resultadoGriffiths,", tao =",1.0/resultadoGriffiths)
    print("cálculo final constantes actuales: ", resultadoSoftware,", tao =",1.0/resultadoSoftware)
    
    #Organizando para llamar muchas veces el proceso global
    lstTiemposSeriales=[]
    lstTiemposParalelo=[]
    lstNumSamples = [i for i in range(100000,1100000,200000)] #25 items
    for nSamples in lstNumSamples:
        #Llamado al método de la clase para calcular integral con Montecarlo
        # nSamples = 500000    #Fijando el número de muestras 
        mc = Montecarlo() #Instanciación de la clase en el objeto mc
        #-----------------------------------------------------------------------
        print("Ejecutar proceso serialmente")
        tic = time.time()
        Gamma = mc.calcIntegral(funcion.f,x1,x2,nSamples)
        tac = time.time()
        print("Cálculo obtenido con Montecarlo: ", Gamma)
        print("Tiempo de vida = 1/Gamma =", 1.0/Gamma, "contra",1.0/resultadoSoftware,"de la ref. con constantes actualizadas.")
        print("proceso completado en",tac-tic,"segundos")
        lstTiemposSeriales.append(tac-tic)
        #-----------------------------------------------------------------------
        print("Ahora para ejecutar en paralelo")
        div = (x2-x1)/10.0  #Se eligen 10 sub-intervalos
        nSamples = int(nSamples/10);
        subInterv = [i for i in np.arange(0.511,1.29,div)]    
        tic = time.time()
        pool = mp.Pool(mp.cpu_count())
        lstParall=[pool.apply_async(mc.calcIntegral,args=(funcion.f,xx,xx+div,nSamples,)) for xx in subInterv]
        pool.close()
        pool.join()
        tac = time.time()
        results = [r.get() for r in lstParall]
        Gamma = np.sum(results)
        print("proceso completado en",tac-tic,"segundos")
        lstTiemposParalelo.append(tac-tic)
        print("Cálculo obtenido con Montecarlo: ", Gamma)
        print("Tiempo de vida = 1/Gamma =", 1.0/Gamma, "contra",1.0/resultadoSoftware,"de la ref. con constantes actualizadas.")
    #Imprimiento los resultados de tiempos
    print(lstTiemposSeriales)
    print(lstTiemposParalelo)
    plt.plot(lstNumSamples,lstTiemposSeriales,label='serie')
    plt.plot(lstNumSamples,lstTiemposParalelo,label='paralelo')
    labelsX = ['{:.0e}'.format(n) for n in lstNumSamples]
    plt.xlabel('muestras')
    plt.ylabel('segundos')
    plt.xticks(lstNumSamples, labelsX)
    plt.legend(fancybox=True)
    plt.show()
    #Guardar las listas en archivos de texto
    np.savetxt('nMuestras02.txt', lstNumSamples, delimiter=';')
    np.savetxt('nMSerials02.txt', lstTiemposSeriales, delimiter=';')
    np.savetxt('nMParalel02.txt', lstTiemposParalelo, delimiter=';')
    
if __name__ == "__main__":
    main()