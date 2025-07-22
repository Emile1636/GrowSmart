#include <Wire.h>
#include <SimpleDHT.h>
#include <Adafruit_AS7341.h>

#define DHTPIN 53
SimpleDHT22 dht22(DHTPIN);
int capteurs[5] = {A0, A2, A4, A6, A8}; // Capteurs d'humidité du sol
#define wetSol 27 // Seuil sol humide
#define drySol 42 // Seuil sol sec

Adafruit_AS7341 as7341;    // Objet AS7341

void setup() {
  Serial.begin(9600);
  Wire.begin();
  
  // Initialisation du capteur spectral AS7341
  if (!as7341.begin()) {
    Serial.println("Erreur d'initialisation du capteur AS7341!");
  } else {
    // Configuration du capteur AS7341
    as7341.setATIME(100);
    as7341.setASTEP(999);
    as7341.setGain(AS7341_GAIN_256X);
  }
}

void loop() {
  float valeurs[17]; // Stocke toutes les valeurs (suppression du BH1750)
  
  // Lecture des capteurs d'humidité du sol
  for (int i = 0; i < 5; i++) {
    int humiditeSol = analogRead(capteurs[i]); 
    valeurs[i] = humiditeSol / 1023.0 * 100.0; // Conversion en %
  }
  
  // Lecture du capteur DHT22 (température et humidité)
  float temperature = 0, humidite = 0;
  int err = dht22.read2(&temperature, &humidite, NULL);
  if (err == SimpleDHTErrSuccess) {
    valeurs[5] = humidite;
    valeurs[6] = temperature;
  } else {
    valeurs[5] = -1; // Code d'erreur pour l'humidité
    valeurs[6] = -1; // Code d'erreur pour la température
  }
  
  // Lecture du capteur spectral AS7341
  if (as7341.readAllChannels()) {
    valeurs[7] = as7341.getChannel(AS7341_CHANNEL_415nm_F1);  // Violet (415nm)
    valeurs[8] = as7341.getChannel(AS7341_CHANNEL_445nm_F2);  // Indigo (445nm)
    valeurs[9] = as7341.getChannel(AS7341_CHANNEL_480nm_F3);  // Bleu (480nm)
    valeurs[10] = as7341.getChannel(AS7341_CHANNEL_515nm_F4); // Cyan (515nm)
    valeurs[11] = as7341.getChannel(AS7341_CHANNEL_555nm_F5); // Vert (555nm)
    valeurs[12] = as7341.getChannel(AS7341_CHANNEL_590nm_F6); // Jaune (590nm)
    valeurs[13] = as7341.getChannel(AS7341_CHANNEL_630nm_F7); // Orange (630nm)
    valeurs[14] = as7341.getChannel(AS7341_CHANNEL_680nm_F8); // Rouge (680nm)
    valeurs[15] = as7341.getChannel(AS7341_CHANNEL_CLEAR);    // Clear
    valeurs[16] = as7341.getChannel(AS7341_CHANNEL_NIR);      // Proche infrarouge
  } else {
    // En cas d'erreur de lecture, remplir avec -1
    for (int i = 7; i < 17; i++) {
      valeurs[i] = -1;
    }
  }
  
  // Envoi des valeurs sous format CSV
  for (int i = 0; i < 17; i++) {
    Serial.print(valeurs[i], 1);
    if (i < 16) Serial.print(",");
  }
  Serial.println();
  
  delay(900000); // Attente de 15 minutes
}
