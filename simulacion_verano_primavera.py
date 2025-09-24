import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
from scipy import stats
from pprint import pprint
import math

#-----------------------------------------------------#
def pedido_de_cafe():
    global fecha_llegada_pedido_cafe
    global stock
    global tiempo
    global ultimo_pedido_cafe
    global pedido_de_cafe_completo
    global pedido_de_cafe_reducido
    global tiempo_final
    
    aux_pedido = False

    if fecha_llegada_pedido_cafe == tiempo_final:
        #Calculo el tamaño de pedido
        #pprint(stock)
        for tipo_cafe, stock_cafe in stock.items():
            if stock_cafe < 10000:
                #print("Pedí café: " + tipo_cafe)
                ultimo_pedido_cafe[tipo_cafe] = pedido_de_cafe_completo
                aux_pedido = True
            else:
                #print("Pedí reducido: " + tipo_cafe)
                ultimo_pedido_cafe[tipo_cafe] = pedido_de_cafe_reducido
                aux_pedido = True
    
    if aux_pedido:
        #Calculo la fecha de llegada del pedido
        fecha_llegada_pedido_cafe = tiempo + random.randint(2, 6)
        #print("Se realizó un pedido de café. Llega: " + str(fecha_llegada_pedido_cafe))

def llegada_de_cafe():
    global fecha_llegada_pedido_cafe
    global stock
    global ultimo_pedido_cafe
    global tiempo
    global tiempo_final
    global quality
    global provider_quality

    #print("Llegó el café (día " + str(tiempo) + ")")
    for tipo_cafe_pedido, cantidad_pedido in ultimo_pedido_cafe.items():
        #print("Nueva qualy: " + str((quality[tipo_cafe_pedido] * stock[tipo_cafe_pedido] + provider_quality[tipo_cafe_pedido] * cantidad_pedido) / (stock[tipo_cafe_pedido] + cantidad_pedido)))
        #print(tipo_cafe_pedido)
        #print("Cantidad pedida: " + str(cantidad_pedido))
        #print("Quali del pedido: " + str(provider_quality[tipo_cafe_pedido]))
        #print("Vieja qualy:" + str(quality[tipo_cafe_pedido]))
        #print("Vieja cant: " + str(stock[tipo_cafe_pedido]))
        nueva_qualy = (quality[tipo_cafe_pedido] * stock[tipo_cafe_pedido] + provider_quality[tipo_cafe_pedido] * cantidad_pedido) / (stock[tipo_cafe_pedido] + cantidad_pedido)
        #print(nueva_qualy - quality[tipo_cafe_pedido])
        quality[tipo_cafe_pedido] = nueva_qualy
        stock[tipo_cafe_pedido] += cantidad_pedido

    fecha_llegada_pedido_cafe = tiempo_final

def calcular_cafe_vendido_segun_fdp(fdp):
    return fdp["distribucion"].rvs(**fdp["args"])

def calculo_de_ventas_diarias():
    #print("Ventas diarias")

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
            

    #print("Las ventas hoy fueron")
    #pprint(ventas_del_dia)
    return ventas_del_dia

def calculo_disminucion_calidad(q0):
    global temperatura_ambiente_seteada
    t = temperatura_ambiente_seteada + 273.15
    k = math.exp(-3412.7 * (1/t) + 6.007)
    return q0 * math.exp(-k)
    
def estimar_perdida_de_calidad():
    global quality
    perdidas_de_calidad = {
            "brazilian": 0,
            "columbian": 0,
            "ethiopia": 0,
            "jamaica": 0
        }
    for tipo, calidad in quality.items():
        perdidas_de_calidad[tipo] += calidad - calculo_disminucion_calidad(calidad)

    #print("hoy se perdio de calidad")
    #pprint(perdidas_de_calidad)
    return perdidas_de_calidad

def rotura_de_cafetera():
    global cafetera_en_uso
    global cafetera_seleccionada

    prob_falla = random.random()
    #print("Prob falla: " + str(prob_falla))
    #print("Resultado: " + str(prob_falla <= cafetera_seleccionada["probabilidad_de_falla"]))
    if prob_falla <= cafetera_seleccionada["probabilidad_de_falla"]:
        #print("Falló la cafetera")
        cafetera_en_uso = "S"
        llegada_de_servicio_tecnico()

def llegada_de_servicio_tecnico():
    global fecha_entrega_cafetera_reparada
    global tiempo
    duracion_de_la_reparacion = round(stats.rdist.rvs(c=1.1362268006606664, loc=0.10017320659825403, scale=4.899826793401747))
    #print("Duración de la reparación: " + str(duracion_de_la_reparacion))
    fecha_entrega_cafetera_reparada = tiempo + (duracion_de_la_reparacion if duracion_de_la_reparacion > 0 else 1)
    #print("Fecha actual: " + str(tiempo))
    #print("Fecha de entrega de la cafetera: " + str(fecha_entrega_cafetera_reparada))

def llegada_de_cafetera_reparada():
    global cafetera_en_uso
    global fecha_entrega_cafetera_reparada
    global tiempo_final

    cafetera_en_uso = "P"
    fecha_entrega_cafetera_reparada = tiempo_final

def estimar_consumo_aire_acondicionado():
    global temperatura_ambiente_seteada
    temperatura_exterior = stats.gompertz.rvs(c=0.034854492527651965, loc = 7.999999949139289, scale = 4.540761573324662)
    #print("Temperatura exterior: " + str(temperatura_exterior))
    #print("Diferencia de temperatura: " + str(abs(temperatura_ambiente_seteada - temperatura_exterior)))
    #print("Watts: " + str(300 * abs(temperatura_ambiente_seteada - temperatura_exterior)))
    return 1.5 * 30 * abs(temperatura_ambiente_seteada - temperatura_exterior)

#-----------------------------------------------------#
def simulacion():
    
    global tiempo
    global tiempo_final
    global fecha_llegada_pedido_cafe
    global fecha_entrega_cafetera_reparada
    global stock
    global quality
    global acum_dias_sin_cafetera
    global acum_gasto_electricidad
    global acum_cafe_vendido_2x1
    global acum_clientes_perdidos_sin_cafe
    global acum_costo_promociones
    global acum_calidad_promedio
    global ventas_totales
    global dias_al_mes_de_promo
    global dias_restantes_de_promo
    global prob_tamanio_vaso_chico
    global prob_tamanio_vaso_mediano
    global prob_tamanio_vaso_grande
    global grs_tamanio_vaso_chico
    global grs_tamanio_vaso_mediano
    global grs_tamanio_vaso_grande
    global costo_cafe
    global cafetera_en_uso
    global cafetera_seleccionada

    acum_temp_dias_de_promo = 0
    while tiempo < tiempo_final:
        #-------------avanzar tiempo en 1 dt----------
        tiempo += 1
        #-------------eventos del propio dia----------
        if tiempo % 30 == 0:
            dias_restantes_de_promo = dias_al_mes_de_promo

        ventas_diarias = calculo_de_ventas_diarias()

        perdidas_de_calidad = estimar_perdida_de_calidad()

        #---------------Eventos comprometidos en dt anteriores---------------
        #si es dia de llegada -> sube stock y calidad
        #print("Tiempo: " + str(tiempo))
        #print("Fecha de llegada de pedido de cafe: " + str(fecha_llegada_pedido_cafe))
        #print("Resultado: " + str(tiempo == fecha_llegada_pedido_cafe))
        if tiempo == fecha_llegada_pedido_cafe:
            llegada_de_cafe()

        #Si llega la cafetera se cambia el tipo de cafetera y sube la calidad
        if tiempo == fecha_entrega_cafetera_reparada:
            llegada_de_cafetera_reparada()

        if cafetera_en_uso == "S":
            #print("La cafetera en uso es S")
            acum_dias_sin_cafetera += 1
            

        #------------Actualizacion del vector de modelo de estado-----------

        #Se actualizan los vectores de estado con las ventas y calidad diarios
        for tipo, ventas in ventas_diarias.items():
            
            while ventas > 0:
                probabilidad_tamanio_vaso = random.random()
                if probabilidad_tamanio_vaso < prob_tamanio_vaso_chico:
                    gramos_de_la_venta = grs_tamanio_vaso_chico
                elif probabilidad_tamanio_vaso < prob_tamanio_vaso_mediano:
                    gramos_de_la_venta = grs_tamanio_vaso_mediano
                else:
                    gramos_de_la_venta = grs_tamanio_vaso_grande

                #print("gramos vendidos: " + str(gramos_de_la_venta))
                #print("ventas totales: " + str(ventas))
                #print("El stock alcanza para: " + str(stock[tipo] / gramos_de_la_venta * ventas) + " dias")

                probabilidad_acepta_promo = 1
                if dias_restantes_de_promo > 0:
                    probabilidad_acepta_promo = random.random()
                    gramos_de_la_venta * (2 if probabilidad_acepta_promo < 0.7 else 1)
                if stock[tipo] >= gramos_de_la_venta:
                    stock[tipo] -= gramos_de_la_venta
                    ventas_totales += 1
                    acum_cafe_vendido_2x1 += (1 if probabilidad_acepta_promo < 0.7 else 0)
                    #print("Grs vendidos: " + str(gramos_de_la_venta))
                    #print("Costo por gramo: " + str(costo_cafe[tipo] / 1000))
                    #print("Costo calculado: " + str(((costo_cafe[tipo]*(gramos_de_la_venta/2))/1000)))
                    acum_costo_promociones += (((costo_cafe[tipo]*(gramos_de_la_venta/2))/1000) if probabilidad_acepta_promo < 0.7 else 0)
                else:
                    acum_clientes_perdidos_sin_cafe += 1
                ventas -= 1
        
        for tipo, perdida in perdidas_de_calidad.items():
            quality[tipo] -= perdida
            #print("New qualy :" + tipo + " " + str(quality[tipo]))

        acum_gasto_electricidad += estimar_consumo_aire_acondicionado() * 1230 #$1230 precio estimado del W en Edesur

        for tipo, _ in acum_calidad_promedio.items():
            
            acum_calidad_promedio[tipo] += quality[tipo] - (10 if cafetera_en_uso == "S" else cafetera_seleccionada["disminucion_calidad"])

        if dias_restantes_de_promo > 0:
            acum_temp_dias_de_promo += 1

        dias_restantes_de_promo -= 1



        #-----------Registro de eventos que comprometen dt futuros----------
        #Si algún café baja de los 12kg se realiza un pedido
        pedido_de_cafe()

        rotura_de_cafetera()

    # Cálculo de resultados
    prom_mensual_dias_sin_operacion = (acum_dias_sin_cafetera / tiempo_final) * 30
    porc_mensual_cafe_vendido_en_2x1 = (acum_cafe_vendido_2x1 / ventas_totales) * 100
    porc_clientes_perdidos_falta_cafe = (acum_clientes_perdidos_sin_cafe / ventas_totales) * 100
    prom_mensual_costo_por_promo = (acum_costo_promociones / tiempo_final) * 30
    prom_mensual_gasto_electricidad = (acum_gasto_electricidad / tiempo_final) * 30
    
    prom_mensual_calidad_cafe = {
        "brazilian": (acum_calidad_promedio["brazilian"] / tiempo_final),
        "columbian": (acum_calidad_promedio["columbian"] /tiempo_final),
        "ethiopia": (acum_calidad_promedio["ethiopia"] / tiempo_final),
        "jamaica": (acum_calidad_promedio["jamaica"] / tiempo_final) 
    }

    # Impresión de resultados
    print("Prom mensual de dias sin cafetera: " + str(prom_mensual_dias_sin_operacion))
    print("Porcentaje mensual de cafe vendido en 2X1: %" + str(porc_mensual_cafe_vendido_en_2x1))
    print("Porcentaje de clientes perdidos por falta de café: " + str(porc_clientes_perdidos_falta_cafe))
    print("Promedio mensual de costo por promociones: $" + str(prom_mensual_costo_por_promo))
    print("Promedio mensual de gasto de electricidad: $" + str(prom_mensual_gasto_electricidad))
    print("Promedio mensual de calidad de café: ")
    pprint(prom_mensual_calidad_cafe)
    print("Café sobrante: ")
    pprint(stock)
    
#-----------------------------------------------------#
def main():

    global tiempo
    global tiempo_final
    global stock
    global quality
    global provider_quality
    global fecha_entrega_cafetera_reparada
    global fecha_llegada_pedido_cafe
    global ultimo_pedido_cafe
    global pedido_de_cafe_completo
    global pedido_de_cafe_reducido
    global cafetera_en_uso
    global acum_dias_sin_cafetera
    global acum_cafe_vendido_2x1
    global acum_clientes_perdidos_sin_cafe
    global acum_costo_promociones
    global acum_calidad_promedio
    global horas_de_trabajo_diarias
    global cafetera_seleccionada
    global temperatura_ambiente_seteada
    global prob_tamanio_vaso_chico
    global prob_tamanio_vaso_mediano
    global prob_tamanio_vaso_grande
    global grs_tamanio_vaso_chico
    global grs_tamanio_vaso_mediano
    global grs_tamanio_vaso_grande
    global costo_cafe
    global dias_al_mes_de_promo
    global dias_restantes_de_promo
    global acum_gasto_electricidad
    global ventas_totales

    #Condiciones iniciales
    quality={
        "brazilian": 87,
        "columbian": 91,
        "ethiopia": 85,
        "jamaica": 89
    }
    stock={
        "brazilian": 6000,
        "columbian": 6000,
        "ethiopia": 6000,
        "jamaica": 6000
    }
    provider_quality={
        "brazilian": 87,
        "columbian": 91,
        "ethiopia": 85,
        "jamaica": 89
    }
    costo_cafe={
        "brazilian": 51000,
        "columbian": 71270,
        "ethiopia": 51380,
        "jamaica": 63370
    }

    horas_de_trabajo_diarias = 12


    #Cafetera en uso principal: P | secundaria: S
    cafetera_en_uso = "P"


    ultimo_pedido_cafe = {
        "brazilian": 0,
        "columbian": 0,
        "ethiopia": 0,
        "jamaica": 0
    }
    pedido_de_cafe_completo = 8000
    pedido_de_cafe_reducido = 2000
    
    prob_tamanio_vaso_chico = 0.33
    prob_tamanio_vaso_mediano = 0.34
    prob_tamanio_vaso_grande = 0.33
    grs_tamanio_vaso_chico = 10
    grs_tamanio_vaso_mediano = 16
    grs_tamanio_vaso_grande = 18

    fecha_entrega_cafetera_reparada = 0

    tiempo = 0
    #tiempo_final = 1000
    #tiempo_final = 10000
    #tiempo_final = 100000
    #tiempo_final = 1000000
    tiempo_final = 10000000


    fecha_llegada_pedido_cafe = tiempo_final
    

    #vars de control
    cafeteras = [
        {
            "modelo": "Luna",
            "precio": "$7.600.000",
            "disminucion_calidad": 5,
            "probabilidad_de_falla": 0.0015
        },
        {
            "modelo": "Neo",
            "precio": "$10.000.000",
            "disminucion_calidad": 3,
            "probabilidad_de_falla": 0.0010
        },
        {
            "modelo": "Saturno",
            "precio": "$10.600.000",
            "disminucion_calidad": 0,
            "probabilidad_de_falla": 0.0008
        }
    ]

    cafetera_seleccionada = cafeteras[0]
    dias_al_mes_de_promo = 30
    temperatura_ambiente_seteada = 18



    #vars de resultado
    acum_dias_sin_cafetera = 0
    acum_cafe_vendido_2x1 = 0
    acum_clientes_perdidos_sin_cafe = 0
    acum_costo_promociones = 0
    acum_gasto_electricidad = 0
    ventas_totales = 0
    acum_calidad_promedio = {
        "brazilian": 0,
        "columbian": 0,
        "ethiopia": 0,
        "jamaica": 0
    }


    cafetera_seleccionada = cafeteras[0]
    dias_restantes_de_promo = dias_al_mes_de_promo
    simulacion()

#-----------------------------------------------------#
if __name__ == "__main__":
    main()

