# TP2 - Fulgor - FEC
from funciones import gf, GFPoly


def traspuesta(M):
     filas = len(M)
     cols  = len(M[0])

     T = []
     for i in range(cols):
          fila = []
          for i in range(filas):
               fila.append(0)
          T.append(fila)

     for i in range(filas):
          for j in range(cols):
               T[j][i] = M[i][j]

     return T

def mult_matrices(A, B):
     filas_A = len(A)
     cols_A  = len(A[0])
     cols_B  = len(B[0])

     C = []
     for i in range(filas_A):
          fila = []
          for i in range(cols_B):
               fila.append(0)
          C.append(fila)

     for i in range(filas_A):
          for j in range(cols_B):
               acum = 0
               for k in range(cols_A):
                    acum = acum + A[i][k] * B[k][j]
               C[i][j] = acum % 2
     return C

def mult_vector_matriz(v, M):
     cols_M = len(M[0])
     C = []
     for i in range(cols_M):
          C.append(0)

     for j in range(cols_M):
          acum = 0
          for k in range(len(v)):
               acum = acum + v[k] * M[k][j]
          C[j] = acum % 2
     return C


def hex_bin(w):
    w = w[2:]  # saca el "0x"

    tabla = {
        '0': [0,0,0,0], '1': [0,0,0,1], '2': [0,0,1,0], '3': [0,0,1,1],
        '4': [0,1,0,0], '5': [0,1,0,1], '6': [0,1,1,0], '7': [0,1,1,1],
        '8': [1,0,0,0], '9': [1,0,0,1], 'A': [1,0,1,0], 'B': [1,0,1,1],
        'C': [1,1,0,0], 'D': [1,1,0,1], 'E': [1,1,1,0], 'F': [1,1,1,1],
    }
    binario = []
    for i in range(len(w)):
        nibble = tabla[w[i]]
        for j in range(len(nibble)):
            binario.append(nibble[j])

    return binario

def xor_vectores(u, w):
     resultado = []
     for i in range(len(u)):
          resultado.append(u[i] ^ w[i])
     return resultado

def peso(v):
     p = 0
     for i in range(len(v)):
          if v[i] == 1:
               p += 1
     return p  

def dec_vbin(num, num_bits=12):
    vector = []
    for i in range(num_bits - 1, -1, -1):
        bit_desplazado = num >> i
        bit = bit_desplazado & 1
        vector.append(bit)
    return vector


def u_i(pos):
     u = [0,0,0,0,0,0,0,0,0,0,0,0]
     u[pos] = 1
     return u

def codificador(mensaje, g):
     c = mult_vector_matriz(dec_vbin(mensaje), g)
     return  c

def deco(recibido):
     r = recibido
     r_msg = r[:12]
     r_par = r[12:]
     s = xor_vectores(mult_vector_matriz(r_msg, B), r_par)
     q = mult_vector_matriz(s, B)
     flag_2 = 0
     pos_2 = 0
     flag_4 = 0
     pos_4 = 0
     flag_corregible = False
     flag_no_corregible = False
     for i in range(len(B)):
          if peso(xor_vectores(s, B[i])) <= 2:
               flag_2 = 1
               pos_2 = i
               break

     for i in range(len(B)):
          if peso(xor_vectores(q, B[i])) <= 2:
               flag_4 = 1
               pos_4 = i
               break

     vector_nulo = [0,0,0,0,0,0,0,0,0,0,0,0]

     if peso(s) <= 3:
          e = vector_nulo + s
          v = xor_vectores(r, e)
          v = v[:12]
          flag_corregible = True
          flag_no_corregible = False
          # print('Caso 1 - errores solo en la paridad, peso del patron:', peso(e))
          return v, e, flag_corregible, flag_no_corregible
          # e = (0 | s)
     elif flag_2 == 1:
          e = u_i(pos_2) + xor_vectores(s, B[pos_2])
          v = xor_vectores(r, e)
          v = v[:12]
          flag_corregible = True
          flag_no_corregible = False
          # print('Caso 2 - 1 error en el mensaje (pos', pos_2, ') + paridad, peso total:', peso(e))
          return v, e, flag_corregible, flag_no_corregible
          # e = (u_{pos_2} | s XOR B[pos_2])
     elif peso(q) <= 3:
          e = q + vector_nulo
          v = xor_vectores(r, e)
          v = v[:12]
          flag_corregible = True
          flag_no_corregible = False
          # print('Caso 3 - errores solo en el mensaje, peso del patron:', peso(e))
          return v, e, flag_corregible, flag_no_corregible
          # e = (q | 0)
     elif flag_4 == 1:
          e = xor_vectores(q, B[pos_4]) + u_i(pos_4)
          v = xor_vectores(r, e)
          v = v[:12]
          flag_corregible = True
          flag_no_corregible = False
          # print('Caso 4 - 1 error en la paridad (pos', pos_4, ') + mensaje, peso total:', peso(e))
          return v, e, flag_corregible, flag_no_corregible
          # e = (q XOR B[pos_4] | u_{pos_4})
     else:
          # print('Caso 5 - No se puede corregir')
          return None, None, False, True



if __name__ == "__main__":
     print('Main')

     B = [[1,0,0,1,1,0,0,0,1,1,1,1],
          [0,1,0,0,1,1,1,0,0,1,1,1],
          [0,0,1,1,0,1,0,1,0,1,1,1],
          [1,0,1,1,1,1,1,0,0,0,1,0],
          [1,1,0,1,1,1,0,1,0,0,0,1],
          [0,1,1,1,1,1,0,0,1,1,0,0],
          [0,1,0,1,0,0,1,1,1,1,0,1],
          [0,0,1,0,1,0,1,1,1,1,1,0],
          [1,0,0,0,0,1,1,1,1,0,1,1],
          [1,1,1,0,0,1,1,1,0,1,0,0],
          [1,1,1,1,0,0,0,1,1,0,1,0],
          [1,1,1,0,1,0,1,0,1,0,0,1]]

     G = [[1,0,0,0,0,0,0,0,0,0,0,0, 1,0,0,1,1,0,0,0,1,1,1,1],
          [0,1,0,0,0,0,0,0,0,0,0,0, 0,1,0,0,1,1,1,0,0,1,1,1],
          [0,0,1,0,0,0,0,0,0,0,0,0, 0,0,1,1,0,1,0,1,0,1,1,1],
          [0,0,0,1,0,0,0,0,0,0,0,0, 1,0,1,1,1,1,1,0,0,0,1,0],
          [0,0,0,0,1,0,0,0,0,0,0,0, 1,1,0,1,1,1,0,1,0,0,0,1],
          [0,0,0,0,0,1,0,0,0,0,0,0, 0,1,1,1,1,1,0,0,1,1,0,0],
          [0,0,0,0,0,0,1,0,0,0,0,0, 0,1,0,1,0,0,1,1,1,1,0,1],
          [0,0,0,0,0,0,0,1,0,0,0,0, 0,0,1,0,1,0,1,1,1,1,1,0],
          [0,0,0,0,0,0,0,0,1,0,0,0, 1,0,0,0,0,1,1,1,1,0,1,1],
          [0,0,0,0,0,0,0,0,0,1,0,0, 1,1,1,0,0,1,1,1,0,1,0,0],
          [0,0,0,0,0,0,0,0,0,0,1,0, 1,1,1,1,0,0,0,1,1,0,1,0],
          [0,0,0,0,0,0,0,0,0,0,0,1, 1,1,1,0,1,0,1,0,1,0,0,1]]

     H = [[1,0,0,1,1,0,0,0,1,1,1,1, 1,0,0,0,0,0,0,0,0,0,0,0],
          [0,1,0,0,1,1,1,0,0,1,1,1, 0,1,0,0,0,0,0,0,0,0,0,0],
          [0,0,1,1,0,1,0,1,0,1,1,1, 0,0,1,0,0,0,0,0,0,0,0,0],
          [1,0,1,1,1,1,1,0,0,0,1,0, 0,0,0,1,0,0,0,0,0,0,0,0],
          [1,1,0,1,1,1,0,1,0,0,0,1, 0,0,0,0,1,0,0,0,0,0,0,0],
          [0,1,1,1,1,1,0,0,1,1,0,0, 0,0,0,0,0,1,0,0,0,0,0,0],
          [0,1,0,1,0,0,1,1,1,1,0,1, 0,0,0,0,0,0,1,0,0,0,0,0],
          [0,0,1,0,1,0,1,1,1,1,1,0, 0,0,0,0,0,0,0,1,0,0,0,0],
          [1,0,0,0,0,1,1,1,1,0,1,1, 0,0,0,0,0,0,0,0,1,0,0,0],
          [1,1,1,0,0,1,1,1,0,1,0,0, 0,0,0,0,0,0,0,0,0,1,0,0],
          [1,1,1,1,0,0,0,1,1,0,1,0, 0,0,0,0,0,0,0,0,0,0,1,0],
          [1,1,1,0,1,0,1,0,1,0,0,1, 0,0,0,0,0,0,0,0,0,0,0,1]]

     H = []
     for i in range(len(B)):
          fila = B[i] + u_i(i)   # [ B[i] | e_i ]
          H.append(fila)

     # EJERCICIO 1

     R = mult_matrices(G, traspuesta(H))

     print(R)

     B2 = mult_matrices(B, B)

     print(B2)
     print('--------------')

     # m = 0xA5C
     m = [[1,0,1,0,0,1,0,1,1,1,0,0]]
     v = mult_matrices(m, G)
     print(v)
     print('--------------')
     compro = mult_matrices(v, traspuesta(H))
     print(compro)
     print('--------------')

     # EJERCICIO 2
     # El peso min es el peso mas chico no nulo, de la tabla d_min = 8

     # Capacidad de correccion t = (d_min-1)/2 = (8-1)/2 = 7/2 = 3
     # Se corrigen hasta 3 errores

     # Capacdad de deteccion = d_min - 1 = 8 - 1 = 7
     # Se detectan hasta 7 errores

     # EJERCICIO 3
     r1 = "0xA5D9A6"
     r2 = "0xA5F9A4"
     r3 = "0xA5C9AA"

     r1 = hex_bin(r1)
     r2 = hex_bin(r2)
     r3 = hex_bin(r3)

     v1, e1, crr1, ncrr1 = deco(r1)
     print('v1:', v1)
     print('e1:', e1)
     print('crr1', crr1)
     print('ncrr1', ncrr1)
     print('--------------')
     v2, e2, crr2, ncrr2 = deco(r2)
     print('v2:', v2)
     print('e2:', e2)
     print('crr2', crr2)
     print('ncrr2', ncrr2)
     print('--------------')     
     v3, e3, crr3, ncrr3 = deco(r3)
     print('v3:', v3)
     print('e3:', e3)
     print('crr3', crr3)
     print('ncrr3', ncrr3)
     print('--------------')


     # EJERCICIO 4
     gf2 = gf(1, 3)   # No se realizo ningun cambio en funciones.py, solo se agregaron las operaciones con matrices en gf

     print("Tabla de suma GF(2):")
     for a in range(gf2.size):
          for b in range(gf2.size):
               print(a, "+", b, "=", gf2.suma(a, b))

     print("Tabla de producto GF(2):")
     for a in range(gf2.size):
          for b in range(gf2.size):
               print(a, "*", b, "=", gf2.producto(a, b))

     print("Inverso de 1:", gf2.inverso(1))
     print('--------------')


     B2 = gf2.mult_matrices(B, B)
     s = gf2.mult_vector_matriz(r1[:12], B)
     p = gf2.peso(s)

     print("B2:", B2)
     print("s:", s)
     print("p:", p)
     print('--------------')


     # EJERCICIO 5
     # Verificaciones

     g_ht = gf2.mult_matrices(G, traspuesta(H))
     print("G * H^T:", g_ht)
     print('--------------')

     b2 = gf2.mult_matrices(B, B)
     print("B * B:", b2)
     print('--------------')

     # Las verificacion dieron correctamente, GHt = 0 y BB = 0

     # Codeword fuerza bruta

     words = [0]*(2**12)
     for i in range(2**12):
          words[i] = i
          # print("palabra", i, " ", words[i])

     codewords = [0]*len(words)

     for i in range(2**12):
          # print("DEC a BIN: ", dec_vbin(words[i]))
          codewords[i] = gf2.mult_vector_matriz(dec_vbin(words[i]),G)

     cont0 = 0 
     cont8 = 0
     cont12 = 0
     cont16 = 0
     cont24 = 0


     for i in range(2**12):
          pesocodew = gf2.peso(codewords[i])
          if pesocodew==0:
               cont0 = cont0 + 1
          elif pesocodew == 8:
               cont8 = cont8 + 1
          elif pesocodew == 12:
               cont12 = cont12 + 1
          elif pesocodew == 16:
               cont16 = cont16 + 1
          elif pesocodew == 24:
               cont24 = cont24 + 1

     print("Peso 0: ", cont0, "Peso 8: ", cont8, "Peso 12: ", cont12, "Peso 16: ", cont16, "Peso 24: ", cont24)

     # Se observa que la simulacion por fuerza bruta coincide con la tabla del Ej 2

     # EJERCICIO 6
     # Declarados arriba, las funciones deco(recibido) y codificador(mensaje, g)

     # EJERCICIO 7

     PO = [0] * 24


     patrones1 = 0
     corregido1 = 0
     otra1 = 0
     detectado1 = 0

     patrones2 = 0
     corregido2 = 0
     otra2 = 0
     detectado2 = 0

     patrones3 = 0
     corregido3 = 0
     otra3 = 0
     detectado3 = 0

     patrones4 = 0
     corregido4 = 0
     otra4 = 0
     detectado4 = 0

     for i in range(24):
          P1 = [0]*24
          P1[i] = 1

          v1, e1, fc1, fnc1 = deco(P1)

          patrones1 = patrones1 + 1
          if fnc1 == True:
               detectado1 = detectado1 + 1
          elif e1 == P1:
               corregido1 = corregido1 + 1
          else:
               otra1 = otra1 + 1

     print('W = 1 -> patrones:', patrones1, 'corregidos:', corregido1, 'otra palabra:', otra1, 'detectados:', detectado1)


     for i in range(24):
          for j in range(i+1, 24):
               P2 = [0]*24
               P2[i] = 1
               P2[j] = 1

               v2, e2, fc2, fnc2 = deco(P2)

               patrones2 = patrones2 + 1
               if fnc2 == True:
                    detectado2 = detectado2 + 1
               elif e2 == P2:
                    corregido2 = corregido2 + 1
               else:
                    otra2 = otra2 + 1

     print('W = 2 -> patrones:', patrones2, 'corregidos:', corregido2, 'otra palabra:', otra2, 'detectados:', detectado2)

          
     for i in range(24):
          for j in range(i+1, 24):
               for h in range(j+1, 24):
                    P3 = [0]*24
                    P3[i] = 1
                    P3[j] = 1
                    P3[h] = 1

                    v3, e3, fc3, fnc3 = deco(P3)

                    patrones3 = patrones3 + 1
                    if fnc3 == True:
                         detectado3 = detectado3 + 1
                    elif e3 == P3:
                         corregido3 = corregido3 + 1
                    else:
                         otra3 = otra3 + 1

     print('W = 3 -> patrones:', patrones3, 'corregidos:', corregido3, 'otra palabra:', otra3, 'detectados:', detectado3)


     for i in range(24):
          for j in range(i+1, 24):
               for h in range(j+1, 24):
                    for t in range(h+1, 24):
                         P4 = [0]*24
                         P4[i] = 1
                         P4[j] = 1
                         P4[h] = 1
                         P4[t] = 1

                         v4, e4, fc4, fnc4 = deco(P4)

                         patrones4 = patrones4 + 1
                         if fnc4 == True:
                              detectado4 = detectado4 + 1
                         elif e4 == P4:
                              corregido4 = corregido4 + 1
                         else:
                              otra4 = otra4 + 1

     print('W = 4 -> patrones:', patrones4, 'corregidos:', corregido4, 'otra palabra:', otra4, 'detectados:', detectado4)
