.model small
.stack 100h
.data
    decnum db 0
    binstr db '0000$'    ; store 4-bit binary as string
.code
main proc
    mov ax,@data
    mov ds,ax

    ; input one decimal digit (0–15 only)
    mov ah,1
    int 21h
    sub al,30h       ; convert ASCII -> number
    mov decnum,al

    ; convert decimal to 4-bit binary
    mov cl,4         ; 4 bits
    mov si,3         ; index into binstr from rightmost
    mov al,decnum

convert_loop:
    mov ah,0
    mov bl,2
    div bl           ; AL / 2 -> quotient in AL, remainder in AH
    add ah,30h       ; convert remainder to ASCII
    mov binstr[si],ah
    dec si
    loop convert_loop

    ; print result
    mov ah,9
    lea dx,binstr
    int 21h

    mov ah,4ch
    int 21h
main endp
end main
