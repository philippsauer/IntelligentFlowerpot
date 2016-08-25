#include <DHT.h>
#include <VirtualWire.h>
#include <NewPing.h>

#define DHTPIN 2     // what digital pin we're connected to
#define DHTTYPE DHT22   // DHT 22  (AM2302), AM2321
#define TRIGGER_PIN  12  // Arduino pin tied to trigger pin on the ultrasonic sensor.
#define ECHO_PIN     11  // Arduino pin tied to echo pin on the ultrasonic sensor.
#define MAX_DISTANCE 200 // Maximum distance we want to ping for (in centimeters). Maximum sensor distance is rated at 400-500cm.

DHT dht(DHTPIN, DHTTYPE);
NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE); // NewPing setup of pins and maxim

void setup()
{
  Serial.begin(9600);
  Serial.println("DHT22 Data Test!");

  vw_set_ptt_inverted(true);
  vw_set_tx_pin(8);
  vw_setup(2000);
  
  dht.begin();
  
}

void loop()
{
  delay(2000);
  
//  // Read Humidity as Celsius (the default)
  float tH = dht.readHumidity();
//  // Read temperature as Celsius (the default)
  float tT = dht.readTemperature();
  
  int h = (int)(tH*100); // float to int
  int t = (int)(tT*100); // float to int
  int s = sonar.ping_cm();
  
  char sensordata[15];
  
  sprintf(sensordata, "%d:%d:%d", h,t,s); 
 
 
  Serial.print("Luftfeuchtigkeit: ");
  Serial.print(h);
  Serial.print(" %\t");
  Serial.print("Temperatur: ");
  Serial.print(t);
  Serial.print(" %\t");
  Serial.print("Distanz: ");
  Serial.print(s);
  Serial.print(" cm\t");
  Serial.print("\n");

  vw_send((uint8_t*)sensordata, strlen(sensordata));
  vw_wait_tx();
  delay(200);
}
