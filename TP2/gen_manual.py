import planteo
from planteo import dec_vbin, deco


B = [[1,0,0,1,1,0,0,0,1,1,1,1],[0,1,0,0,1,1,1,0,0,1,1,1],[0,0,1,1,0,1,0,1,0,1,1,1],
     [1,0,1,1,1,1,1,0,0,0,1,0],[1,1,0,1,1,1,0,1,0,0,0,1],[0,1,1,1,1,1,0,0,1,1,0,0],
     [0,1,0,1,0,0,1,1,1,1,0,1],[0,0,1,0,1,0,1,1,1,1,1,0],[1,0,0,0,0,1,1,1,1,0,1,1],
     [1,1,1,0,0,1,1,1,0,1,0,0],[1,1,1,1,0,0,0,1,1,0,1,0],[1,1,1,0,1,0,1,0,1,0,0,1]]
planteo.B = B

def vec_a_int(v):
    n = 0
    for i in range(len(v)):
        n = (n << 1) | v[i]
    return n



entradas = [
    "A5D9A6",   # r1 del enunciado
    "A5F9A4",   # r2 del enunciado
    "A5C9AA",   # r3 del enunciado (no corregible)
    "000000",   # codeword del mensaje 0, sin error
    "000001",   # codeword 0 con 1 error en la paridad -> corrige a msg 000
    "800000",   # codeword 0 con 1 error en el mensaje  -> corrige a msg 000
]
# =================================================

f = open("vec_manual.txt", "w")
for hx in entradas:
    rx = int(hx, 16)
    v, e, corr, ncorr = deco(dec_vbin(rx, 24))
    u_flag = 1 if ncorr else 0
    c_flag = 1 if corr else 0
    if ncorr:
        msg_i, err_i = 0, 0
    else:
        msg_i, err_i = vec_a_int(v), vec_a_int(e)
    f.write(format(rx,"06x")+" "+format(msg_i,"03x")+" "+format(err_i,"06x")+
            " "+str(c_flag)+" "+str(u_flag)+"\n")
f.close()