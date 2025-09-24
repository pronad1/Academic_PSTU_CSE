.MODEL SMALL
.DATA
M1 DB 0AH,0DH,'enter M : $'
M2 DB 0AH,0DH,'enter N : $'
M3 DB 0AH,0DH,'RESULT IS $'
.CODE
MAIN PROC
MOV AX,@DATA
MOV DS,AX
MOV AH,9
LEA DX,M1
INT 21H
;--------

MOV BX,AX ; M in BX
MOV AH,9
LEA DX,M2
INT 21H

PUSH AX
;----------------
MOV AH,9
LEA DX,M3
INT 21H
MOV AH,2 ;print " . "
MOV DL,'.'

INT 21H
;----------------
POP AX
XCHG AX,BX ;AX is M BX is N
WHILE_: MOV CX,10
MOV DX,0
IMUL CX ;AX=AX*10
DIV BX

MOV AX,DX ;Replace M by R
CMP DX,0
JNE WHILE_
;----------------
;------------------------------
MOV AH,4CH
INT 21H
MAIN ENDP


END MAIN


