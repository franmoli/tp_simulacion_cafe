import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

def rotura_de_cafetera():
    #TODO: calcular probabilidad de rotura de cafetera y en caso de que rompa, actualizar var de estado
    print("Rotura de cafetera")

def llegada_de_cafe():
    #TODO: sumar a la variable de estado las cantidades pedidas 
    print("Llegó el café")

def calculo_de_ventas_diarias():
    #TODO: calcular ventas diarias y retornar valores
    print("Ventas diarias")
    return {
            "brazilian": 0,
            "columbian": 0,
            "ethiopia": 0,
            "jamaica": 0
        }

def calculo_de_perdida_de_calidad():
    #TODO: calcular perdida de calidad diaria y retornar valores
    return {
            "brazilian": 0,
            "columbian": 0,
            "ethiopia": 0,
            "jamaica": 0
        }

def llegada_de_cafetera_reparada():
    print("Llegó la cafetera reparada")
    #TODO: volver a poner la cafetera en principal
    #TODO: subir la calidad de todos los cafés

def llegada_de_servicio_tecnico():
    print("Llega el servicio tecnico a retirar la cafetera")
    #TODO: calcular el tiempo de reparacion de la cafetera y sumarlo al dia de llegada

def pedido_de_cafe():
    print("Aaa")
    #TODO: calcular el tiempo en que tarda en llegar un tecnico

#-----------------------------------------------------#
def simulacion():
    while tiempo < tiempo_final:
        #-------------avanzar tiempo en 1 dt----------
        tiempo += 1
        #-------------eventos del propio dia----------
        #calcular o usar todo lo que entra ?? creo que no va nada
       
        #calcular o usar todo lo que sale
        
        ventas_diarias = calculo_de_ventas_diarias()

        perdida_de_calidad = calculo_de_perdida_de_calidad()

        rotura_de_cafetera()

        #---------------Eventos comprometidos en dt anteriores---------------
         #si es dia de llegada -> sube stock y calidad
        if tiempo == fecha_llegada_pedido_cafe:
            llegada_de_cafe()

        #Si llega la cafetera se cambia el tipo de cafetera y sube la calidad
        if tiempo == fecha_entrega_cafetera_reparada:
            llegada_de_cafetera_reparada()
            
        #Si llegó el técnico se actualiza la fecha de llegada de la cafetera reparada
        if tiempo == fecha_llegada_servicio_tecnico:
            llegada_de_servicio_tecnico()

        #------------Actualizacion del vector de modelo de estado-----------

        #Se actualizan los vectores de estado con las ventas y calidad diarios
        for tipo, ventas in ventas_diarias.items():
            stock[tipo] -= ventas
        
        for tipo, perdida in perdida_de_calidad.items():
            stock[tipo] -= perdida

        #-----------Registro de eventos que comprometen dt futuros----------
        #Si algún café baja de los 12kg se realiza un pedido
        if any(stock < 12 for tipo, stock in stock.items()):
            pedido_de_cafe()

        #efectuar control de maxima ?? creo que no hay

    #totalizacion de resultados
    #TODO: calcular estos resultados
    prom_mensual_dias_sin_operacion = 0
    porc_mensual_cafe_vendido_en_2x1 = 0
    porc_clientes_perdidos_falta_cafe = 0
    prom_mensual_costo_por_promo = 0
    prom_mensual_gasto_electricidad = 0
    prom_mensual_calidad_cafe = {
        "brazilian": 0,
        "columbian": 0,
        "ethiopia": 0,
        "jamaica": 0
    }
    #impresion de resultados
    #TODO: imprimir esos resultados
    

#-----------------------------------------------------#
def main():
    
    global tiempo
    global tiempo_final
    global stock
    global quality
    global provider_quality
    global fecha_entrega_cafetera_reparada
    global fecha_llegada_pedido_cafe
    global fecha_llegada_servicio_tecnico
    global cafetera_en_uso
    global acum_dias_sin_cafetera
    global acum_cafe_vendido_2x1
    global acum_clientes_perdidos_sin_cafe
    global acum_costo_promociones
    global acum_calidad_promedio

    #Condiciones iniciales
    quality={
        "brazilian": 0,
        "columbian": 0,
        "ethiopia": 0,
        "jamaica": 0
    }
    stock={
        "brazilian": 12,
        "columbian": 12,
        "ethiopia": 12,
        "jamaica": 12
    }
    provider_quality={
        "brazilian": 87,
        "columbian": 91,
        "ethiopia": 85,
        "jamaica": 89
    }


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
    acum_calidad_promedio = {
        "brazilian": 0,
        "columbian": 0,
        "ethiopia": 0,
        "jamaica": 0
    }

    simulacion()

#-----------------------------------------------------#
if __name__ == "__main__":
    main()

