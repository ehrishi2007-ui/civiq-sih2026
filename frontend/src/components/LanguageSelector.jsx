import { useLanguage } from '../context/LanguageContext';
import { Globe } from 'lucide-react';

export default function LanguageSelector() {
  const { language, setLanguage } = useLanguage();

  return (
    <div className="flex items-center gap-2">
      <Globe className="w-4 h-4 text-slate-500" />
      <select
        value={language}
        onChange={(e) => setLanguage(e.target.value)}
        className="block w-full rounded-md border-0 py-1.5 pl-3 pr-8 text-slate-900 ring-1 ring-inset ring-slate-300 focus:ring-2 focus:ring-civiq-600 sm:text-sm sm:leading-6"
      >
        <option value="en">English</option>
        <option value="hi">हिंदी (Hindi)</option>
        <option value="ta">தமிழ் (Tamil)</option>
        <option value="te">తెలుగు (Telugu)</option>
      </select>
    </div>
  );
}
