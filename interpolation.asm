section .data
input_file    db "quadrant.img", 0
output_file   db "output.img", 0
buffer        times 10000 db 0      ; Reservamos 10,000 bytes, suficiente para 9409 bytes

section .text
global _start

_start:
    ; Abrir archivo de entrada
    mov eax, 5          ; sys_open
    mov ebx, input_file ; nombre del archivo
    mov ecx, 0          ; O_RDONLY
    int 0x80
    mov esi, eax        ; guardar file descriptor en esi

    ; Leer archivo en buffer
    mov eax, 3          ; sys_read
    mov ebx, esi        ; fd
    mov ecx, buffer     ; buffer
    mov edx, 9409       ; número de bytes exactos a leer (97 x 97)
    int 0x80
    mov edi, eax        ; guardar número de bytes leídos

    ; Procesar: sumar 1 a cada byte
    xor ecx, ecx        ; índice = 0

process_loop:
    cmp ecx, edi        ; ¿ya procesamos todos los bytes?
    jge open_output     ; si sí, ir a abrir archivo de salida
    mov al, [buffer + ecx] ; cargar buffer[i]
    add al, 1               ; sumar 1 (overflow permitido)
    mov [buffer + ecx], al  ; guardar de vuelta
    inc ecx                ; i++
    jmp process_loop

open_output:
    ; Abrir/crear archivo de salida
    mov eax, 5              ; sys_open
    mov ebx, output_file
    mov ecx, 0x241          ; O_WRONLY | O_CREAT | O_TRUNC (577 decimal)
    mov edx, 0666o          ; permisos rw-rw-rw-
    int 0x80
    mov esi, eax            ; guardar file descriptor de salida

    ; Escribir buffer modificado
    mov eax, 4              ; sys_write
    mov ebx, esi
    mov ecx, buffer
    mov edx, edi            ; cantidad de bytes a escribir
    int 0x80

    ; Salir del programa
    mov eax, 1              ; sys_exit
    xor ebx, ebx
    int 0x80
