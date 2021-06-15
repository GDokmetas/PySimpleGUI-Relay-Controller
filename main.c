/*
 * SerialRole_2.c
 *
 * Created: 13.06.2021 13:57:00
 * Author : PC
 */ 

#include <avr/io.h>
#define F_CPU 16000000UL
#include <util/delay.h>
#include <avr/interrupt.h>
#define BAUD 9600
#define BAUDRATE ((F_CPU)/(BAUD*16UL)-1)
void uart_basla(uint32_t baud);
void uart_gonder(uint8_t data);
void uart_string(const char *s );
volatile uint8_t a;
int main(void)
{
	
	uart_basla(9600);

	sei();
	DDRD |= (1<<PORTD4);
	DDRD |= (1<<PORTD5);
	DDRD |= (1<<PORTD6);
	DDRD |= (1<<PORTD7);
	
	_delay_ms(100); // MCU Kendine Gelsin
	while (1)
	{
		if (a=='1')
		PORTD |= (1<<4);
		if (a=='2')
		PORTD &= ~(1<<4);
		if (a=='3')
		PORTD |= (1<<5);
		if (a=='4')
		PORTD &= ~(1<<5);
		if (a=='5')
		PORTD |= (1<<6);
		if (a=='6')
		PORTD &= ~(1<<6);
		if (a=='7')
		PORTD |= (1<<7);
		if (a=='8')
		PORTD &=~(1<<7);
	}
}



void uart_basla(uint32_t baud){
	uint16_t baudRate=F_CPU/baud/16-1;
	UBRR0H=(baudRate>>8);
	UBRR0L=baudRate;
	UCSR0B|=(1<<RXEN0)|(1<<TXEN0);
	UCSR0C|=(1<<UCSZ01)|(1<<UCSZ00);
	UCSR0B |= (1<<RXCIE0);
}


ISR (USART_RX_vect)
{
	while(!(UCSR0A & (1<<RXC0)));
	a = UDR0;
}

