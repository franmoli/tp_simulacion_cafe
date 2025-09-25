import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
from scipy import stats
from pprint import pprint
import math

class Simulacion:

    def __init__(self):
        self.seteo_de_variables_iniciales()

    #-----------------------------------------------------#
    def pedido_de_cafe(self):
        stocks_menores_al_umbral = sum(1 for cant_stock in self.stock.values() if cant_stock < 5000)
        #pprint(self.stock)
        #print(stocks_menores_al_umbral)
        if self.fecha_llegada_pedido_cafe == self.tiempo_final and stocks_menores_al_umbral >= 2:
            #print("Pedido")
            self.acum_temp_pedidos_cafe += 1
            #Calculo el tamaño de pedido
            for tipo_cafe, stock_cafe in self.stock.items():
                if stock_cafe < 10000:
                    self.ultimo_pedido_cafe[tipo_cafe] = self.pedido_de_cafe_completo
                else:
                    self.ultimo_pedido_cafe[tipo_cafe] = self.pedido_de_cafe_reducido
            self.fecha_llegada_pedido_cafe = self.tiempo + random.randint(2, 6)
            #pprint(self.ultimo_pedido_cafe)

    def llegada_de_cafe(self):
        for tipo_cafe_pedido, cantidad_pedido in self.ultimo_pedido_cafe.items():
            nueva_qualy = (self.quality[tipo_cafe_pedido] * self.stock[tipo_cafe_pedido] + self.provider_quality[tipo_cafe_pedido] * cantidad_pedido) / (self.stock[tipo_cafe_pedido] + cantidad_pedido)
            self.quality[tipo_cafe_pedido] = nueva_qualy
            self.stock[tipo_cafe_pedido] += cantidad_pedido
        self.fecha_llegada_pedido_cafe = self.tiempo_final

    def calcular_cafe_vendido_segun_fdp(self, fdp):
        return fdp["distribucion"].rvs(**fdp["args"])

    def calculo_de_ventas_diarias(self):
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
        for i in range(self.horas_de_trabajo_diarias):
            for tipo_cafe, fdp in fdps_por_tipo_cafe.items():
                ventas = self.calcular_cafe_vendido_segun_fdp(fdp)
                ventas_del_dia[tipo_cafe] += round(ventas)
                

        #print("Las ventas hoy fueron")
        #pprint(ventas_del_dia)
        return ventas_del_dia

    def calculo_disminucion_calidad(self, q0):
        t = self.temperatura_ambiente_seteada + 273.15
        k = math.exp(-3412.7 * (1/t) + 6.007)
        return q0 * math.exp(-k)
        
    def estimar_perdida_de_calidad(self):
        perdidas_de_calidad = {
            "brazilian": 0,
            "columbian": 0,
            "ethiopia": 0,
            "jamaica": 0
        }
        for tipo, calidad in self.quality.items():
            perdidas_de_calidad[tipo] += calidad - self.calculo_disminucion_calidad(calidad)
        return perdidas_de_calidad

    def rotura_de_cafetera(self):
        prob_falla = random.random()
        if prob_falla <= self.cafetera_seleccionada["probabilidad_de_falla"]:
            self.cafetera_en_uso = "S"
            self.llegada_de_servicio_tecnico()

    def llegada_de_servicio_tecnico(self):
        duracion_de_la_reparacion = round(stats.rdist.rvs(c=1.1362268006606664, loc=0.10017320659825403, scale=4.899826793401747))
        self.fecha_entrega_cafetera_reparada = self.tiempo + (duracion_de_la_reparacion if duracion_de_la_reparacion > 0 else 1)


    def llegada_de_cafetera_reparada(self):
        self.cafetera_en_uso = "P"
        self.fecha_entrega_cafetera_reparada = self.tiempo_final

    def adquirir_otro_producto(self, gramos, tipo_original):
        
        candidatos = [t for t, s in self.stock.items() if t != tipo_original and s > gramos]
        #print("Los candidatos a repartir son: ")
        #pprint(candidatos)

        if not candidatos: 
            return False
        
        variedad_elegida = random.choice(candidatos)

        grs_regalados_en_la_promo = 0
        if self.dias_restantes_de_promo > 0:
            grs_regalados_en_la_promo = gramos * 0.7

        self.stock[variedad_elegida] -= gramos
        self.ventas_totales += gramos
        self.acum_cafe_vendido_2x1 += grs_regalados_en_la_promo
        self.acum_costo_promociones += grs_regalados_en_la_promo * self.costo_cafe[variedad_elegida] / 1000




    def estimar_consumo_aire_acondicionado(self):
        temperatura_exterior = stats.johnsonsb.rvs(a=0.7754053225581187, b=1.4858895610018643, loc = 2.2426877152581275, scale = 34.80171045035129)
        return 1.5 * 30 * abs(self.temperatura_ambiente_seteada - temperatura_exterior)

    #-----------------------------------------------------#
    def simulacion(self):


        while self.tiempo < self.tiempo_final:
            #-------------avanzar tiempo en 1 dt----------
            self.tiempo += 1
            #-------------eventos del propio dia----------
            if self.tiempo % 30 == 0:
                #print("reseteo")
                self.dias_restantes_de_promo = self.dias_al_mes_de_promo

            ventas_diarias = self.calculo_de_ventas_diarias()

            self.perdidas_de_calidad = self.estimar_perdida_de_calidad()

            #---------------Eventos comprometidos en dt anteriores---------------
            #si es dia de llegada -> sube stock y calidad

            if self.tiempo == self.fecha_llegada_pedido_cafe:
                self.llegada_de_cafe()

            #Si llega la cafetera se cambia el tipo de cafetera y sube la calidad
            if self.tiempo == self.fecha_entrega_cafetera_reparada:
                self.llegada_de_cafetera_reparada()

            if self.cafetera_en_uso == "S":
                self.acum_dias_sin_cafetera += 1
                

            #------------Actualizacion del vector de modelo de estado-----------

            #Se actualizan los vectores de estado con las ventas y calidad diarios
            for tipo, ventas in ventas_diarias.items():

                gramos_de_la_venta =  (ventas * 0.33 * self.grs_tamanio_vaso_chico
                                        + ventas * 0.34 * self.grs_tamanio_vaso_mediano
                                        + ventas * 0.33 * self.grs_tamanio_vaso_grande)

                #print("Venta inicial: " + str(gramos_de_la_venta))
                if self.dias_restantes_de_promo > 0:
                    gramos_de_la_venta += gramos_de_la_venta * 0.35
                    #print("Venta por promo: " + str(gramos_de_la_venta))
                
                #sirvo todo lo que pueda se la venta si mi estock me alcanza para al menos 1 vaso
                gramos_efectivamente_servidos = min(gramos_de_la_venta, self.stock[tipo]) if self.stock[tipo] > 10 else 0
                #print("Venta final: " + str(gramos_efectivamente_servidos))
                #pprint(self.stock)

                grs_regalados_en_la_promo = 0
                if self.dias_restantes_de_promo > 0:
                    grs_regalados_en_la_promo = gramos_efectivamente_servidos * 0.7

                self.stock[tipo] -= gramos_efectivamente_servidos
                self.ventas_totales += gramos_efectivamente_servidos
                self.acum_cafe_vendido_2x1 += grs_regalados_en_la_promo
                self.acum_costo_promociones += grs_regalados_en_la_promo * self.costo_cafe[tipo] / 1000

                if gramos_efectivamente_servidos < gramos_de_la_venta:

                    gramos_no_servidos = gramos_de_la_venta - gramos_efectivamente_servidos

                    gramos_que_eligen_otro_prod = gramos_no_servidos * 0.8

                    gramos_se_retiran_sin_comprar = gramos_no_servidos * 0.2

                    self.acum_ventas_perdidas_sin_cafe += gramos_se_retiran_sin_comprar * (ventas / gramos_de_la_venta)
                    
                    self.adquirir_otro_producto(gramos_que_eligen_otro_prod, tipo)





                #self.ventas_totales += 1
                #self.acum_cafe_vendido_2x1 += (1 if probabilidad_acepta_promo < 0.7 else 0)
                #self.acum_costo_promociones += (((self.costo_cafe[tipo]*(gramos_de_la_venta/2))/1000) if probabilidad_acepta_promo < 0.7 else 0)
                #self.acum_ventas_perdidas_sin_cafe += 1
        

            for tipo, perdida in self.perdidas_de_calidad.items():
                self.quality[tipo] -= perdida

            self.acum_gasto_electricidad += self.estimar_consumo_aire_acondicionado() * 1230 #$1230 precio estimado del W en Edesur

            for tipo, _ in self.acum_calidad_promedio.items():
                self.acum_calidad_promedio[tipo] += self.quality[tipo] - (10 if self.cafetera_en_uso == "S" else self.cafetera_seleccionada["disminucion_calidad"])

            if self.dias_restantes_de_promo > 0:
                self.dias_restantes_de_promo -= 1
            
            #-----------Registro de eventos que comprometen dt futuros----------
            #Si dos variedades de café bajan de los 5kg se realiza un pedido
            self.pedido_de_cafe()

            self.rotura_de_cafetera()

        # Cálculo de resultados
        prom_mensual_dias_sin_operacion = (self.acum_dias_sin_cafetera / self.tiempo_final) * 30
        porc_mensual_cafe_vendido_en_2x1 = (self.acum_cafe_vendido_2x1 / self.ventas_totales) * 100
        porc_ventas_perdidas_falta_cafe = (self.acum_ventas_perdidas_sin_cafe / self.ventas_totales) * 100
        prom_mensual_costo_por_promo = (self.acum_costo_promociones / self.tiempo_final) * 30
        prom_mensual_gasto_electricidad = (self.acum_gasto_electricidad / self.tiempo_final) * 30
        
        prom_mensual_calidad_cafe = {
            "brazilian": round(self.acum_calidad_promedio["brazilian"] / self.tiempo_final, 2),
            "columbian": round(self.acum_calidad_promedio["columbian"] /self.tiempo_final, 2),
            "ethiopia": round(self.acum_calidad_promedio["ethiopia"] / self.tiempo_final, 2),
            "jamaica": round(self.acum_calidad_promedio["jamaica"] / self.tiempo_final, 2)
        }

        # Impresión de resultados
        print("Prom mensual de dias sin cafetera: " + str(prom_mensual_dias_sin_operacion))
        print("Porcentaje mensual de cafe vendido en 2X1: %" + str(round(porc_mensual_cafe_vendido_en_2x1, 2)))
        print("Porcentaje de ventas perdidass por falta de café: %" + str(round(porc_ventas_perdidas_falta_cafe, 2)))
        print("Promedio mensual de costo por promociones: $" + str(round(prom_mensual_costo_por_promo, 2)))
        print("Promedio mensual de gasto de electricidad: $" + str(round(prom_mensual_gasto_electricidad, 2)))
        print("Promedio mensual de calidad de café: ")
        pprint(prom_mensual_calidad_cafe)
        

    def seteo_de_variables_iniciales(self):
    

        #Condiciones iniciales
        self.quality={
            "brazilian": 87,
            "columbian": 91,
            "ethiopia": 85,
            "jamaica": 89
        }
        self.stock={
            "brazilian": 30000,
            "columbian": 30000,
            "ethiopia": 30000,
            "jamaica": 30000
        }
        self.provider_quality={
            "brazilian": 87,
            "columbian": 91,
            "ethiopia": 85,
            "jamaica": 89
        }
        self.costo_cafe={
            "brazilian": 51000,
            "columbian": 71270,
            "ethiopia": 51380,
            "jamaica": 63370
        }

        self.horas_de_trabajo_diarias = 12

        #Cafetera en uso principal: P | secundaria: S
        self.cafetera_en_uso = "P"

        self.ultimo_pedido_cafe = {
            "brazilian": 0,
            "columbian": 0,
            "ethiopia": 0,
            "jamaica": 0
        }
        self.pedido_de_cafe_completo = 30000
        self.pedido_de_cafe_reducido = 15000
        
        self.prob_tamanio_vaso_chico = 0.33
        self.prob_tamanio_vaso_mediano = 0.34
        self.prob_tamanio_vaso_grande = 0.33
        self.grs_tamanio_vaso_chico = 10
        self.grs_tamanio_vaso_mediano = 16
        self.grs_tamanio_vaso_grande = 24

        self.fecha_entrega_cafetera_reparada = 0

        self.tiempo = 0
        #self.tiempo_final = 1000
        #self.tiempo_final = 10000
        self.tiempo_final = 100000
        #self.tiempo_final = 1000000
        #self.tiempo_final = 10000000

        self.fecha_llegada_pedido_cafe = self.tiempo_final
        
        #vars de control
        self.cafeteras = [
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

        self.cafetera_seleccionada = self.cafeteras[2]
        self.dias_al_mes_de_promo = 0
        self.temperatura_ambiente_seteada = 24

        #vars de resultado
        self.acum_dias_sin_cafetera = 0
        self.acum_cafe_vendido_2x1 = 0
        self.acum_ventas_perdidas_sin_cafe = 0
        self.acum_costo_promociones = 0
        self.acum_gasto_electricidad = 0
        self.acum_temp_pedidos_cafe = 0
        self.ventas_totales = 0
        self.acum_pedidos = 0
        self.acum_calidad_promedio = {
            "brazilian": 0,
            "columbian": 0,
            "ethiopia": 0,
            "jamaica": 0
        }

        self.dias_restantes_de_promo = self.dias_al_mes_de_promo


#-----------------------------------------------------#
def simulacion_completa():
    sim = Simulacion()

    #por cada cafetera
    for caf in range(0, 3):
        #por cantidad de dias de promo
        for promos in range(1,25, 5):
            for temp in range(12, 28, 4):

                sim.seteo_de_variables_iniciales()
                sim.cafetera_seleccionada = sim.cafeteras[caf]
                sim.dias_al_mes_de_promo = promos
                sim.temperatura_ambiente_seteada = temp

                print("-----------------Nueva simulacion-----------")
                print("Cafetera: " + sim.cafetera_seleccionada["modelo"] )
                print("Dias al mes de promo: " + str(promos))
                print("Temperatura seteada: " + str(temp))

                sim.simulacion()

def simulacion_manual():
    sim = Simulacion()
    sim.seteo_de_variables_iniciales()
    sim.cafetera_seleccionada = sim.cafeteras[0]
    sim.dias_al_mes_de_promo = 10
    sim.temperatura_ambiente_seteada = 20

    sim.simulacion()

#-----------------------------------------------------#
if __name__ == "__main__":
    simulacion_completa()
