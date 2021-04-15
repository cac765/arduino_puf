/*==================================================================
 | Project: ASSIGNMENT NUMBER AND TITLE
 |
 | Author: STUDENT’S NAME HERE
 + -----------------------------------------------------------------
 |
 | Description: DESCRIBE THE PROBLEM THAT THIS PROGRAM WAS WRITTEN  
 |              TO SOLVE.
 |
 | Input: DESCRIBE THE INPUT THAT THE PROGRAM REQUIRES.
 |
 | Output: DESCRIBE THE OUTPUT THAT THE PROGRAM PRODUCES.
 |
 | Algorithm: OUTLINE THE APPROACH USED BY THE PROGRAM TO SOLVE THE
 | PROBLEM.
 |
 | Required Features Not Included: DESCRIBE HERE ANY REQUIREMENTS OF
 | THE ASSIGNMENT THAT THE PROGRAM DOES NOT ATTEMPT TO SOLVE.
 |
 | Known Bugs: IF THE PROGRAM DOES NOT FUNCTION CORRECTLY IN SOME
 | SITUATIONS, DESCRIBE THE SITUATIONS AND PROBLEMS HERE.
 |
 *================================================================*/  


;=======================
; setup the interrupt vector
; next instr gets written to addr 0x0000
.ORG 0x0000								; next instruction address 0x0000
	jmp reset							; PC = 0x0000 RESET


;=======================
; initialization
;
reset:
	clr r1								; set SREG to 0
	out SREG, r1

	ldi r28, LOW(RAMEND)				; init stack pointer to point to RAMEND
	ldi r29, HIGH(RAMEND)
	out SPL, r28
	out SPH, r29

	rcall USART_Init					; initialize serial communications
	sei									; enable global interrupts
	rjmp main


;=======================
; initialize the USART
;
USART_Init:
	ldi r16, 103						; =16MHz / (16 * 9600BAUD) - 1
	clr r17								; r16 r17 used to set 9600 baud rate

	sts UBRR0H, r17						; set baud rate
	sts UBRR0L, r16

	ldi r16, (1<<RXEN0) | (1<<TXEN0)	; enable Rx and Tx
	sts UCSR0B, r16

	ldi r16, (1<<USBS0) | (3<<UCSZ00)	; set frame format
	sts  UCSR0C, r16					; 8 data bits, no parity, 2 stop bits
	ret


;=======================
; send a byte over serial wire
; byte to send is in r19
USART_Transmit:
	lds r16, UCSR0A						; wait for empty transmit buffer
	sbrs r16, UDRE0						
	rjmp USART_Transmit

	sts UDR0, r19						; put data (r19) into buffer, sends the data
	ret


;=======================
; main program body
;
main:
	ldi r26, LOW(0x0100)				; load SRAM start address into upper and lower bytes
	ldi r27, HIGH(0x0100)


SRAM_Byte:
	ld r19, X+							; load value (r19) from SRAM address and increment
	rcall USART_Transmit				; transmit byte (r19) through USART

	cpi r27, 0x09						; check if X=0x0900 at end of SRAM address
	breq stop							; branch if result zero

	rjmp SRAM_Byte						; otherwise continue

stop:
	rjmp stop							; Program "End"


.EXIT									; tells assembler it's over here!
	
