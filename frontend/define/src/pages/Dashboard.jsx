import React from 'react';
import AircraftTimelineChart from '../components/AircraftTimelineChart';

const Dashboard = () => {
    return (
        <div className='bg-gray-800'>
            <h1>Dashboard</h1>
            <p>Overview of current assignments and key metrics.</p>
            
            <div style={{ marginTop: '20px' }}>
                <h2>Timeline Chart</h2>
                <AircraftTimelineChart />
            </div>
        </div>
    );
};

export default Dashboard;
