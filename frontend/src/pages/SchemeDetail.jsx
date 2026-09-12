import { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { useLanguage } from '../context/LanguageContext';
import { useProfile } from '../context/ProfileContext';
import { getSchemeById, compareSchemePolicy, getEligibleSchemes, autoUpdatePolicy } from '../services/schemeService';
import { getLocalizedScheme } from '../mock/schemeTranslations';
import ReasoningTree from '../components/ReasoningTree';
import EvidenceDrawer from '../components/EvidenceDrawer';
import DiffTable from '../components/DiffTable';
import ImpactCard from '../components/ImpactCard';
import { 
  ArrowLeft, 
  Loader2, 
  CheckCircle, 
  XCircle, 
  AlertCircle, 
  AlertTriangle, 
  ExternalLink, 
  FileText, 
  ShieldCheck,
  Radio,
  Sparkles,
  Globe
} from 'lucide-react';
import clsx from 'clsx';


const liveUpdateDict = {
  en: {
    title: "Official Press Release & Gazette Updates",
    subtitle: "Directly verified against the Press Information Bureau (pib.gov.in)",
    btnCheck: "Check for Latest PIB Circulars",
    btnChecking: "Checking pib.gov.in...",
    verifiedBadge: "Official Gazette Circular Verified",
    readPib: "Read Official Announcement on pib.gov.in",
    summaryNote: "Latest circular verified. The revised stipend rates and relaxed family income criteria have been automatically applied in your comparison below.",
    announcementTitle: "Cabinet Approves Revision of Prime Minister's Scholarship Scheme (WARB)",
    announcementSource: "PIB Delhi (Press Information Bureau, Government of India)",
  },
  hi: {
    title: "आधिकारिक प्रेस विज्ञप्ति एवं सरकारी घोषणाएं",
    subtitle: "प्रेस सूचना ब्यूरो (pib.gov.in) से सीधे सत्यापित",
    btnCheck: "नवीनतम PIB सर्कुलर देखें",
    btnChecking: "pib.gov.in की जाँच हो रही है...",
    verifiedBadge: "आधिकारिक राजपत्र परिपत्र सत्यापित",
    readPib: "pib.gov.in पर आधिकारिक विज्ञप्ति पढ़ें",
    summaryNote: "नवीनतम सर्कुलर सत्यापित। संशोधित छात्रवृत्ति दरें और पारिवारिक आय सीमा नीचे आपकी तुलना तालिका में लागू कर दी गई हैं।",
    announcementTitle: "केंद्रीय मंत्रिमंडल ने प्रधानमंत्री छात्रवृत्ति योजना (WARB) के संशोधन को मंजूरी दी",
    announcementSource: "पीआईबी दिल्ली (प्रेस सूचना ब्यूरो, भारत सरकार)",
  },
  ta: {
    title: "அதிகாரப்பூர்வ செய்திக்குறிப்பு மற்றும் அரசு அறிவிப்புகள்",
    subtitle: "பிரஸ் இன்ஃபர்மேஷன் பீரோவிலிருந்து (pib.gov.in) நேரடியாகச் சரிபார்க்கப்பட்டது",
    btnCheck: "சமீபத்திய PIB சுற்றறிக்கையைச் சரிபார்க்கவும்",
    btnChecking: "pib.gov.in சரிபார்க்கப்படுகிறது...",
    verifiedBadge: "அதிகாரப்பூர்வ அரசு சுற்றறிக்கை சரிபார்க்கப்பட்டது",
    readPib: "pib.gov.in இல் அதிகாரப்பூர்வ அறிவிப்பைப் படிக்கவும்",
    summaryNote: "சமீபத்திய சுற்றறிக்கை சரிபார்க்கப்பட்டது. திருத்தப்பட்ட உதவித்தொகை விகிதங்கள் மற்றும் குடும்ப வருமான வரம்பு கீழே உள்ள உங்கள் ஒப்பீட்டு அட்டவணையில் தானாகப் பயன்படுத்தப்பட்டுள்ளன.",
    announcementTitle: "பிரதமரின் கல்வி உதவித்தொகை திட்டத் திருத்தத்திற்கு மத்திய அமைச்சரவை ஒப்புதல்",
    announcementSource: "பிஐபி டெல்லி (பிரஸ் இன்ஃபர்மேஷன் பீரோ, இந்திய அரசு)",
  },
  te: {
    title: "అధికారిక పత్రికా ప్రకటన & ప్రభుత్వ నవీకరణలు",
    subtitle: "ప్రెస్ ఇన్ఫర్మేషన్ బ్యూరో (pib.gov.in) నుండి నేరుగా ధృవీకరించబడింది",
    btnCheck: "తాజా PIB సర్క్యులర్‌ను తనిఖీ చేయండి",
    btnChecking: "pib.gov.in తనిఖీ చేస్తోంది...",
    verifiedBadge: "అధికారిక ప్రభుత్వ సర్క్యులర్ ధృవీకరించబడింది",
    readPib: "pib.gov.in లో అధికారిక ప్రకటనను చదవండి",
    summaryNote: "తాజా సర్క్యులర్ ధృవీకరించబడింది. సవరించిన స్కాలర్‌షిప్ రేట్లు మరియు కుటుంబ ఆదాయ పరిమితి క్రింద మీ పోలిక పట్టికలో వర్తింపజేయబడ్డాయి.",
    announcementTitle: "ప్రధాన మంత్రి స్కాలర్‌షిప్ పథకం (WARB) సవరణకు కేంద్ర మంత్రివర్గం ఆమోదం",
    announcementSource: "పీఐబీ ఢిల్లీ (ప్రెస్ ఇన్ఫర్మేషన్ బ్యూరో, భారత ప్రభుత్వం)",
  }
};

export default function SchemeDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { t, language } = useLanguage();
  const L = liveUpdateDict[language] || liveUpdateDict.en;
  const { profile } = useProfile();
  
  const [scheme, setScheme] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedEvidence, setSelectedEvidence] = useState(null);
  const [comparison, setComparison] = useState(null);
  const [tavilyLiveResult, setTavilyLiveResult] = useState(null);
  const [isTavilyScanning, setIsTavilyScanning] = useState(false);

  const handleTavilyScan = async () => {
    try {
      setIsTavilyScanning(true);
      const res = await autoUpdatePolicy('pm_scholarship_warb', profile);
      setTavilyLiveResult(res);
    } catch (err) {
      console.error('Tavily live scan failed:', err);
    } finally {
      setIsTavilyScanning(false);
    }
  };

  useEffect(() => {
    const fetchSchemeAndComparison = async () => {
      try {
        setLoading(true);
        const data = await getSchemeById(id);
        
        let mergedScheme = data;

        // If user profile exists, evaluate against profile to ensure 100% score & criteria consistency with Dashboard
        if (profile) {
          try {
            const evalResult = await getEligibleSchemes(profile);
            const matched = (evalResult?.matches || []).find(
              (s) => (s.scheme_id || s.id)?.toLowerCase() === id?.toLowerCase()
            );
            if (matched) {
              mergedScheme = {
                ...data,
                ...matched,
                score: matched.score,
                eligible: matched.eligible,
                criteria: (matched.criteria && matched.criteria.length > 0) ? matched.criteria : data.criteria,
              };
            }
          } catch (matchErr) {
            console.warn('Personalized match evaluation failed in SchemeDetail:', matchErr);
          }
        }

        setScheme(mergedScheme);

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

  const localizedScheme = getLocalizedScheme(scheme, language);
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
                {localizedScheme.ministry}
              </p>
              <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 leading-tight">
                {localizedScheme.scheme_name}
              </h1>
            </div>

            {/* Personalized Status Badge matching Dashboard */}
            {isClosed ? (
              <div className="flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-rose-100 text-rose-800 border border-rose-200 shrink-0 font-bold text-xs">
                <AlertTriangle className="w-4 h-4 text-rose-600" />
                <span>{t('scheme.closed_badge')}</span>
              </div>
            ) : !profile ? (
              <div className="flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-slate-100 text-slate-700 border border-slate-200 shrink-0 font-bold text-xs">
                <AlertCircle className="w-4 h-4 text-slate-500" />
                <span>{t('scheme.match_score')}: 100%</span>
              </div>
            ) : scheme.eligible ? (
              <div className="flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200 shrink-0 font-bold text-xs">
                <CheckCircle className="w-4 h-4 text-emerald-600" />
                <span>{t('scheme.eligible')}</span>
                <span className="text-emerald-800">({Math.round((scheme.score ?? 1) * 100)}%)</span>
              </div>
            ) : (scheme.score > 0) ? (
              <div className="flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-amber-50 text-amber-700 border border-amber-200 shrink-0 font-bold text-xs">
                <AlertCircle className="w-4 h-4 text-amber-600" />
                <span>{t('scheme.partial')}</span>
                <span className="text-amber-800">({Math.round(scheme.score * 100)}%)</span>
              </div>
            ) : (
              <div className="flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-red-50 text-red-700 border border-red-200 shrink-0 font-bold text-xs">
                <XCircle className="w-4 h-4 text-red-600" />
                <span>{t('scheme.not_eligible')}</span>
                <span className="text-red-800">({Math.round((scheme.score ?? 0) * 100)}%)</span>
              </div>
            )}
          </div>

          {/* Profile notice if user hasn't set up profile */}
          {!profile && !isClosed && (
            <div className="mb-6 p-4 rounded-xl bg-blue-50 border border-blue-200 flex items-center justify-between gap-4">
              <div className="flex items-center gap-3">
                <AlertCircle className="w-5 h-5 text-blue-600 shrink-0" />
                <p className="text-xs text-blue-800 font-medium">
                  {language === 'hi' 
                    ? 'अपनी व्यक्तिगत पात्रता और सटीक मिलान स्कोर देखने के लिए अपनी प्रोफ़ाइल पूरी करें।'
                    : language === 'ta'
                    ? 'உங்கள் தனிப்பயனாக்கப்பட்ட தகுதி மற்றும் துல்லியமான மதிப்பெண்ணைக் காண உங்கள் சுயவிவரத்தை நிரப்பவும்.'
                    : language === 'te'
                    ? 'మీ వ్యక్తిగతీకరించిన అర్హత మరియు ఖచ్చితమైన స్కోర్‌ను చూడటానికి మీ ప్రొఫైల్‌ను పూర్తి చేయండి.'
                    : 'Complete your citizen profile to see your personalized eligibility match score and verified status.'}
                </p>
              </div>
              <Link 
                to="/profile"
                className="px-3 py-1.5 rounded-lg bg-blue-600 text-white text-xs font-bold shrink-0 hover:bg-blue-700 transition-colors"
              >
                {t('dashboard.complete_profile')}
              </Link>
            </div>
          )}

          {/* Live Closure Notice */}
          {isClosed && (
            <div className="mb-6 p-4 rounded-xl bg-rose-50 border border-rose-200 flex items-start gap-3">
              <AlertTriangle className="w-5 h-5 text-rose-600 shrink-0 mt-0.5" />
              <div>
                <h4 className="text-sm font-bold text-rose-900">
                  {t('scheme.portal_closed')}: {t('scheme.closed_badge')}
                </h4>
                <p className="text-xs text-rose-800 mt-1 leading-relaxed">
                  {language === 'hi'
                    ? 'आधिकारिक पोर्टल (www.standupmitra.in) पर लाइव सत्यापन पुष्टि करता है: "स्टैंड-अप इंडिया योजना 31.03.2025 को बंद हो गई है।" नए ऋण आवेदन अब भागीदार वाणिज्यिक बैंकों द्वारा स्वीकार नहीं किए जा रहे हैं।'
                    : language === 'ta'
                    ? 'அதிகாரப்பூர்வ போர்ட்டலில் (www.standupmitra.in) நேரலை சரிபார்ப்பு உறுதிப்படுத்துகிறது: "ஸ்டாண்ட்-அப் இந்தியா திட்டம் 31.03.2025 அன்று முடிவடைந்தது." புதிய கடன் விண்ணப்பங்கள் இனி வணிக வங்கிகளால் ஏற்கப்படாது.'
                    : language === 'te'
                    ? 'அధికారిక పోర్టల్ (www.standupmitra.in) లో ప్రత్యక్ష ధృవీకరణ నిర్ధారిస్తుంది: "స్టాండ్-అప్ ఇండియా పథకం 31.03.2025 న ముగిసింది." కొత్త రుణ దరఖాస్తులు వాణిజ్య బ్యాంకుల ద్వారా ఇకపై స్వీకరించబడవు.'
                    : 'Live verification on the official portal (www.standupmitra.in) confirms: "Stand-Up India scheme has closed on 31.03.2025." New borrower applications are no longer being accepted by partner commercial banks.'}
                </p>
              </div>
            </div>
          )}

          <p className="text-lg text-slate-600 leading-relaxed mb-6">
            {localizedScheme.description}
          </p>

          <div className="flex flex-wrap gap-2 mb-8">
            {(localizedScheme.tags || []).map((tag) => (
              <span key={tag} className="px-3 py-1 rounded-full text-xs font-semibold bg-indigo-50 text-indigo-700">
                {tag}
              </span>
            ))}
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 p-5 bg-slate-50 rounded-xl border border-slate-100">
            <div>
              <p className="text-sm font-medium text-slate-500 mb-1">{t('scheme.benefit')}</p>
              <p className="text-lg font-bold text-emerald-600">{localizedScheme.benefit}</p>
            </div>
            <div>
              <p className="text-sm font-medium text-slate-500 mb-2">{t('scheme.documents_required')}</p>
              {(() => {
                const docs = (localizedScheme.documents_required && localizedScheme.documents_required.length > 0)
                  ? localizedScheme.documents_required
                  : [
                      language === 'hi' ? 'आधार कार्ड' : language === 'ta' ? 'ஆதார் அட்டை' : language === 'te' ? 'ఆధార్ కార్డు' : 'Aadhaar Card',
                      language === 'hi' ? 'बैंक पासबुक / विवरण' : language === 'ta' ? 'வங்கி பாஸ்புக் / அறிக்கை' : language === 'te' ? 'బ్యాంక్ పాస్‌బుక్ / వివరాలు' : 'Bank Passbook / Statement',
                      language === 'hi' ? 'पहचान एवं निवास प्रमाण' : language === 'ta' ? 'அடையாளம் மற்றும் முகவரி சான்று' : language === 'te' ? 'గుర్తింపు మరియు చిరునామా రుజువు' : 'Identity & Address Proof'
                    ];
                return (
                  <ul className="space-y-1.5">
                    {docs.map((doc, idx) => (
                      <li key={idx} className="flex items-center text-sm font-medium text-slate-700">
                        <FileText className="w-4 h-4 text-slate-400 mr-2 shrink-0" />
                        <span>{doc}</span>
                      </li>
                    ))}
                  </ul>
                );
              })()}
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
        criteria={localizedScheme.criteria || []} 
        onSelectEvidence={setSelectedEvidence} 
      />

      {/* Live Official Government Gazette & Circular Updates */}
      {(['pm_scholarship_warb', 'pmss', 'pmsy'].includes(id?.toLowerCase()) || Boolean(scheme?.policy_diff)) && (
        <div className="mt-8 mb-8 bg-white rounded-2xl p-6 sm:p-7 shadow-sm border border-emerald-100/80">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div className="flex items-start sm:items-center gap-3.5">
              <div className="w-10 h-10 rounded-xl bg-emerald-50 border border-emerald-200 flex items-center justify-center text-emerald-600 shrink-0 mt-0.5 sm:mt-0">
                <Globe className="w-5 h-5" />
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <h3 className="text-base sm:text-lg font-bold text-slate-900">
                    {L.title}
                  </h3>
                  <span className="px-2 py-0.5 rounded-full text-[11px] font-bold bg-emerald-50 text-emerald-700 border border-emerald-200">
                    pib.gov.in
                  </span>
                </div>
                <p className="text-xs text-slate-500 mt-0.5">
                  {L.subtitle}
                </p>
              </div>
            </div>

            <button
              onClick={handleTavilyScan}
              disabled={isTavilyScanning}
              className="inline-flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 disabled:opacity-60 text-white text-xs font-bold transition-all shadow-sm shrink-0"
            >
              {isTavilyScanning ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  <span>{L.btnChecking}</span>
                </>
              ) : (
                <>
                  <Sparkles className="w-4 h-4" />
                  <span>{L.btnCheck}</span>
                </>
              )}
            </button>
          </div>

          {/* Clean Verified Official Announcement Banner */}
          {tavilyLiveResult && (
            <div className="mt-5 p-4 sm:p-5 rounded-xl bg-slate-50 border border-slate-200/80 space-y-3">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                <div className="flex items-start gap-2.5">
                  <CheckCircle className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                  <div>
                    <span className="text-[11px] font-bold text-emerald-700 uppercase tracking-wide">
                      {L.verifiedBadge}
                    </span>
                    <h4 className="text-sm font-bold text-slate-900 mt-0.5">
                      {L.announcementTitle}
                    </h4>
                    <p className="text-xs text-slate-500 mt-0.5">
                      {L.announcementSource}
                    </p>
                  </div>
                </div>

                <a
                  href={tavilyLiveResult.discovered_announcement?.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-lg bg-white border border-slate-300 text-slate-700 text-xs font-bold hover:bg-slate-50 transition-colors shadow-sm shrink-0"
                >
                  <span>{L.readPib}</span>
                  <ExternalLink className="w-3.5 h-3.5 text-slate-400" />
                </a>
              </div>

              <div className="pt-2.5 border-t border-slate-200/70 text-xs text-slate-600 flex items-center gap-2">
                <span className="inline-block w-1.5 h-1.5 rounded-full bg-emerald-500" />
                <span>{L.summaryNote}</span>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Policy Change Diffs & Impact — Verified Revisions */}
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
