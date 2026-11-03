import React from 'react';
import { Cloud, Map, LineChart, Activity } from 'lucide-react';
import { ActiveTab } from '../types';

interface SideNavProps { activeTab: ActiveTab; onSelectTab: (tab: ActiveTab) => void; }
export const SideNav: React.FC<SideNavProps> = ({ activeTab, onSelectTab }) => <nav className="fixed left-0 top-0 h-full w-[72px] z-50 border-r border-[#d8d4c8] bg-[#eef0e9] flex flex-col items-center py-4 gap-2 hidden md:flex" aria-label="Navigasi utama"><button onClick={() => onSelectTab('forecast')} className="mb-3"><Cloud className="w-5 h-5 text-[#1f6056]" /><span className="block text-[9px]">PANG</span></button>{[[LineChart, 'forecast', 'Prakiraan'], [Map, 'map', 'Peta'], [Activity, 'eval', 'Nilai']].map(([Icon, tab, label]) => <button key={String(tab)} onClick={() => onSelectTab(tab as ActiveTab)} aria-current={activeTab === tab ? 'page' : undefined} className={`w-full h-12 ${activeTab === tab ? 'text-[#1f6056] bg-white' : 'text-[#849495]'}`} title={String(label)}>{React.createElement(Icon as typeof Map, { className: 'w-4 h-4 mx-auto' })}<span className="block text-[9px] uppercase">{String(label)}</span></button>)}</nav>;
