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
    mov bl,al   ; b3

    mov ah,1
    int 21h
    sub al,30h
    mov bh,al   ; b2

    mov ah,1
    int 21h
    sub al,30h
    mov cl,al   ; b1

    mov ah,1
    int 21h
    sub al,30h
    mov ch,al   ; b0

    ; ---- result initialize ----
    mov result,0

    ; b3 * 8
    mov al,bl
    mov ah,0
    mov dl,8
    mul dl
    add result,al

    ; b2 * 4
    mov al,bh
    mov ah,0
    mov dl,4
    mul dl
    add result,al

    ; b1 * 2
    mov al,cl
    mov ah,0
    mov dl,2
    mul dl
    add result,al

    ; b0 * 1
    add result,ch

    ; ---- print result ----
    mov al,result