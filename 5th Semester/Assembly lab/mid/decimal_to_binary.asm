.model small
.stack 100h
.data
d db 0
bin db '0000$'
.code
main proc
    mov ax,@data
    mov ds,ax
    
    mov ah,1
    int 21h
    sub al,30h
    mov d,al
    
    mov si,3
    mov al,d  
    
    con:
    mov ah,0
    mov bl,2
    div bl
    add ah,30h
    mov bin[si],ah
    dec si
    loop con
    
    mov ah,2
    mov dx,0Ah
    int 21h
    mov dx,0Dh
    int 21h
    
    mov ah,9
    lea dx,bin
    int 21h
    
    mov ah,4ch
    int 21h
    main endp
end main   

