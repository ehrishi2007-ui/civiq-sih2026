import { useState, useRef, useEffect } from 'react';
import { useLanguage } from '../context/LanguageContext';
import { askQuestion } from '../services/askService';
import { Send, User, Bot, Loader2, Info, BookOpen, ChevronDown, FileText, ExternalLink } from 'lucide-react';
import clsx from 'clsx';

function renderFormattedText(text) {
  const parts = text.split(/(\*\*[^*]+\*\*)/g);
  return parts.map((part, i) => {
    if (part.startsWith('**') && part.endsWith('**')) {
      return (
        <strong key={i} className="font-bold text-slate-900">
          {part.slice(2, -2)}
        </strong>
      );
    }
    return part;
  });
}

function FormattedBotMessage({ content, sources }) {
  const { t } = useLanguage();
  const [showSources, setShowSources] = useState(false);
  const lines = (content || '').split('\n');

  return (
    <div className="space-y-2 w-full">
      <div className="text-slate-800 leading-relaxed space-y-2">
        {lines.map((line, idx) => {
          const trimmed = line.trim();
          if (!trimmed) return <div key={idx} className="h-1" />;

          if (trimmed.startsWith('### ') || trimmed.startsWith('## ')) {
            const title = trimmed.replace(/^#+\s*/, '').replace(/\*\*/g, '');
            return (
              <h4 key={idx} className="font-bold text-slate-900 text-sm sm:text-base mt-2 mb-1 flex items-center gap-1.5">
                <span className="w-1.5 h-1.5 rounded-full bg-civiq-600 inline-block shrink-0"></span>
                {title}
              </h4>
            );
          }

          if (trimmed.startsWith('* ') || trimmed.startsWith('- ')) {
            const bulletText = trimmed.replace(/^[\*\-]\s*/, '');
            return (
              <div key={idx} className="flex items-start gap-2 pl-2">
                <span className="text-civiq-600 font-bold mt-1 text-xs shrink-0">•</span>
                <span className="flex-1">{renderFormattedText(bulletText)}</span>
              </div>
            );
          }

          return (
            <p key={idx} className="leading-relaxed">
              {renderFormattedText(trimmed)}
            </p>
          );
        })}
      </div>

      {sources && sources.length > 0 && (
        <div className="mt-3 pt-3 border-t border-slate-200/80">
          <button
            type="button"
            onClick={() => setShowSources(!showSources)}
            className="inline-flex items-center gap-1.5 text-xs font-semibold text-civiq-700 hover:text-civiq-800 bg-civiq-50 hover:bg-civiq-100 px-2.5 py-1 rounded-md transition-colors"
          >
            <BookOpen className="w-3.5 h-3.5" />
            <span>{sources.length} {t('ask.citations')}</span>
            <ChevronDown className={clsx('w-3 h-3 transition-transform', showSources && 'rotate-180')} />
          </button>

          {showSources && (
            <div className="mt-2 space-y-2">
              {sources.map((src, sIdx) => {
                const docName = src.doc_name || src.document;
                return (
                  <div key={sIdx} className="bg-white border border-slate-200 rounded-lg p-3 text-xs shadow-xs">
                    <div className="flex flex-wrap items-center justify-between font-bold text-slate-800 mb-1 gap-2">
                      <span className="flex items-center gap-1 text-civiq-700">
                        <FileText className="w-3.5 h-3.5" />
                        {docName || 'Official Document'}
                      </span>
                      <div className="flex items-center gap-2">
                        <span className="text-slate-500 font-medium">{t('common.pg')} {src.page}</span>
                        {docName && (
                          <a
                            href={`http://127.0.0.1:8000/api/v1/documents/${encodeURIComponent(docName)}${src.page ? `#page=${src.page}` : ''}`}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="inline-flex items-center gap-1 px-2 py-0.5 rounded bg-civiq-100 hover:bg-civiq-200 text-civiq-800 text-xs font-bold transition-colors shadow-2xs"
                            title="Open official PDF"
                          >
                            <ExternalLink className="w-3 h-3" />
                            {t('ask.open_pdf')}
                          </a>
                        )}
                      </div>
                    </div>
                    {src.section && (
                      <p className="text-slate-500 font-semibold mb-1">{src.section}</p>
                    )}
                    {src.quote && (
                      <blockquote className="italic text-slate-600 border-l-2 border-civiq-300 pl-2 mt-1">
                        "{src.quote}"
                      </blockquote>
                    )}
                  </div>
                );
              })}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default function AskChat() {
  const { t } = useLanguage();
  const [messages, setMessages] = useState([
    {
      role: 'system',
      content: t('ask.initial_message'),
      sources: []
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMsg = input.trim();
    setInput('');
    setMessages(prev => [...prev, { role: 'user', content: userMsg, sources: [] }]);
    setIsLoading(true);

    try {
      const response = await askQuestion(userMsg);
      setMessages(prev => [
        ...prev,
        {
          role: 'system',
          content: response.answer || response.text || 'Information retrieved.',
          sources: response.sources || []
        }
      ]);
    } catch (error) {
      setMessages(prev => [
        ...prev,
        {
          role: 'system',
          content: t('ask.error_message'),
          sources: []
        }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-8 sm:px-6 lg:px-8 h-[calc(100vh-4rem)] flex flex-col">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-slate-900 mb-2">{t('ask.title')}</h1>
        <p className="text-slate-600">{t('ask.subtitle')}</p>
      </div>

      <div className="flex-1 bg-white rounded-2xl shadow-sm border border-slate-200 flex flex-col overflow-hidden">
        
        {/* Chat area */}
        <div className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-6">
          {messages.map((msg, idx) => (
            <div key={idx} className={clsx(
              'flex max-w-[90%] sm:max-w-[80%]',
              msg.role === 'user' ? 'ml-auto' : 'mr-auto'
            )}>
              {msg.role !== 'user' && (
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-civiq-100 flex items-center justify-center mr-3 mt-1">
                  <Bot className="w-5 h-5 text-civiq-600" />
                </div>
              )}
              
              <div className={clsx(
                'px-4 py-3 rounded-2xl text-sm sm:text-base leading-relaxed shadow-sm w-full',
                msg.role === 'user' 
                  ? 'bg-civiq-600 text-white rounded-tr-sm' 
                  : 'bg-slate-50 border border-slate-200/80 text-slate-800 rounded-tl-sm'
              )}>
                {msg.role === 'user' ? (
                  <p className="whitespace-pre-wrap">{msg.content}</p>
                ) : (
                  <FormattedBotMessage content={msg.content} sources={msg.sources} />
                )}
              </div>

              {msg.role === 'user' && (
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-slate-200 flex items-center justify-center ml-3 mt-1">
                  <User className="w-5 h-5 text-slate-600" />
                </div>
              )}
            </div>
          ))}

          {isLoading && (
            <div className="flex max-w-[80%] mr-auto">
              <div className="flex-shrink-0 w-8 h-8 rounded-full bg-civiq-100 flex items-center justify-center mr-3 mt-1">
                <Bot className="w-5 h-5 text-civiq-600" />
              </div>
              <div className="px-4 py-3 rounded-2xl bg-slate-50 border border-slate-100 text-slate-500 rounded-tl-sm flex items-center gap-2">
                <Loader2 className="w-4 h-4 animate-spin text-civiq-600" />
                <span className="text-sm font-medium">{t('ask.thinking')}</span>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input area */}
        <div className="p-4 bg-slate-50 border-t border-slate-200">
          <form onSubmit={handleSubmit} className="flex items-end gap-3 max-w-4xl mx-auto">
            <div className="flex-1 relative">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder={t('ask.placeholder')}
                disabled={isLoading}
                className="w-full px-4 py-3 rounded-xl border-slate-300 focus:border-civiq-500 focus:ring-civiq-500 pr-12 shadow-sm disabled:opacity-50"
              />
            </div>
            <button
              type="submit"
              disabled={!input.trim() || isLoading}
              className="flex-shrink-0 px-4 py-3 bg-civiq-600 text-white rounded-xl font-medium hover:bg-civiq-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors shadow-sm inline-flex items-center"
            >
              <Send className="w-5 h-5 sm:mr-2" />
              <span className="hidden sm:inline">{t('ask.send')}</span>
            </button>
          </form>
          <div className="mt-3 flex items-center justify-center text-xs text-slate-400 gap-1">
            <Info className="w-3 h-3" />
            AI can make mistakes. Verify important information.
          </div>
        </div>

      </div>
    </div>
  );
}
