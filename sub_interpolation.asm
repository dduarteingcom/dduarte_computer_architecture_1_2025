BITS 64            ; <-- ¡MUY IMPORTANTE!
section .bss
input_buffer resb 97*97
output_buffer resb 385*385
temp_interp resq 6

section .text
global _start

_start:
    ;Abrir quadrant.img
    mov rax, 2
    lea rdi, [rel input_filename]
    xor rsi, rsi
    xor rdx, rdx
    syscall
    mov r8, rax
    ;leer input_buffer
    mov rax, 0
    mov rdi, r8
    lea rsi, [rel input_buffer]    ; <-- para read, OK aquí
    mov rdx, 97*97
    syscall
    ;cerrar archivo
    mov rax, 3      ; syscall close
    mov rdi, r8     ; el file descriptor abierto
    syscall
    ; rsi -> input_buffer
    ; rdi -> output_buffer
    lea rsi, [rel input_buffer]
    lea rdi, [rel output_buffer]
    xor r14, r14 ; fila (x) = 0
outer_loop: 
    xor r13, r13
    
inner_loop:
    ; === Cargar A, B, C, D ===
    ;offset_x = x * 97
    mov r8, r14
    imul r8, r8, 4        ; r8 = rcx * 4
    imul r8, r8, 97      ; r8 = (rcx * 4) * 97

    ;offset_x = x +1 * 97
    mov r9, r14
    inc r9
    imul r9, r9, 97
    ; === Cargar píxeles ===

    ; A = input[x][y]
    mov r10, r8
    add r10, r13
    movzx eax, byte[rsi + r10]
    ; B = input[x][y+1]
    inc r10
    movzx ebx, byte[rsi + r10]
    ; C = input[x+1][y]
    mov r10, r9
    add r10, r13
    movzx ecx, byte[rsi + r10]
    ; D = input[x+1][y+1]
    inc r10
    movzx edx, byte[rsi + r10]

    ;  === Cargar A, B, C, D al output_buffer ===

    ;offset_x = x * 4 * 385
    mov r9, r14
    imul r9, 4
    imul r9, 385
    ;offset_x = (x*4 + 3) * 385
    mov r10, r14
    imul r10 , 4
    add r10, 3
    imul r10, 385
    ;offset_y = y * 4
    mov r11, r13
    imul r11, r11, 4
    ; output[4x][4y] = A
    mov r12, r9
    add r12, r11 
    mov [rdi + r12], al
    ;output[4x][4y + 3] = B
    mov r12, r9
    add r12, r11
    add r12, 3
    mov [rdi + r12], bl
    ; output[4x + 3][4y] = C
    mov r12, r10
    add r12, r11
    mov [rdi + r12], cl
    ; output[4x + 3][4y + 3] = D
    mov r12, r10
    add r12, r11
    add r12, 3
    mov [rdi + r12], dl
    
     mov [rel temp_interp + 0*8], al
     mov [rel temp_interp + 1*8], bl
    ;Tengo disponibles los 
    
    ;offset_x = x * 4
    mov r9, r14
    imul r9, 4
    ;offset_y ya está aplicado

    ; a1 = (2/3)*A + (1/3)*B pos [4x,4y+1]
    mov al, [rel temp_interp + 0*8]
    mov bl, 2
    mov r8b, [rel temp_interp + 1*8]
    mov r12b, 1
    mov r10, r9
    imul r10, r10, 385
    add r10, r11
    add r10, 1
    add r10, rdi
    mov r15, r10
    call interpolar

    ; a2 = (1/3)*A + (2/3)*B pos [4x,4y+2]
    mov al, [rel temp_interp + 0*8]
    mov bl, 1
    mov r8b, [rel temp_interp + 1*8]
    mov r12b, 2
    mov r10, r9
    imul r10, r10, 385
    add r10, r11
    add r10, 2
    add r10, rdi
    mov r15, r10
    call interpolar

    ; c1 = (2/3)*A + (1/3)*C pos [4x + 1,4y]
    mov al, [rel temp_interp + 0*8]
    mov bl, 2
    mov r8b, cl
    mov r12b, 1
    mov r10, r9
    add r10 , 1
    imul r10, r10, 385
    add r10, r11
    add r10, rdi
    mov r15, r10
    mov [rel temp_interp + 2*8], r15
    call interpolar

    ; c2 = (2/3)*B + (1/3)*D pos [4x + 1,4y + 3]
    mov al, [rel temp_interp + 1*8]
    mov bl, 2
    mov r8b, dl
    mov r12b, 1
    mov r10, r9
    add r10, 1
    imul r10, r10, 385
    add r10, r11
    add r10, 3
    add r10, rdi
    mov r15, r10
    mov [rel temp_interp + 3*8], r15
    call interpolar

    ; g1 = (1/3)*A + (2/3)*C pos [4x + 2,4y]
    mov al, [rel temp_interp + 0*8]
    mov bl, 1
    mov r8b, cl
    mov r12b, 2
    mov r10, r9
    add r10, 2
    imul r10, r10, 385
    add r10, r11
    add r10, rdi
    mov r15, r10
    mov [rel temp_interp + 4*8], r15
    call interpolar

    ; g2 = (1/3)*B + (2/3)*D pos [4x + 2,4y + 3]
    mov al, [rel temp_interp + 1*8]
    mov bl, 1
    mov r8b, dl
    mov r12b, 2
    mov r10, r9
    add r10, 2
    imul r10, r10, 385
    add r10, r11
    add r10, 3
    add r10, rdi
    mov r15, r10
    mov [rel temp_interp + 5*8], r15
    call interpolar

    ; k1 = (2/3)*C + (1/3)*D pos [4x + 3,4y + 1]
    mov al, cl
    mov bl, 2
    mov r8b, dl
    mov r12b, 1
    mov r10, r9
    add r10, 3
    imul r10, r10, 385
    add r10, r11
    add r10, 1
    add r10, rdi
    mov r15, r10
    call interpolar

    ; k2 = (1/3)*C + (2/3)*D pos [4x + 3,4y + 2]
    mov al, cl
    mov bl, 1
    mov r8b, dl
    mov r12b, 2
    mov r10, r9
    add r10, 3
    imul r10, r10, 385
    add r10, r11
    add r10, 2
    add r10, rdi
    mov r15, r10
    call interpolar
    ; d = (2/3) * c1 + (1/3)*c2 pos [4x + 1,4y + 1]
    mov r15, [rel temp_interp + 2*8]   ; rax = dirección donde se guardó c1
    mov al, [r15]                      ; al = pixel c1
    mov bl, 2
    mov r12, [rel temp_interp + 3*8]   ; rbx = dirección donde se guardó c2
    mov r8b, [r12]  
    mov r12b, 1
    mov r10, r9
    add r10, 1
    imul r10, r10, 385
    add r10, r11
    add r10, 1
    add r10, rdi
    mov r15, r10
    call interpolar

    ; e = (1/3) * c1 + (2/3)*c2  pos [4x + 1,4y + 2]
    mov r15, [rel temp_interp + 2*8]   ; rax = dirección donde se guardó c1
    mov al, [r15]                      ; al = pixel c1
    mov bl, 1
    mov r12, [rel temp_interp + 3*8]   ; rbx = dirección donde se guardó c2
    mov r8b, [r12]  
    mov r12b, 2
    mov r10, r9
    add r10, 1
    imul r10, r10, 385
    add r10, r11
    add r10, 2
    add r10, rdi
    mov r15, r10
    call interpolar

    ; h = (2/3) * g1 + (1/3)*g2 pos [4x + 2,4y + 1]
    mov r15, [rel temp_interp + 4*8]   ; rax = dirección donde se guardó c1
    mov al, [r15]
    mov bl, 2
    mov r12, [rel temp_interp + 5*8]   ; rbx = dirección donde se guardó c2
    mov r8b, [r12] 
    mov r12b, 1
    mov r10, r9
    add r10, 2
    imul r10, r10, 385
    add r10, r11
    add r10, 1
    add r10, rdi
    mov r15, r10
    call interpolar
    ; i = (1/3) * g1 + (2/3)*g2 pos [4x + 2,4y + 2]
    mov r15, [rel temp_interp + 4*8]   ; rax = dirección donde se guardó c1
    mov al, [r15]
    mov bl, 1
    mov r12, [rel temp_interp + 5*8]   ; rbx = dirección donde se guardó c2
    mov r8b, [r12] 
    mov r12b, 2
    mov r10, r9
    add r10, 2
    imul r10, r10, 385
    add r10, r11
    add r10, 2
    add r10, rdi
    mov r15, r10
    call interpolar
    ; Incrementar columna
    inc r13
    cmp r13, 96         ; 0..95
    jl inner_loop
    inc r14
    cmp r14, 96         ; 0..95
    jl outer_loop
    ; Copiar pixel (96,96) de input_buffer a (192,192) de output_buffer
    ; Cargar último pixel
    movzx eax, byte [rsi + 96*97 + 96]
    ; Calcular posición en output_buffer
    mov r8, 192
    imul r8, 385          ; 192 * 385
    add r8, 192           ; +192 columnas
    add r8, rdi           ; base de output_buffer

    ; Guardar
    mov [r8], al
    ; ------------------------------------
    ; Escribir output_buffer a output.img
    ; ------------------------------------

    ; Abrir (crear) output.img en modo escritura (O_WRONLY | O_CREAT | O_TRUNC)
    mov rax, 2                  ; syscall open
    lea rdi, [rel output_filename]
    mov rsi, 577                ; O_WRONLY | O_CREAT | O_TRUNC = 0x241 = 577
    mov rdx, 0o666              ; permisos rw-rw-rw- (0666 octal)
    syscall
    mov r8, rax                 ; guardar el fd de salida en r8

    ; Escribir 385*385 bytes del output_buffer
    mov rax, 1                  ; syscall write
    mov rdi, r8                 ; fd de salida
    lea rsi, [rel output_buffer]; buffer origen
    mov rdx, 385*385            ; tamaño a escribir
    syscall

    ; Cerrar archivo de salida
    mov rax, 3                  ; syscall close
    mov rdi, r8                 ; fd de salida
    syscall


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
    mov dl, r8b          ; Guardar valor derecho en DL
    mul bl              ; AL * peso_izq
    mov cl, al          ; Guardar resultado parcial

    mov al, dl          ; AL = valor derecho
    mul r12b              ; AL * peso_der
    add al, cl          ; Sumar ambos productos

    ; para garantizar que AH=0 antes de div dl
    and ax, 0x00FF          ; Limpiar AH para división
    mov dl, 3           ; Divisor
    add al, 1           ; <<<<<<<<<<<<<<  Aquí redondeamos
    div dl              ; AL = AL / 3 (ya redondeado)

    mov [r15], al       ; Guardar resultado
    ret

section .data
input_filename db "quadrant.img", 0
output_filename db "output.img", 0
