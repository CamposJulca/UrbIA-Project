import React from 'react';
import { Link } from 'react-router-dom';

const Header = () => {
  return (
    <header className="bg-gray-800 text-white p-4 shadow flex justify-between items-center">
      <h1 className="text-xl font-bold">🌆 UrbIA</h1>
      <nav className="space-x-6">
        <Link to="/" className="hover:text-yellow-300">Inicio</Link>
        <Link to="/devices" className="hover:text-yellow-300">Sensores</Link>
      </nav>
    </header>
  );
};

export default Header;
