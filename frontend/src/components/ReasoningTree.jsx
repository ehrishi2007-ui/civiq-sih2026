import { Check, X, FileSearch } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import clsx from 'clsx';

export default function ReasoningTree({ criteria, onSelectEvidence }) {
  const { t } = useLanguage();

  return (
    <div className="bg-white rounded-xl border border-slate-200 overflow-hidden">
      <div className="px-5 py-4 border-b border-slate-200 bg-slate-50">
        <h3 className="text-lg font-bold text-slate-900">{t('scheme.reasoning_title')}</h3>
      </div>
      <div className="divide-y divide-slate-100">
        {criteria.map((crit, idx) => (
          <div key={idx} className="p-4 sm:p-5 flex items-start gap-4 hover:bg-slate-50 transition-colors">
            <div className={clsx(
              'mt-1 flex-shrink-0 w-6 h-6 rounded-full flex items-center justify-center',
              crit.pass ? 'bg-emerald-100 text-emerald-600' : 'bg-red-100 text-red-600'
            )}>
              {crit.pass ? <Check className="w-4 h-4" /> : <X className="w-4 h-4" />}
            </div>
            
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-slate-900 mb-1">{crit.label}</p>
              <div className="flex items-center gap-2">
                <span className={clsx(
                  'text-xs font-semibold px-2 py-0.5 rounded',
                  crit.pass ? 'bg-emerald-50 text-emerald-700' : 'bg-red-50 text-red-700'
                )}>
                  {crit.pass ? t('reasoning.pass') : t('reasoning.fail')}
                </span>
                
                {crit.evidence && (
                  <button
                    onClick={() => onSelectEvidence(crit.evidence)}
                    className="inline-flex items-center text-xs font-medium text-civiq-600 hover:text-civiq-700 bg-civiq-50 hover:bg-civiq-100 px-2 py-0.5 rounded transition-colors"
                  >
                    <FileSearch className="w-3 h-3 mr-1" />
                    {t('reasoning.view_evidence')}
                  </button>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
