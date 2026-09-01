# TP2 - Fulgor - FEC

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


def u_i(pos):
     u = [0,0,0,0,0,0,0,0,0,0,0,0]
     u[pos] = 1
     return u

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
          print('Caso 1')
          e = vector_nulo + s
          v = xor_vectores(r, e)
          v=v[:12]
          return e,v
          # e = (0 | s)
     elif flag_2 == 1:
          print('Caso 2 - un error en el mensaje, posicion:', pos_2)
          e = u_i(pos_2) + xor_vectores(s, B[pos_2])
          v = xor_vectores(r, e)
          v=v[:12]
          return e,v
          # e = (u_{pos_2} | s XOR B[pos_2])
     elif peso(q) <= 3:
          print('Caso 3 - errores todos en el mensaje')
          e = q + vector_nulo
          v = xor_vectores(r, e)
          v=v[:12]
          return e,v
          # e = (q | 0)
     elif flag_4 == 1:
          print('Caso 4 - un error en la paridad, posicion:', pos_4)
          e = xor_vectores(q, B[pos_4]) + u_i(pos_4)
          v = xor_vectores(r, e)
          v=v[:12]
          return e,v
          # e = (q XOR B[pos_4] | u_{pos_4})
     else:
          print('Caso 5 - No se puede corregir')
          return None, None



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

G = [[1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,1,0,0,0,1,1,1,1],
     [0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,1,1,0,0,1,1,1],
     [0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,1,0,1,0,1,0,1,1,1],
     [0,0,0,1,0,0,0,0,0,0,0,0,1,0,1,1,1,1,1,0,0,0,1,0],
     [0,0,0,0,1,0,0,0,0,0,0,0,1,1,0,1,1,1,0,1,0,0,0,1],
     [0,0,0,0,0,1,0,0,0,0,0,0,0,1,1,1,1,1,0,0,1,1,0,0],
     [0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,1,0,0,1,1,1,1,0,1],
     [0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,1,0,1,1,1,1,1,0],
     [0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,1,1,1,0,1,1],
     [0,0,0,0,0,0,0,0,0,1,0,0,1,1,1,0,0,1,1,1,0,1,0,0],
     [0,0,0,0,0,0,0,0,0,0,1,0,1,1,1,1,0,0,0,1,1,0,1,0],
     [0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,1,0,1,0,1,0,0,1]]

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

v1, e1 = deco(r1)
print('v1:', v1)
print('e1:', e1)
print('--------------')
v2, e2 = deco(r2)
print('v2:', v2)
print('e2:', e2)
print('--------------')
v3, e3 = deco(r3)
print('v3:', v3)
print('e3:', e3)
print('--------------')
