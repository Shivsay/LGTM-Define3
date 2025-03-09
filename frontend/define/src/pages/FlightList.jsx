import React, { useState, useEffect } from 'react';

const FlightTable = () => {
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
    <div className="container mx-auto p-4">
      <h2 className="text-2xl font-semibold mb-4">Flight Schedule</h2>
      <div className="overflow-x-auto">
        <table className="min-w-full bg-white border border-gray-300 shadow-sm rounded-lg">
          <thead>
            <tr className="bg-gray-100">
              <th className="py-2 px-4 border-b text-left">Flight ID</th>
              <th className="py-2 px-4 border-b text-left">Date</th>
              <th className="py-2 px-4 border-b text-left">From</th>
              <th className="py-2 px-4 border-b text-left">To</th>
              <th className="py-2 px-4 border-b text-left">Departure</th>
              <th className="py-2 px-4 border-b text-left">Arrival</th>
              <th className="py-2 px-4 border-b text-left">Aircraft</th>
              <th className="py-2 px-4 border-b text-right">Capacity</th>
            </tr>
          </thead>
          <tbody>
            {flightData.map((flight, index) => (
              <tr key={index} className={index % 2 === 0 ? 'bg-gray-50' : 'bg-white'}>
                <td className="py-2 px-4 border-b font-medium">{flight.flight_identifier}</td>
                <td className="py-2 px-4 border-b">{flight.flight_date}</td>
                <td className="py-2 px-4 border-b">{flight.departure_station}</td>
                <td className="py-2 px-4 border-b">{flight.arrival_station}</td>
                <td className="py-2 px-4 border-b">{formatDateTime(flight.scheduled_time_of_departure)}</td>
                <td className="py-2 px-4 border-b">{formatDateTime(flight.scheduled_time_of_arrival)}</td>
                <td className="py-2 px-4 border-b">{flight.aircraft_type}</td>
                <td className="py-2 px-4 border-b text-right">{flight.physical_seating_capacity}</td>
              </tr>
            ))}
          </tbody>
          <tfoot>
            <tr className="bg-gray-100">
              <td className="py-2 px-4 border-t font-semibold" colSpan={7}>Total Flights</td>
              <td className="py-2 px-4 border-t text-right font-semibold">{flightData.length}</td>
            </tr>
          </tfoot>
        </table>
      </div>
    </div>
  );
};

export default FlightTable;

