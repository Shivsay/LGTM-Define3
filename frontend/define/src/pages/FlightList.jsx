import React from 'react';

const FlightList = ({ flights }) => {
    return (
       <div className="relative overflow-x-auto">
    <table className="w-full text-sm text-left rtl:text-right text-gray-500 dark:text-gray-400">
        <thead className="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
            <tr>
                <th scope="col" className="px-6 py-3">
                   Flight Identifier
                </th>
                <th scope="col" className="px-6 py-3">
                   Flight Date
                </th>
                <th scope="col" className="px-6 py-3">
                    Departure Station
                </th>
                 <th scope="col" className="px-6 py-3">
                    Scheduled Time of Departure
                </th>
                 <th scope="col" className="px-6 py-3">
                    Arrival Station
                </th>
                 <th scope="col" className="px-6 py-3">
                    Scheduled Time of Arrival
                </th>
                 <th scope="col" className="px-6 py-3">
                    Aircraft Type
                </th>
                 <th scope="col" className="px-6 py-3">
                    Physical Seating Capacity
                </th>
                 <th scope="col" className="px-6 py-3">
                    Minimum Ground Time
                </th>
                 <th scope="col" className="px-6 py-3">
                    Onward Flight Information
                </th>
            </tr>
        </thead>
        <tbody>
             {/* {arr.map((item, index) => (
            <tr className="bg-white border-b dark:bg-gray-800 dark:border-gray-700 border-gray-200">
                <th scope="row" className="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                    {item}
                </th>
                <td className="px-6 py-4">
                   {item.aircraft_type}
                </td>
                <td className="px-6 py-4">
                    {item.seating_capacity}
                </td>
            </tr>
                ))} */}
                       <tr className="bg-white border-b dark:bg-    gray-800 dark:border-gray-700 border-gray-200">
                <th scope="row" className="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                    {item.flight_identifier}
                </th>
                <td className="px-6 py-4">
                   {item.flight_date}
                </td>
                <td className="px-6 py-4">
                    {item.departure_station}
                </td>
                <td className="px-6 py-4">
                    {item.scheduled_time_of_departure}
                </td>
                <td className="px-6 py-4">
                    {item.aircraft_type}
                </td>
                <td className='px-6 py-4'>
                    {item.seating_capacity}
                    </td>
            </tr>
        </tbody>
    </table>
</div>

    );
};

export default FlightList;
