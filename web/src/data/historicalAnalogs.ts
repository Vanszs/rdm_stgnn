import { HistoricalAnalog } from '../types';

export const HISTORICAL_ANALOGS: HistoricalAnalog[] = [
  { id: 'FAISS-01', rank: 1, datetime: '12 Apr 2005 05:00 WIB', patternType: 'Kondisi Kering', similarityPercent: 82.5, distanceL2: 1.412, rainRateMmH: 0.0, accumulatedRainMm: 0.0, peakWindKmh: 14.8, tempCelsius: 16.5, humidityPercent: 88.2, pressureHpa: 847.2, outcomeSummary: 'Analog historis riil: Presipitasi 0.0 mm/jam, angin 14.8 km/jam, kelembapan 88%.' },
  { id: 'FAISS-02', rank: 2, datetime: '26 Nov 2007 13:00 WIB', patternType: 'Hujan Sedang', similarityPercent: 78.4, distanceL2: 1.845, rainRateMmH: 2.3, accumulatedRainMm: 2.3, peakWindKmh: 21.2, tempCelsius: 18.2, humidityPercent: 94.1, pressureHpa: 846.8, outcomeSummary: 'Analog historis riil: Presipitasi 2.3 mm/jam, angin 21.2 km/jam, kelembapan 94%.' },
  { id: 'FAISS-03', rank: 3, datetime: '19 Okt 2014 13:00 WIB', patternType: 'Hujan Orografis Ekstrem', similarityPercent: 74.1, distanceL2: 2.334, rainRateMmH: 6.1, accumulatedRainMm: 6.1, peakWindKmh: 28.5, tempCelsius: 17.1, humidityPercent: 98.0, pressureHpa: 844.5, outcomeSummary: 'Analog historis riil: Presipitasi 6.1 mm/jam, angin 28.5 km/jam, kelembapan 98%.' },
];
