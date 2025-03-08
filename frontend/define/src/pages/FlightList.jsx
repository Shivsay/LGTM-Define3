import React from 'react';

const FlightList = ({ flights }) => {
    return (
        <div>
            <h1>Flights</h1>
            <ul>
                {flights.map(flight => (
                    <li key={flight.id}>
                        {flight.flight_identifier} - {flight.departure_station} to {flight.arrival_station}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default FlightList;
