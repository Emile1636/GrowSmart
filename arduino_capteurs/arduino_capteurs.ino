#include <SimpleDHT.h>

#define DHTPIN 53        // Broche DATA du DHT22 sur la pin 53 
#define LDR_PIN A15      // Broche capteur de lumière sur la pin A15
SimpleDHT22 dht22(DHTPIN);

int capteurs[5] = {A0, A2, A4, A6, A8}; // Broches des capteurs d'humidité du sol
#define wetSol 27   // Valeur max considérée comme sol 'mouillé' (en %)
#define drySol 42   // Valeur min considérée comme sol 'sec' (en %)

void setup() {
  Serial.begin(9600);
}

void loop() {
  // Lecture et affichage des données des capteurs d'humidité du sol
  for (int i = 0; i < 5; i++) {
    int humiditeSol = analogRead(capteurs[i]); // Lire la broche analogique (0-1023)
    float humiditePourcentage = humiditeSol / 1023.0 * 100.0; // Conversion en %

    // Affichage compact des capteurs de sol
    Serial.print(" C");
    Serial.print(i + 1);
    Serial.print(": ");
    Serial.print(humiditePourcentage, 1);
    Serial.print("% - ");
    
    if (humiditePourcentage < wetSol) {
      Serial.print("Sol trop humide");
    } else if (humiditePourcentage >= wetSol && humiditePourcentage < drySol) {
      Serial.print("Humidité idéale");
    } else {
      Serial.print("Sol trop sec");
    }
    Serial.println();
  }

  // Lecture et affichage des données du capteur DHT22
  float temperature = 0;
  float humidite = 0;
  int err = dht22.read2(&temperature, &humidite, NULL);
  
  if (err != SimpleDHTErrSuccess) {
    Serial.println("Erreur de lecture du capteur DHT22 !");
  } else {
    Serial.print(" Humidité ambiante: ");
    Serial.print(humidite, 1);
    Serial.println(" %");
    Serial.print(" Température ambiante: ");
    Serial.print(temperature, 1);
    Serial.println("Â°C ");
  }
  
  // Lecture et affichage des données du capteur de lumire
  int valeurBrute = analogRead(LDR_PIN);  // Lecture de la tension du LDR (0-1023)
  float pourcentageLuminosite = (valeurBrute / 1023.0) * 100.0; // Conversion en %

  Serial.print(" Luminosité: ");
  Serial.print(pourcentageLuminosite, 1);
  Serial.println("%");

  Serial.println("-----------------------------");
  delay(900000); // Attente de 15 minutes avant de recommencer
}
