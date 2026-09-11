import { Sparkles } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import clsx from 'clsx';

export default function ImpactCard({ impact }) {
  const { t } = useLanguage();

  if (!impact) return null;

  return (
    <div className="bg-gradient-to-br from-indigo-50 to-white rounded-xl border border-indigo-100 p-5 mt-6 relative overflow-hidden">
      <div className="absolute top-0 right-0 p-4 opacity-10">
        <Sparkles className="w-24 h-24 text-indigo-600" />
      </div>
      
      <div className="relative z-10">
        <h3 className="text-sm font-bold text-indigo-900 uppercase tracking-wider mb-4 flex items-center gap-2">
          <Sparkles className="w-4 h-4" />
          {t('scheme.impact_title')}
        </h3>
        
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div className="bg-white/60 rounded-lg p-3 border border-indigo-50">
            <p className="text-xs text-slate-500 mb-1">{t('impact.financial')}</p>
            <div className="flex items-end gap-2">
              <span className={clsx(
                'text-lg font-bold',
                impact.direction === 'positive' ? 'text-emerald-600' : 'text-red-600'
              )}>
                {impact.delta}
              </span>
            </div>
            <p className="text-xs text-slate-500 mt-1">
              From {impact.old_benefit} → {impact.new_benefit}
            </p>
          </div>
          
          <div className="bg-white/60 rounded-lg p-3 border border-indigo-50">
            <p className="text-xs text-slate-500 mb-1">{t('impact.status')}</p>
            <p className="text-sm font-medium text-slate-900">
              {impact.status_change}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
