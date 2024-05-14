import { useState } from 'react';
import './App.css';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import { loanApplicationsContext } from './lib/Context';
import { ToastProvider } from 'react-toast-notifications';
import { AppBar, Button, Toolbar, Typography } from '@mui/material';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Dashboard from './components/Dashboard/Dashboard';
import AnalyticsPage from './components/AnalyticsPage/AnalyticsPage';

const theme = createTheme({
  palette: {
    primary: {
      main: 'rgb(24, 24, 24)',
    },
    secondary: {
      main: 'rgb(213, 45, 52)',
    },
    error: {
      main: '#ff5722',
    },
    info: {
      main: '#4caf50',
    },
  },
});

function App() {
  const [count, setCount] = useState(0);
  const [loanApplications, setLoanApplications] = useState([]);

  return (
    <ThemeProvider theme={theme}>
      <ToastProvider>
        <loanApplicationsContext.Provider value={[loanApplications, setLoanApplications]}>
          <Router>
            <AppBar position="static">
              <Toolbar>
                <div className='logo-img-div'>
                  <img className='logo-img' src="https://media.licdn.com/dms/image/C5603AQHQCQZ_GU1bDA/profile-displayphoto-shrink_800_800/0/1517496277853?e=2147483647&v=beta&t=pY-bBCznB3f19NGF80WExWC80Kbu-UPELwqdcsQrbvE" alt="" />

                </div>
                <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                  BC Loan Management Dashboard
                </Typography>
                <Button component={Link} to="/" color="inherit">
                  Home
                </Button>
                <Button component={Link} to="/analytics" color="inherit">
                  Analytics
                </Button>
              </Toolbar>
            </AppBar>
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/analytics" element={<AnalyticsPage />} />
            </Routes>
          </Router>
        </loanApplicationsContext.Provider>
      </ToastProvider>
    </ThemeProvider>
  );
}

export default App;