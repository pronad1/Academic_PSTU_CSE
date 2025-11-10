.model small
.stack 100h
.data
p db 'Enter two number: $'
q db 'Enter three number: $'
.code
main proc
    mov ax,@data
    mov ds,ax
    
    mov ah,9
    lea dx,p
    int 21h
    
    mov ah,1
    int 21h
    mov bh,al
    
    mov ah,1
    int 21h
    mov bl,al
    
    add bl,bh
    
    mov ah,2
    mov dl,0Ah
    int 21h
    mov dl,0Dh
    int 21h
    
    mov ah,2
    mov dl,bl
    sub dl,48
    int 21h
    
    mov ah,2
    mov dl,0Ah
    int 21h
    mov dl,0Dh
    int 21h
    
    mov ah,9
    lea dx,q
    int 21h
    
    mov ah,1
    int 21h
    mov bl,al
    
    int 21h
    mov bh,al
    
    add bl,bh
    sub bl,48
    
    int 21h
    mov cl,al
    
    add bl,cl
    sub bl,48
    
    mov ah,2
    mov dl,0Ah
    int 21h
    mov dl,0Dh
    int 21h
    
    mov ah,2
    mov dl,bl
    int 21h
    
    
    main endp
end main