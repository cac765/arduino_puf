/*==================================================================
 | Project: INF639 Project 3
 |
 | Author: Corey Cline
 + -----------------------------------------------------------------
 |
 | Description: Assembly program to dump all SRAM data onto Serial
 |				using ATMEGA328p Arduino board.
 |
 | Input: None, runs on boot
 |
 | Output: SRAM Data from memory address 0x0100 to 0x08FF
 |
 | Algorithm: Initialize USART and RAM begin, send bytes one at a
 |			  time and increment address until reach end, then jmp
 |			  to infinite loop to stop sending serial but keeping
 |			  data buffer open.
 |
 | Required Features Not Included: None
 |
 | Known Bugs: None
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
	ldi r16, 8							; =16MHz / (16 * 115200BAUD) - 1
	clr r17								; r16 r17 used to set 9600 baud rate

	sts UBRR0H, r17						; set baud rate
	sts UBRR0L, r16

	ldi r16, (1<<RXEN0) | (1<<TXEN0)	; enable Rx and Tx
	sts UCSR0B, r16

	ldi r16, (1<<USBS0) | (3<<UCSZ00)	; set frame format
	sts  UCSR0C, r16					; 8 data bits, no parity, 2 stop bits
	ret


;=======================
; receive a byte over serial wire
; byte received is stored in r20
USART_Receive:
	lds r16, UCSR0A						; wait for receive complete flag
	sbrs r16, RXC0
	rjmp USART_Receive

	lds r20, UDR0						; store data from buffer in r20
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
	
