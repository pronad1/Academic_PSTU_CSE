.model small
.stack 100h  
.data
msg db 'Enter two numbers : $'
a db ?
b db ?

.code

main proc
      mov ax,@data
      mov ds,ax
                 ; multiply two static number
      
      mov al,3
      mov bl,3
      mul bl
      
      mov ah,2
      mov dl,al
      add dl,48
      int 21h 
      
      mov ah,2
      mov dl,0Ah
      int 21h
      mov dl,0Dh
      int 21h
      
                 ; multiply dynamic value
      
      
      mov ah,9
      lea dx,msg
      int 21h
      
      mov ah,1
      int 21h
      sub al,48
      mov a,al
      
      int 21h
      sub al,48
      
      mul a  ;al=al*a
      
      aam    ;AAM = ASCII Adjust after Multiply
      
      
      mov bx,ax
      
      mov ah,2
      mov dl,bh
      add dl,48
      int 21h
      
      mov ah,2
      mov dl,bl
      add dl,48
      int 21h
      
      exit:
      mov ah,4ch
      int 21h
      main endp
end main