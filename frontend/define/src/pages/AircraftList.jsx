// AircraftList.js
import React from 'react';

const AircraftList = ({ aircraft }) => {
    return (
        <div>
            <h1>Aircraft</h1>
            <ul>
                {aircraft.map(ac => (
                    <li key={ac.id}>
                        {ac.registration} - {ac.type} ({ac.seating_capacity} seats)
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default AircraftList;