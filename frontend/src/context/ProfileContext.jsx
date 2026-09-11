import { createContext, useContext, useReducer } from 'react';

const ProfileContext = createContext();

const defaultProfile = {
  full_name: '',
  age: '',
  gender: 'male',
  category: 'General',
  state: '',
  district: '',
  is_rural: false,
  annual_income: '',
  occupation: '',
  education: '',
  has_land: false,
  land_acres: '',
  has_bpl_card: false,
  disability: false,
  minority: false,
  ration_card_type: 'None',
  documents: [],
};

function profileReducer(state, action) {
  switch (action.type) {
    case 'SET_PROFILE':
      return { ...action.payload };
    case 'UPDATE_FIELD':
      return { ...(state || defaultProfile), [action.field]: action.value };
    case 'CLEAR_PROFILE':
      return { ...defaultProfile };
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
