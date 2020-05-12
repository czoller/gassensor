#include <Wire.h>
#include "MutichannelGasSensor.h"

void setup() {
    Serial.begin(115200);  // start serial for output
    gas.begin(0x04);//the default I2C address of the slave is 0x04
    gas.powerOn();
    Serial.println("GASES=NH3,CO,NO2,C3H8,C4H10,CH4,H2,C2H5OH");
    Serial.println("UNITS=ppm,ppm,ppm,ppm,ppm,ppm,ppm,ppm");
}

void loop() {
    float c;

    Serial.print("DATA=");

    c = gas.measure_NH3();
    if (c >= 0) {
        Serial.print(c);
    } else {
        Serial.print("invalid");
    }
    Serial.print(",");

    c = gas.measure_CO();
    if (c >= 0) {
        Serial.print(c);
    } else {
        Serial.print("invalid");
    }
    Serial.print(",");

    c = gas.measure_NO2();
    if (c >= 0) {
        Serial.print(c);
    } else {
        Serial.print("invalid");
    }
    Serial.print(",");

    c = gas.measure_C3H8();
    if (c >= 0) {
        Serial.print(c);
    } else {
        Serial.print("invalid");
    }
    Serial.print(",");

    c = gas.measure_C4H10();
    if (c >= 0) {
        Serial.print(c);
    } else {
        Serial.print("invalid");
    }
    Serial.print(",");

    c = gas.measure_CH4();
    if (c >= 0) {
        Serial.print(c);
    } else {
        Serial.print("invalid");
    }
    Serial.print(",");

    c = gas.measure_H2();
    if (c >= 0) {
        Serial.print(c);
    } else {
        Serial.print("invalid");
    }
    Serial.print(",");

    c = gas.measure_C2H5OH();
    if (c >= 0) {
        Serial.print(c);
    } else {
        Serial.print("invalid");
    }
    Serial.println();

    delay(1000);
}
