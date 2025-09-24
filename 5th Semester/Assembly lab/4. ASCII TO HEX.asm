.MODEL SMALL
.DATA
M1 DB 0AH,0DH,'TYPE A CHARACTER :','$'
M2 DB 0AH,0DH,'THE ASCII CODE OF '
C1 DB ?,' IN HEXA IS ','$'
.CODE
MAIN PROC
MOV AX,@DATA ;intialize DS
MOV DS,AX
;------------
BEGIN: MOV AH,9 ;prompt user
LEA DX,M1
INT 21h
MOV AH,1 ;read char.
INT 21H
CMP AL,0DH ;if CR exit
JE OUT_
MOV C1,AL ;store char.
MOV BL,AL ;take a copy of char
MOV AH,9 ;display 2nd MSG
LEA DX,M2

INT 21H
;-------------

MOV CL,4
SHR C1,CL ;prapare for display 1st half
;* note below
ADD C1,30H ;convert to char.
MOV DL,C1
JMP EXE1
continue: AND BL,0FH ;convert 2nd half to char.
CMP BL,9 ;if >9 mean A,B,C…..hex ch.
JG ERROR_
ADD BL,30H ;convert to char.
MOV DL,BL
JMP EXE2
EXE1: MOV AH,2 ;1st half displayed
INT 21H
JMP continue
EXE2: MOV AH,2
INT 21H ;2nd half displayed
JMP BEGIN ;ask if you want to do it again
;------------
ERROR_: ADD BL,37H ;convert to A,B,C…. hexa ch.
MOV DL,BL
MOV AH,2 ;display it

INT 21H

JMP BEGIN ;ask if you want to do it again
OUT_: MOV AH,4CH ;return to DOS
INT 21H
MAIN ENDP
END MAIN



