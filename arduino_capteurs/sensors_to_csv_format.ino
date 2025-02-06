#include <Wire.h>
#include <BH1750.h>
#include <SimpleDHT.h>

#define DHTPIN 53
SimpleDHT22 dht22(DHTPIN);

int capteurs[5] = {A0, A2, A4, A6, A8}; // Capteurs d'humidité du sol
#define wetSol 27 // Seuil sol humide
#define drySol 42 // Seuil sol sec

BH1750 capteurLuminosite;  // Objet BH1750

void setup() {
  Serial.begin(9600);
  Wire.begin();
  capteurLuminosite.begin(BH1750::CONTINUOUS_HIGH_RES_MODE);
}

void loop() {
  float valeurs[8]; // Stocke toutes les valeurs à envoyer

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

  // Lecture du capteur de luminosité BH1750
  float lux = capteurLuminosite.readLightLevel();
  valeurs[7] = lux; // Valeur en lux (pas de conversion)

  // Envoi des valeurs sous format CSV
  for (int i = 0; i < 8; i++) {
    Serial.print(valeurs[i], 1);
    if (i < 7) Serial.print(",");
  }
  Serial.println();

  delay(900000); // Attente de 15 minutes
}
