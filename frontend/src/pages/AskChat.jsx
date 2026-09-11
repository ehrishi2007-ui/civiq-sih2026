import { useState, useRef, useEffect } from 'react';
import { useLanguage } from '../context/LanguageContext';
import { askQuestion } from '../services/askService';
import { Send, User, Bot, Loader2, Info } from 'lucide-react';
import clsx from 'clsx';

export default function AskChat() {
  const { t } = useLanguage();
  const [messages, setMessages] = useState([
    { role: 'system', content: 'Hi! I am CiviQ. Ask me any question about government schemes, eligibility, or application processes.' }
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
    setMessages(prev => [...prev, { role: 'user', content: userMsg }]);
    setIsLoading(true);

    try {
      const response = await askQuestion(userMsg);
      setMessages(prev => [...prev, { role: 'system', content: response.answer }]);
    } catch (error) {
      setMessages(prev => [...prev, { role: 'system', content: 'Sorry, I am having trouble connecting right now.' }]);
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
              'flex max-w-[85%] sm:max-w-[75%]',
              msg.role === 'user' ? 'ml-auto' : 'mr-auto'
            )}>
              {msg.role !== 'user' && (
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-civiq-100 flex items-center justify-center mr-3 mt-1">
                  <Bot className="w-5 h-5 text-civiq-600" />
                </div>
              )}
              
              <div className={clsx(
                'px-4 py-3 rounded-2xl text-sm sm:text-base leading-relaxed shadow-sm',
                msg.role === 'user' 
                  ? 'bg-civiq-600 text-white rounded-tr-sm' 
                  : 'bg-slate-50 border border-slate-100 text-slate-800 rounded-tl-sm'
              )}>
                {msg.content}
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
                <Loader2 className="w-4 h-4 animate-spin" />
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
