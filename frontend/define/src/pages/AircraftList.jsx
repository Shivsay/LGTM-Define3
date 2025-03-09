// AircraftList.js
import React from 'react';
import { useState,useEffect } from 'react';

const AircraftList = ({ aircraft }) => {
    const arr =[{'aircraft_registration': 'iN344', 'aircraft_type': 'A320', 'seating_capacity': 175}, {'aircraft_registration': 'LO947', 'aircraft_type': 'B777', 'seating_capacity': 384}, {'aircraft_registration': 'KQ007', 'aircraft_type': 'A320', 'seating_capacity': 165}, {'aircraft_registration': 'ml859', 'aircraft_type': 'B777', 'seating_capacity': 336}, {'aircraft_registration': 'hU508', 'aircraft_type': 'A320', 'seating_capacity': 165}, {'aircraft_registration': 'oP403', 'aircraft_type': 'A380', 'seating_capacity': 406}, {'aircraft_registration': 'At386', 'aircraft_type': 'B777', 'seating_capacity': 364}, {'aircraft_registration': 'Tn960', 'aircraft_type': 'B777', 'seating_capacity': 333}, {'aircraft_registration': 'mW958', 'aircraft_type': 'A380', 'seating_capacity': 414}, {'aircraft_registration': 'mo974', 'aircraft_type': 'A320', 'seating_capacity': 171}]
    const [loading, setLoading] = useState(true);

    useEffect(() => {
    const fetchCards = async () => {
      const apiUrl ='http://127.0.0.1:8000/api/get-aircraft/';
      try {
        const res = await fetch(apiUrl);
        const data = await res.json();
        console.log(data)
        setCards(data);
      } catch (error) {
        console.log('Error fetching data', error);
      } finally {
        setLoading(false);
      }
    };

    fetchCards();
  }, []);

    return (
        // <div>
        //     <h1>Aircraft</h1>
        //     <ul>
        //         {aircraft.map(ac => (
        //             <li key={ac.id}>
        //                 {ac.registration} - {ac.type} ({ac.seating_capacity} seats)
        //             </li>
        //         ))}
        //     </ul>
        // </div>

<div className="relative overflow-x-auto mt-15">
    <table className="w-full text-sm text-left rtl:text-right text-gray-500 dark:text-gray-400">
        <thead className="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
            <tr>
                <th scope="col" className="px-6 py-3">
                    Aircraft Registration
                </th>
                <th scope="col" className="px-6 py-3">
                   Aircraft Type
                </th>
                <th scope="col" className="px-6 py-3">
                    Seating Capatcity
                </th>
            </tr>
        </thead>
        <tbody>
             {arr.map((item, index) => (
            <tr key={index} className="bg-white border-b dark:bg-gray-800 dark:border-gray-700 border-gray-200">
                <th scope="row" className="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                    {item.aircraft_registration}
                </th>
                <td className="px-6 py-4">
                   {item.aircraft_type}
                </td>
                <td className="px-6 py-4">
                    {item.seating_capacity}
                </td>
            </tr>
                ))}
            
        </tbody>
    </table>
</div>

    );
};

export default AircraftList;
