BITS 64            ; <-- ¡MUY IMPORTANTE!

section .data
A db 10
B db 20
C db 30
D db 40

a_1 db 0
a_2 db 0
c_1 db 0
c_2 db 0
g_1 db 0
g_2 db 0
k_1 db 0
k_2 db 0
section .bss
buffer resb 32

section .text
global _start

_start:

    ; a1 = (2/3)*A + (1/3)*B
    mov al, [rel A]
    mov bl, 2
    mov ah, [rel B]
    mov bh, 1
    mov rdi, a_1
    call interpolar

    ; a2 = (1/3)*A + (2/3)*B
    mov al, [rel A]
    mov bl, 1
    mov ah, [rel B]
    mov bh, 2
    mov rdi, a_2
    call interpolar

    ; c1 = (2/3)*A + (1/3)*C
    mov al, [rel A]
    mov bl, 2
    mov ah, [rel C]
    mov bh, 1
    mov rdi, c_1
    call interpolar

    ; c2 = (2/3)*B + (1/3)*D
    mov al, [rel B]
    mov bl, 2
    mov ah, [rel D]
    mov bh, 1
    mov rdi, c_2
    call interpolar

    ; g1 = (1/3)*A + (2/3)*C
    mov al, [rel A]
    mov bl, 1
    mov ah, [rel C]
    mov bh, 2
    mov rdi, g_1
    call interpolar

    ; g2 = (1/3)*B + (2/3)*D
    mov al, [rel B]
    mov bl, 1
    mov ah, [rel D]
    mov bh, 2
    mov rdi, g_2
    call interpolar

    ; k1 = (2/3)*C + (1/3)*D
    mov al, [rel C]
    mov bl, 2
    mov ah, [rel D]
    mov bh, 1
    mov rdi, k_1
    call interpolar

    ; k2 = (1/3)*C + (2/3)*D
    mov al, [rel C]
    mov bl, 1
    mov ah, [rel D]
    mov bh, 2
    mov rdi, k_2
    call interpolar
    ; d = (2/3) * c1 + (1/3)*c2
    mov al, [rel c_1]
    mov bl, 2
    mov ah, [rel c_2]
    mov bh, 1
    lea rdi, [rel buffer + 0]
    call interpolar

    ; e = (1/3) * c1 + (2/3)*c2
    mov al, [rel c_1]
    mov bl, 1
    mov ah, [rel c_2]
    mov bh, 2
    lea rdi, [rel buffer + 1]
    call interpolar

    ; h = (2/3) * g1 + (1/3)*g2
    mov al, [rel g_1]
    mov bl, 2
    mov ah, [rel g_2]
    mov bh, 1
    lea rdi, [rel buffer + 2]
    call interpolar

    

    ; i = (1/3) * g1 + (2/3)*g2
    mov al, [rel g_1]
    mov bl, 1
    mov ah, [rel g_2]
    mov bh, 2
    lea rdi, [rel buffer + 3]
    call interpolar

    ; Salir
    mov rax, 60         ; syscall number for exit
    xor rdi, rdi        ; status 0
    syscall

; --------------------------------------------------
; Subrutina interpolar:
; AL = valor izquierdo
; BL = peso izquierdo
; AH = valor derecho
; BH = peso derecho
; RDI = destino donde guardar resultado
; --------------------------------------------------
interpolar:
    mov dl, ah          ; Guardar valor derecho en DL
    mul bl              ; AL * peso_izq
    mov cl, al          ; Guardar resultado parcial

    mov al, dl          ; AL = valor derecho
    mul bh              ; AL * peso_der
    add al, cl          ; Sumar ambos productos

    xor ah, ah          ; Limpiar AH para división
    mov dl, 3           ; Divisor
    add al, 1           ; <<<<<<<<<<<<<<  Aquí redondeamos
    div dl              ; AL = AL / 3 (ya redondeado)

    mov [rdi], al       ; Guardar resultado
    ret

