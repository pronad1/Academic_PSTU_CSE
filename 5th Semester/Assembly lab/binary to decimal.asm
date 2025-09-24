
INCLUDE 'EMU8086.INC'
.model small
.stack 100h
.data

.code
main proc
    mov BX,0
    mov AH,1
    FOR1: 
    INT 21H
   
   
   CMP AL,0DH
   JE END_FOR1
   SUB AL,30H
   SHL BX,1 
   OR BL,AL
   JMP FOR1
   
  
   
    END_FOR1: 
     PRINTN
    
    mov AH,2 
    ADD BL,30H
    MOV DL,BL
    int 21h
    
    exit:
    mov ah,4ch
    int 21h
    main endp
end main