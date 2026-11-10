import React from 'react';
import { Clock, RefreshCw } from 'lucide-react';

interface TimelineScrubberProps {
  nowWib: string;
  validAtWib: string;
  dataStatus: string;
  isEra5: boolean;
  isSample?: boolean;
}

/** Compact one-line forecast bar: data hour -> target hour -> source. */
const TimelineScrubberComponent: React.FC<TimelineScrubberProps> = ({
  nowWib,
  validAtWib,
  dataStatus,
  isEra5,
  isSample,
}) => {
  return (
    <div
      role="region"
      aria-label="Informasi waktu prakiraan"
      className="glass-panel w-full max-w-4xl rounded-2xl px-4 py-2.5 flex flex-wrap items-center gap-x-4 gap-y-2 border border-slate-700/60 bg-slate-900/90 backdrop-blur-xl shadow-[0_10px_35px_rgba(0,0,0,0.6)]"
    >
      <div className="flex items-center gap-2 min-w-0">
        <RefreshCw className="w-4 h-4 text-[#1f6056] flex-shrink-0" />
        <span className="text-[9px] font-mono-data font-bold text-[#849495] uppercase tracking-wider flex-shrink-0">Data</span>
        <span className="text-[11px] font-mono-data font-bold text-[#dae2fd] truncate">{nowWib}</span>
      </div>

      <span className="text-[#5f685e] text-xs font-bold">→</span>

      <div className="flex items-center gap-2 min-w-0">
        <Clock className="w-4 h-4 text-[#1f6056] flex-shrink-0" />
        <span className="text-[9px] font-mono-data font-bold text-[#849495] uppercase tracking-wider flex-shrink-0">Target</span>
        <span className="text-[11px] font-mono-data font-bold text-[#dae2fd] truncate">{validAtWib}</span>
      </div>

      <div className="ml-auto flex items-center gap-1.5" title={dataStatus}>
        <span className={`w-2 h-2 rounded-full ${isEra5 ? 'bg-[#1f6056]' : 'bg-[#a46b13]'}`} />
        <span className="text-[10px] font-mono-data text-[#849495]">{isEra5 ? 'ERA5 · 7 hari lalu' : isSample ? 'Contoh data' : 'Arsip data uji'}</span>
      </div>
    </div>
  );
};

export const TimelineScrubber = React.memo(TimelineScrubberComponent);
