import React, { useState, useEffect } from 'react';
import { Chart } from 'react-google-charts';
import axios from 'axios';

const AircraftTimelineChart = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const response = await axios.get('http://127.0.0.1:8000/api/solve/');
        transformData(response.data);
        setLoading(false);
      } catch (err) {
        setError('Failed to fetch data: ' + err.message);
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const transformData = (apiData) => {
    if (!apiData || !apiData.assignments) {
      setError('Invalid data format');
      return;
    }

    // Initialize with header row
    const chartData = [
      [
        { type: 'string', id: 'Aircraft' },
        { type: 'string', id: 'Flight' },
        { type: 'string', id: 'style', role: 'style' },
        { type: 'date', id: 'Start' },
        { type: 'date', id: 'End' },
      ],
    ];

    // Generate colors for different activity types
    const flightColor = '#4285F4'; // Blue for flights
    const preassignmentColor = '#9E9E9E'; // Gray for preassignments

    // Process each aircraft and its schedule
    apiData.assignments.forEach((assignment) => {
      const aircraft = assignment.aircraft;
      
      assignment.schedule.forEach((item) => {
        const startTime = new Date(item.start_time);
        const endTime = new Date(item.end_time);
        
        let label = '';
        let color = preassignmentColor;
        
        if (item.type === 'flight') {
          label = `${item.flight_identifier}: ${item.departure_station} → ${item.arrival_station}`;
          color = flightColor;
        } else if (item.type === 'preassignment') {
          label = item.description;
        }
        
        chartData.push([
          aircraft,
          label,
          color,
          startTime,
          endTime,
        ]);
      });
    });

    setData(chartData);
  };

  const options = {
    height: 800,
    timeline: {
      showRowLabels: true,
      groupByRowLabel: true,
    },
    avoidOverlappingGridLines: false,
    hAxis: {
      format: 'HH:mm',
    },
  };

  if (loading) {
    return <div className="flex justify-center items-center h-64 text-lg">Loading timeline data...</div>;
  }

  if (error) {
    return <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">{error}</div>;
  }

  return (
    <div className="w-full h-full">
      <div className="bg-white p-4 rounded-lg shadow-md">
        <h2 className="text-xl font-bold mb-4">Aircraft Assignment Timeline</h2>
        <div className="flex mb-4 text-sm">
          <div className="flex items-center mr-4">
            <div className="w-4 h-4 bg-blue-500 mr-1"></div>
            <span>Flight</span>
          </div>
          <div className="flex items-center">
            <div className="w-4 h-4 bg-gray-400 mr-1"></div>
            <span>Preassignment</span>
          </div>
        </div>
        {data.length > 1 ? (
          <div className="overflow-x-auto">
            <Chart
              chartType="Timeline"
              data={data}
              options={options}
              width="100%"
              className="min-w-full"
            />
          </div>
        ) : (
          <div className="text-center py-8">No schedule data available</div>
        )}
      </div>
    </div>
  );
};

export default AircraftTimelineChart;
