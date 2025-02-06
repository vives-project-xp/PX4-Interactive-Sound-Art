# Tonen

Noten/ toonhoogtes kunnen in verschillende sleutels bevinden, dit zorgt ervoor dat de instrumenten "mooi" samen klinken zolang
de noten die gespeeld worden in die toonlader/sleutel horen.

![Diatonic Chords in Each Key](fotos/diatonic-chords-in-each-key.png)

# Van 1 .Wav naar verschillende tonen gaan

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