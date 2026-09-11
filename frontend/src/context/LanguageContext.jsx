import { createContext, useContext, useState, useCallback } from 'react';
import translations from '../mock/translations';

const LanguageContext = createContext();

export function LanguageProvider({ children }) {
  const [language, setLanguageState] = useState(() => {
    try {
      return localStorage.getItem('civiq_language') || 'en';
    } catch {
      return 'en';
    }
  });

  const setLanguage = useCallback((lang) => {
    setLanguageState(lang);
    try {
      localStorage.setItem('civiq_language', lang);
    } catch (e) {
      console.error('Failed to save language to localStorage:', e);
    }
  }, []);

  const t = useCallback(
    (key) => {
      const langMap = translations[language] || translations.en;
      return langMap[key] || translations.en[key] || key;
    },
    [language]
  );

  return (
    <LanguageContext.Provider value={{ language, setLanguage, t }}>
      {children}
    </LanguageContext.Provider>
  );
}

export function useLanguage() {
  const context = useContext(LanguageContext);
  if (!context) throw new Error('useLanguage must be used within LanguageProvider');
  return context;
}
