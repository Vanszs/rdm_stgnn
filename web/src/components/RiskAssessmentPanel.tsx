import React from 'react';
import { Info } from 'lucide-react';

export const RiskAssessmentPanel: React.FC = () => <div role="region" aria-label="Konteks Model Nowcasting" className="w-full h-full flex flex-col justify-center gap-2">
  <div className="flex items-center gap-2 text-[#b9cacb]"><Info className="w-4 h-4 text-[#1f6056]" /><h3 className="font-mono-data text-xs font-bold uppercase">Konteks Model RDM-STGNN</h3></div>
  <p className="text-xs leading-relaxed text-[#dae2fd]">Nowcasting T+1 jam berbasis model difusi graf spasio-temporal (Skenario 3, 10-fitur) pada simpul target Puncak (1529 mdpl) dengan 50 lintasan difusi stokastik.</p>
</div>;
