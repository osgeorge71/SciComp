import numpy as np
import multiprocessing as mp
import time
#print("Número de procesadores: ", mp.cpu_count())

#Llenar una lista con valores, proceso apoyado con un for
# lst = [0 for i in range(5)] #-devuelve--> [0,0,0,0,0]
# print(lst)
# lst = [i for i in range(5)] #-devuelve--> [0,1,2,3,4]
# print(lst)

#Varios argumentos
# def test_var_args(f_arg, *argv):
#     print("primer argumento normal:", f_arg)
#     for arg in argv:
#         print("argumentos de *argv:", arg)

# test_var_args('python', 'foo', 'bar')

#Manejo de argumentos con nombre
# def saludame(**kwargs):
#     for key, value in kwargs.items():
#         print(key,value)

# saludame(nombre="abc", tel="123")

#funciones como parámetros
def seno(x1,x2):
    acum=0.0
    for x in range(x1,x2):
        acum+=np.sin(x)
    return acum

# def coseno(x):
#     return np.cos(x)

# def ejecutarFuncion(func, *args):
#     #opcional
#     #for arg in args:
#     return(func(args))

#print(ejecutarFuncion(coseno,0))

def main():
    print("Ejecutar proceso serialmente")
    tic = time.time()
    argSin = [i*100000 for i in range(10)]
    print(argSin)
    #argSin = [i*np.pi/2.0 for i in range(10000000)]
    lstSerial = [seno(x,x+99999) for x in argSin]
    tac = time.time()
    print("proceso completado en",tac-tic,"segundos")
    #print(lstSerial)
    print("Ahora para ejecutar en paralelo")
    tic = time.time()
    pool = mp.Pool(mp.cpu_count())
    lstParall=[pool.apply_async(seno,args=(xx,xx+99999,)) for xx in argSin]
    pool.close()
    pool.join()
    tac = time.time()
    results = [r.get() for r in lstParall]
    print("proceso completado en",tac-tic,"segundos")
    #print(results)
    #print(lst[0].get())
    if set(lstSerial) == set(results):
        print("las listas son iguales")
        
if __name__ == "__main__":
    main()
