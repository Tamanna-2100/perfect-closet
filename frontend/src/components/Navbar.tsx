import React from "react";
import { Sparkles, Compass, ShieldCheck } from "lucide-react";

export const Navbar: React.FC = () => {
  return (
    <header className="sticky top-0 z-50 backdrop-blur-md bg-stone-950/80 border-b border-stone-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-full bg-gradient-to-tr from-amber-600 via-rose-500 to-indigo-500 flex items-center justify-center p-0.5 shadow-lg shadow-amber-950/50">
            <div className="w-full h-full bg-stone-950 rounded-full flex items-center justify-center">
              <Sparkles className="w-5 h-5 text-amber-300" />
            </div>
          </div>
          <div>
            <span className="text-xl font-serif tracking-widest text-stone-100 uppercase font-semibold">
              Perfect Closet
            </span>
            <span className="block text-[10px] tracking-widest uppercase text-stone-400 font-sans">
              Haute Colorimetry &amp; Styling
            </span>
          </div>
        </div>

        <nav className="hidden md:flex items-center space-x-6 text-xs uppercase tracking-wider text-stone-300 font-medium">
          <span className="flex items-center gap-1.5 text-stone-400 bg-stone-900/60 px-3 py-1.5 rounded-full border border-stone-800">
            <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
            Deterministic CV (CIELAB + ITA)
          </span>
          <span className="flex items-center gap-1.5 text-amber-200/90 bg-amber-950/30 px-3 py-1.5 rounded-full border border-amber-900/40">
            <Compass className="w-3.5 h-3.5 text-amber-400" />
            12-Season Architecture
          </span>
        </nav>
      </div>
    </header>
  );
};
