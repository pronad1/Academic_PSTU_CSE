.DATA
    PROMPT  DB  'The 256 ASCII Characters are : $'

 .CODE
   MAIN PROC
     MOV AX, @DATA                ; initialize DS   
     MOV DS, AX

     LEA DX, PROMPT               ; load and print PROMPT 
     MOV AH, 9
     INT 21H

     MOV CX, 256                  ; initialize CX

     MOV AH, 2                    ; set output function  
     MOV DL, 0                    ; initialize DL with first ASCII character

     @LOOP:                       ; loop label
       INT 21H                    ; print ASCII character

       INC DL                     ; increment DL to next ASCII character
       DEC CX                     ; decrement CX
     JNZ @LOOP                    ; jump to label @LOOP if CX is 0

     MOV AH, 4CH                  ; return control to DOS
     INT 21H
   MAIN ENDP
 END MAIN