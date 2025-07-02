import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import HomePage from './pages/HomePage';  // ← ESTE ES EL CAMBIO CORRECTO
import Header from './components/Header';

const App = () => {
  return (
    <Router>
      <Header />
      <Routes>
        <Route path="/" element={<HomePage />} /> {/* ← Y AQUÍ TAMBIÉN */}
        <Route path="/devices" element={<Dashboard />} />
      </Routes>
    </Router>
  );
};

export default App;
