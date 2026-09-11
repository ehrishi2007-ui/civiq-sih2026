import { useState } from 'react';
import { useLanguage } from '../context/LanguageContext';
import { checkMyth } from '../services/mythService';
import { ShieldQuestion, Search, AlertTriangle, CheckCircle, XCircle, FileText, Loader2, ExternalLink } from 'lucide-react';
import { mockMythClaims } from '../mock/myths';
import clsx from 'clsx';

export default function MythBuster() {
  const { t } = useLanguage();
  const [claim, setClaim] = useState('');
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleCheck = async (textToSearch) => {
    const text = textToSearch || claim;
    if (!text.trim()) return;

    if (textToSearch) {
      setClaim(textToSearch);
    }

    setIsLoading(true);
    setResult(null);

    try {
      const res = await checkMyth(text);
      setResult(res);
    } catch (error) {
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  };

  const getVerdictConfig = (verdict) => {
    switch (verdict) {
      case 'TRUE':
        return { icon: CheckCircle, color: 'text-emerald-600', bg: 'bg-emerald-50', border: 'border-emerald-200' };
      case 'FALSE':
        return { icon: XCircle, color: 'text-red-600', bg: 'bg-red-50', border: 'border-red-200' };
      case 'PARTIALLY TRUE':
      default:
        return { icon: AlertTriangle, color: 'text-amber-600', bg: 'bg-amber-50', border: 'border-amber-200' };
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-12 sm:px-6 lg:px-8">
      
      <div className="text-center mb-12">
        <div className="inline-flex items-center justify-center p-3 bg-indigo-50 rounded-2xl mb-4">
          <ShieldQuestion className="w-10 h-10 text-indigo-600" />
        </div>
        <h1 className="text-3xl font-bold text-slate-900 mb-3">{t('myths.title')}</h1>
        <p className="text-lg text-slate-600 max-w-2xl mx-auto">{t('myths.subtitle')}</p>
      </div>

      <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-2 pl-4 flex items-center mb-6">
        <Search className="w-6 h-6 text-slate-400 mr-2" />
        <input
          type="text"
          value={claim}
          onChange={(e) => setClaim(e.target.value)}
          placeholder={t('myths.placeholder')}
          className="flex-1 border-0 focus:ring-0 text-lg py-3 bg-transparent"
          onKeyDown={(e) => e.key === 'Enter' && handleCheck()}
        />
        <button
          onClick={() => handleCheck()}
          disabled={!claim.trim() || isLoading}
          className="px-6 py-3 bg-civiq-600 text-white font-bold rounded-xl hover:bg-civiq-700 transition-colors disabled:opacity-50 ml-2"
        >
          {isLoading ? <Loader2 className="w-5 h-5 animate-spin" /> : t('myths.check')}
        </button>
      </div>

      {!result && !isLoading && (
        <div className="mt-8">
          <p className="text-sm font-semibold text-slate-500 uppercase tracking-wider mb-4 px-2">
            {t('myths.examples')}
          </p>
          <div className="flex flex-wrap gap-2">
            {mockMythClaims.map((example, idx) => (
              <button
                key={idx}
                onClick={() => handleCheck(example)}
                className="text-left px-4 py-2 rounded-lg border border-slate-200 bg-white hover:border-civiq-300 hover:bg-civiq-50 text-slate-700 text-sm transition-all"
              >
                "{example}"
              </button>
            ))}
          </div>
        </div>
      )}

      {result && (
        <div className="mt-8 animate-in fade-in slide-in-from-bottom-4">
          <div className={clsx('rounded-2xl border overflow-hidden', getVerdictConfig(result.verdict).border)}>
            
            <div className={clsx('px-6 py-4 flex items-center gap-3 border-b', getVerdictConfig(result.verdict).bg, getVerdictConfig(result.verdict).border)}>
              {(() => {
                const Icon = getVerdictConfig(result.verdict).icon;
                return <Icon className={clsx('w-8 h-8', getVerdictConfig(result.verdict).color)} />;
              })()}
              <div>
                <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-0.5">{t('myths.verdict')}</p>
                <p className={clsx('text-xl font-bold', getVerdictConfig(result.verdict).color)}>
                  {result.verdict}
                </p>
              </div>
            </div>

            <div className="p-6 bg-white">
              <h3 className="text-lg font-bold text-slate-900 mb-3">{t('myths.fact_check')}</h3>
              <p className="text-slate-700 leading-relaxed mb-8">
                {result.explanation}
              </p>

              {result.sources && result.sources.length > 0 && (
                <div>
                  <h4 className="text-sm font-bold text-slate-900 mb-3 flex items-center gap-2">
                    <FileText className="w-4 h-4 text-slate-500" />
                    {t('myths.official_sources')}
                  </h4>
                  <div className="space-y-3">
                    {result.sources.map((src, idx) => (
                      <div key={idx} className="bg-slate-50 rounded-lg p-4 border border-slate-100">
                        <div className="flex flex-wrap items-center justify-between gap-2 mb-2 text-sm text-slate-600">
                          <div className="flex items-center gap-2">
                            <span className="font-semibold text-slate-800">{src.document}</span>
                            <span>•</span>
                            <span>{t('common.pg')} {src.page}</span>
                          </div>
                          {src.document && (
                            <a
                              href={`http://127.0.0.1:8000/api/v1/documents/${encodeURIComponent(src.document)}${src.page ? `#page=${src.page}` : ''}`}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="inline-flex items-center gap-1 px-2.5 py-1 rounded bg-civiq-100 hover:bg-civiq-200 text-civiq-800 text-xs font-bold transition-colors shadow-2xs"
                              title="Open official PDF document"
                            >
                              <ExternalLink className="w-3.5 h-3.5" />
                              {t('myths.open_pdf')}
                            </a>
                          )}
                        </div>
                        <p className="text-sm text-slate-600 italic border-l-2 border-slate-300 pl-3">
                          "{src.quote}"
                        </p>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>

          </div>
        </div>
      )}

    </div>
  );
}
