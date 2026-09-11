import { Link } from 'react-router-dom';
import clsx from 'clsx';
import { useLanguage } from '../context/LanguageContext';
import { CheckCircle, XCircle, AlertCircle, ArrowRight } from 'lucide-react';
import { getLocalizedScheme } from '../mock/schemeTranslations';

export default function SchemeCard({ scheme: rawScheme }) {
  const { t, language } = useLanguage();
  const scheme = getLocalizedScheme(rawScheme, language);
  
  const isClosed = scheme.is_closed || scheme.status === 'CLOSED' || (scheme.closing_date && new Date(scheme.closing_date) < new Date()) || (scheme.scheme_id === 'standup_india' || scheme.id === 'standup_india');

  const statusConfig = {
    closed: {
      icon: AlertCircle,
      color: 'text-rose-700',
      bg: 'bg-rose-50',
      border: 'border-rose-300',
      label: t('scheme.closed_badge'),
    },
    eligible: {
      icon: CheckCircle,
      color: 'text-emerald-600',
      bg: 'bg-emerald-50',
      border: 'border-emerald-200',
      label: t('scheme.eligible'),
    },
    not_eligible: {
      icon: XCircle,
      color: 'text-red-600',
      bg: 'bg-red-50',
      border: 'border-red-200',
      label: t('scheme.not_eligible'),
    },
    partial: {
      icon: AlertCircle,
      color: 'text-amber-600',
      bg: 'bg-amber-50',
      border: 'border-amber-200',
      label: t('scheme.partial'),
    },
  };

  const status = isClosed ? 'closed' : (scheme.eligible ? 'eligible' : scheme.score > 0 ? 'partial' : 'not_eligible');
  const config = statusConfig[status];
  const StatusIcon = config.icon;

  return (
    <div className={clsx('rounded-xl border bg-white shadow-sm transition-all hover:shadow-md overflow-hidden', config.border)}>
      <div className={clsx('px-4 py-3 border-b flex items-center justify-between', config.bg, config.border)}>
        <div className="flex items-center gap-2">
          <StatusIcon className={clsx('w-5 h-5', config.color)} />
          <span className={clsx('font-medium text-sm', config.color)}>{config.label}</span>
        </div>
        <div className="text-sm font-medium text-slate-500">
          {isClosed ? t('scheme.portal_inactive') : `${t('scheme.match_score')}: ${Math.round(scheme.score * 100)}%`}
        </div>
      </div>
      
      <div className="p-5">
        <div className="mb-4">
          <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1">
            {scheme.ministry}
          </p>
          <h3 className="text-lg font-bold text-slate-900 leading-tight">
            {scheme.scheme_name}
          </h3>
        </div>
        
        <p className="text-slate-600 text-sm mb-4 line-clamp-2">
          {scheme.description}
        </p>

        <div className="mb-4">
          <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-sm font-medium bg-indigo-50 text-indigo-700">
            {t('scheme.benefit')}: {scheme.benefit}
          </span>
        </div>

        <div className="flex flex-wrap gap-2 mb-6">
          {scheme.tags.map((tag) => (
            <span key={tag} className="px-2 py-0.5 rounded text-xs font-medium bg-slate-100 text-slate-600">
              {tag}
            </span>
          ))}
        </div>

        <Link
          to={`/scheme/${scheme.scheme_id || scheme.id}`}
          className="inline-flex items-center justify-center w-full px-4 py-2 text-sm font-medium text-white bg-civiq-600 rounded-lg hover:bg-civiq-700 transition-colors"
        >
          {t('scheme.view_details')}
          <ArrowRight className="w-4 h-4 ml-2" />
        </Link>
      </div>
    </div>
  );
}
