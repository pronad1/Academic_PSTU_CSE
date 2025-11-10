.MODEL SMALL
.STACK 100h

.DATA
    prompt_msg   DB 'Enter a number (-128 to 127): $'
    high_msg     DB 0Dh, 0Ah, 'HIGH VALUE$'      
    neg_msg      DB 0Dh, 0Ah, 'NEGATIVE VALUE$'
    med_msg      DB 0Dh, 0Ah, 'MEDIUM RANGE$'

    input_buffer LABEL BYTE
    max_len      DB 6       
    actual_len   DB ?       
    input_string DB 6 DUP('$') 
    
    input_val    DB ?       
    is_negative  DB 0       

.CODE
MAIN PROC
    MOV AX, @DATA
    MOV DS, AX   
    
    LEA DX, prompt_msg
    MOV AH, 09h         
    INT 21h

    LEA DX, input_buffer
    MOV AH, 0Ah         
    INT 21h

    
    LEA SI, input_string  
    XOR BX, BX            
    MOV CL, [actual_len]  
    XOR CH, CH           
    
    CMP BYTE PTR [SI], '-'
    JNE Parse_Loop        
    
    MOV [is_negative], 1  
    INC SI                
    DEC CX         

Parse_Loop:
    CMP CX, 0             
    JE Done_Parsing       
    
    MOV AL, [SI]          
    SUB AL, '0'                                          
    
    PUSH AX               
    MOV AX, BX            
    MOV DX, 10            
    MUL DX                
    MOV BX, AX            
    POP AX                
    ADD BL, AL           
    
    INC SI                
    DEC CX                
    JMP Parse_Loop        

Done_Parsing:
    CMP [is_negative], 1
    JNE Store_Value
    NEG BX               
    
Store_Value:
    MOV [input_val], BL
    
    MOV AH, 02h
    MOV DL, 0Dh
    INT 21h
    MOV DL, 0Ah
    INT 21h

    MOV AL, [input_val]
    
    CMP AL, 50
    JG L_HIGH            
    CMP AL, 0
    JL L_NEGATIVE        
    
L_MEDIUM:
    LEA DX, med_msg
    MOV AH, 09h
    INT 21h
    JMP L_END            

L_HIGH:
    LEA DX, high_msg
    MOV AH, 09h
    INT 21h
    JMP L_END           

L_NEGATIVE:
    LEA DX, neg_msg
    MOV AH, 09h
    INT 21h

L_END:
    ; Terminate the program
    MOV AH, 4Ch
    INT 21h

MAIN ENDP
END MAIN