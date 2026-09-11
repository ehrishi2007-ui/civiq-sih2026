import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useLanguage } from '../context/LanguageContext';
import { useProfile } from '../context/ProfileContext';
import { getEligibleSchemes } from '../services/schemeService';
import SchemeCard from '../components/SchemeCard';
import { Loader2, LayoutGrid, CheckCircle } from 'lucide-react';

export default function Dashboard() {
  const { t } = useLanguage();
  const { profile } = useProfile();
  const [schemes, setSchemes] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!profile) {
      setLoading(false);
      return;
    }

    const fetchSchemes = async () => {
      try {
        const response = await getEligibleSchemes(profile);
        setSchemes(response.matches || []);
      } catch (error) {
        console.error('Failed to fetch schemes:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchSchemes();
  }, [profile]);

  if (!profile) {
    return (
      <div className="max-w-md mx-auto my-16 p-8 bg-white rounded-2xl shadow-sm border border-slate-200 text-center animate-in fade-in slide-in-from-bottom-4">
        <div className="w-16 h-16 bg-civiq-50 rounded-full flex items-center justify-center mx-auto mb-4">
          <LayoutGrid className="w-8 h-8 text-civiq-600" />
        </div>
        <h2 className="text-xl font-bold text-slate-900 mb-2">{t('dashboard.empty')}</h2>
        <p className="text-sm text-slate-600 mb-6 leading-relaxed">
          Set up your citizen profile to see personalized scheme matches, eligibility trees, and benefit calculations.
        </p>
        <Link
          to="/profile"
          className="inline-flex items-center justify-center px-6 py-3 text-sm font-bold text-white bg-civiq-600 rounded-lg hover:bg-civiq-700 transition-colors shadow-sm w-full"
        >
          Complete Citizen Profile
        </Link>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[50vh] px-4">
        <Loader2 className="w-10 h-10 text-civiq-600 animate-spin mb-4" />
        <p className="text-slate-600 font-medium animate-pulse">{t('dashboard.loading')}</p>
      </div>
    );
  }

  const eligibleCount = schemes.filter(s => s.eligible).length;

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
      <div className="mb-8 animate-in fade-in slide-in-from-bottom-4">
        <h1 className="text-2xl font-bold text-slate-900 mb-2">{t('dashboard.title')}</h1>
        <p className="text-slate-600">
          Showing schemes matching profile for <span className="font-semibold text-slate-800">{profile.full_name}</span>
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8 animate-in fade-in slide-in-from-bottom-6">
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-5 flex items-center">
          <div className="w-12 h-12 bg-civiq-50 rounded-lg flex items-center justify-center mr-4">
            <LayoutGrid className="w-6 h-6 text-civiq-600" />
          </div>
          <div>
            <p className="text-sm font-medium text-slate-500 uppercase tracking-wider">{t('dashboard.total_schemes')}</p>
            <p className="text-2xl font-bold text-slate-900">{schemes.length}</p>
          </div>
        </div>
        
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-5 flex items-center">
          <div className="w-12 h-12 bg-emerald-50 rounded-lg flex items-center justify-center mr-4">
            <CheckCircle className="w-6 h-6 text-emerald-600" />
          </div>
          <div>
            <p className="text-sm font-medium text-slate-500 uppercase tracking-wider">{t('dashboard.eligible')}</p>
            <p className="text-2xl font-bold text-slate-900">{eligibleCount}</p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {schemes.map((scheme, idx) => (
          <div key={scheme.scheme_id} className={`animate-in fade-in slide-in-from-bottom-8`} style={{ animationDelay: `${idx * 100}ms` }}>
            <SchemeCard scheme={scheme} />
          </div>
        ))}
      </div>
    </div>
  );
}
