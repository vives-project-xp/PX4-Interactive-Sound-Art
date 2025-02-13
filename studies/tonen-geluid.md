# Tonen

Noten/ toonhoogtes kunnen in verschillende sleutels bevinden, dit zorgt ervoor dat de instrumenten "mooi" samen klinken zolang
de noten die gespeeld worden in die toonlader/sleutel horen. We kunnen ook kijken als alle 12 noten mogelijk zijn. Je kunt het best beginnen met de sleutel die alle witte noten bevat: C-majeur (C D E F G A B C). (pentatonisch is misschien ook mogelijk)

![volledige 12 noten](fotos/image.png)

# Hoe?

- afstand binnenlezen via ultrasone sensor (berekening afstand: Afstand = (Tijd∗Snelheidvangeluid)/2)
- Zet om naar frequentie of sample 
- speelt toon af met juist pitch of sample


- Bv: om de 10cm een noot (dus 120cm)
- 1 noot die doorklinkt (dus we werken met hele noten voor te beginnen)
- Voorlopig met apparte files werken, (misschien later noten in code veranderen)
- Latere uitbreiding (akkoorden, gebroken akkoorden, arpegio's etc...)

- Voor te beginnen, raad ik aan om om de 10 cm, een noot te laten spelen, (dus 70cm in totaal) of  om de 20 cm (dus 140cm in totaal). Dus de 30-40cm range zal bv een C5 spelen en de 40-50cm range zal de D5 spelen (hogere noot)

## Voorbeeldcode met samples

```using System;
using System.IO;
using System.Threading;
using NAudio.Wave;

class Program
{
    static bool running = true;
    static int distance = 50; // Startafstand in cm
    static string basePath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "..", "..", "..", "..", "samples");
    static Dictionary<int, string> distanceToSample = new Dictionary<int, string>
    {
        { 10, Path.Combine(basePath, "a.mp3") },
        { 20, Path.Combine(basePath, "b.mp3") },
        { 30, Path.Combine(basePath, "c.mp3") },
        { 40, Path.Combine(basePath, "d.mp3") },
        { 50, Path.Combine(basePath, "e.mp3") },
        { 60, Path.Combine(basePath, "f.mp3") },
        { 70, Path.Combine(basePath, "g.mp3") }
    };

    static void Main()
    {
        Console.WriteLine("Gebruik de pijltjestoetsen om de afstand te veranderen. Druk op Escape om te stoppen.");
        Console.WriteLine("Zoeken naar bestanden in: " + basePath);

        while (running)
        {
            if (Console.KeyAvailable)
            {
                var key = Console.ReadKey(true).Key;
                if (key == ConsoleKey.Escape)
                {
                    running = false;
                }
                else if (key == ConsoleKey.UpArrow)
                {
                    distance = Math.Min(70, distance + 10);
                }
                else if (key == ConsoleKey.DownArrow)
                {
                    distance = Math.Max(10, distance - 10);
                }

                Console.Clear();
                Console.WriteLine("Huidige afstand: " + distance + " cm");
                if (distanceToSample.ContainsKey(distance))
                {
                    string sample = distanceToSample[distance];
                    Console.WriteLine("Afspelen: " + sample);
                    Thread soundThread = new Thread(() => PlaySample(sample));
                    soundThread.Start();
                }
            }
        }
    }

    static void PlaySample(string samplePath)
    {
        if (File.Exists(samplePath))
        {
            using (var audioFile = new Mp3FileReader(samplePath))
            using (var outputDevice = new WaveOutEvent())
            {
                outputDevice.Init(audioFile);
                outputDevice.Play();
                while (outputDevice.PlaybackState == PlaybackState.Playing)
                {
                    Thread.Sleep(100);
                }
            }
        }
        else
        {
            Console.WriteLine("Sample niet gevonden: " + samplePath);
        }
    }
}
```