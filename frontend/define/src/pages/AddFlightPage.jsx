import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom';
const AddFlightPage = ({ addFlightSubmit }) => {
  const [flightidentifier, setFlightIdentifier] = useState('');
  const [flightdate, setFlightDate] = useState('');
  const [departurestation, setDepartureStation] = useState('');
  const [timeofdeparture,setTimeOfDeparture] = useState('');
  const [arrivalstation, setArrivalStation] = useState('');
  const [timeofarrival, setTimeOfArrival] = useState('');
  const [aircrafttype, setAircraftType] = useState('');
  const [seatingcapacity, setSeatingCapacity] = useState('');
  const [mingroundtime, setMinGroundTime] = useState('');
  const [onwardflightinformation, setOnwardFlightInformation] = useState('');


  const navigate = useNavigate();

  const submitForm = (e) => {
    e.preventDefault();

    const newFlight = {
      flight_identifier:flightidentifier,
      flight_date:flightdate,
      departure_station:departurestation,
      scheduled_time_of_departure:timeofdeparture,
      arrival_station:arrivalstation,
      time_of_arrival:timeofarrival,
      aircraft_type:aircrafttype,
      seating_capacity:seatingcapacity,
      minimum_ground_time:mingroundtime,
      onward_flight_information:onwardflightinformation,
    };

    addAssignmentSubmit(newFlight);

    // toast.success('Aircraft Added Successfully');

    return navigate('/dashboard');
  }

  return (
       <section className='bg-indigo-50'>
      <div className='container m-auto max-w-2xl py-24'>
        <div className='bg-white px-6 py-8 mb-4 shadow-md rounded-md border m-4 md:m-0'>
          <form onSubmit={submitForm}>
            <h2 className='text-3xl text-center font-semibold mb-6'>Add Flight</h2>

            <div className='mb-4'>
              <label className='block text-gray-700 font-bold mb-2'>
                Flight Identifier
              </label>
              <input
                type='text'
                id='identifier'
                name='identifier'
                className='border rounded w-full py-2 px-3 mb-2'
                placeholder=''
                required
                autoComplete="off"
                value={flightidentifier}
                onChange={(e) => setFlightIdentifier(e.target.value)}
              />
            </div>

            <div className='mb-4'>
              <label className='block text-gray-700 font-bold mb-2'>
                Flight Date
              </label>
              <input
                type='text'
                id='flightdate'
                name='flightdate'
                className='border rounded w-full py-2 px-3 mb-2'
                placeholder=''
                required
                autoComplete="off"
                value={flightdate}
                onChange={(e) => setFlightDate(e.target.value)}/>
                
            </div><div className='mb-4'>
              <label className='block text-gray-700 font-bold mb-2'>
                Departure Station
              </label>  
              <input
                type='text'
                id='depaturestation'
                name='depaturestation'
                className='border rounded w-full py-2 px-3 mb-2'
                placeholder=''
                required
                autoComplete="off"
                value={departurestation}
                onChange={(e) => setDepartureStation(e.target.value)}
              />
            </div>
              
             <div className='mb-4'>
              <label className='block text-gray-700 font-bold mb-2'>
                Time Of Departure 
              </label>
              <input
                type='text'
                id='timeofdeparture'
                name='timeofdeparture'
                className='border rounded w-full py-2 px-3 mb-2'
                placeholder=''
                autoComplete="off"
                required
                value={timeofdeparture}
                onChange={(e) => setTimeOfDeparture(e.target.value)}
              />
            </div>
          
            <div className='mb-4'>
              <label className='block text-gray-700 font-bold mb-2'>
                Arrival Station
              </label>
              <input
                type='text'
                id='arrivalstation'
                name='arrivalstation' 
                className='border rounded w-full py-2 px-3 mb-2'
                placeholder=''
                autoComplete="off"
                required
                value={arrivalstation}
                onChange={(e) => setArrivalStation(e.target.value)}
              />
            </div>

            <div className='mb-4'>
              <label className='block text-gray-700 font-bold mb-2'>
                Scheduled Time Of Arrival
              </label>
              <input
                type='text'
                id='timeofarrival'
                name='timeofarrival' 
                autoComplete='off'
                className='border rounded w-full py-2 px-3 mb-2'
                placeholder=''
                required
                value={timeofarrival}
                onChange={(e) => setTimeOfArrival(e.target.value)}
              />
            </div>

             <div className='mb-4'>
              <label className='block text-gray-700 font-bold mb-2'>
                Aircraft Type
              </label>
              <input
                type='text'
                id='aircrafttype'
                autoComplete='off'
                name='aircrafttype' 
                className='border rounded w-full py-2 px-3 mb-2'
                placeholder=''
                required
                value={aircrafttype}
                onChange={(e) => setAircraftType(e.target.value)}
              />
            </div>

            <div className='mb-4'>
              <label className='block text-gray-700 font-bold mb-2'>
                Physical Seating Capacity
              </label>
              <input
                type='number'
                id='seatingcapacity'
                name='seatingcapacity' 
                className='border rounded w-full py-2 px-3 mb-2'
                autoComplete='off'
                placeholder=''
                required
                value={seatingcapacity}
                onChange={(e) => setSeatingCapacity(e.target.value)}
              />
            </div>

            <div className='mb-4'>
              <label className='block text-gray-700 font-bold mb-2'>
                Minimum Ground Time
              </label>
              <input
                type='number'
                id='mingroundtime'
                name='mingroundtime' 
                autoComplete='off'
                className='border rounded w-full py-2 px-3 mb-2'
                placeholder=''
                required
                value={mingroundtime}
                onChange={(e) => setMinGroundTime(e.target.value)}
              />
            </div>
            {/* <div className='mb-4'>
              <label className='block text-gray-700 font-bold mb-2'>
                Onward Flight Information
              </label>
              <input
                type='text'
                id='onwardflightinformation'
                name='onwardflightinformation' 
                className='border rounded w-full py-2 px-3 mb-2'
                placeholder=''
                required
                value={onwardflightinformation}
                onChange={(e) => setFlightInformation (e.target.value)}
              />
            </div> */}
            <div>
              <button
                className='bg-gray-800 hover:bg-gray-900 text-white font-bold py-2 px-4 rounded-full w-full focus:outline-none focus:shadow-outline'
                type='submit'>
                Add Flight
              </button>
            </div> 

          </form>
        </div>
      </div>
    </section>
  )
}
export default AddFlightPage;