#ifndef CONFIG_H_INCLUDED
#define CONFIG_H_INCLUDED

#define BAUD 9600
#define MYUBRR F_CPU/16/BAUD-1
#define FRAME_START 'R'
#define FRAME_STOP 'n'


//constans with commands
#define DEVICE_ID "RelayCardByBigBen\n\r"
#define ERROR_BAD_FRAME "Rerror01\n\r"
#define ERROR_UNKNOWN_COMMAND "Rerror02\n\r"
#define ERROR_BAD_ARGUMENT "Rerror03\n\r"
#define ERROR_UNKNOWN "Rerror04\n\r"
#define INFO_COMMAND_EXECUTE_OK "Rcok\n\r"
#define INFO_COMMAND_EXECUTE_WITH_ERRORS "Rcer\n\r"

#endif // CONFIG_H_INCLUDED
