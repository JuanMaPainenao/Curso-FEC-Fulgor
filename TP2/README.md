# TP2 — Código de Golay extendido (24,12)

Modelo de referencia en Python y verificación del RTL contra él.

## Requisitos

- Python 3
- Icarus Verilog (`iverilog`, `vvp`)
- GTKWave (opcional, para ver ondas)

## 1. Generar los vectores

```
python3 gen_vectores.py
```

Deja los `vec_*.txt` que consumen los testbenches.

## 2. Correr los testbenches

```
# popcount12
iverilog -o sim tb_popcount.v golay_popcount12.v && vvp sim

# golay_mult_b  (B^2=I, no usa vectores)
iverilog -o sim tb_golay_mult_b.v golay_mult_b.v && vvp sim

# golay_syndrome
iverilog -o sim tb_golay_syndrome.v golay_syndrome.v golay_mult_b.v && vvp sim

# golay_row_search
iverilog -o sim tb_golay_row_search.v golay_row_search.v golay_popcount12.v && vvp sim

# golay_err_gen
iverilog -o sim tb_golay_err_gen.v golay_err_gen.v && vvp sim

# golay_encoder
iverilog -o sim tb_golay_encoder.v golay_encoder.v golay_mult_b.v && vvp sim

# golay_decoder (completo)
iverilog -o sim tb_golay_decoder.v golay_decoder.v golay_syndrome.v golay_mult_b.v \
                golay_popcount12.v golay_row_search.v golay_err_gen.v golay_correct.v && vvp sim
```

Cada uno imprime `N casos, 0 fallas` si está OK.

## 3. Prueba manual (valores sueltos)

Editá la lista `entradas` en `gen_manual.py` y corré:

```
python3 gen_manual.py
iverilog -o sim tb_manual.v golay_decoder.v golay_syndrome.v golay_mult_b.v \
                golay_popcount12.v golay_row_search.v golay_err_gen.v golay_correct.v && vvp sim
```

Imprime, por cada valor, la salida del RTL y la del golden lado a lado con `OK`/`DIFF`.

## 4. Ver ondas con GTKWave

Agregá al testbench que quieras mirar (dentro de un `initial`):

```verilog
initial begin
    $dumpfile("ondas.vcd");
    $dumpvars(0, tb_golay_decoder);   // el nombre del modulo del TB
end
```

Corré ese test (genera `ondas.vcd`) y abrilo:

```
gtkwave ondas.vcd
```
