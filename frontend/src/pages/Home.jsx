import logoImg from '../assets/logo.jpeg';
import { Link, useNavigate } from 'react-router-dom';
import { useLanguage } from '../context/LanguageContext';
import { ShieldCheck, BrainCircuit, FileSearch, HelpCircle } from 'lucide-react';

export default function Home() {
  const { t } = useLanguage();
  const navigate = useNavigate();

  const features = [
    {
      icon: ShieldCheck,
      title: t('home.feature1_title'),
      description: t('home.feature1_desc'),
      color: 'bg-blue-100 text-blue-600',
    },
    {
      icon: BrainCircuit,
      title: t('home.feature2_title'),
      description: t('home.feature2_desc'),
      color: 'bg-indigo-100 text-indigo-600',
    },
    {
      icon: FileSearch,
      title: t('home.feature3_title'),
      description: t('home.feature3_desc'),
      color: 'bg-emerald-100 text-emerald-600',
    },
    {
      icon: HelpCircle,
      title: t('home.feature4_title'),
      description: t('home.feature4_desc'),
      color: 'bg-amber-100 text-amber-600',
    },
  ];

  return (
    <div className="flex flex-col items-center justify-center min-h-[calc(100vh-4rem)] px-4 py-16 sm:px-6 lg:px-8 bg-slate-50">
      <div className="max-w-3xl w-full text-center space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
        
        {/* Hero Section */}
        <div className="space-y-4">
          <div className="flex justify-center mb-6">
            <div className="p-3 sm:p-4 bg-white rounded-3xl shadow-sm border border-slate-200/80 inline-flex items-center justify-center">
              <img src={logoImg} alt="CiviQ - Empowering Every Citizen" className="h-24 sm:h-32 md:h-36 w-auto object-contain" />
            </div>
          </div>
          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold text-slate-900 tracking-tight leading-tight">
            CiviQ
            <span className="block text-2xl sm:text-3xl lg:text-4xl text-civiq-600 mt-2 font-bold">
              {t('home.tagline')}
            </span>
          </h1>
          <p className="max-w-2xl mx-auto text-lg sm:text-xl text-slate-600 leading-relaxed">
            {t('home.description')}
          </p>
        </div>

        {/* CTA */}
        <div className="pt-4 pb-8">
          <button
            onClick={() => navigate('/profile')}
            className="inline-flex items-center justify-center px-8 py-4 text-lg font-bold text-white bg-civiq-600 rounded-full shadow-xl shadow-civiq-600/20 hover:bg-civiq-700 hover:shadow-civiq-600/40 hover:-translate-y-0.5 transition-all duration-200"
          >
            {t('home.cta')}
          </button>
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 pt-8 border-t border-slate-200">
          {features.map((feature, idx) => {
            const Icon = feature.icon;
            return (
              <div key={idx} className="flex flex-col items-center text-center p-6 bg-white rounded-2xl shadow-sm border border-slate-100 hover:shadow-md transition-shadow">
                <div className={`w-12 h-12 rounded-xl flex items-center justify-center mb-4 ${feature.color}`}>
                  <Icon className="w-6 h-6" />
                </div>
                <h3 className="text-lg font-bold text-slate-900 mb-2">{feature.title}</h3>
                <p className="text-slate-600 text-sm leading-relaxed">{feature.description}</p>
              </div>
            );
          })}
        </div>

      </div>
    </div>
  );
}
