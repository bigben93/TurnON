#include <avr/io.h>
#include <util/delay.h>
#include "config.h"

void USART_init (unsigned int ubrr)
{
    //set speed of transmission
    UBRRH = (unsigned char)(ubrr>>8);
    UBRRL = (unsigned char)ubrr;

    //enable transmission
    UCSRB = (1<<RXEN)|(1<<TXEN);

    //format ramki: bit startu, 8 bit danych, 2 bity stopu
    //format of frame: bit of start, 8 bits of data, 2 bits of stop
    UCSRC = (1<<USBS)|(3<<UCSZ0);

}

//function sending reply
void USART_transmit(char *data)
{
    int i=0;
    while (data[i] != '\0')
    {
        //waiting forwmpty buffer
        while ( !( UCSRA & (1<<UDRE)) ) ;

        //placing the data in the buffer and send
        UDR = data[i];
        i++;

    }

}

//functions received single char
char USART_receive(void)
{
    //waiting for data
    while ( !(UCSRA & (1<<RXC)) ) ;

    //sending data from buffer
    return UDR;
}

//checking format of frame
//function can return
//1 - good frame
//0 - bad frame
int frame_is_ok(char *command, int char_counter)
{
  if (command[0] == FRAME_START && command[char_counter] == FRAME_STOP) return 1;
  else return 0;
}

//fuction set relay
void relay_set(char *command)
{
    // informations about relays are from cell number 2
    int i = 2;

    //status mowi o stanie wykonania operacji
    //1- operacja wykonan bez problemu
    //0- wystapily bledy
    //status telling about status of executing operation
    //1- operation executed without problems
    //0- occurred some erros
    int status = 1;

    while (command[i] != 'n' && i < 8)
    {
        // 0 means "relay is turn off"
        if (command[i] == '0')
        {
            PORTB &= ~(1<<i);

        }

        //1 means "relay is turn on"
        else if (command[i] == '1')
        {
            PORTB |= (1<<i);

        }

        //if argument is other than 0 or 1 returned is error
        else
        {
            USART_transmit(ERROR_BAD_ARGUMENT);
            status = 0;

        }

       i++;
    }

    //sending message about status of operation
    if (status == 1)
    {
        USART_transmit(INFO_COMMAND_EXECUTE_OK);
    }

    else
    {
        USART_transmit(INFO_COMMAND_EXECUTE_WITH_ERRORS);
    }

}

//checking status of relays and sending it to computer
void relay_status(void)
{
    //i - number of pin
    int i = 2;
    //j - index of table. [0] is char of beginning frame
    int j = 1;
    //ttable with message to send
    char relay_status_tab[10] = "Rtest";

    while (i < 8)
    {
        if ( PORTB & (1 << i) )
        {
            relay_status_tab[j] = '1';
        }

        else if ( !(PORTB & (1 << i)) )
        {
            relay_status_tab[j] = '0';
        }

       i++;
       j++;
    }

    //endind of frame making. Adding chars ending frame
    relay_status_tab[7] = '\n';
    relay_status_tab[8] = '\r';

    //sending message about current status of relays
    USART_transmit(relay_status_tab);

}


int main()
{
	DDRB = 0b11111111;
	PORTB = 0b0000000;

	USART_init(MYUBRR);
	int char_counter = 0;
    char command[10] = "test";

	while (1)
	{
		char_counter = 0;

        //receiving chars until an FRAME_STOP
		while (char_counter < 9)
		{
		    command[char_counter] = USART_receive();

		    if (command[char_counter] == FRAME_STOP) break;
		    else ;

		    char_counter++;
		}

        //checking format of frame. on beggining must be FRAME_START
        if (frame_is_ok(command, char_counter))
        {
            switch (command[1])
            {
                case 'D':
                USART_transmit(DEVICE_ID);
                break;

                case 'S':
                relay_set(command);
                break;

                case 'I':
                relay_status();
                break;


                default:
                USART_transmit(ERROR_UNKNOWN_COMMAND);
                break;
            }
        }

        else USART_transmit(ERROR_BAD_FRAME);
	}
	return 0;
}
