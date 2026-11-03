import { ObservationNode, NodeId, TimelineFrame, NowcastDistribution } from '../types';

export const NODES_LIST: Record<NodeId, ObservationNode> = {
  MAIN: { id: 'MAIN', name: 'MAIN', locationName: 'Petak puncak', role: 'Titik utama prakiraan', lat: -6.75, lng: 107.00, elevation: 1529, isTarget: true, color: '#1f6056' },
  UP: { id: 'UP', name: 'UP', locationName: 'Petak utara', role: 'Petak utara', lat: -6.50, lng: 107.00, elevation: 162, isTarget: false, color: '#a46b13' },
  DOWN: { id: 'DOWN', name: 'DOWN', locationName: 'Petak selatan', role: 'Petak selatan', lat: -7.00, lng: 107.00, elevation: 0, isTarget: false, color: '#9c3f1d' },
  LEFT: { id: 'LEFT', name: 'LEFT', locationName: 'Petak barat', role: 'Petak barat', lat: -6.75, lng: 106.75, elevation: 823, isTarget: false, color: '#2c7569' },
  RIGHT: { id: 'RIGHT', name: 'RIGHT', locationName: 'Petak timur', role: 'Petak timur', lat: -6.75, lng: 107.25, elevation: 288, isTarget: false, color: '#5f7965' },
};

const WIB_TZ = 'Asia/Jakarta';
const dtfDate = new Intl.DateTimeFormat('id-ID', { day: 'numeric', month: 'short', year: 'numeric', timeZone: WIB_TZ });
const dtfTime = new Intl.DateTimeFormat('id-ID', { hour: '2-digit', minute: '2-digit', hour12: false, timeZone: WIB_TZ });
const dateLabel = (d: Date) => dtfDate.format(d).replace(/\./g, '');
const timeLabel = (d: Date) => dtfTime.format(d).replace(/\./g, ':');
const wibLabel = (d: Date) => `${dateLabel(d)}, ${timeLabel(d)} WIB`;

const HOUR_MS = 3_600_000;
const lastFullHour = new Date(Math.floor(Date.now() / HOUR_MS) * HOUR_MS - HOUR_MS);
const windowStart = new Date(lastFullHour.getTime() - 5 * HOUR_MS);
const targetHour = new Date(lastFullHour.getTime() + HOUR_MS);
const SAMPLE_VALID_AT = wibLabel(targetHour);
const SAMPLE_WINDOW = dateLabel(windowStart) === dateLabel(lastFullHour)
  ? `${timeLabel(windowStart)} – ${timeLabel(lastFullHour)} WIB`
  : `${dateLabel(windowStart)} ${timeLabel(windowStart)} – ${dateLabel(lastFullHour)} ${timeLabel(lastFullHour)} WIB`;

export const TIMELINE_FRAMES: TimelineFrame[] = [{
  offset: 'Now',
  timeWib: wibLabel(lastFullHour),
  windowRangeWib: SAMPLE_WINDOW,
  description: `Contoh data: 6 pembacaan jam terakhir (${SAMPLE_WINDOW}) dipakai untuk memperkirakan 1 jam berikutnya.`,
  telemetries: {
    MAIN: { nodeId: 'MAIN', tempCelsius: 8.2, dewPointCelsius: 8.0, rainIntensityMmH: 14.8, humidityPercent: 98, windSpeedKmh: 34, windDirectionDeg: 220, pressureHpa: 705 },
    UP: { nodeId: 'UP', tempCelsius: 17.0, dewPointCelsius: 16.2, rainIntensityMmH: 6.4, humidityPercent: 92, windSpeedKmh: 22, windDirectionDeg: 220, pressureHpa: 855 },
    DOWN: { nodeId: 'DOWN', tempCelsius: 20.0, dewPointCelsius: 19.1, rainIntensityMmH: 16.5, humidityPercent: 95, windSpeedKmh: 28, windDirectionDeg: 190, pressureHpa: 898 },
    LEFT: { nodeId: 'LEFT', tempCelsius: 18.5, dewPointCelsius: 18.0, rainIntensityMmH: 18.2, humidityPercent: 96, windSpeedKmh: 32, windDirectionDeg: 250, pressureHpa: 882 },
    RIGHT: { nodeId: 'RIGHT', tempCelsius: 18.1, dewPointCelsius: 16.9, rainIntensityMmH: 5.0, humidityPercent: 88, windSpeedKmh: 18, windDirectionDeg: 205, pressureHpa: 872 },
  },
}];

function makeDistribution(variable: NowcastDistribution['variable'], unit: string, samples: number[], observedNow?: number): NowcastDistribution {
  const sorted = [...samples].sort((a, b) => a - b);
  const pick = (q: number) => sorted[Math.floor(q * (sorted.length - 1))];
  const mean = sorted.reduce((sum, value) => sum + value, 0) / sorted.length;
  return { horizon: 'T+1h', validAtWib: SAMPLE_VALID_AT, samples: sorted, mean: Number(mean.toFixed(2)), p10: Number(pick(.1).toFixed(2)), p25: Number(pick(.25).toFixed(2)), p50: Number(pick(.5).toFixed(2)), p75: Number(pick(.75).toFixed(2)), p90: Number(pick(.9).toFixed(2)), observedNow, unit, variable };
}

function samples(center: number, spread: number): number[] {
  return Array.from({ length: 30 }, (_, index) => Math.max(0, center + spread * (((index + .5) / 30) * 2 - 1) + Math.sin(index * 1.7) * spread * .05));
}

export const SAMPLE_NOWCAST = {
  precipitation: makeDistribution('precipitation', 'mm/jam', samples(12.8, 5.4), 14.8),
  wind_speed: makeDistribution('wind_speed', 'km/jam', samples(12, 4)),
  relative_humidity: makeDistribution('relative_humidity', '%', samples(94.0, 3.5), 98),
};

