.model small
.stack 100h
.data
result db 0
.code
main proc
    mov ax,@data
    mov ds,ax
    
    
    mov ah,1
    int 21h
    sub al,30h
    mov bl,al
    
    int 21h
    sub al,30h
    mov bh,al
    
    int 21h
    sub al,30h
    mov cl,al
    
    int 21h
    sub al,30h
    mov ch,al
    
    mov result,0
    
    mov al,bl
    mov dl,8
    mul dl
    add result,al
    
    mov al,bh
    mov dl,4
    mul dl
    add result,al
    
    mov al,cl
    mov dl,2
    mul dl
    add result,al
    
    add result,ch
    
    mov al,result
   