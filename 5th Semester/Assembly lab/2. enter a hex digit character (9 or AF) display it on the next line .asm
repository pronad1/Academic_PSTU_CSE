.MODEL SMALL
.STACK 64
;------------------------------------
.DATA
CR EQU 0DH
LF EQU 0AH
M1 DB CR,LF,'ENTER A HEXA DIGIT :','$'
M2 DB CR,LF,'IN DECIMAL IT IS :'
C1 DB ?,'$'
M3 DB CR,LF,'DO YOU WANT TO DO IT AGAIN ?$'
DB 'Y/N','$'
M4 DB CR,LF,'ILLEGAL CHARACTER - ENTER $'
DB '0..9OR A..F :','$'
M5 DB CR,LF,'IN DECIMAL IT IS :1'
C2 DB ?,'$'
;-----------------------------------
.CODE
MAIN PROC
MOV AX,@DATA ;Initialize DS
MOV DS,AX
BEGIN: MOV AH,9
LEA DX,M1
INT 21H
;--------
NEW: MOV AH,1 ;read hexa digit
INT 21H
;--------
CMP AL,'0' ;detictive for errors
JL ILLEGAL
CMP AL,'9'
JG ILLEGAL
;--------
MOV C1,AL
MOV AH,9
LEA DX,M2
INT 21H
;--------
MSG: MOV AH,9 ; do you want to do it again
LEA DX,M3
INT 21H
;---------
MOV AH,1 ; yes or no
INT 21H
CMP AL,'Y'
JE BEGIN
CMP AL,'y'
JE BEGIN
JMP ENDD ;any char. else go out
;---------
ILLEGAL: CMP AL,'A' ; detictive for letter error
JL ILLEGAL2
CMP AL,'F'
JG ILLEGAL2
SUB AL,11H
MOV C2,AL
;--------
MOV AH,9
LEA DX,M5
INT 21H
;---------
JMP MSG
;--------
ILLEGAL2: MOV AH,9
LEA DX,M4
INT 21H
JMP NEW
ENDD: MOV AH,4CH
INT 21H
MAIN ENDP
END MAIN