.model small
.stack 100h

.code
main proc
    
    mov ax,1h
    mov cx,5h
    
    count:
    mul cx
    loop count
    
    exit:
    mov dx,4ch
    int 21h
    main endp
end main