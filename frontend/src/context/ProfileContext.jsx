import { createContext, useContext, useReducer } from 'react';

const ProfileContext = createContext();

function profileReducer(state, action) {
  switch (action.type) {
    case 'SET_PROFILE':
      return { ...action.payload };
    case 'UPDATE_FIELD':
      return state ? { ...state, [action.field]: action.value } : state;
    case 'CLEAR_PROFILE':
      return null;
    default:
      return state;
  }
}

export function ProfileProvider({ children }) {
  const [profile, dispatch] = useReducer(profileReducer, null);

  return (
    <ProfileContext.Provider value={{ profile, dispatch }}>
      {children}
    </ProfileContext.Provider>
  );
}

export function useProfile() {
  const context = useContext(ProfileContext);
  if (!context) throw new Error('useProfile must be used within ProfileProvider');
  return context;
}
