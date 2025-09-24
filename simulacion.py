import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
from scipy import stats
from pprint import pprint

#-----------------------------------------------------#

def rotura_de_cafetera():
    prob_falla = random.random()

    if cafetera == "LUNA" and prob_falla <= 0.0015:
        print("Falló la cafetera")
        llegada_de_servicio_tecnico()
    elif cafetera == "NEO" and prob_falla <= 0.001:
        print("Falló la cafetera")
        llegada_de_servicio_tecnico()
    elif cafetera == "SATURNO" and prob_falla <= 0.0008:
        print("Falló la cafetera")
        llegada_de_servicio_tecnico()

def llegada_de_cafe():
    #TODO: sumar a la variable de estado las cantidades pedidas 
    print("Llegó el café")

def calcular_cafe_vendido_segun_fdp(fdp):
    return fdp["distribucion"].rvs(**fdp["args"])

def calculo_de_ventas_diarias():
    print("Ventas diarias")

    ventas_del_dia = {
            "brazilian": 0,
            "columbian": 0,
            "ethiopia": 0,
            "jamaica": 0
        }

    fdps_por_tipo_cafe = {
            "brazilian": {
                "distribucion": stats.gompertz,
                "args": {  

                    'c': 3.469448137457656,
                    'loc': 0.9999999999220399,
                    'scale': 20.75482845260361
                }
            },
            "columbian": {
                "distribucion": stats.mielke,
                "args": {   
                    'k': 0.8215669903417332,
                    's': 2.9968417938323064,
                    'loc': 0.9999999999999999,
                    'scale': 7.821896828095555
                }
            },
            "ethiopia": {
                "distribucion": stats.gompertz,
                "args": {   
                    'c': 3.2584654268287254,
                    'loc': 0.9999999999466094,
                    'scale': 20.519405815512926
                }
            },
            "jamaica": {
                "distribucion": stats.exponpow,
                "args": {   
                    'b': 0.6776736215652588,
                    'loc': 0.9999999999999998,
                    'scale': 8.100892711284596
                }
            }
        }
    
    #fdp de cada tipo de cafe, en ventas por hora, se debe calcular por las horas de trabajo diarias
    for i in range(horas_de_trabajo_diarias):
        for tipo_cafe, fdp in fdps_por_tipo_cafe.items():
            ventas = calcular_cafe_vendido_segun_fdp(fdp)
            ventas_del_dia[tipo_cafe] += round(ventas)


    print("Las ventas hoy fueron")
    pprint(ventas_del_dia)
    return ventas_del_dia

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
    print("Llegó el servicio tecnico a retirar la cafetera")
    
    fecha_entrega_cafetera_reparada = tiempo + stats.rdist.rvs(**{
        'c': 1.1362268006606664,
        'loc': 0.10017320659825403,
        'scale': 4.899826793401747
    })

    cafetera_en_uso = "S"

def pedido_de_cafe():
    print("Aaa")
    #TODO: calcular el tiempo en que tarda en llegar un tecnico

#-----------------------------------------------------#
def simulacion():
    
    global tiempo
    global tiempo_final
    global fecha_llegada_pedido_cafe
    global fecha_entrega_cafetera_reparada
    global fecha_llegada_servicio_tecnico
    global stock
    global quality


    while tiempo < tiempo_final:
        #-------------avanzar tiempo en 1 dt----------
        tiempo += 1
        #-------------eventos del propio dia----------
        #calcular o usar todo lo que entra ?? creo que no va nada
        
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
            quality[tipo] -= perdida

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

    global cafetera
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
    global horas_de_trabajo_diarias

    #Control

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
    cafetera = "LUNA" #LUNA, NEO, SATURNO

    horas_de_trabajo_diarias = 12


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

