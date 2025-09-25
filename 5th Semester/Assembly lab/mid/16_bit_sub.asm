.model small
.stack 100h
.code
main proc
    
    mov ax, 1234h ; first 16-bit number
    mov bx, 2314h ; second 16-bit number
    sub ax, bx    ; subtract bx from ax
    sbb ax, 0      ; subtract with borrow if needed   
    
    exit:
    mov dx,4ch
    int 21h
    main endp
end