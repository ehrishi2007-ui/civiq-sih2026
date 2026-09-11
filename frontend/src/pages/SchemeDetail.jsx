import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useLanguage } from '../context/LanguageContext';
import { useProfile } from '../context/ProfileContext';
import { getSchemeById, compareSchemePolicy } from '../services/schemeService';
import ReasoningTree from '../components/ReasoningTree';
import EvidenceDrawer from '../components/EvidenceDrawer';
import DiffTable from '../components/DiffTable';
import ImpactCard from '../components/ImpactCard';
import { ArrowLeft, Loader2, CheckCircle, ExternalLink, FileText, AlertTriangle, ShieldCheck } from 'lucide-react';
import clsx from 'clsx';

export default function SchemeDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { t } = useLanguage();
  const { profile } = useProfile();
  
  const [scheme, setScheme] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedEvidence, setSelectedEvidence] = useState(null);
  const [comparison, setComparison] = useState(null);

  useEffect(() => {
    const fetchSchemeAndComparison = async () => {
      try {
        const data = await getSchemeById(id);
        setScheme(data);

        // Only fetch comparison for schemes with policy changes (PMSS)
        const isPMSS = ['pm_scholarship_warb', 'pmss', 'pmsy'].includes(id?.toLowerCase()) || Boolean(data?.policy_diff);
        if (isPMSS) {
          try {
            const compRes = await compareSchemePolicy('pm_scholarship_warb', profile);
            if (compRes && (compRes.changes?.length > 0 || compRes.verified)) {
              setComparison(compRes);
            }
          } catch (compErr) {
            setComparison(null);
          }
        } else {
          setComparison(null);
        }
      } catch (error) {
        console.error('Failed to fetch scheme details:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchSchemeAndComparison();
  }, [id, profile]);

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

  const isClosed = scheme.is_closed || scheme.status === 'CLOSED' || (scheme.closing_date && new Date(scheme.closing_date) < new Date()) || (scheme.scheme_id === 'standup_india' || scheme.id === 'standup_india');

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
                  {isClosed ? (
                    <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-rose-100 text-rose-800 shrink-0 font-bold text-xs">
                      <AlertTriangle className="w-3.5 h-3.5 text-rose-600" />
                      {t('scheme.closed_badge')}
                    </div>
                  ) : (
                    <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-slate-100 shrink-0">
                      <span className="text-sm font-medium text-slate-600">{t('scheme.match_score')}:</span>
                      <span className="text-sm font-bold text-slate-900">{Math.round(scheme.score * 100)}%</span>
                    </div>
                  )}
                </div>

                {isClosed && (
                  <div className="mb-6 p-4 rounded-xl bg-rose-50 border border-rose-200 flex items-start gap-3">
                    <AlertTriangle className="w-5 h-5 text-rose-600 shrink-0 mt-0.5" />
                    <div>
                      <h4 className="text-sm font-bold text-rose-900">
                        Official Portal Notification: {t('scheme.closed_badge')}
                      </h4>
                      <p className="text-xs text-rose-800 mt-1 leading-relaxed">
                        Live verification on the official portal (<strong>www.standupmitra.in</strong>) confirms: <em>"Stand-Up India scheme has closed on 31.03.2025."</em> New borrower applications are no longer being accepted by partner commercial banks.
                      </p>
                    </div>
                  </div>
                )}

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
              
              <div className="px-6 py-4 bg-slate-50 border-t border-slate-200 flex items-center justify-between">
                {isClosed ? (
                  <>
                    <span className="text-xs font-semibold text-rose-700 bg-rose-50 px-3 py-1.5 rounded-lg border border-rose-200">
                      {t('scheme.portal_closed')}
                    </span>
                    <a
                      href={scheme.application_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center px-5 py-2 text-sm font-medium text-slate-700 bg-white border border-slate-300 rounded-lg hover:bg-slate-50 transition-colors shadow-sm"
                    >
                      {t('scheme.visit_portal')} (standupmitra.in)
                      <ExternalLink className="w-4 h-4 ml-2" />
                    </a>
                  </>
                ) : (
                  <>
                    <div />
                    <a
                      href={scheme.application_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center px-6 py-2.5 text-sm font-bold text-white bg-civiq-600 rounded-lg hover:bg-civiq-700 transition-colors shadow-sm"
                    >
                      {t('scheme.apply_now')}
                      <ExternalLink className="w-4 h-4 ml-2" />
                    </a>
                  </>
                )}
              </div>
            </div>

      <h2 className="text-xl font-bold text-slate-900 mb-4">{t('scheme.why_seeing')}</h2>
      
      {/* Visual Eligibility Tree */}
      <ReasoningTree 
        criteria={scheme.criteria} 
        onSelectEvidence={setSelectedEvidence} 
      />

      {/* Policy Change Diffs & Impact — Verified Revisions */}
      {comparison && comparison.verified && comparison.changes && comparison.changes.length > 0 && (
        <div className="mt-12 mb-8">
          <div className="flex items-center justify-between mb-2">
            <h2 className="text-xl font-bold text-slate-900">
              {t('scheme.policy_comparison')} ({comparison.old_version || '2023-24'} vs {comparison.new_version || '2026-27'})
            </h2>
            <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-bold bg-emerald-100 text-emerald-800">
              <ShieldCheck className="w-3.5 h-3.5 mr-1 text-emerald-600" />
              {t('scheme.verified_guidelines')}
            </span>
          </div>

          <p className="text-slate-600 mb-4">
            {comparison.message || "Verified comparison between official PMSS 2023-24 guidelines and revised policy notification."}
          </p>

          {/* Render Verified DiffTable */}
          <DiffTable changes={comparison.changes} />

          {/* Personalized Impact Card if impact is evaluated */}
          {comparison.impact && (
            <ImpactCard impact={comparison.impact} />
          )}

          {comparison.personalized_impact && (
            <div className="bg-slate-50 border border-slate-200 rounded-xl p-5 mt-4">
              <h4 className="text-sm font-bold text-slate-900 mb-1">{t('scheme.eligibility_impact')}</h4>
              <p className="text-sm text-slate-700 leading-relaxed">
                {comparison.personalized_impact}
              </p>
            </div>
          )}
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
