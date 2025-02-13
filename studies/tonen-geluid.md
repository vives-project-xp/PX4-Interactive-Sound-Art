# Tonen

Noten/ toonhoogtes kunnen in verschillende sleutels bevinden, dit zorgt ervoor dat de instrumenten "mooi" samen klinken zolang
de noten die gespeeld worden in die toonlader/sleutel horen. We kunnen ook kijken als alle 12 noten mogelijk zijn. Je kunt het best beginnen met de sleutel die alle witte noten bevat: C-majeur (C D E F G A B C). 

![volledige 12 noten](fotos/image.png)

# Hoe?

<<<<<<< HEAD
- afstand binnenlezen via ultrasone sensor (berekening afstand: Afstand = (Tijd∗Snelheidvangeluid)/2)
- Zet om naar frequentie of sample 
- speelt toon af met juist pitch of sample

=======
De code in c# om van 1 toon, de volledige toonlader maken

``` c#
using System;
using NAudio.Wave;
using NAudio.Wave.SampleProviders;

class Program
{
    static void Main()
    {
        string inputFilePath = "path/to/your/piano_note.wav";
        string higherPitchFilePath = "higher_pitch_piano_note.wav";
        string lowerPitchFilePath = "lower_pitch_piano_note.wav";

        ChangePitch(inputFilePath, higherPitchFilePath, 4);
        ChangePitch(inputFilePath, lowerPitchFilePath, -3);
    }

    static void ChangePitch(string inputFilePath, string outputFilePath, int semitones)
    {
        using (var reader = new AudioFileReader(inputFilePath))
        {
            var pitchShifter = new SmbPitchShiftingSampleProvider(reader.ToSampleProvider());
            pitchShifter.PitchFactor = (float)Math.Pow(2.0, semitones / 12.0);

            WaveFileWriter.CreateWaveFile16(outputFilePath, pitchShifter);
        }
    }
}
>>>>>>> 6e622c1ccd4069b45165733ec6985ee411d6778c
