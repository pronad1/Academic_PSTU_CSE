.model small
.stack 100h
.code

main proc
    
    mov ax, 1234h
    mov bx,0020h
    
    mul bx
    
    main endp
end main