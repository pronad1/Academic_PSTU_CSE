.model small
.stack 100h
.data
st db 'Enter the string : $'
 msg db 21
db ?
db 21 dup('$')

.code
main proc
    mov ax,@data
    mov ds,ax
    
    mov ah,9
    lea dx,st
    int 21h
    
    
    lea dx,msg  
    mov ah,0Ah
    int 21h
    
    mov ah,2
    mov dl,0Ah
    int 21h
    mov dl,0Dh
    int 21h
    
    mov ah,9
    lea dx,msg+2
    int 21h
    
    exit:
    mov dh,4ch
    int 21h
    main endp
end main
