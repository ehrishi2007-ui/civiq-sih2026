import logoImg from '../assets/logo.jpeg';
import { Link, useLocation } from 'react-router-dom';
import clsx from 'clsx';
import { Home, User, LayoutDashboard, MessageCircleQuestion, ShieldQuestion } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import LanguageSelector from './LanguageSelector';

export default function Navbar() {
  const { t } = useLanguage();
  const location = useLocation();

  const navItems = [
    { path: '/', label: t('nav.home'), icon: Home },
    { path: '/profile', label: t('nav.profile'), icon: User },
    { path: '/dashboard', label: t('nav.dashboard'), icon: LayoutDashboard },
    { path: '/ask', label: t('nav.ask'), icon: MessageCircleQuestion },
    { path: '/myths', label: t('nav.myths'), icon: ShieldQuestion },
  ];

  return (
    <nav className="bg-white border-b border-slate-200 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex">
            <Link to="/" className="flex-shrink-0 flex items-center gap-2.5 py-1">
              <img src={logoImg} alt="CiviQ Logo" className="h-9 sm:h-10 w-auto object-contain" />
            </Link>
            <div className="hidden sm:ml-8 sm:flex sm:space-x-8">
              {navItems.map((item) => {
                const Icon = item.icon;
                const isActive = location.pathname === item.path;
                return (
                  <Link
                    key={item.path}
                    to={item.path}
                    className={clsx(
                      'inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium',
                      isActive
                        ? 'border-civiq-500 text-slate-900'
                        : 'border-transparent text-slate-500 hover:border-slate-300 hover:text-slate-700'
                    )}
                  >
                    <Icon className="w-4 h-4 mr-2" />
                    {item.label}
                  </Link>
                );
              })}
            </div>
          </div>
          <div className="flex items-center">
            <LanguageSelector />
          </div>
        </div>
      </div>
    </nav>
  );
}
