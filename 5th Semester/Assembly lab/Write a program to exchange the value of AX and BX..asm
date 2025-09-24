.DATA
         
.CODE
MAIN PROC
      MOV AX,DATA
      MOV DS,AX
      MOV AL,02
      MOV AH,09 
      MOV BH,03
      MOV BL,05     
      XCHG AX,BX 
      
      MOV AH,4CH
      INT 21h
      MAIN ENDP
END MAIN

