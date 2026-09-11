import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useLanguage } from '../context/LanguageContext';
import { useProfile } from '../context/ProfileContext';
import DigiLockerModal from '../components/DigiLockerModal';
import { saveProfile } from '../services/profileService';

export default function ProfileWizard() {
  const { t } = useLanguage();
  const navigate = useNavigate();
  const { profile, dispatch } = useProfile();
  const [showDigiLocker, setShowDigiLocker] = useState(true);
  const [step, setStep] = useState(1);
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Initialize empty profile if null
  const localProfile = profile || {
    full_name: '', age: '', gender: 'male', category: 'General',
    state: '', district: '', is_rural: false,
    annual_income: '', occupation: '', education: '',
    has_land: false, land_acres: '', has_bpl_card: false,
    disability: false, minority: false, ration_card_type: 'None',
    documents: []
  };

  const handleUpdate = (field, value) => {
    dispatch({ type: 'UPDATE_FIELD', field, value });
  };

  const handleSubmit = async () => {
    setIsSubmitting(true);
    try {
      await saveProfile(localProfile);
      navigate('/dashboard');
    } catch (error) {
      console.error('Failed to save profile:', error);
      // Even if mock save fails, proceed to dashboard in this demo
      navigate('/dashboard');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
      <DigiLockerModal
        isOpen={showDigiLocker && !profile}
        onClose={() => setShowDigiLocker(false)}
        onComplete={() => setShowDigiLocker(false)}
      />

      <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
        <div className="px-6 py-8 border-b border-slate-200 bg-slate-50">
          <h1 className="text-2xl font-bold text-slate-900">{t('profile.title')}</h1>
          
          {/* Progress bar */}
          <div className="mt-6 flex items-center justify-between relative">
            <div className="absolute left-0 top-1/2 w-full h-1 bg-slate-200 -z-10 -translate-y-1/2"></div>
            <div className="absolute left-0 top-1/2 h-1 bg-civiq-600 -z-10 -translate-y-1/2 transition-all duration-300" style={{ width: `${((step - 1) / 3) * 100}%` }}></div>
            {[1, 2, 3, 4].map((s) => (
              <div key={s} className={`w-8 h-8 rounded-full flex items-center justify-center font-bold text-sm transition-colors ${step >= s ? 'bg-civiq-600 text-white shadow-md' : 'bg-white text-slate-400 border-2 border-slate-200'}`}>
                {s}
              </div>
            ))}
          </div>
        </div>

        <div className="p-6 sm:p-8">
          {step === 1 && (
            <div className="space-y-6 animate-in fade-in slide-in-from-right-4">
              <h2 className="text-lg font-bold text-slate-900 mb-4">{t('profile.step1')}</h2>
              
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">{t('profile.full_name')}</label>
                <input
                  type="text"
                  value={localProfile.full_name}
                  onChange={(e) => handleUpdate('full_name', e.target.value)}
                  className="block w-full rounded-lg border-slate-300 shadow-sm focus:border-civiq-500 focus:ring-civiq-500 sm:text-sm"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">{t('profile.age')}</label>
                  <input
                    type="number"
                    value={localProfile.age}
                    onChange={(e) => handleUpdate('age', parseInt(e.target.value) || '')}
                    className="block w-full rounded-lg border-slate-300 shadow-sm focus:border-civiq-500 focus:ring-civiq-500 sm:text-sm"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">{t('profile.gender')}</label>
                  <select
                    value={localProfile.gender}
                    onChange={(e) => handleUpdate('gender', e.target.value)}
                    className="block w-full rounded-lg border-slate-300 shadow-sm focus:border-civiq-500 focus:ring-civiq-500 sm:text-sm"
                  >
                    <option value="male">Male</option>
                    <option value="female">Female</option>
                    <option value="other">Other</option>
                  </select>
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">{t('profile.category')}</label>
                <select
                  value={localProfile.category}
                  onChange={(e) => handleUpdate('category', e.target.value)}
                  className="block w-full rounded-lg border-slate-300 shadow-sm focus:border-civiq-500 focus:ring-civiq-500 sm:text-sm"
                >
                  <option value="General">General</option>
                  <option value="OBC">OBC</option>
                  <option value="SC">SC</option>
                  <option value="ST">ST</option>
                </select>
              </div>
            </div>
          )}

          {step === 2 && (
            <div className="space-y-6 animate-in fade-in slide-in-from-right-4">
              <h2 className="text-lg font-bold text-slate-900 mb-4">{t('profile.step2')}</h2>
              
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">{t('profile.state')}</label>
                  <input
                    type="text"
                    value={localProfile.state}
                    onChange={(e) => handleUpdate('state', e.target.value)}
                    className="block w-full rounded-lg border-slate-300 shadow-sm focus:border-civiq-500 focus:ring-civiq-500 sm:text-sm"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">{t('profile.district')}</label>
                  <input
                    type="text"
                    value={localProfile.district}
                    onChange={(e) => handleUpdate('district', e.target.value)}
                    className="block w-full rounded-lg border-slate-300 shadow-sm focus:border-civiq-500 focus:ring-civiq-500 sm:text-sm"
                  />
                </div>
              </div>

              <div className="flex items-center">
                <input
                  id="is_rural"
                  type="checkbox"
                  checked={localProfile.is_rural}
                  onChange={(e) => handleUpdate('is_rural', e.target.checked)}
                  className="h-4 w-4 rounded border-slate-300 text-civiq-600 focus:ring-civiq-600"
                />
                <label htmlFor="is_rural" className="ml-2 block text-sm font-medium text-slate-700">
                  {t('profile.is_rural')}
                </label>
              </div>
            </div>
          )}

          {step === 3 && (
            <div className="space-y-6 animate-in fade-in slide-in-from-right-4">
              <h2 className="text-lg font-bold text-slate-900 mb-4">{t('profile.step3')}</h2>
              
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">{t('profile.annual_income')}</label>
                <div className="relative rounded-md shadow-sm">
                  <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                    <span className="text-slate-500 sm:text-sm">₹</span>
                  </div>
                  <input
                    type="number"
                    value={localProfile.annual_income}
                    onChange={(e) => handleUpdate('annual_income', parseInt(e.target.value) || 0)}
                    className="block w-full rounded-lg border-slate-300 pl-7 shadow-sm focus:border-civiq-500 focus:ring-civiq-500 sm:text-sm"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">{t('profile.occupation')}</label>
                  <input
                    type="text"
                    value={localProfile.occupation}
                    onChange={(e) => handleUpdate('occupation', e.target.value)}
                    className="block w-full rounded-lg border-slate-300 shadow-sm focus:border-civiq-500 focus:ring-civiq-500 sm:text-sm"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">{t('profile.education')}</label>
                  <input
                    type="text"
                    value={localProfile.education}
                    onChange={(e) => handleUpdate('education', e.target.value)}
                    className="block w-full rounded-lg border-slate-300 shadow-sm focus:border-civiq-500 focus:ring-civiq-500 sm:text-sm"
                  />
                </div>
              </div>
            </div>
          )}

          {step === 4 && (
            <div className="space-y-6 animate-in fade-in slide-in-from-right-4">
              <h2 className="text-lg font-bold text-slate-900 mb-4">{t('profile.step4')}</h2>
              
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium text-slate-700">{t('profile.has_land')}</span>
                <div className="flex gap-4">
                  <label className="inline-flex items-center">
                    <input type="radio" checked={localProfile.has_land} onChange={() => handleUpdate('has_land', true)} className="text-civiq-600 focus:ring-civiq-600" />
                    <span className="ml-2 text-sm text-slate-700">Yes</span>
                  </label>
                  <label className="inline-flex items-center">
                    <input type="radio" checked={!localProfile.has_land} onChange={() => handleUpdate('has_land', false)} className="text-civiq-600 focus:ring-civiq-600" />
                    <span className="ml-2 text-sm text-slate-700">No</span>
                  </label>
                </div>
              </div>

              {localProfile.has_land && (
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">{t('profile.land_acres')}</label>
                  <input
                    type="number"
                    step="0.1"
                    value={localProfile.land_acres}
                    onChange={(e) => handleUpdate('land_acres', parseFloat(e.target.value) || 0)}
                    className="block w-full rounded-lg border-slate-300 shadow-sm focus:border-civiq-500 focus:ring-civiq-500 sm:text-sm"
                  />
                </div>
              )}

              <div className="flex items-center justify-between">
                <span className="text-sm font-medium text-slate-700">{t('profile.has_bpl_card')}</span>
                <input
                  type="checkbox"
                  checked={localProfile.has_bpl_card}
                  onChange={(e) => handleUpdate('has_bpl_card', e.target.checked)}
                  className="h-4 w-4 rounded border-slate-300 text-civiq-600 focus:ring-civiq-600"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">{t('profile.ration_card_type')}</label>
                <select
                  value={localProfile.ration_card_type}
                  onChange={(e) => handleUpdate('ration_card_type', e.target.value)}
                  className="block w-full rounded-lg border-slate-300 shadow-sm focus:border-civiq-500 focus:ring-civiq-500 sm:text-sm"
                >
                  <option value="None">None</option>
                  <option value="PHH">PHH</option>
                  <option value="AAY">AAY</option>
                </select>
              </div>
            </div>
          )}

          {/* Navigation */}
          <div className="mt-8 pt-6 border-t border-slate-200 flex items-center justify-between">
            <button
              onClick={() => setStep(Math.max(1, step - 1))}
              disabled={step === 1}
              className="px-4 py-2 text-sm font-medium text-slate-700 bg-white border border-slate-300 rounded-lg hover:bg-slate-50 disabled:opacity-50"
            >
              {t('profile.prev')}
            </button>
            
            {step < 4 ? (
              <button
                onClick={() => setStep(step + 1)}
                className="px-6 py-2 text-sm font-bold text-white bg-civiq-600 rounded-lg hover:bg-civiq-700 shadow-sm transition-colors"
              >
                {t('profile.next')}
              </button>
            ) : (
              <button
                onClick={handleSubmit}
                disabled={isSubmitting}
                className="px-6 py-2 text-sm font-bold text-white bg-emerald-600 rounded-lg hover:bg-emerald-700 shadow-sm transition-colors flex items-center"
              >
                {isSubmitting ? '...' : t('profile.submit')}
              </button>
            )}
          </div>

        </div>
      </div>
    </div>
  );
}
