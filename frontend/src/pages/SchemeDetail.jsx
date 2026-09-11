import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useLanguage } from '../context/LanguageContext';
import { getSchemeById } from '../services/schemeService';
import ReasoningTree from '../components/ReasoningTree';
import EvidenceDrawer from '../components/EvidenceDrawer';
import DiffTable from '../components/DiffTable';
import ImpactCard from '../components/ImpactCard';
import { mockDiffData, mockImpactData } from '../mock/diffData';
import { ArrowLeft, Loader2, CheckCircle, ExternalLink, FileText } from 'lucide-react';
import clsx from 'clsx';

export default function SchemeDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { t } = useLanguage();
  
  const [scheme, setScheme] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedEvidence, setSelectedEvidence] = useState(null);

  useEffect(() => {
    const fetchScheme = async () => {
      try {
        const data = await getSchemeById(id);
        setScheme(data);
      } catch (error) {
        console.error('Failed to fetch scheme details:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchScheme();
  }, [id]);

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-[50vh]">
        <Loader2 className="w-10 h-10 text-civiq-600 animate-spin" />
      </div>
    );
  }

  if (!scheme) {
    return (
      <div className="text-center py-12">
        <p className="text-slate-600">Scheme not found.</p>
        <button onClick={() => navigate('/dashboard')} className="mt-4 text-civiq-600 hover:underline">
          {t('scheme.back')}
        </button>
      </div>
    );
  }

  const diffData = mockDiffData[id]?.changes;
  const impactData = mockImpactData[id];

  return (
    <div className="max-w-4xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
      <button 
        onClick={() => navigate('/dashboard')}
        className="inline-flex items-center text-sm font-medium text-slate-500 hover:text-slate-900 mb-6 transition-colors"
      >
        <ArrowLeft className="w-4 h-4 mr-1" />
        {t('scheme.back')}
      </button>

      <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden mb-8">
        <div className="p-6 sm:p-8">
          <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-4 mb-6">
            <div>
              <p className="text-sm font-bold text-slate-500 uppercase tracking-wider mb-1">
                {scheme.ministry}
              </p>
              <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 leading-tight">
                {scheme.scheme_name}
              </h1>
            </div>
            <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-slate-100 shrink-0">
              <span className="text-sm font-medium text-slate-600">Match Score:</span>
              <span className="text-sm font-bold text-slate-900">{Math.round(scheme.score * 100)}%</span>
            </div>
          </div>

          <p className="text-lg text-slate-600 leading-relaxed mb-6">
            {scheme.description}
          </p>

          <div className="flex flex-wrap gap-2 mb-8">
            {scheme.tags.map((tag) => (
              <span key={tag} className="px-3 py-1 rounded-full text-xs font-semibold bg-indigo-50 text-indigo-700">
                {tag}
              </span>
            ))}
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 p-5 bg-slate-50 rounded-xl border border-slate-100">
            <div>
              <p className="text-sm font-medium text-slate-500 mb-1">{t('scheme.benefit')}</p>
              <p className="text-lg font-bold text-emerald-600">{scheme.benefit}</p>
            </div>
            <div>
              <p className="text-sm font-medium text-slate-500 mb-2">{t('scheme.documents_required')}</p>
              <ul className="space-y-1">
                {scheme.documents_required.map((doc, idx) => (
                  <li key={idx} className="flex items-center text-sm font-medium text-slate-700">
                    <FileText className="w-4 h-4 text-slate-400 mr-2 shrink-0" />
                    {doc}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
        
        <div className="px-6 py-4 bg-slate-50 border-t border-slate-200 flex justify-end">
          <a
            href={scheme.application_url}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center px-6 py-2.5 text-sm font-bold text-white bg-civiq-600 rounded-lg hover:bg-civiq-700 transition-colors shadow-sm"
          >
            {t('scheme.apply_now')}
            <ExternalLink className="w-4 h-4 ml-2" />
          </a>
        </div>
      </div>

      <h2 className="text-xl font-bold text-slate-900 mb-4">Why am I seeing this?</h2>
      
      {/* Visual Eligibility Tree */}
      <ReasoningTree 
        criteria={scheme.criteria} 
        onSelectEvidence={setSelectedEvidence} 
      />

      {/* Policy Change Diffs & Impact */}
      {diffData && (
        <div className="mt-12 mb-8">
          <h2 className="text-xl font-bold text-slate-900 mb-2">Recent Policy Updates (2024)</h2>
          <p className="text-slate-600 mb-4">See what changed in this scheme's latest guidelines and how it affects you.</p>
          <DiffTable changes={diffData} />
          <ImpactCard impact={impactData} />
        </div>
      )}

      <EvidenceDrawer 
        evidence={selectedEvidence}
        isOpen={!!selectedEvidence}
        onClose={() => setSelectedEvidence(null)}
      />
    </div>
  );
}
