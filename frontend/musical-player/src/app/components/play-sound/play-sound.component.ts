import { Component, Input, OnInit } from '@angular/core';
import * as Tone from 'tone';

@Component({
  selector: 'app-play-sound',
  templateUrl: './play-sound.component.html',
  styleUrls: ['./play-sound.component.scss'],
})
export class PlaySoundComponent implements OnInit {
  @Input() processedImage: any;

  constructor() {}

  ngOnInit(): void {}

  timeFromDurations(value: any, i: any, arr: any) {
    const prevTime = arr[i - 1]?.time;
    value.time = prevTime + arr[i - 1]?.duration || 0;
    return value;
  }

  onClick() {
    const notes = JSON.parse(this.processedImage.Notes[0]).flat();
    const mappedNotes = notes.map(this.timeFromDurations);

    const synth = new Tone.Synth().toDestination();
    const part = new Tone.Part((time, value) => {
      if (value.pitch == 'pause') {
        synth.triggerAttackRelease(value.note, value.duration, time);
      }
      else
        synth.triggerAttackRelease(value.pitch, value.duration, time);
    }, mappedNotes).start(0);

    Tone.Transport.start();
  }
}
