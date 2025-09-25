.model small
.stack 100h

.code
main proc
    mov ax,4h
    mov bx,1h
    
   next_guess:
   mov ax,4h
   div bx
   cmp ax,bx
   je done
   
   add bx,1
   jmp next_guess
   
   done:
   mov ax,bx
   
   
   exit:
   mov bx,4ch
   int 21h
   main endp
end main