export type TimedWord = {text:string;startFrame:number;durationFrames:number};
export type ValidatedWord = TimedWord & {index:number;endFrame:number};
export declare function luminance(hex:string):number;
export declare function contrastRatio(a:string,b:string):number;
export declare function verifyPalette(foreground:string,background:string,
  opts?:{largeText?:boolean}):{ratio:number;minimum:number;passes:boolean;scope:string};
export declare function validateWords(words:TimedWord[],sceneDurationFrames:number):ValidatedWord[];
export declare function wordAtFrame(words:TimedWord[],sceneDurationFrames:number,frame:number):ValidatedWord|null;
export declare function entranceProgress(word:ValidatedWord,frame:number,entranceFrames?:number):number;
