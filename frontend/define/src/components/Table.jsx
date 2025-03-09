import React from 'react'

const Table = () => {
//     useEffect(() => {
//     const fetchCards = async () => {
//       const apiUrl = ForAircraft ? 'http://127.0.0.1:8000/api/get-aircraft/' : 'http://127.0.0.1:8000/api/put-aircraft/';
//       try {
//         const res = await fetch(apiUrl);
//         const data = await res.json();
//         setCards(data);
//       } catch (error) {
//         console.log('Error fetching data', error);
//       } finally {
//         setLoading(false);
//       }
//     };

//     fetchCards();
//   }, []);


const arr =[{'aircraft_registration': 'iN344', 'aircraft_type': 'A320', 'seating_capacity': 175}, {'aircraft_registration': 'LO947', 'aircraft_type': 'B777', 'seating_capacity': 384}, {'aircraft_registration': 'KQ007', 'aircraft_type': 'A320', 'seating_capacity': 165}, {'aircraft_registration': 'ml859', 'aircraft_type': 'B777', 'seating_capacity': 336}, {'aircraft_registration': 'hU508', 'aircraft_type': 'A320', 'seating_capacity': 165}, {'aircraft_registration': 'oP403', 'aircraft_type': 'A380', 'seating_capacity': 406}, {'aircraft_registration': 'At386', 'aircraft_type': 'B777', 'seating_capacity': 364}, {'aircraft_registration': 'Tn960', 'aircraft_type': 'B777', 'seating_capacity': 333}, {'aircraft_registration': 'mW958', 'aircraft_type': 'A380', 'seating_capacity': 414}, {'aircraft_registration': 'mo974', 'aircraft_type': 'A320', 'seating_capacity': 171}]



  return (
    <table className="table-auto">
  <thead>
    <tr>
      <th>Aircraft Registration</th>
      <th>Aircraft Type</th>
      <th>Seating Capatcity</th>
    </tr>
  </thead>
  <tbody>
    {arr.map((item, index) => (
      <tr key={index}>
        <td>{item.aircraft_registration}</td>
        <td>{item.aircraft_type}</td>
        <td>{item.seating_capacity}</td>
      </tr>
    ))}
  </tbody>
</table>
  )
}

export default Table