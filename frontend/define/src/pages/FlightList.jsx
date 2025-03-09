import React, { useState, useEffect } from 'react';

const FlightList = () => {
  const [flightData, setFlightData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchFlightData = async () => {
      try {
        setLoading(true);
        const response = await fetch('http://127.0.0.1:8000/api/get-flight/');
        
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        
        const data = await response.json();
        setFlightData(data);
        setLoading(false);
      } catch (err) {
        setError(`Error fetching flight data: ${err.message}`);
        setLoading(false);
      }
    };
    fetchFlightData();
  }, []);

  // Format date and time for better display
  const formatDateTime = (dateTimeString) => {
    if (!dateTimeString) return '';
    const dateTime = new Date(dateTimeString);
    return dateTime.toLocaleString();
  };

  if (loading) {
    return <div className="flex justify-center p-6">Loading flight data...</div>;
  }

  if (error) {
    return <div className="text-red-600 p-4 border border-red-300 rounded bg-red-50">{error}</div>;
  }

  return (
    <div className="relative overflow-x-auto mt-16">
      {/*<h2 className="text-2xl font-semibold mb-4">Flight Schedule</h2>*/}
      <table className="w-full text-sm text-left rtl:text-right text-gray-500 dark:text-gray-400">
        <thead className="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
          <tr>
            <th scope="col" className="px-6 py-3">Flight ID</th>
            <th scope="col" className="px-6 py-3">Date</th>
            <th scope="col" className="px-6 py-3">From</th>
            <th scope="col" className="px-6 py-3">To</th>
            <th scope="col" className="px-6 py-3">Departure</th>
            <th scope="col" className="px-6 py-3">Arrival</th>
            <th scope="col" className="px-6 py-3">Aircraft</th>
            <th scope="col" className="px-6 py-3">Capacity</th>
          </tr>
        </thead>
        <tbody>
          {flightData.map((flight, index) => (
            <tr key={index} className="bg-white border-b dark:bg-gray-800 dark:border-gray-700 border-gray-200">
              <th scope="row" className="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                {flight.flight_identifier}
              </th>
              <td className="px-6 py-4">{flight.flight_date}</td>
              <td className="px-6 py-4">{flight.departure_station}</td>
              <td className="px-6 py-4">{flight.arrival_station}</td>
              <td className="px-6 py-4">{formatDateTime(flight.scheduled_time_of_departure)}</td>
              <td className="px-6 py-4">{formatDateTime(flight.scheduled_time_of_arrival)}</td>
              <td className="px-6 py-4">{flight.aircraft_type}</td>
              <td className="px-6 py-4">{flight.physical_seating_capacity}</td>
            </tr>
          ))}
        </tbody>
        <tfoot>
          <tr className="bg-gray-50 dark:bg-gray-700">
            <th scope="row" colSpan={7} className="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
              Total Flights
            </th>
            <td className="px-6 py-4 font-medium text-gray-900 dark:text-white">
              {flightData.length}
            </td>
          </tr>
        </tfoot>
      </table>
    </div>
  );
};

export default FlightList;
