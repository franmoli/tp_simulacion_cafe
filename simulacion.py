import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats



def simulacion():
    while tiempo < tiempo_final:
        #-------------avanzar tiempo en 1 dt----------
        tiempo += 1
        #-------------eventos del propio dia----------
        #calcular o usar todo lo que entra ?? creo que no va nada
       
        #calcular o usar todo lo que sale
        #todos los dias -> sale stock por venta y baja calidad
        #TODO: calcular ventas diarias
        ventas_diarias = []
        #TODO: calcular perdida de calidad diaria
        perdida_de_calidad = []

        #TODO: calcular probabilidad de rotura de cafetera



        #---------------Eventos comprometidos en dt anteriores---------------
         #si es dia de llegada -> sube stock y calidad
        if tiempo == fecha_llegada_pedido_cafe:
            print("AA")
            #TODO: sumar las variables de las cantidades que pediste

        if tiempo == fecha_entrega_cafetera_reparada:
            #TODO: volver a poner la cafetera en principal

        if tiempo == fecha_llegada_servicio_tecnico:
            #TODO: calcular el tiempo de reparacion de la cafetera y sumarlo al dia de llegada


        #------------Actualizacion del vector de modelo de estado-----------
        #TODO: restar a cada estado
        stock - ventas_diarias
        quality - perdida_de_calidad

        #-----------Registro de enentos que comprometen dt futuros----------
        #efectuar control de minima
        if stock[tipo_cafe] < 12:
            print("Aaa")
            #TODO: pedir cafe
            #TODO: calcular fecha de llegada del pedido y actualizar variables

        #efectuar control de maxima ?? creo que no hay




    #totalizacion de resultados
    #impresion de resultados
    #parar



def main():
    global brazilian_stock
    global columbian_stock
    global ethiopia_stock
    global jamaica_stock
    global brazilian_quality
    global columbian_quality
    global ethiopia_quality
    global jamaica_quality
    global brazilian_provider_quality
    global columbian_provider_quality
    global ethipoa_provider_quality
    global jamaica_provider_quality
    global tiempo
    global tiempo_final
    global stock
    global quality
    global fecha_entrega_cafetera_reparada
    global fecha_llegada_pedido_cafe
    global fecha_llegada_servicio_tecnico
    global cafetera_en_uso
    global acum_dias_sin_cafetera
    global acum_calidad_promedio_bra
    global acum_calidad_poromedio_eth
    global acum_cafe_vendido_2x1
    global acum_calidad_promedio_col
    global acum_calidad_promedio_jam
    global acum_clientes_perdidos_sin_cafe
    global acum_costo_promociones

    #Condiciones iniciales
    brazilian_stock = columbian_stock = ethiopia_stock = jamaica_stock = 0
    brazilian_quality = columbian_quality = ethiopia_quality = jamaica_quality = 0

    brazilian_provider_quality = 87
    columbian_provider_quality = 91
    ethipoa_provider_quality = 85
    jamaica_provider_quality = 89

    stock = [brazilian_stock, columbian_stock, ethiopia_stock, jamaica_stock]
    quality =[brazilian_quality, columbian_quality, ethiopia_quality, jamaica_quality]

    #Cafetera en uso principal: P | secundaria: S
    cafetera_en_uso = "P"

    fecha_llegada_pedido_cafe = 0
    fecha_llegada_servicio_tecnico = 0
    fecha_entrega_cafetera_reparada = 0

    tiempo = 0
    tiempo_final = 1000000

    #vars de resultado
    acum_dias_sin_cafetera = 0
    acum_cafe_vendido_2x1 = 0
    acum_clientes_perdidos_sin_cafe = 0
    acum_costo_promociones = 0
    acum_calidad_promedio_bra = 0
    acum_calidad_promedio_col = 0
    acum_calidad_poromedio_eth = 0
    acum_calidad_promedio_jam = 0


    simulacion()


    
        


if __name__ == "__main__":
    main()

