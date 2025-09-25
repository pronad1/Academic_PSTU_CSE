.model small
.stack 100h
.code
main proc
    
    mov ax,1234h
    mov bx,1111h
    
    add ax,bx
    
    exit:
    mov bx,4ch
    int 21h
    main endp
end main
