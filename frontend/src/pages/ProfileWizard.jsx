import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useLanguage } from '../context/LanguageContext';
import { useProfile } from '../context/ProfileContext';
import DigiLockerModal from '../components/DigiLockerModal';
import { saveProfile } from '../services/profileService';
import {
  GraduationCap,
  Wheat,
  Briefcase,
  Hammer,
  User,
  Sparkles,
  CheckCircle2,
  AlertCircle
} from 'lucide-react';
import clsx from 'clsx';

export default function ProfileWizard() {
  const { t } = useLanguage();
  const navigate = useNavigate();
  const { profile, dispatch } = useProfile();
  const [showDigiLocker, setShowDigiLocker] = useState(false);
  const [step, setStep] = useState(1);
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Canonical blank profile state
  const blankProfile = {
    full_name: '',
    age: '',
    gender: 'female',
    category: 'General',
    state: '',
    district: '',
    is_rural: false,
    annual_income: '',
    occupation: 'Student',
    education: '10th Pass',
    marks_percentage: '',
    has_land: false,
    land_acres: '',
    has_bpl_card: false,
    is_ex_serviceman: false,
    enterprise_type: 'greenfield',
    ration_card_type: 'None',
  };

  const localProfile = profile || blankProfile;

  const handleReset = () => {
    dispatch({ type: 'CLEAR_PROFILE' });
    dispatch({ type: 'SET_PROFILE', payload: { ...blankProfile } });
    setStep(1);
    setShowDigiLocker(false);
  };

  const handleUpdate = (field, value) => {
    dispatch({ type: 'UPDATE_FIELD', field, value });
  };

  // Demo Persona Quick-Fill
  const loadPreset = (preset) => {
    if (preset === 'priya') {
      const priyaData = {
        full_name: 'Priya Ramesh',
        age: 20,
        gender: 'female',
        category: 'OBC',
        state: 'Tamil Nadu',
        district: 'Chennai',
        is_rural: false,
        annual_income: 300000,
        occupation: 'Student',
        education: '12th Pass',
        marks_percentage: 72,
        has_land: false,
        land_acres: 0,
        has_bpl_card: false,
        is_ex_serviceman: false,
        enterprise_type: 'none',
        ration_card_type: 'None',
      };
      dispatch({ type: 'SET_PROFILE', payload: priyaData });
    } else if (preset === 'farmer') {
      const farmerData = {
        full_name: 'Ramesh Kumar',
        age: 42,
        gender: 'male',
        category: 'General',
        state: 'Uttar Pradesh',
        district: 'Varanasi',
        is_rural: true,
        annual_income: 180000,
        occupation: 'Farmer',
        education: '10th Pass',
        marks_percentage: 55,
        has_land: true,
        land_acres: 2.5,
        has_bpl_card: true,
        is_ex_serviceman: false,
        enterprise_type: 'agriculture',
        ration_card_type: 'PHH',
      };
      dispatch({ type: 'SET_PROFILE', payload: farmerData });
    } else if (preset === 'entrepreneur') {
      const womanData = {
        full_name: 'Anita Devi',
        age: 29,
        gender: 'female',
        category: 'SC',
        state: 'Maharashtra',
        district: 'Pune',
        is_rural: false,
        annual_income: 250000,
        occupation: 'Entrepreneur',
        education: 'Graduate',
        marks_percentage: 68,
        has_land: false,
        land_acres: 0,
        has_bpl_card: false,
        is_ex_serviceman: false,
        enterprise_type: 'greenfield',
        ration_card_type: 'None',
      };
      dispatch({ type: 'SET_PROFILE', payload: womanData });
    }
  };

  const handleSubmit = async () => {
    setIsSubmitting(true);
    try {
      const sanitizedProfile = {
        ...localProfile,
        age: parseInt(localProfile.age, 10) || 0,
        annual_income: parseFloat(localProfile.annual_income) || 0.0,
        marks_percentage: parseFloat(localProfile.marks_percentage) || 0.0,
        land_acres: localProfile.has_land ? (parseFloat(localProfile.land_acres) || 0.0) : 0.0,
        has_land: Boolean(localProfile.has_land),
        has_bpl_card: Boolean(localProfile.has_bpl_card),
        is_rural: Boolean(localProfile.is_rural),
        is_ex_serviceman: Boolean(localProfile.is_ex_serviceman),
      };
      await saveProfile(sanitizedProfile);
      dispatch({ type: 'SET_PROFILE', payload: sanitizedProfile });
      navigate('/dashboard');
    } catch (error) {
      console.error('Failed to save profile:', error);
      navigate('/dashboard');
    } finally {
      setIsSubmitting(false);
    }
  };

  const isStudent = localProfile.occupation === 'Student';
  const isFarmer = localProfile.occupation === 'Farmer';
  const isEntrepreneur = localProfile.occupation === 'Entrepreneur';

  return (
    <div className="max-w-3xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
      <DigiLockerModal
        isOpen={showDigiLocker && !profile}
        onClose={() => setShowDigiLocker(false)}
        onComplete={() => setShowDigiLocker(false)}
      />

      {/* Demo Persona Bar */}
      <div className="bg-gradient-to-r from-civiq-50 to-indigo-50 border border-civiq-200 rounded-xl p-3.5 mb-6 shadow-xs flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
        <div className="flex items-center gap-2">
          <Sparkles className="w-4 h-4 text-civiq-600 shrink-0" />
          <span className="text-xs font-bold text-slate-800 uppercase tracking-wide">
            {t('profile.quickfill_title')}
          </span>
        </div>
        <div className="flex flex-wrap gap-2 w-full sm:w-auto">
          <button
            type="button"
            onClick={() => loadPreset('priya')}
            className="px-2.5 py-1 text-xs font-semibold bg-white border border-civiq-300 text-civiq-700 hover:bg-civiq-100 rounded-lg shadow-2xs transition-colors"
          >
            {t('profile.quickfill_priya')}
          </button>
          <button
            type="button"
            onClick={() => loadPreset('farmer')}
            className="px-2.5 py-1 text-xs font-semibold bg-white border border-emerald-300 text-emerald-700 hover:bg-emerald-50 rounded-lg shadow-2xs transition-colors"
          >
            {t('profile.quickfill_farmer')}
          </button>
          <button
            type="button"
            onClick={() => loadPreset('entrepreneur')}
            className="px-2.5 py-1 text-xs font-semibold bg-white border border-indigo-300 text-indigo-700 hover:bg-indigo-50 rounded-lg shadow-2xs transition-colors"
          >
            {t('profile.quickfill_entrepreneur')}
          </button>
          <button
            type="button"
            onClick={handleReset}
            className="px-2.5 py-1 text-xs font-bold bg-white border border-rose-300 text-rose-700 hover:bg-rose-50 rounded-lg shadow-2xs transition-colors"
          >
            {t('profile.quickfill_reset')}
          </button>
          <button
            type="button"
            onClick={() => setShowDigiLocker(true)}
            className="px-2.5 py-1 text-xs font-semibold bg-white border border-slate-300 text-slate-700 hover:bg-slate-100 rounded-lg shadow-2xs transition-colors"
          >
            {t('profile.quickfill_digilocker')}
          </button>
        </div>
      </div>

      <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
        <div className="px-6 py-6 border-b border-slate-200 bg-slate-50">
          <div className="flex items-center justify-between">
            <h1 className="text-2xl font-extrabold text-slate-900">{t('profile.title')}</h1>
            <span className="text-xs font-bold px-2.5 py-1 rounded-full bg-civiq-100 text-civiq-800">
              {t('profile.step_of').replace('{step}', step)}
            </span>
          </div>

          {/* Progress bar */}
          <div className="mt-5 flex items-center justify-between relative">
            <div className="absolute left-0 top-1/2 w-full h-1 bg-slate-200 -z-10 -translate-y-1/2"></div>
            <div
              className="absolute left-0 top-1/2 h-1 bg-civiq-600 -z-10 -translate-y-1/2 transition-all duration-300"
              style={{ width: `${((step - 1) / 3) * 100}%` }}
            ></div>
            {[1, 2, 3, 4].map((s) => (
              <div
                key={s}
                className={clsx(
                  'w-8 h-8 rounded-full flex items-center justify-center font-bold text-xs transition-colors',
                  step >= s ? 'bg-civiq-600 text-white shadow-md' : 'bg-white text-slate-400 border-2 border-slate-200'
                )}
              >
                {s}
              </div>
            ))}
          </div>
        </div>

        <div className="p-6 sm:p-8">
          {/* STEP 1: Personal & Demographics */}
          {step === 1 && (
            <div className="space-y-5 animate-in fade-in slide-in-from-right-4">
              <div>
                <h2 className="text-lg font-bold text-slate-900">{t('profile.step1_title')}</h2>
                <p className="text-xs text-slate-500">{t('profile.step1_desc')}</p>
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">{t('profile.full_name')}</label>
                <input
                  type="text"
                  value={localProfile.full_name}
                  onChange={(e) => handleUpdate('full_name', e.target.value)}
                  placeholder="e.g. Priya Ramesh"
                  className="block w-full rounded-lg border-slate-300 shadow-sm focus:border-civiq-500 focus:ring-civiq-500 sm:text-sm"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">{t('profile.age')}</label>
                  <input
                    type="number"
                    value={localProfile.age}
                    onChange={(e) => handleUpdate('age', parseInt(e.target.value, 10) || '')}
                    placeholder="e.g. 20"
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
                    <option value="female">{t('profile.gender_female')}</option>
                    <option value="male">{t('profile.gender_male')}</option>
                    <option value="other">{t('profile.gender_other')}</option>
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
                  <option value="OBC">OBC (Other Backward Class)</option>
                  <option value="SC">SC (Scheduled Caste)</option>
                  <option value="ST">ST (Scheduled Tribe)</option>
                </select>
              </div>
            </div>
          )}

          {/* STEP 2: Location */}
          {step === 2 && (
            <div className="space-y-5 animate-in fade-in slide-in-from-right-4">
              <div>
                <h2 className="text-lg font-bold text-slate-900">{t('profile.step2_title')}</h2>
                <p className="text-xs text-slate-500">{t('profile.step2_desc')}</p>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">{t('profile.state')}</label>
                  <input
                    type="text"
                    value={localProfile.state}
                    onChange={(e) => handleUpdate('state', e.target.value)}
                    placeholder="e.g. Tamil Nadu"
                    className="block w-full rounded-lg border-slate-300 shadow-sm focus:border-civiq-500 focus:ring-civiq-500 sm:text-sm"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">{t('profile.district')}</label>
                  <input
                    type="text"
                    value={localProfile.district}
                    onChange={(e) => handleUpdate('district', e.target.value)}
                    placeholder="e.g. Chennai"
                    className="block w-full rounded-lg border-slate-300 shadow-sm focus:border-civiq-500 focus:ring-civiq-500 sm:text-sm"
                  />
                </div>
              </div>

              <div className="p-4 bg-slate-50 border border-slate-200 rounded-xl flex items-center justify-between">
                <div>
                  <p className="text-sm font-bold text-slate-800">{t('profile.is_rural')}</p>
                  <p className="text-xs text-slate-500">{t('profile.is_rural_desc')}</p>
                </div>
                <input
                  id="is_rural"
                  type="checkbox"
                  checked={localProfile.is_rural}
                  onChange={(e) => handleUpdate('is_rural', e.target.checked)}
                  className="h-5 w-5 rounded border-slate-300 text-civiq-600 focus:ring-civiq-600"
                />
              </div>
            </div>
          )}

          {/* STEP 3: Citizen Category & Economic Background */}
          {step === 3 && (
            <div className="space-y-6 animate-in fade-in slide-in-from-right-4">
              <div>
                <h2 className="text-lg font-bold text-slate-900">{t('profile.step3_title')}</h2>
                <p className="text-xs text-slate-500">
                  {t('profile.step3_desc')}
                </p>
              </div>

              <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
                {[
                  { id: 'Student', label: t('profile.cat_student'), icon: GraduationCap, color: 'text-indigo-600' },
                  { id: 'Farmer', label: t('profile.cat_farmer'), icon: Wheat, color: 'text-emerald-600' },
                  { id: 'Entrepreneur', label: t('profile.cat_entrepreneur'), icon: Briefcase, color: 'text-blue-600' },
                  { id: 'Worker', label: t('profile.cat_worker'), icon: Hammer, color: 'text-amber-600' },
                  { id: 'Other', label: t('profile.cat_other'), icon: User, color: 'text-slate-600' },
                ].map((item) => {
                  const Icon = item.icon;
                  const isSelected = localProfile.occupation === item.id;
                  return (
                    <button
                      key={item.id}
                      type="button"
                      onClick={() => handleUpdate('occupation', item.id)}
                      className={clsx(
                        'p-4 rounded-xl border text-left transition-all flex flex-col justify-between h-28',
                        isSelected
                          ? 'border-civiq-600 bg-civiq-50/60 ring-2 ring-civiq-600/20 shadow-xs'
                          : 'border-slate-200 bg-white hover:border-slate-300'
                      )}
                    >
                      <Icon className={clsx('w-6 h-6', item.color)} />
                      <div>
                        <p className={clsx('text-xs font-bold', isSelected ? 'text-civiq-900' : 'text-slate-800')}>
                          {item.label}
                        </p>
                      </div>
                    </button>
                  );
                })}
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">
                  {t('profile.annual_income')}
                </label>
                <div className="relative rounded-md shadow-sm">
                  <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                    <span className="text-slate-500 sm:text-sm font-bold">₹</span>
                  </div>
                  <input
                    type="number"
                    value={localProfile.annual_income}
                    onChange={(e) => handleUpdate('annual_income', parseInt(e.target.value, 10) || 0)}
                    placeholder="e.g. 300000"
                    className="block w-full rounded-lg border-slate-300 pl-7 shadow-sm focus:border-civiq-500 focus:ring-civiq-500 sm:text-sm"
                  />
                </div>
                <p className="text-xs text-slate-500 mt-1">
                  {t('profile.annual_income_desc')}
                </p>
              </div>
            </div>
          )}

          {/* STEP 4: ADAPTIVE TARGETED QUESTIONS */}
          {step === 4 && (
            <div className="space-y-6 animate-in fade-in slide-in-from-right-4">
              <div className="flex items-center gap-2 pb-3 border-b border-slate-100">
                <span className="px-2.5 py-0.5 rounded-full text-xs font-bold bg-civiq-100 text-civiq-700">
                  {localProfile.occupation || 'General'} Specific Details
                </span>
                <p className="text-xs text-slate-500">
                  {t('profile.step4_desc')}
                </p>
              </div>

              {/* ADAPTIVE SECTION FOR STUDENTS */}
              {isStudent && (
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-1">
                      {t('profile.edu_level')}
                    </label>
                    <select
                      value={localProfile.education}
                      onChange={(e) => handleUpdate('education', e.target.value)}
                      className="block w-full rounded-lg border-slate-300 shadow-sm focus:border-civiq-500 focus:ring-civiq-500 sm:text-sm"
                    >
                      <option value="10th Pass">10th Pass</option>
                      <option value="12th Pass">12th Pass / Diploma (MEQ)</option>
                      <option value="Graduate">Graduation / Undergraduate</option>
                      <option value="Postgraduate">Postgraduate / Professional</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-1">
                      {t('profile.meq_marks')}
                    </label>
                    <div className="relative rounded-md shadow-sm">
                      <input
                        type="number"
                        step="0.1"
                        value={localProfile.marks_percentage}
                        onChange={(e) => handleUpdate('marks_percentage', parseFloat(e.target.value) || 0)}
                        placeholder="e.g. 72"
                        className="block w-full rounded-lg border-slate-300 pr-8 shadow-sm focus:border-civiq-500 focus:ring-civiq-500 sm:text-sm"
                      />
                      <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-3">
                        <span className="text-slate-500 sm:text-sm font-bold">%</span>
                      </div>
                    </div>
                    <p className="text-xs text-slate-500 mt-1 flex items-center gap-1">
                      <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600 inline" />
                      {t('profile.meq_hint')}
                    </p>
                  </div>

                  <div className="p-4 bg-indigo-50/60 border border-indigo-100 rounded-xl flex items-center justify-between">
                    <div>
                      <p className="text-sm font-bold text-indigo-900">{t('profile.ex_serviceman')}</p>
                      <p className="text-xs text-indigo-700">{t('profile.ex_serviceman_desc')}</p>
                    </div>
                    <input
                      type="checkbox"
                      checked={localProfile.is_ex_serviceman}
                      onChange={(e) => handleUpdate('is_ex_serviceman', e.target.checked)}
                      className="h-5 w-5 rounded border-indigo-300 text-civiq-600 focus:ring-civiq-600"
                    />
                  </div>
                </div>
              )}

              {/* ADAPTIVE SECTION FOR FARMERS */}
              {isFarmer && (
                <div className="space-y-4">
                  <div className="p-4 bg-emerald-50/60 border border-emerald-200 rounded-xl">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm font-bold text-emerald-950">{t('profile.own_land')}</p>
                        <p className="text-xs text-emerald-800">{t('profile.own_land_desc')}</p>
                      </div>
                      <div className="flex gap-4">
                        <label className="inline-flex items-center">
                          <input
                            type="radio"
                            checked={localProfile.has_land === true}
                            onChange={() => handleUpdate('has_land', true)}
                            className="text-civiq-600 focus:ring-civiq-600"
                          />
                          <span className="ml-1.5 text-sm font-bold text-slate-800">{t('profile.yes')}</span>
                        </label>
                        <label className="inline-flex items-center">
                          <input
                            type="radio"
                            checked={localProfile.has_land === false}
                            onChange={() => handleUpdate('has_land', false)}
                            className="text-civiq-600 focus:ring-civiq-600"
                          />
                          <span className="ml-1.5 text-sm font-bold text-slate-800">{t('profile.no')}</span>
                        </label>
                      </div>
                    </div>

                    {localProfile.has_land && (
                      <div className="mt-4 pt-4 border-t border-emerald-200/80">
                        <label className="block text-sm font-medium text-emerald-950 mb-1">
                          {t('profile.land_acres')}
                        </label>
                        <input
                          type="number"
                          step="0.1"
                          value={localProfile.land_acres}
                          onChange={(e) => handleUpdate('land_acres', parseFloat(e.target.value) || 0)}
                          placeholder="e.g. 2.5"
                          className="block w-full rounded-lg border-emerald-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 sm:text-sm bg-white"
                        />
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* ADAPTIVE SECTION FOR ENTREPRENEURS */}
              {isEntrepreneur && (
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-1">{t('profile.enterprise_nature')}</label>
                    <select
                      value={localProfile.enterprise_type}
                      onChange={(e) => handleUpdate('enterprise_type', e.target.value)}
                      className="block w-full rounded-lg border-slate-300 shadow-sm focus:border-civiq-500 focus:ring-civiq-500 sm:text-sm"
                    >
                      <option value="greenfield">{t('profile.greenfield')}</option>
                      <option value="expansion">{t('profile.expansion')}</option>
                    </select>
                    <p className="text-xs text-slate-500 mt-1">
                      {t('profile.enterprise_desc')}
                    </p>
                  </div>
                </div>
              )}

              {/* ADAPTIVE SECTION FOR WORKERS / GENERAL CITIZENS */}
              {!isStudent && !isFarmer && !isEntrepreneur && (
                <div className="space-y-4">
                  <div className="flex items-center justify-between p-4 bg-slate-50 border border-slate-200 rounded-xl">
                    <div>
                      <p className="text-sm font-bold text-slate-800">{t('profile.bpl_card')}</p>
                      <p className="text-xs text-slate-500">{t('profile.bpl_desc')}</p>
                    </div>
                    <input
                      type="checkbox"
                      checked={localProfile.has_bpl_card}
                      onChange={(e) => handleUpdate('has_bpl_card', e.target.checked)}
                      className="h-5 w-5 rounded border-slate-300 text-civiq-600 focus:ring-civiq-600"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-1">{t('profile.ration_card')}</label>
                    <select
                      value={localProfile.ration_card_type}
                      onChange={(e) => handleUpdate('ration_card_type', e.target.value)}
                      className="block w-full rounded-lg border-slate-300 shadow-sm focus:border-civiq-500 focus:ring-civiq-500 sm:text-sm"
                    >
                      <option value="None">{t('profile.ration_card_none')}</option>
                      <option value="PHH">{t('profile.ration_card_phh')}</option>
                      <option value="AAY">{t('profile.ration_card_aay')}</option>
                    </select>
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Navigation Controls */}
          <div className="mt-8 pt-6 border-t border-slate-200 flex items-center justify-between">
            <button
              type="button"
              onClick={() => setStep(Math.max(1, step - 1))}
              disabled={step === 1}
              className="px-4 py-2 text-sm font-medium text-slate-700 bg-white border border-slate-300 rounded-lg hover:bg-slate-50 disabled:opacity-40 transition-colors"
            >
              {t('profile.prev')}
            </button>

            {step < 4 ? (
              <button
                type="button"
                onClick={() => setStep(step + 1)}
                className="px-6 py-2 text-sm font-bold text-white bg-civiq-600 rounded-lg hover:bg-civiq-700 shadow-sm transition-colors"
              >
                {t('profile.next')}
              </button>
            ) : (
              <button
                type="button"
                onClick={handleSubmit}
                disabled={isSubmitting}
                className="px-6 py-2 text-sm font-bold text-white bg-emerald-600 hover:bg-emerald-700 rounded-lg shadow-sm transition-colors flex items-center gap-1.5"
              >
                {isSubmitting ? t('profile.evaluating') : t('profile.submit')}
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
