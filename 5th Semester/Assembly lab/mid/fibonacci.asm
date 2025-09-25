.model small
.stack 100h
.code
main proc
    
    
    mov ax,1h
    mov bx,1h
    mov dx,1h
    
    mov cx,5h
    
    repeat:
    mov ax,dx
    add dx,bx
    mov bx,ax
    
    sub cx,1h
    cmp cx,0h
    jne repeat
    
    
    exit:
    mov dx,4ch
    int 21h
    main endp
end main