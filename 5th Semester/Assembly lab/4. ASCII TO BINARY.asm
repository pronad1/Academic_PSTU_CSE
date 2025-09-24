.MODEL SMALL
.DATA
M1 DB 'TYPE A CHARACTER :','$'
M2 DB 0AH,0DH,'THE ASCII CODE OF '
C1 DB ?,' IN BINARY IS :','$'
M3 DB 0AH,0DH,'THE NUMBER OF 1 BIT IS '
C2 DB ?,'$'
.CODE
MAIN PROC
MOV AX,@DATA ;Initialize DS
MOV DS,AX
MOV AH,9 ;prompt the user
LEA DX,M1
INT 21H
;-------------
MOV AH,1 ;read character
INT 21H
MOV BL,AL
MOV C1,AL ;store character
MOV AH,9 ;display results


LEA DX,M2
INT 21H

MOV BH,0 ;counter for one’s
MOV CX,8
MOV AH,2
L1: SHL BL,1 ;display content of BL
JC L2
MOV DL,'0'
INT 21H
JMP L4
L2: MOV DL,'1'
INT 21H
INC BH ;count number of one’s
L4: LOOP L1
ADD BH,30H ;convert to char.
MOV C2,BH
MOV AH,9 ;display number of one’s
LEA DX,M3
INT 21H
;-------------------
MOV AH,4CH ;return to DOS
INT 21H
MAIN ENDP
END MAIN


