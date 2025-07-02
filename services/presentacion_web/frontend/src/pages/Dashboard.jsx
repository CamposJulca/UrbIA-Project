import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Dashboard = () => {
  const [devices, setDevices] = useState([]);

  useEffect(() => {
    const fetchDevices = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/devices');
        setDevices(response.data.dispositivos);
      } catch (error) {
        console.error('Error al obtener dispositivos:', error);
      }
    };

    fetchDevices();
  }, []);

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <h2 className="text-2xl font-bold mb-6 text-gray-800">Sensores activos</h2>

      {devices.length === 0 ? (
        <p className="text-gray-600">No hay sensores disponibles.</p>
      ) : (
        <div className="overflow-x-auto">
          <table className="min-w-full bg-white rounded-xl shadow-md">
            <thead className="bg-indigo-100 text-indigo-800 font-semibold text-sm uppercase">
              <tr>
                <th className="px-4 py-2 border-b text-left">Nombre</th>
                <th className="px-4 py-2 border-b text-left">Tipo</th>
                <th className="px-4 py-2 border-b text-left">Estado</th>
              </tr>
            </thead>
            <tbody>
              {devices.map((device) => (
                <tr key={device.id} className="hover:bg-gray-50">
                  <td className="px-4 py-2 border-b">{device.nombre}</td>
                  <td className="px-4 py-2 border-b capitalize">{device.tipo}</td>
                  <td className="px-4 py-2 border-b">
                    <span
                      className={`px-2 py-1 text-sm rounded-full font-medium ${
                        device.activo ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                      }`}
                    >
                      {device.activo ? 'Activo' : 'Inactivo'}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
