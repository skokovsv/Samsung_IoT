/****************************************************************
GestureTest.ino
APDS-9960 RGB and Gesture Sensor
Shawn Hymel @ SparkFun Electronics
May 30, 2014
https://github.com/sparkfun/APDS-9960_RGB_and_Gesture_Sensor

Tests the gesture sensing abilities of the APDS-9960. Configures
APDS-9960 over I2C and waits for gesture events. Calculates the
direction of the swipe (up, down, left, right) and displays it
on a serial console. 

To perform a NEAR gesture, hold your hand
far above the sensor and move it close to the sensor (within 2
inches). Hold your hand there for at least 1 second and move it
away.

To perform a FAR gesture, hold your hand within 2 inches of the
sensor for at least 1 second and then move it above (out of
range) of the sensor.

Hardware Connections:

IMPORTANT: The APDS-9960 can only accept 3.3V!
 
Wemos Pin  APDS-9960 Board  Function
 
 3.3V         VCC              Power
 GND          GND              Ground
 D3           SDA              I2C Data
 D1           SCL              I2C Clock
 D6           INT              Interrupt
 D7           -                LED

Resources:
Include Wire.h and SparkFun_APDS-9960.h

Development environment specifics:
Written in Arduino 1.0.5
Tested with SparkFun Arduino Pro Mini 3.3V

This code is beerware; if you see me (or any other SparkFun 
employee) at the local, and you've found our code helpful, please
buy us a round!

Distributed as-is; no warranty is given.

Modified for ESP8266 by Jon Ulmer Nov 2016
****************************************************************/
void ICACHE_RAM_ATTR interruptRoutine();
#include <Wire.h>
#include <SparkFun_APDS9960.h>

#include <ESP8266WiFi.h>

#include <ESP8266WebServer.h>

//home
// #define WIFI_SSID "TP-Link_92A2"
// #define WIFI_PASS "33886985"

//mobile
#define WIFI_SSID "gesture"
#define WIFI_PASS "228359123"

const char* www_username = "admin";
const char* www_password = "0909";

// #define WIFI_SSID "AndroidAP2590"
// #define WIFI_PASS "baykal228"

// home wi-fi
// IPAddress staticIP(192,168,0,115);
// IPAddress gateway(192,168,0,254);
// IPAddress subnet(255,255,255,0);

// mobile wi-fi
IPAddress staticIP(172,20,10,10);
IPAddress gateway(172,20,10,1);
IPAddress subnet(255,255,255,240);



// Pins on wemos D1 mini
#define APDS9960_INT    12  //AKA GPIO12 -- Interupt pin
#define APDS9960_SDA    4  //AKA GPIO0
#define APDS9960_SCL    5  //AKA GPIO5
// Constants

// Global Variables
SparkFun_APDS9960 apds = SparkFun_APDS9960();
volatile bool isr_flag = 0;

int up = 13;
int down = 2;
int left = 14;
int right = 16;

ESP8266WebServer server(80);



void setup() {

  

  pinMode(up, OUTPUT);
  pinMode(down, OUTPUT);
  pinMode(left, OUTPUT);
  pinMode(right, OUTPUT);
   
   digitalWrite(up,LOW);
   delay(500);

   digitalWrite(up,HIGH);
  digitalWrite(down,LOW);
  delay(500);

  digitalWrite(down,HIGH);
  digitalWrite(left,LOW);
  delay(500);

  digitalWrite(left,HIGH);
  digitalWrite(right,LOW);
  delay(500);
  digitalWrite(right,HIGH);
  

  //Start I2C with pins defined above
  Wire.begin(APDS9960_SDA,APDS9960_SCL);

  // Set interrupt pin as input
  pinMode(APDS9960_INT, INPUT);

  // Initialize Serial port
  Serial.begin(115200);
  Serial.println();
  Serial.println(F("--------------------------------"));
  Serial.println(F("--------------------------------"));
  
  // Initialize interrupt service routine
  attachInterrupt(APDS9960_INT, interruptRoutine, FALLING);

  // Initialize APDS-9960 (configure I2C and initial values)
  if ( apds.init() ) {
    Serial.println(F("APDS-9960 initialization complete"));
  } else {
    Serial.println(F("Something went wrong during APDS-9960 init!"));
  }
  
  // Start running the APDS-9960 gesture sensor engine
  if ( apds.enableGestureSensor(true) ) {
    Serial.println(F("Gesture sensor is now running"));
  } else {
    Serial.println(F("Something went wrong during gesture sensor init!"));
  }

 
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  WiFi.config(staticIP, gateway, subnet);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  
  Serial.println("Connected");
  Serial.println(WiFi.localIP());

  server.on("/", handleRoot);

        
  server.on("/SwitchOn", handleSwitchOn); 
  server.on("/SwitchOff", handleSwitchOff);
  server.on("/UP", handleUP);
  server.on("/DOWN", handleDOWN);
  server.on("/LEFT", handleLEFT);
  server.on("/RIGHT", handleRIGHT);
  server.on("/INVERSE", handleINVERSE);
  server.on("/MODE_1", handleMODE_1);      
  server.on("/MODE_2", handleMODE_2);   

 
server.begin();
Serial.println("HTTP server started");

         
  
  
  // server.begin();                 
  // Serial.println("HTTP server started");
}

void loop() {

  server.handleClient();

  if( isr_flag == 1 ) {
    server.handleClient();
    
    detachInterrupt(APDS9960_INT);
    handleGesture();
    isr_flag = 0;
    attachInterrupt(APDS9960_INT, interruptRoutine, FALLING);
  }
}

void ICACHE_RAM_ATTR interruptRoutine() {
  isr_flag = 1;
}



// перехват жестов
void handleGesture() {
    if ( apds.isGestureAvailable() ) {
    switch ( apds.readGesture() ) {
      case DIR_UP:
        Serial.println("UP");
        digitalWrite(right,!digitalRead(right));
        break;
      case DIR_DOWN:
        Serial.println("DOWN");
        digitalWrite(left,!digitalRead(left));
        break;
      case DIR_LEFT:
        Serial.println("LEFT");
        digitalWrite(up,!digitalRead(up));
        break;
      case DIR_RIGHT:
        Serial.println("RIGHT");
        digitalWrite(down,!digitalRead(down));
        break;
      case DIR_NEAR:
        
        break;
      case DIR_FAR:
        Serial.println("FAR");
        digitalWrite(up,!digitalRead(up));
        digitalWrite(down,!digitalRead(down));
        digitalWrite(left,!digitalRead(left));
        digitalWrite(right,!digitalRead(right));
        break;
      default:
        Serial.println("NONE");
    }
  }
}

// веб-страница
void handleRoot() 
{

  if(!server.authenticate(www_username, www_password)) {
    return server.requestAuthentication();
  }


// pinMode( Sw1, OUTPUT); pinMode( Sw2, OUTPUT);
 Serial.println("You called root page");

 String MAIN_page = "<!DOCTYPE HTML><html><head>";

  MAIN_page+=" <meta charset=""utf-8"">";   // Шрифт 
  MAIN_page+="<title>LAMP</title>";   // Имя в запросе браузера
  MAIN_page+="<style type= ""text/css "">";  // Настройки стиля текста
  
  MAIN_page+="a.buttons { color: #fff; text-decoration: none;  user-select: none; background: rgb(0, 139, 139); padding: .7em 1.5em; outline: none;}" ;
  MAIN_page+="a.buttons:hover { background: rgb(32, 178, 170); }"; // эффект при наведении мышки "hover-эффект"
  MAIN_page+="a.buttons:active { background: rgb(0, 128, 128); }"; // эффект при нажатии левой кнопки мышки
  MAIN_page+=".div_but{ width: 1000px; }";
  MAIN_page+=".but_up{ text-align: center; }";
  MAIN_page+=".but_down{ text-align: center; }";
  MAIN_page+=".status{ text-align: center; }";
  
  MAIN_page+="h1 {font-family: 'Times New Roman', Times, serif; font-style: italic;}";
  MAIN_page+="</style></head>";
  MAIN_page+="<body style=""text-align: center"" bgcolor=""#ADD8E6"">";
  
  MAIN_page+="<h1>LAMP</h1>"; // Текст в начале страницы -Заголовок

  MAIN_page+="<div class=""status""><p>UP led is now: ";

  if(digitalRead(up)==0){
    MAIN_page+="<b>ON</b></p>";
  }
  else{
    MAIN_page+="<b>OFF</b></p>";
  }

  MAIN_page+="<p>DOWN led is now: ";

  if(digitalRead(down)==0){
    MAIN_page+="<b>ON</b></p>";
  }
  else{
    MAIN_page+="<b>OFF</b></p>";
  }

  MAIN_page+="<p>LEFT led is now: ";

  if(digitalRead(left)==0){
    MAIN_page+="<b>ON</b></p>";
  }
  else{
    MAIN_page+="<b>OFF</b></p>";
  }

  MAIN_page+="<p>RIGHT led is now: ";

  if(digitalRead(right)==0){
    MAIN_page+="<b>ON</b></p></div>";
  }
  else{
    MAIN_page+="<b>OFF</b></p></div>";
  }
  
  // buttons all led
  MAIN_page+="<a href=""SwitchOn"" class=""buttons"">Включить Led</a> <br><br><br>";
  MAIN_page+="<a href=""SwitchOff"" class=""buttons"">Выключить Led</a> <br><br><br>";
  MAIN_page+="<a href=""INVERSE"" class=""buttons"">Инверсия</a> <br><br><br>";

  //classic side buttons
  MAIN_page+="<div class=""div_but""> <p class=""but_up""><a href=""UP"" class=""buttons"">UP</a> </p><br><br>" ;
  

  MAIN_page+="<p><a style = ""margin-left:250px"" href=""LEFT"" class=""buttons"">LEFT</a> ";
  MAIN_page+="<a style = ""margin-left:700px"" href=""RIGHT"" class=""buttons"">RIGHT</a> </p> <br><br> ";

  MAIN_page+="<p class=""but_down""><a href=""DOWN"" class=""buttons"">DOWN</a></p></div>";

 //mode
  MAIN_page+="<a href=""MODE_1"" class=""buttons"">MODE 1</a> <br><br><br>";
  MAIN_page+="<a href=""MODE_2"" class=""buttons"">MODE 2</a> <br><br><br>";

  
  MAIN_page+="<br><br> </body></html>"; // конец страницы

  server.send(200, "text/html", MAIN_page); //Send web page
}
  



void handleSwitchOn()
{

  if(!server.authenticate(www_username, www_password)) {
    return server.requestAuthentication();
  }

  digitalWrite(up,LOW);
  digitalWrite(down,LOW);
  digitalWrite(left,LOW);
  digitalWrite(right,LOW);
  //  delay(1000);
  //  digitalWrite(d,LOW);
  
  server.sendHeader("Location", "/", true);
  server.send(302, "text/plane", "");
}

void handleSwitchOff()
{

  if(!server.authenticate(www_username, www_password)) {
    return server.requestAuthentication();
  }

  digitalWrite(up,HIGH); 
  digitalWrite(down,HIGH); 
  digitalWrite(left,HIGH); 
  digitalWrite(right,HIGH); 

  server.sendHeader("Location", "/", true);
  server.send(302, "text/plane", "");
}

void handleUP()
{

  if(!server.authenticate(www_username, www_password)) {
    return server.requestAuthentication();
  }

  int status = digitalRead(up);
  digitalWrite(up,!status); 
  
  int q = 5;

  server.sendHeader("Location", "/", true);
  server.send(302, "text/plane", "",q);
}

void handleDOWN()
{

  if(!server.authenticate(www_username, www_password)) {
    return server.requestAuthentication();
  }

  int status = digitalRead(down);
  digitalWrite(down,!status); 
  
  server.sendHeader("Location", "/", true);
  server.send(302, "text/plane", "");
}

void handleLEFT()
{
  if(!server.authenticate(www_username, www_password)) {
    return server.requestAuthentication();
  }

  int status = digitalRead(left);
  digitalWrite(left,!status); 
  

  server.sendHeader("Location", "/", true);
  server.send(302, "text/plane", "");
}

void handleRIGHT()
{
  if(!server.authenticate(www_username, www_password)) {
    return server.requestAuthentication();
  }

  int status = digitalRead(right);
  digitalWrite(right,!status); 
  

  server.sendHeader("Location", "/", true);
  server.send(302, "text/plane", "");
}

void handleINVERSE()
{
  if(!server.authenticate(www_username, www_password)) {
    return server.requestAuthentication();
  }

        digitalWrite(up,!digitalRead(up));
        digitalWrite(down,!digitalRead(down));
        digitalWrite(left,!digitalRead(left));
        digitalWrite(right,!digitalRead(right));
  

  server.sendHeader("Location", "/", true);
  server.send(302, "text/plane", "");
}

void handleMODE_1()
{

  digitalWrite(up,HIGH); 
  digitalWrite(down,HIGH); 
  digitalWrite(left,HIGH); 
  digitalWrite(right,HIGH); 

  for(int i=0;i<3;i++){
    digitalWrite(up,LOW);
    delay(300);
    digitalWrite(up,HIGH);
    digitalWrite(right,LOW);
    delay(300);
    digitalWrite(right,HIGH);
    digitalWrite(down,LOW);
    delay(300);
    digitalWrite(down,HIGH);
    digitalWrite(left,LOW);
    delay(300);
    digitalWrite(left,HIGH);
    delay(300);
  }
  
  server.sendHeader("Location", "/", true);
  server.send(302, "text/plane", "");
}

void handleMODE_2()
{

  digitalWrite(up,HIGH); 
  digitalWrite(down,HIGH); 
  digitalWrite(left,HIGH); 
  digitalWrite(right,HIGH); 

  for(int i=0;i<5;i++){
    digitalWrite(up,LOW);
    digitalWrite(down,LOW);
    delay(400);
    digitalWrite(up,HIGH);
    digitalWrite(down,HIGH);
    delay(400);
    digitalWrite(right,LOW);
    digitalWrite(left,LOW);
    delay(400);
    digitalWrite(right,HIGH);
    digitalWrite(left,HIGH);
    delay(400);
  }
  
  server.sendHeader("Location", "/", true);
  server.send(302, "text/plane", "");
}

