
	.MODEL SMALL
	.STACK 100H
	.DATA
		d1 dw 16
	.CODE
		MAIN PROC FAR
		MOV AX,@DATA
		MOV DS,AX

	MOV ax,d1 
	
	mov BX,02H
	MOV CX,00H
	MOV DX,00H 
	
	again:
    DIV BX;
    PUSH DX;
    INC CX;
    
    CMP AX,0;
    
    JNE again  
    
    
    
    L1:
    pop dx  
    
    ADD DX,48
    
    MOV AH,02H  
    
    INT 21H
    
    LOOP L1
     
    
    MOV AH,4CH
    INT 21H
    
    MAIN ENDP
    
END MAIN	
	
	
	
	
	
	
	
	