org 100h

.data
msg1 db 'Enter n: $'
msg2 db 10,13,'Enter numbers: $'
msg3 db 10,13,'Original: $'
msg4 db 10,13,'Reversed: $'
arr db 9 dup(?)
n db ?

.code
start:
    mov ax, @data
    mov ds, ax

    ; Get n
    mov ah, 9
    lea dx, msg1
    int 21h
    mov ah, 1
    int 21h
    sub al, '0'
    mov n, al

    ; Get numbers
    mov ah, 9
    lea dx, msg2
    int 21h
    mov cl, n
    mov si, offset arr
L1: mov ah, 1
    int 21h
    cmp al, ' '
    je L1
    cmp al, 13
    je L1
    sub al, '0'
    mov [si], al
    inc si
    dec cl
    jnz L1

    ; Print original
    mov ah, 9
    lea dx, msg3
    int 21h
    mov cl, n
    mov si, offset arr
L2: mov ah, 2
    mov dl, [si]
    add dl, '0'
    int 21h
    mov dl, ' '
    int 21h
    inc si
    dec cl
    jnz L2

    ; Reverse in place
    mov cl, n
    shr cl, 1
    mov si, offset arr
    mov di, si
    mov al, n
    dec al
    mov ah, 0
    add di, ax
L3: mov al, [si]
    mov bl, [di]
    mov [di], al
    mov [si], bl
    inc si
    dec di
    dec cl
    jnz L3

    ; Print reversed
    mov ah, 9
    lea dx, msg4
    int 21h
    mov cl, n
    mov si, offset arr
L4: mov ah, 2
    mov dl, [si]
    add dl, '0'
    int 21h
    mov dl, ' '
    int 21h
    inc si
    dec cl
    jnz L4

    mov ah, 4Ch
    int 21h