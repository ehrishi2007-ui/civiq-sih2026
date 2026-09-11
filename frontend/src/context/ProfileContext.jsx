import { createContext, useContext, useReducer } from 'react';

const ProfileContext = createContext();

const defaultProfile = {
  full_name: '',
  age: '',
  gender: 'female',
  category: 'General',
  state: '',
  district: '',
  is_rural: false,
  annual_income: '',
  occupation: 'Student',
  education: '10th Pass',
  marks_percentage: '',
  has_land: false,
  land_acres: '',
  has_bpl_card: false,
  is_ex_serviceman: false,
  enterprise_type: 'greenfield',
  ration_card_type: 'None',
  disability: false,
  minority: false,
  documents: [],
};

function getSavedProfile() {
  try {
    const saved = localStorage.getItem('civiq_user_profile');
    if (saved) return JSON.parse(saved);
  } catch (e) {
    console.error('Failed to load profile from localStorage:', e);
  }
  return null;
}

function profileReducer(state, action) {
  let nextState = state;
  switch (action.type) {
    case 'SET_PROFILE':
      nextState = { ...action.payload };
      break;
    case 'UPDATE_FIELD':
      nextState = { ...(state || defaultProfile), [action.field]: action.value };
      break;
    case 'CLEAR_PROFILE':
      nextState = null;
      break;
    default:
      return state;
  }
  try {
    if (nextState) {
      localStorage.setItem('civiq_user_profile', JSON.stringify(nextState));
    } else {
      localStorage.removeItem('civiq_user_profile');
    }
  } catch (e) {
    console.error('Failed to save profile to localStorage:', e);
  }
  return nextState;
}

export function ProfileProvider({ children }) {
  const [profile, dispatch] = useReducer(profileReducer, null, getSavedProfile);

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
