import React from 'react';
import { Link } from 'react-router-dom';

const NotFoundPage = () => {
  return (
    <div className="p-6 text-center">
      <h1 className="text-4xl font-bold text-red-600">404</h1>
      <p className="text-gray-600 mt-2">Página no encontrada.</p>
      <Link to="/" className="text-blue-600 hover:underline mt-4 block">
        Volver al inicio
      </Link>
    </div>
  );
};

export default NotFoundPage;
