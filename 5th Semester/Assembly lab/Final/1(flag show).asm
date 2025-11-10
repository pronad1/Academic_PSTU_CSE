include 'emu8086.inc'      ; for scan_num (keyboard integer input)

org 100h

jmp start                  ; skip over data


; ---------- DATA ----------
NUM1    db ?               ; user input 1 (8-bit)
NUM2    db ?               ; user input 2 (8-bit)
RESULT  db ?               ; final 8-bit result
CFVAL   db ?               ; '0' or '1' for CF
ZFVAL   db ?               ; '0' or '1' for ZF

msgIn1  db 'Enter NUM1 (0..255): $'
msgIn2  db 0Dh,0Ah, 'Enter NUM2 (0..255): $'
msgCF   db 0Dh,0Ah, 'CF = ', '$'
msgZF   db 0Dh,0Ah, 'ZF = ', '$'
msgRes  db 0Dh,0Ah, 'RESULT (hex) = ', '$'


; ---------- CODE ----------
start:

    ; ===== read NUM1 from user =====
    mov  dx, offset msgIn1
    mov  ah, 9
    int  21h

    call scan_num          ; signed/unsigned integer in CX
    mov  al, cl            ; take low 8 bits
    mov  NUM1, al

    ; ===== read NUM2 from user =====
    mov  dx, offset msgIn2
    mov  ah, 9
    int  21h

    call scan_num
    mov  al, cl
    mov  NUM2, al

    ; ===== 1) Load NUM1 and NUM2 =====
    mov  al, NUM1          ; AL = NUM1
    mov  bl, NUM2          ; BL = NUM2

    ; ===== 2) NUM1 - NUM2 using SBB (SUBB) =====
    clc                     ; clear carry so "borrow" = 0
    sbb  al, bl             ; AL = NUM1 - NUM2 - CF

    ; ===== 3) Rotate result left through carry 3 times (ROL) =====
    rol  al, 1
    rol  al, 1
    rol  al, 1

    ; ===== 4) Add rotated result with original NUM1 using ADC =====
    mov  bl, NUM1
    adc  al, bl            ; AL = AL + NUM1 + CF

    ; ===== 5) Logical right shift of final result by 2 bits =====
    shr  al, 1
    shr  al, 1

    ; ===== 6) Store final result in RESULT =====
    mov  RESULT, al

    ; ===== capture CF and ZF after last SHR =====

    ; CF
    mov  dl, '1'
    jc   cf_is_one
    mov  dl, '0'
cf_is_one:
    mov  CFVAL, dl

    ; ZF
    mov  dl, '1'
    jz   zf_is_one
    mov  dl, '0'
zf_is_one:
    mov  ZFVAL, dl

    ; ===== 7) Display RESULT (hex), CF and ZF =====

    ; print "RESULT (hex) = "
    mov  dx, offset msgRes
    mov  ah, 9
    int  21h

    ; show RESULT as 2 hex digits
    mov  al, RESULT
    call print_hex8        ; small helper below

    ; print "CF = "
    mov  dx, offset msgCF
    mov  ah, 9
    int  21h
    mov  dl, CFVAL
    mov  ah, 2
    int  21h

    ; print "ZF = "
    mov  dx, offset msgZF
    mov  ah, 9
    int  21h
    mov  dl, ZFVAL
    mov  ah, 2
    int  21h

    ; exit to DOS
    mov  ah, 4Ch
    int  21h


; ===== helper: print AL as 2 hex digits =====
; uses: AL, destroys AH, BL, CL, DL
print_hex8:
    push ax
    push bx
    push cx
    push dx

    mov  bl, al           ; BL = value
    mov  cx, 2            ; 2 hex digits

next_nibble:
    rol  bl, 4            ; high nibble ? low nibble
    mov  dl, bl
    and  dl, 0Fh
    add  dl, '0'
    cmp  dl, '9'
    jbe  ph_out
    add  dl, 7            ; 'A'..'F'
ph_out:
    mov  ah, 2
    int  21h
    loop next_nibble

    pop  dx
    pop  cx
    pop  bx
    pop  ax
    ret


; needed for scan_num macro
DEFINE_SCAN_NUM

end start
