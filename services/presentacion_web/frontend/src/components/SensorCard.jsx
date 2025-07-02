import React from 'react';

const SensorCard = ({ name, type, data }) => {
  return (
    <div className="bg-white shadow rounded-xl p-4 border border-gray-100">
      <h2 className="text-lg font-semibold text-gray-700">{name}</h2>
      <p className="text-sm text-gray-500 mb-2">Tipo: {type}</p>
      <ul className="text-sm">
        {data && Object.entries(data).map(([key, value]) => (
          <li key={key}>
            <span className="font-medium">{key}:</span> {value}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default SensorCard;
