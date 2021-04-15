#define GEN_REG_START 0x0000
#define IO_REG_START 0x0020
#define EXT_IO_REG_START 0x0060
#define SRAM_START 0x0100
#define SRAM_END 0x08FF

//uint8_t *ptr = 0;
char buf[3] = {0};

void setup() 
{
    Serial.begin(115200);
    while (!Serial);

    uint8_t *ptr = 0;
    byte val;

    Serial.println("SRAM:");
    for (ptr = SRAM_START; ptr <= SRAM_END; ptr++)
    {
        val = *ptr;
        sprintf(buf, "%02X ", val);
        Serial.print(buf);
        Serial.print(" ");
        //Serial.println((int)ptr);
    }
}

void loop() 
{
    while(1);   
}
