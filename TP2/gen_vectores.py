import planteo
from planteo import dec_vbin, mult_vector_matriz, xor_vectores, peso, deco

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
planteo.B = B

def vec_a_int(v):
    n = 0
    for i in range(len(v)):
        n = (n << 1) | v[i]
    return n

def popcount_int(x):
    p = 0
    for i in range(12):
        p = p + ((x >> i) & 1)
    return p

def codeword(msg_int):
    m = dec_vbin(msg_int, 12)
    par = mult_vector_matriz(m, B)
    return m + par # mensaje | paridad]

def syndrome_golden(rx_int):
    r = dec_vbin(rx_int, 24)
    r_msg = r[0:12]
    r_par = r[12:24]
    s = xor_vectores(mult_vector_matriz(r_msg, B), r_par)
    return vec_a_int(s)

B_int = []
for i in range(12):
    B_int.append(vec_a_int(B[i]))

def row_search_int(v): # v entero de 12 bits
    for i in range(12):
        cand = v ^ B_int[i]
        if popcount_int(cand) <= 2:
            return 1, i, cand
    return 0, 0, 0

def row_search_vec(v): # v vector de 12
    for i in range(12):
        cand = xor_vectores(v, B[i])
        if peso(cand) <= 2:
            return 1, i, cand
    return 0, 0, [0]*12

def intermedios(e_vec):               # espeja las etapas E1/E2 del pipeline
    r_msg = e_vec[0:12]
    r_par = e_vec[12:24]
    s = xor_vectores(mult_vector_matriz(r_msg, B), r_par)
    q = mult_vector_matriz(s, B)
    fs, idx_s, res_s = row_search_vec(s)
    fq, idx_q, res_q = row_search_vec(q)
    return s, q, peso(s), peso(q), fs, idx_s, res_s, fq, idx_q, res_q

# un generador por modulo
def gen_popcount(nombre):
    f = open(nombre, "w")
    for x in range(4096):
        w = popcount_int(x)
        f.write(format(x, "03x") + " " + format(w, "x") + "\n")
    f.close()

def gen_encoder(nombre):
    f = open(nombre, "w")
    for msg in range(4096):
        cw = vec_a_int(codeword(msg))
        f.write(format(msg, "03x") + " " + format(cw, "06x") + "\n")
    f.close()

def gen_syndrome(nombre):
    f = open(nombre, "w")
    # las 4096 codewords -> sindrome 0  (comprobacion H*c^T = 0)
    for msg in range(4096):
        rx = vec_a_int(codeword(msg))
        f.write(format(rx, "06x") + " " + "000" + "\n")
    # recibidos con error conocido -> sindrome != 0
    patrones = [0x800000, 0x000001, 0x001001, 0x900000, 0x000007]
    base = vec_a_int(codeword(0xA5C))
    for e in patrones:
        rx = base ^ e
        s = syndrome_golden(rx)
        f.write(format(rx, "06x") + " " + format(s, "03x") + "\n")
    f.close()

def gen_row_search(nombre):
    f = open(nombre, "w")
    for v in range(4096):
        found, idx, res = row_search_int(v)
        f.write(format(v, "03x") + " " + str(found) + " " +
                format(idx, "x") + " " + format(res, "03x") + "\n")
    f.close()

def escribir_caso(f, e_vec):
    s, q, w_s, w_q, fs, idx_s, res_s, fq, idx_q, res_q = intermedios(e_vec)
    v, e, corr, ncorr = deco(e_vec)   # golden: patron y flag de no-corregible
    if ncorr:
        o_err, o_unc = 0, 1
    else:
        o_err, o_unc = vec_a_int(e), 0
    campos = [format(vec_a_int(s),"03x"), format(vec_a_int(q),"03x"),
              format(vec_a_int(res_s),"03x"), format(vec_a_int(res_q),"03x"),
              format(w_s,"x"), format(w_q,"x"), format(idx_s,"x"), format(idx_q,"x"),
              str(fs), str(fq), format(o_err,"06x"), str(o_unc)]
    f.write(" ".join(campos) + "\n")

def gen_err_gen(nombre):
    f = open(nombre, "w")
    escribir_caso(f, [0]*24)                                  # peso 0
    for i in range(24):                                       # peso 1
        e=[0]*24; e[i]=1; escribir_caso(f, e)
    for i in range(24):                                       # peso 2
        for j in range(i+1,24):
            e=[0]*24; e[i]=1; e[j]=1; escribir_caso(f, e)
    for i in range(24):                                       # peso 3
        for j in range(i+1,24):
            for k in range(j+1,24):
                e=[0]*24; e[i]=1; e[j]=1; e[k]=1; escribir_caso(f, e)
    for i in range(24):                                       # peso 4
        for j in range(i+1,24):
            for k in range(j+1,24):
                for l in range(k+1,24):
                    e=[0]*24; e[i]=1; e[j]=1; e[k]=1; e[l]=1; escribir_caso(f, e)
    f.close()

def escribir_dec(f, rx_vec):
    rx = vec_a_int(rx_vec)
    v, e, corr, ncorr = deco(rx_vec)        # golden
    u_flag = 1 if ncorr else 0
    c_flag = 1 if corr else 0
    if ncorr:
        msg_i, err_i = 0, 0                  # no validos; el TB los ignora
    else:
        msg_i, err_i = vec_a_int(v), vec_a_int(e)
    f.write(format(rx,"06x")+" "+format(msg_i,"03x")+" "+format(err_i,"06x")+
            " "+str(c_flag)+" "+str(u_flag)+"\n")

def gen_decoder(nombre):
    f = open(nombre, "w")
    # Parte 1: las 4096 codewords SIN error -> decodifica al mensaje, err=0
    for msg in range(4096):
        escribir_dec(f, codeword(msg))
    # Parte 2: mensaje fijo 0xA5C con errores de peso 1..4 
    base = codeword(0xA5C)
    for i in range(24):
        e=[0]*24; e[i]=1; escribir_dec(f, xor_vectores(base, e))
    for i in range(24):
        for j in range(i+1,24):
            e=[0]*24; e[i]=1; e[j]=1; escribir_dec(f, xor_vectores(base, e))
    for i in range(24):
        for j in range(i+1,24):
            for k in range(j+1,24):
                e=[0]*24; e[i]=1; e[j]=1; e[k]=1; escribir_dec(f, xor_vectores(base, e))
    for i in range(24):
        for j in range(i+1,24):
            for k in range(j+1,24):
                for l in range(k+1,24):
                    e=[0]*24; e[i]=1;e[j]=1;e[k]=1;e[l]=1; escribir_dec(f, xor_vectores(base, e))
    f.close()

# correr todos
if __name__ == "__main__":
    gen_popcount("vec_popcount.txt")
    gen_encoder("vec_encoder.txt")
    gen_syndrome("vec_syndrome.txt")
    gen_row_search("vec_row_search.txt")
    gen_err_gen("vec_err_gen.txt")
    gen_decoder("vec_decoder.txt")
    print("Vectores generados")