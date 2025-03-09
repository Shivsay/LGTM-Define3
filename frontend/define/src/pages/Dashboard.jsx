import React from 'react';
import FlightGanttChart from '../components/FlightGanttChart';
import AircraftTimelineChart from '../components/AircraftTimelineChart';

const Dashboard = () => {
    return (
        <div className='bg-gray-800'>
            <h1>Dashboard</h1>
            <p>Overview of current assignments and key metrics.</p>
            
            <div style={{ marginTop: '20px' }}>
                <h2>Flight Schedule</h2>
                <FlightGanttChart />
                <h2>Timeline Chart</h2>
                <AircraftTimelineChart />
            </div>
        </div>
    );
};

export default Dashboard;
