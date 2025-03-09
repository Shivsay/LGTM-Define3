import React from 'react';
import FlightGanttChart from '../components/FlightGanttChart';

const Dashboard = () => {
    return (
        <div className='bg-gray-800'>
            <h1>Dashboard</h1>
            <p>Overview of current assignments and key metrics.</p>
            
            <div style={{ marginTop: '20px' }}>
                <h2>Flight Schedule</h2>
                <FlightGanttChart />
            </div>
        </div>
    );
};

export default Dashboard;
