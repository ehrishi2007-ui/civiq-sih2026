import { ArrowRight, TrendingUp, TrendingDown } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import clsx from 'clsx';

export default function DiffTable({ changes }) {
  const { t } = useLanguage();

  if (!changes || changes.length === 0) return null;

  return (
    <div className="bg-white rounded-xl border border-slate-200 overflow-hidden mt-6">
      <div className="px-5 py-4 border-b border-slate-200 bg-slate-50">
        <h3 className="text-lg font-bold text-slate-900">{t('scheme.diff_title')}</h3>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-sm text-left">
          <thead className="text-xs text-slate-500 bg-slate-50 uppercase border-b border-slate-200">
            <tr>
              <th className="px-5 py-3 font-medium">Parameter</th>
              <th className="px-5 py-3 font-medium">Previous Policy</th>
              <th className="px-5 py-3 font-medium">New Policy (2024)</th>
              <th className="px-5 py-3 font-medium">Change</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {changes.map((change, idx) => (
              <tr key={idx} className="hover:bg-slate-50 transition-colors">
                <td className="px-5 py-3 font-medium text-slate-900">{change.field}</td>
                <td className="px-5 py-3 text-slate-500 line-through decoration-slate-300">{change.old_value}</td>
                <td className="px-5 py-3 font-medium text-slate-900">{change.new_value}</td>
                <td className="px-5 py-3">
                  <span className={clsx(
                    'inline-flex items-center px-2 py-0.5 rounded text-xs font-semibold',
                    change.direction === 'up' ? 'bg-emerald-100 text-emerald-700' : 'bg-red-100 text-red-700'
                  )}>
                    {change.direction === 'up' ? (
                      <TrendingUp className="w-3 h-3 mr-1" />
                    ) : (
                      <TrendingDown className="w-3 h-3 mr-1" />
                    )}
                    {change.change_label}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
