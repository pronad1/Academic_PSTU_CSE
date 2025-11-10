include 'emu8086.inc'      ; for scan_num (keyboard integer input)

org 100h
jmp start                  ; skip over data


; ---------- DATA ----------
N       dw ?              
RESULT  dw ?               

msgPrompt db 'Enter a non-negative number: $'
msgRes    db 0Dh,0Ah, 'Result = ', '$'

factorial:
    push bp
    mov  bp, sp           ; set up stack frame

    mov  ax, [bp+4]       ; AX = n
    cmp  ax, 0
    jz   base_case        ; if n == 0 ? 1

    ; ---- recursive case: n * factorial(n-1) ----
    dec  ax               ; AX = n-1
    push ax               ; push (n-1) as argument
    call factorial        ; AX = factorial(n-1)

    mov  bx, [bp+4]       ; BX = original n
    mul  bx               ; AX = AX * BX  (16-bit, so keep N small)
    jmp  fact_done

base_case:
    mov  ax, 1            ; 0! = 1

fact_done:
    pop  bp
    ret  2                ; remove 1 word parameter and return


; =====================================================
; print_dec:
; Prints AX as unsigned decimal using int 21h.
; =====================================================
print_dec:
    push bx
    push cx
    push dx

    cmp  ax, 0
    jne  pd_not_zero

    ; AX == 0 ? print '0'
    mov  dl, '0'
    mov  ah, 2
    int  21h
    jmp  pd_done

pd_not_zero:
    xor  cx, cx           ; digit count = 0

pd_loop:
    xor  dx, dx           ; clear DX before DIV
    mov  bx, 10
    div  bx               ; AX = AX / 10, remainder in DX
    push dx               ; save remainder (digit)
    inc  cx               ; digit++
    cmp  ax, 0
    jne  pd_loop

    ; print digits in reverse
pd_print:
    pop  dx
    add  dl, '0'          ; 0..9 ? '0'..'9'
    mov  ah, 2
    int  21h
    loop pd_print

pd_done:
    pop  dx
    pop  cx
    pop  bx
    ret


; ================== MAIN ==================
start:
    ; ----- prompt for input -----
    mov  dx, offset msgPrompt
    mov  ah, 9
    int  21h

    ; read signed integer from keyboard ? CX
    call scan_num         ; EMU8086 macro, from emu8086.inc
    mov  [N], cx          ; store user input in N

    ; ----- compute factorial(N) -----
    mov  ax, [N]
    push ax
    call factorial        ; AX = N!
    mov  [RESULT], ax

    ; ----- print "Result = " -----
    mov  dx, offset msgRes
    mov  ah, 9
    int  21h

    ; print RESULT in decimal
    mov  ax, [RESULT]
    call print_dec

    ; newline
    mov  dl, 0Dh
    mov  ah, 2
    int  21h
    mov  dl, 0Ah
    mov  ah, 2
    int  21h

    ; exit to DOS
    mov  ah, 4Ch
    int  21h


; needed for scan_num macro
DEFINE_SCAN_NUM

end start