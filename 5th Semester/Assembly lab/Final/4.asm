.MODEL SMALL
.STACK 100h
.DATA
ArrayA DB 10, 23, 45, 12, 8, 7, 19, 6, 30, 15
ArrayB DB 'H','e','l','l','o','A','I','O','U','b'
VowelSet DB 'AEIOUaeiou'
VowelCount DB 0
Sum DW 0

MsgArrayA DB 'Modified Array A: $'
MsgVowel DB 13,10,'Vowel Count: $'

.CODE
MAIN PROC
    MOV AX, @DATA
    MOV DS, AX

;============================
; Step 1: Reverse ArrayA
;============================
    LEA SI, ArrayA
    LEA DI, ArrayA+9
ReverseLoop:
    CMP SI, DI
    JAE ReverseDone
    MOV AL, [SI]
    MOV BL, [DI]
    MOV [SI], BL
    MOV [DI], AL
    INC SI
    DEC DI
    JMP ReverseLoop
ReverseDone:

;============================
; Step 2: Count vowels
;============================
    LEA SI, ArrayB
    MOV CX, 10
    MOV AL, 0
CountVowels:
    MOV AL, [SI]
    MOV DI, 0
CheckVowel:
    MOV BL, VowelSet[DI]
    CMP AL, BL
    JE VowelFound
    INC DI
    CMP DI, 10
    JL CheckVowel
    JMP NextChar
VowelFound:
    INC VowelCount
NextChar:
    INC SI
    LOOP CountVowels

;============================
; Step 3: Modify ArrayA
;============================
    LEA SI, ArrayA
    MOV CX, 10
    XOR AX, AX            ; sum
ModifyLoop:
    MOV AL, [SI]
    MOV BL, AL
    TEST BL, 1
    JZ EvenNum
OddNum:
    SUB BL, 3
    JMP Update
EvenNum:
    ADD BL, BL
Update:
    ADD AX, BX
    MOV [SI], BL
    INC SI
    CMP AX, 200h
    JA DoneModify
    LOOP ModifyLoop
DoneModify:

;============================
; Step 4: Display Modified Array A
;============================
    MOV DX, OFFSET MsgArrayA
    MOV AH, 09h
    INT 21h

    LEA SI, ArrayA
    MOV CX, 10
DisplayLoop:
    MOV AL, [SI]
    ; convert number to ASCII (supports 0-255)
    MOV AH, 0
    AAM                 ; divide AL by 10: AH = tens, AL = units
    ADD AH, '0'
    ADD AL, '0'
    MOV DL, AH
    MOV AH, 02h
    INT 21h
    MOV DL, AL
    MOV AH, 02h
    INT 21h
    MOV DL, ' '
    MOV AH, 02h
    INT 21h
    INC SI
    LOOP DisplayLoop

;============================
; Step 5: Display Vowel Count
;============================
    MOV DX, OFFSET MsgVowel
    MOV AH, 09h
    INT 21h

    MOV AL, VowelCount
    ADD AL, '0'
    MOV DL, AL
    MOV AH, 02h
    INT 21h

;============================
; Exit program
;============================
    MOV AH, 4Ch
    INT 21h

MAIN ENDP
END MAIN
