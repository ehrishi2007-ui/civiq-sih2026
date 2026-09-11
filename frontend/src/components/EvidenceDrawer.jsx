import { X, FileText, Quote, ExternalLink } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import clsx from 'clsx';

export default function EvidenceDrawer({ evidence, isOpen, onClose }) {
  const { t } = useLanguage();
  const docName = evidence?.document || evidence?.doc_name;

  return (
    <>
      {/* Backdrop */}
      <div 
        className={clsx(
          'fixed inset-0 bg-slate-900/40 backdrop-blur-sm z-40 transition-opacity duration-300',
          isOpen ? 'opacity-100' : 'opacity-0 pointer-events-none'
        )}
        onClick={onClose}
      />
      
      {/* Drawer */}
      <div
        className={clsx(
          'fixed right-0 top-0 bottom-0 w-full sm:w-[400px] bg-white shadow-2xl z-50 transform transition-transform duration-300 ease-in-out flex flex-col',
          isOpen ? 'translate-x-0' : 'translate-x-full'
        )}
      >
        <div className="px-5 py-4 border-b border-slate-200 flex items-center justify-between bg-slate-50">
          <div className="flex items-center gap-2 text-slate-900 font-bold">
            <FileText className="w-5 h-5 text-civiq-600" />
            {t('scheme.evidence_title')}
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded-md text-slate-400 hover:text-slate-600 hover:bg-slate-200 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {evidence ? (
          <div className="p-5 flex-1 overflow-y-auto">
            <div className="space-y-6">
              
              <div>
                <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1">
                  {t('evidence.document')}
                </p>
                <div className="p-3 bg-slate-100 rounded-lg text-slate-800 text-sm font-medium flex items-start gap-2">
                  <FileText className="w-4 h-4 text-slate-500 mt-0.5" />
                  <span>{docName}</span>
                </div>
                {docName && (
                  <a
                    href={`http://127.0.0.1:8000/api/v1/documents/${encodeURIComponent(docName)}${evidence.page ? `#page=${evidence.page}` : ''}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="mt-2.5 inline-flex items-center justify-center gap-1.5 w-full px-3.5 py-2 rounded-lg bg-civiq-600 hover:bg-civiq-700 text-white text-xs font-bold shadow-xs transition-colors"
                  >
                    <ExternalLink className="w-3.5 h-3.5" />
                    {t('evidence.view_pdf')}
                  </a>
                )}
              </div>
              
              <div className="flex gap-4">
                <div className="flex-1">
                  <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1">
                    {t('evidence.page')}
                  </p>
                  <div className="p-2 bg-slate-50 border rounded-lg text-slate-800 text-sm font-medium">
                    {t('common.pg')} {evidence.page}
                  </div>
                </div>
                <div className="flex-2">
                  <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1">
                    {t('evidence.section')}
                  </p>
                  <div className="p-2 bg-slate-50 border rounded-lg text-slate-800 text-sm font-medium">
                    {evidence.section}
                  </div>
                </div>
              </div>

              <div>
                <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">
                  {t('evidence.quote')}
                </p>
                <div className="relative p-4 bg-indigo-50 rounded-xl text-indigo-900 text-sm leading-relaxed border border-indigo-100">
                  <Quote className="absolute top-2 left-2 w-8 h-8 text-indigo-200 -z-0 opacity-50" />
                  <span className="relative z-10 italic">
                    "{evidence.quote}"
                  </span>
                </div>
              </div>

            </div>
          </div>
        ) : (
          <div className="p-5 flex items-center justify-center h-full text-slate-400 text-sm">
            {t('evidence.empty')}
          </div>
        )}
      </div>
    </>
  );
}
