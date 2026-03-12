#include <SPI.h>
#include <RH_RF95.h>
#include <Console.h>
#include <Process.h>

RH_RF95 rf95;
String apiKey = "W07OV1U1NLAAMCTG";
float frequency = 868.0;

void setup() {
  Bridge.begin(115200);
  Console.begin();
  rf95.init();
  rf95.setFrequency(frequency);
  rf95.setTxPower(13);
  Console.println("Gateway prête : GPS + BPM");
}

void loop() {
  if (rf95.waitAvailableTimeout(3000)) {
    uint8_t buf[RH_RF95_MAX_MESSAGE_LEN];
    uint8_t len = sizeof(buf);

    if (rf95.recv(buf, &len)) {
      String data = "";
      for (int i = 0; i < len; i++) {
        data += (char)buf[i];
      }

      Console.print("Trame reçue : ");
      Console.println(data);

      // Séparer lat, lon, bpm
      int idx1 = data.indexOf(',');
      int idx2 = data.indexOf(',', idx1 + 1);

      if (idx1 > 0 && idx2 > idx1) {
        String lat = data.substring(0, idx1);
        String lon = data.substring(idx1 + 1, idx2);
        String bpm = data.substring(idx2 + 1);

        Console.println("Latitude : " + lat);
        Console.println("Longitude : " + lon);
        Console.println("BPM : " + bpm);

        String urlData = "field1=" + lat + "&field2=" + lon + "&field3=" + bpm;
        uploadToThingSpeak(urlData);
      }
    }
  }
}

void uploadToThingSpeak(String data) {
  String url = "http://api.thingspeak.com/update?api_key=" + apiKey + "&" + data;

  Console.println("Envoi à ThingSpeak :");
  Console.println(url);

  Process p;
  p.begin("curl");
  p.addParameter("-k");
  p.addParameter(url);
  Console.println("Url envoyé :" + url);
  p.run();
  int code=p.exitValue();
  Console.print("Code retour curl : ");
  Console.println(code);
  Console.println("Réponse ThingSpeak :");
  while (p.available()) {
    char c = p.read();
    Console.write(c);
  }

  Console.println("\n===============================");
}
