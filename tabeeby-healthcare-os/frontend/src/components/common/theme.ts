import { createTheme } from '@mui/material/styles';

export const medicalTheme = createTheme({
  palette: {
    primary: { main: '#009688', light: '#4DB6AC', dark: '#00796B' },
    secondary: { main: '#FF5722', light: '#FF8A65', dark: '#E64A19' },
    error: { main: '#F44336' },
    warning: { main: '#FF9800' },
    success: { main: '#4CAF50' },
    info: { main: '#2196F3' },
  },
  typography: {
    fontFamily: '"Segoe UI", "Tajawal", sans-serif',
    h1: { fontSize: '2rem', fontWeight: 700 },
    h2: { fontSize: '1.5rem', fontWeight: 600 },
    h3: { fontSize: '1.25rem', fontWeight: 600 },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: { textTransform: 'none', borderRadius: 8 },
      },
    },
  },
});