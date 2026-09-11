import { useState } from 'react';
import { useLanguage } from '../context/LanguageContext';
import { useProfile } from '../context/ProfileContext';
import { X, ShieldCheck, Loader2 } from 'lucide-react';
import digilockerData from '../mock/digilocker_data';

export default function DigiLockerModal({ isOpen, onClose, onComplete }) {
  const { t } = useLanguage();
  const { dispatch } = useProfile();
  const [loading, setLoading] = useState(false);

  if (!isOpen) return null;

  const handleImport = () => {
    setLoading(true);
    // Simulate network delay
    setTimeout(() => {
      dispatch({ type: 'SET_PROFILE', payload: digilockerData });
      setLoading(false);
      onComplete();
    }, 1500);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-sm">
      <div className="bg-white rounded-2xl shadow-xl w-full max-w-md overflow-hidden animate-in fade-in zoom-in-95 duration-200">
        <div className="p-6">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-indigo-50 text-indigo-600 rounded-xl flex items-center justify-center">
                <ShieldCheck className="w-6 h-6" />
              </div>
              <h2 className="text-xl font-bold text-slate-900">{t('digilocker.title')}</h2>
            </div>
            <button onClick={onClose} className="text-slate-400 hover:text-slate-500">
              <X className="w-5 h-5" />
            </button>
          </div>

          <p className="text-slate-600 mb-6">
            {t('digilocker.consent')}
          </p>

          <div className="space-y-3">
            <button
              onClick={handleImport}
              disabled={loading}
              className="w-full flex items-center justify-center py-2.5 px-4 rounded-xl text-white bg-civiq-600 hover:bg-civiq-700 font-medium transition-colors disabled:opacity-70"
            >
              {loading ? (
                <>
                  <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                  {t('digilocker.importing')}
                </>
              ) : (
                t('digilocker.import')
              )}
            </button>
            <button
              onClick={onClose}
              disabled={loading}
              className="w-full flex items-center justify-center py-2.5 px-4 rounded-xl text-slate-700 bg-slate-100 hover:bg-slate-200 font-medium transition-colors"
            >
              {t('digilocker.skip')}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
