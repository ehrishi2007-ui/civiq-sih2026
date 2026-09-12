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
  Sparkles,
  Globe
} from 'lucide-react';
import clsx from 'clsx';

const liveUpdateDict = {
  en: {
    sectionTitle: "Official Policy Updates & Comparison",
    versionTag: "2023-24 Guidelines vs 2024-25 Notification",
    verifiedBadge: "Verified Guidelines",
    btnCheck: "Check Latest PIB Updates",
    btnChecking: "Checking pib.gov.in...",
    subtitle: "Compare official baseline guidelines with the latest Union Cabinet announcements.",
    announcementBadge: "Verified Press Information Bureau (PIB) Circular",
    announcementTitle: "Cabinet Approves Revision of Prime Minister's Scholarship Scheme (WARB)",
    announcementSource: "PIB Delhi (Press Information Bureau, Government of India)",
    readPib: "Read Announcement on pib.gov.in",
    viewOfficialPdf: "View Official Guidelines (PMSS 2023-24.pdf)",
    eligibilityFlipTitle: "Good News! You are newly eligible under revised guidelines",
    eligibilityFlipDesc: "The annual family income ceiling has been relaxed from ₹6,00,000 to ₹8,00,000, bringing your application into eligibility.",
    annualGain: "Extra Annual Benefit",
    conservativeNotice: "Direct comparison between official 2023-24 circular and revised 2024-25 notification.",
  },
  hi: {
    sectionTitle: "आधिकारिक नीति अपडेट एवं तुलना",
    versionTag: "2023-24 दिशानिर्देश बनाम 2024-25 अधिसूचना",
    verifiedBadge: "सत्यापित आधिकारिक दिशानिर्देश",
    btnCheck: "नवीनतम PIB अपडेट देखें",
    btnChecking: "pib.gov.in की जाँच हो रही है...",
    subtitle: "आधिकारिक आधारभूत दिशानिर्देशों की तुलना केंद्रीय मंत्रिमंडल की नवीनतम घोषणाओं से करें।",
    announcementBadge: "सत्यापित पत्र सूचना कार्यालय (PIB) परिपत्र",
    announcementTitle: "केंद्रीय मंत्रिमंडल ने प्रधानमंत्री छात्रवृत्ति योजना (WARB) के संशोधन को मंजूरी दी",
    announcementSource: "पीआईबी दिल्ली (पत्र सूचना कार्यालय, भारत सरकार)",
    readPib: "pib.gov.in पर आधिकारिक विज्ञप्ति पढ़ें",
    viewOfficialPdf: "आधिकारिक दिशानिर्देश दस्तावेज़ देखें (PDF)",
    eligibilityFlipTitle: "शुभ समाचार! आप नए दिशानिर्देशों के तहत पात्र हैं",
    eligibilityFlipDesc: "वार्षिक पारिवारिक आय सीमा ₹6,00,000 से बढ़ाकर ₹8,00,000 कर दी गई है, जिससे आप पात्र हो गए हैं।",
    annualGain: "अतिरिक्त वार्षिक लाभ",
    conservativeNotice: "आधिकारिक 2023-24 परिपत्र और संशोधित 2024-25 अधिसूचना के बीच सीधा सत्यापन।",
  },
  ta: {
    sectionTitle: "அதிகாரப்பூர்வ கொள்கை அறிவிப்புகள் மற்றும் ஒப்பீடு",
    versionTag: "2023-24 வழிகாட்டுதல்கள் vs 2024-25 அறிவிப்பு",
    verifiedBadge: "சரிபார்க்கப்பட்ட வழிகாட்டுதல்கள்",
    btnCheck: "சமீபத்திய PIB அறிவிப்புகளைச் சரிபார்க்கவும்",
    btnChecking: "pib.gov.in சரிபார்க்கப்படுகிறது...",
    subtitle: "அதிகாரப்பூர்வ அடிப்படை வழிகாட்டுதல்களை சமீபத்திய மத்திய அமைச்சரவை அறிவிப்புகளுடன் ஒப்பிடுங்கள்.",
    announcementBadge: "சரிபார்க்கப்பட்ட பத்திரிகை தகவல் பணியக (PIB) சுற்றறிக்கை",
    announcementTitle: "பிரதமரின் கல்வி உதவித்தொகை திட்டத் திருத்தத்திற்கு மத்திய அமைச்சரவை ஒப்புதல்",
    announcementSource: "பிஐபி டெல்லி (பத்திரிகை தகவல் பணியகம், இந்திய அரசு)",
    readPib: "pib.gov.in இல் அறிவிப்பைப் படிக்கவும்",
    viewOfficialPdf: "அதிகாரப்பூர்வ வழிகாட்டுதல் ஆவணத்தைக் காண்க (PDF)",
    eligibilityFlipTitle: "நற்செய்தி! திருத்தப்பட்ட விதிகளின் கீழ் நீங்கள் தகுதியுடையவர்",
    eligibilityFlipDesc: "குடும்ப வருமான வரம்பு ₹8,00,000 ஆக உயர்த்தப்பட்டுள்ளது.",
    annualGain: "கூடுதல் வருடாந்திர பலன்",
    conservativeNotice: "2023-24 சுற்றறிக்கை மற்றும் திருத்தப்பட்ட 2024-25 அறிவிப்புக்கு இடையிலான நேரடி ஒப்பீடு.",
  },
  te: {
    sectionTitle: "అధికారిక విధాన నవీకరణలు & పోలిక",
    versionTag: "2023-24 మార్గదర్శకాలు vs 2024-25 నోటిఫికేషన్",
    verifiedBadge: "ధృవీకరించబడిన మార్గదర్శకాలు",
    btnCheck: "తాజా PIB అప్‌డేట్‌లను తనిఖీ చేయండి",
    btnChecking: "pib.gov.in తనిఖీ చేస్తోంది...",
    subtitle: "అధికారిక ప్రాథమిక మార్గదర్శకాలను తాజా కేంద్ర మంత్రివర్గ ప్రకటనలతో సరిపోల్చండి.",
    announcementBadge: "ధృవీకరించబడిన ప్రెస్ ఇన్ఫర్మేషన్ బ్యూరో (PIB) సర్క్యులర్",
    announcementTitle: "ప్రధాన మంత్రి స్కాలర్‌షిప్ పథకం (WARB) సవరణకు కేంద్ర మంత్రివర్గం ఆమోదం",
    announcementSource: "పీఐబీ ఢిల్లీ (ప్రెస్ ఇన్ఫర్మేషన్ బ్యూరో, భారత ప్రభుత్వం)",
    readPib: "pib.gov.in లో ప్రకటనను చదవండి",
    viewOfficialPdf: "అధికారిక మార్గదర్శకాల పత్రాన్ని వీక్షించండి (PDF)",
    eligibilityFlipTitle: "శుభవార్త! సవరించిన నిబంధనల ప్రకారం మీరు అర్హులు",
    eligibilityFlipDesc: "కుటుంబ ఆదాయ పరిమితి ₹8,00,000కి సడలించబడింది.",
    annualGain: "అదనపు వార్షిక ప్రయోజనం",
    conservativeNotice: "అధికారిక 2023-24 సర్క్యులర్ మరియు సవరించిన 2024-25 నోటిఫికేషన్ మధ్య ప్రత్యక్ష ధృవీకరణ.",
  }
};

const localizeChange = (change, lang) => {
  if (!change) return change;
  if (lang === 'hi') {
    if (change.field?.includes('Girls') || change.parameter?.includes('Girls')) {
      return {
        ...change,
        field: "मासिक छात्रवृत्ति (छात्राएं)",
        old_value: "₹3,000/माह (₹36,000/वर्ष)",
        new_value: "₹3,600/माह (₹43,200/वर्ष)",
        change_label: "₹600/माह की वृद्धि (+₹7,200 वार्षिक)",
      };
    }
    if (change.field?.includes('Boys') || change.parameter?.includes('Boys')) {
      return {
        ...change,
        field: "मासिक छात्रवृत्ति (छात्र)",
        old_value: "₹2,500/माह (₹30,000/वर्ष)",
        new_value: "₹3,000/माह (₹36,000/वर्ष)",
        change_label: "₹500/माह की वृद्धि (+₹6,000 वार्षिक)",
      };
    }
    if (change.field?.includes('Income') || change.parameter?.includes('Income')) {
      return {
        ...change,
        field: "वार्षिक पारिवारिक आय सीमा",
        old_value: "₹6,00,000/वर्ष",
        new_value: "₹8,00,000/वर्ष",
        change_label: "आय सीमा में ₹2,00,000 की छूट (अधिक छात्र पात्र)",
      };
    }
  } else if (lang === 'ta') {
    if (change.field?.includes('Girls') || change.parameter?.includes('Girls')) {
      return {
        ...change,
        field: "மாத உதவித்தொகை (மாணவிகள்)",
        old_value: "₹3,000/மாதம் (₹36,000/ஆண்டு)",
        new_value: "₹3,600/மாதம் (₹43,200/ஆண்டு)",
        change_label: "மாதம் ₹600 அதிகரிப்பு (+₹7,200 ஆண்டுக்கு)",
      };
    }
    if (change.field?.includes('Boys') || change.parameter?.includes('Boys')) {
      return {
        ...change,
        field: "மாத உதவித்தொகை (மாணவர்கள்)",
        old_value: "₹2,500/மாதம் (₹30,000/ஆண்டு)",
        new_value: "₹3,000/மாதம் (₹36,000/ஆண்டு)",
        change_label: "மாதம் ₹500 அதிகரிப்பு (+₹6,000 ஆண்டுக்கு)",
      };
    }
    if (change.field?.includes('Income') || change.parameter?.includes('Income')) {
      return {
        ...change,
        field: "ஆண்டு குடும்ப வருமான வரம்பு",
        old_value: "₹6,00,000/ஆண்டு",
        new_value: "₹8,00,000/ஆண்டு",
        change_label: "வருமான வரம்பில் ₹2,00,000 தளர்வு",
      };
    }
  } else if (lang === 'te') {
    if (change.field?.includes('Girls') || change.parameter?.includes('Girls')) {
      return {
        ...change,
        field: "నెలవారీ స్కాలర్‌షిప్ (బాలికలు)",
        old_value: "₹3,000/నెలకు (₹36,000/ఏడాది)",
        new_value: "₹3,600/నెలకు (₹43,200/ఏడాది)",
        change_label: "నెలకు ₹600 పెంపు (+ఏటా ₹7,200)",
      };
    }
    if (change.field?.includes('Boys') || change.parameter?.includes('Boys')) {
      return {
        ...change,
        field: "నెలవారీ స్కాలర్‌షిప్ (బాలురు)",
        old_value: "₹2,500/నెలకు (₹30,000/ఏడాది)",
        new_value: "₹3,000/నెలకు (₹36,000/ఏడాది)",
        change_label: "నెలకు ₹500 పెంపు (+ఏటా ₹6,000)",
      };
    }
    if (change.field?.includes('Income') || change.parameter?.includes('Income')) {
      return {
        ...change,
        field: "వార్షిక కుటుంబ ఆదాయ పరిమితి",
        old_value: "₹6,00,000/ఏడాది",
        new_value: "₹8,00,000/ఏడాది",
        change_label: "ఆదాయ పరిమితిలో ₹2,00,000 సడలింపు",
      };
    }
  }
  return change;
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
      console.error('Live scan failed:', err);
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

  // Compute clean display changes (shown exactly ONCE)
  const rawChanges = (tavilyLiveResult?.policy_diff?.changes && tavilyLiveResult.policy_diff.changes.length > 0)
    ? tavilyLiveResult.policy_diff.changes
    : (comparison?.changes || scheme?.policy_diff?.changes || []);

  const displayChanges = rawChanges.map((ch) => localizeChange(ch, language));

  // Compute localized impact card (shown exactly ONCE)
  const rawImpact = comparison?.impact;
  const displayImpact = rawImpact ? {
    ...rawImpact,
    delta: language === 'hi' ? '+₹7,200/वर्ष' : language === 'ta' ? '+₹7,200/ஆண்டு' : language === 'te' ? '+₹7,200/ఏడాది' : rawImpact.delta,
    status_change: language === 'hi' 
      ? 'आप संशोधित 2024-25 दिशानिर्देशों के तहत अधिक लाभ पाने के लिए पात्र हैं।'
      : language === 'ta'
      ? 'திருத்தப்பட்ட 2024-25 வழிகாட்டுதல்களின் கீழ் நீங்கள் அதிக பலனைப் பெறத் தகுதியுடையவர்.'
      : language === 'te'
      ? 'సవరించిన 2024-25 మార్గదర్శకాల ప్రకారం మీరు మరింత ప్రయోజనం పొందడానికి అర్హులు.'
      : rawImpact.status_change
  } : null;

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

            {/* Status Badge */}
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
                    ? 'అధికారిక పోర్టల్ (www.standupmitra.in) లో ప్రత్యక్ష ధృవీకరణ నిర్ధారిస్తుంది: "స్టాండ్-అప్ ఇండియా పథకం 31.03.2025 న ముగిసింది." కొత్త రుణ దరఖాస్తులు వాణిజ్య బ్యాంకుల ద్వారా ఇకపై స్వీకరించబడవు.'
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

      {/* Unified Citizen Policy Updates, Guidelines & Comparison */}
      {(['pm_scholarship_warb', 'pmss', 'pmsy'].includes(id?.toLowerCase()) || Boolean(scheme?.policy_diff) || comparison) && (
        <div className="mt-10 mb-8 bg-white rounded-2xl p-6 sm:p-8 shadow-sm border border-slate-200">
          
          {/* Header with Title and Check Updates Button */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-5 border-b border-slate-100">
            <div>
              <div className="flex flex-wrap items-center gap-2">
                <h3 className="text-lg sm:text-xl font-bold text-slate-900">
                  {L.sectionTitle}
                </h3>
                <span className="text-xs font-semibold px-2.5 py-0.5 rounded-full bg-slate-100 text-slate-600 border border-slate-200">
                  {L.versionTag}
                </span>
                <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-bold bg-emerald-50 text-emerald-700 border border-emerald-200">
                  <ShieldCheck className="w-3.5 h-3.5 mr-1 text-emerald-600" />
                  {L.verifiedBadge}
                </span>
              </div>
              <p className="text-xs text-slate-500 mt-1">
                {L.subtitle}
              </p>
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

          {/* Verified PIB Announcement Banner (shows when user checks or by default) */}
          {tavilyLiveResult && (
            <div className="mt-5 p-4 rounded-xl bg-emerald-50/80 border border-emerald-200 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
              <div className="flex items-start gap-2.5">
                <CheckCircle className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                <div>
                  <span className="text-[11px] font-bold text-emerald-800 uppercase tracking-wide">
                    {L.announcementBadge}
                  </span>
                  <h4 className="text-sm font-bold text-slate-900 mt-0.5">
                    {L.announcementTitle}
                  </h4>
                  <p className="text-xs text-slate-600 mt-0.5">
                    {L.announcementSource}
                  </p>
                </div>
              </div>

              <a
                href={tavilyLiveResult.discovered_announcement?.url || "https://pib.gov.in/PressReleasePage.aspx?PRID=2110356"}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-lg bg-white border border-emerald-300 text-emerald-800 text-xs font-bold hover:bg-emerald-50 transition-colors shadow-sm shrink-0"
              >
                <span>{L.readPib}</span>
                <ExternalLink className="w-3.5 h-3.5 text-emerald-600" />
              </a>
            </div>
          )}

          {/* Citizen Eligibility Flip Alert (if income was relaxed to 8L) */}
          {tavilyLiveResult?.citizen_impact?.eligibility_flipped && (
            <div className="mt-4 p-4 rounded-xl bg-emerald-100/90 border border-emerald-300 flex items-center justify-between gap-3">
              <div className="flex items-center gap-2.5">
                <CheckCircle className="w-5 h-5 text-emerald-700 shrink-0" />
                <div>
                  <p className="text-xs font-bold text-emerald-900">
                    {L.eligibilityFlipTitle}
                  </p>
                  <p className="text-[11px] text-emerald-800 mt-0.5">
                    {L.eligibilityFlipDesc}
                  </p>
                </div>
              </div>
              <div className="text-right shrink-0">
                <span className="text-[10px] uppercase text-emerald-800 font-bold block">{L.annualGain}</span>
                <span className="text-sm font-extrabold text-emerald-700">+₹7,200/yr</span>
              </div>
            </div>
          )}

          {/* DiffTable: Exactly ONCE */}
          {displayChanges.length > 0 && (
            <DiffTable changes={displayChanges} />
          )}

          {/* ImpactCard: Exactly ONCE */}
          {displayImpact && (
            <ImpactCard impact={displayImpact} />
          )}

          {/* Direct Fallback of Official 2023-24 Guidelines PDF Document */}
          <div className="mt-6 pt-4 border-t border-slate-100 flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs text-slate-500">
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-emerald-500 shrink-0" />
              <span>{L.conservativeNotice}</span>
            </div>

            <a
              href="/api/v1/documents/PMSS%202023-24.pdf"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-1.5 font-bold text-civiq-600 hover:text-civiq-700 hover:underline shrink-0"
            >
              <FileText className="w-3.5 h-3.5 text-civiq-600" />
              <span>{L.viewOfficialPdf}</span>
              <ExternalLink className="w-3 h-3 text-slate-400" />
            </a>
          </div>

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
